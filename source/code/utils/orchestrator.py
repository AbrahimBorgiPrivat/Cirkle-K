import json
import os
import pandas as pd
import time
import threading
import random
import numpy as np

from tqdm import tqdm
from datetime import datetime, timedelta, date, time
from utils import env
from sqlalchemy import MetaData, text, Table, Column
from sqlalchemy.exc import OperationalError, TimeoutError, NoSuchTableError
from sqlalchemy.schema import CreateSchema
from classes.db_engine import DatabaseEngine


"""
Loads a JSON file containing a list of dictionaries from the specified folder.  
Returns the data if valid; otherwise prints an error and returns an empty list.  
Validates that the JSON structure is a list.
"""

def load_json_file(folder_path:str, 
                   file_name:str) -> list[dict]:
    file_path = os.path.join(folder_path, file_name)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                raise ValueError("JSON file must contain a list of dictionaries")
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return []

"""
Transforms a list of dictionaries by selecting and renaming keys, 
optionally adding extra fields and timestamps for creation and update. 
Returns the processed list of standardized dictionaries.
"""

def select_columns(data_list: list[dict], 
                   selected_keys_with_rename: dict, 
                   extra_fields=None,
                   with_update_and_created_time: bool=True) -> list[dict]:
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    processed_list = []
    extra_fields = extra_fields or {} 
    for row in tqdm(data_list):
        if isinstance(row, dict):
            new_row = {new_key: row.get(old_key, None) for old_key, new_key in selected_keys_with_rename.items()}
            new_row.update(extra_fields)
            if with_update_and_created_time:
                current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                new_row['updatetime'] = current_time
                new_row['createdtime'] = current_time
            processed_list.append(new_row)
    return processed_list

"""
Executes a SQL query with optional timeout and retry logic. 
Handles transient database errors and enforces timeout using a separate thread. 
Returns the result as a list of dictionaries 
"""

def get_data_from_db(db_name: str,
                     sql_query: str,
                     username: str = env.POSTGRES_USERNAME,
                     password: str = env.POSTGRES_PASSWORD,
                     server: str = env.POSTGRES_HOST,
                     port: int = env.POSTGRES_PORT,
                     db_type: str = 'postgresql',
                     retries: int = 1,  
                     delay: int = 2,
                     timeout: int = None):  # Timeout in seconds (default: None, no timeout)
    engine = DatabaseEngine(
        db=db_name,
        server=server,
        username=username,
        password=password,
        port=port,
        db_type=db_type,
    ).get_engine()
    attempt = 0
    while attempt <= retries:
        try:
            result_data = []
            query_exception = None

            def execute_query():
                nonlocal result_data, query_exception
                try:
                    with engine.connect() as connection:
                        result = connection.execute(text(sql_query))
                        columns = result.keys()
                        result_data = [dict(zip(columns, row)) for row in result]
                except Exception as e:
                    query_exception = e

            query_thread = threading.Thread(target=execute_query)
            query_thread.start()
            query_thread.join(timeout=timeout)

            if query_thread.is_alive():
                print(f"Query attempt {attempt+1} timed out after {timeout} seconds. Retrying...")
                attempt += 1
                time.sleep(delay)
                continue

            if query_exception:
                raise query_exception
            return result_data

        except (OperationalError, TimeoutError) as e:
            if attempt < retries:
                print(f"Database query failed (attempt {attempt+1}/{retries}). Retrying in {delay} seconds...")
                time.sleep(delay)
                attempt += 1
            else:
                print(f"Query failed after {retries} retries. Raising error.")
                raise

"""
Ensures that a table exists in the specified schema with the correct columns and primary key. 
Creates the schema/table if allowed and validates the structure if it already exists. 
Raises errors for mismatches unless auto-creation is enabled.
"""

def ensure_table_structure(db_name: str,
                           schema_name: str,
                           table_name: str,
                           fields_dict: dict,
                            username: str = env.POSTGRES_USERNAME,
                            password: str = env.POSTGRES_PASSWORD,
                            server: str = env.POSTGRES_HOST,
                            port: int = env.POSTGRES_PORT,
                            db_type: str = 'postgresql',
                            create_table_if_not_exist: bool = False):

    engine = DatabaseEngine(
            db=db_name,
            server=server,
            username=username,
            password=password,
            port=port,
            db_type=db_type,
        ).get_engine()
    with engine.connect() as connection:
        result = connection.execute(text("""
                        SELECT schema_name FROM information_schema.schemata WHERE schema_name = :schema
                    """), {"schema": schema_name})
    if result.fetchone() is None:
        if not create_table_if_not_exist:
            raise RuntimeError(f"Schema '{schema_name}' does not exist.")
        else:
            with engine.begin() as connection:
                connection.execute(CreateSchema(schema_name))
            print(f"-- Schema '{schema_name}' created.")
    
    metadata =  MetaData(schema=schema_name)
    try:
        existing_table = Table(table_name, metadata, autoload_with=engine)
        existing_columns = {col.name.lower(): type(col.type) for col in existing_table.columns}
        existing_primary_keys = {col.name.lower() for col in existing_table.primary_key.columns}

        input_columns = {}
        input_primary_keys = set()
        for col_name, col_info in fields_dict.items():
            col_type = col_info["type"] if isinstance(col_info, dict) else col_info
            input_columns[col_name.lower()] = type(col_type)
            if isinstance(col_info, dict) and col_info.get("primary_key", False):
                input_primary_keys.add(col_name.lower())

        for col, col_type in input_columns.items():
            if col not in existing_columns:
                raise RuntimeError(f"Missing column '{col}' in table '{schema_name}.{table_name}'.")
            
            existing = existing_columns[col].__class__.__name__.lower()
            expected = col_type.__class__.__name__.lower()
            if existing != expected:
                raise RuntimeError(f"Type mismatch for column '{col}': expected '{expected}', got '{existing}'")
        
        if existing_primary_keys != input_primary_keys:
            raise RuntimeError(f"Primary key mismatch in table '{schema_name}.{table_name}': Expected {input_primary_keys}, got {existing_primary_keys}")
        return True

    except NoSuchTableError:
        if not create_table_if_not_exist:
            raise RuntimeError(f"Table '{schema_name}.{table_name}' does not exist.")
        else:
            columns = []
            for name, col_info in fields_dict.items():
                col_type = col_info["type"] if isinstance(col_info, dict) else col_info
                is_pk = isinstance(col_info, dict) and col_info.get("primary_key", False)
                kwargs = {"primary_key": is_pk}
                if isinstance(col_info, dict) and "autoincrement" in col_info:
                    kwargs["autoincrement"] = col_info["autoincrement"]
                columns.append(Column(name, col_type, **kwargs))

            new_table = Table(table_name, metadata, *columns)
            new_table.create(bind=engine)
            print(f"-- Table '{schema_name}.{table_name}' created with fields: {list(fields_dict.keys())}")
            return True

"""
Performs bulk UPSERT into a target table using a list of dictionaries as input. 
Builds a dynamic SQL statement with conflict handling on primary keys, optionally updating specified fields. 
Handles nested structures and nulls, and returns the number of rows processed.
"""

def update_insert_dw(db_name: str,
                     schema: str,
                     table: str,
                     new_data: list[dict],
                     pk: list[str],
                     update_fields: list[str],
                     not_included_in_update_fields: list = [],
                     username: str = env.POSTGRES_USERNAME,
                     password: str = env.POSTGRES_PASSWORD,
                     server: str = env.POSTGRES_HOST,
                     port: int = env.POSTGRES_PORT,
                     db_type: str = 'postgresql',) -> int:
    
    db_instance = DatabaseEngine(db=db_name, 
                                 server=server, 
                                 username=username, 
                                 password=password,
                                 port=port,
                                 db_type=db_type)
    source = db_instance.get_engine()
    meta = MetaData(schema=schema)
    meta.reflect(bind=source)

    if not new_data:
        return 0

    Upserts = len(new_data)
    columns = new_data[0].keys()
    insert_values = ", ".join([
        f"({', '.join([f':{column}_{i}' for column in columns])})"
        for i in range(1, Upserts + 1)
    ])
    pk_clause = ", ".join(pk)
    insert_clause = ", ".join(pk + update_fields)
    if not update_fields:
        stmt = f"""
            INSERT INTO {schema}.{table} ({insert_clause})
            VALUES {insert_values}
            ON CONFLICT ({pk_clause})
            DO NOTHING
        """
    else:
        only_update_fields = [item for item in update_fields if item not in not_included_in_update_fields] 
        update_clause = ", ".join([f"{field} = EXCLUDED.{field}" for field in only_update_fields])
        stmt = f"""
            INSERT INTO {schema}.{table} ({insert_clause})
            VALUES {insert_values}
            ON CONFLICT ({pk_clause})
            DO UPDATE SET {update_clause}
        """
    params_insert = {}
    for i, row in enumerate(new_data, start=1):
        for column, value in row.items():
            if isinstance(value, dict):
                params_insert[f"{column}_{i}"] = json.dumps(value)
            elif isinstance(value, list):
                if all(isinstance(item, dict) for item in value):  
                    params_insert[f"{column}_{i}"] = json.dumps(value)
                else:
                    params_insert[f"{column}_{i}"] = value
            elif pd.isna(value):
                params_insert[f"{column}_{i}"] = None
            else:
                params_insert[f"{column}_{i}"] = value
    with source.begin() as connection:
        connection.execute(text(stmt), params_insert)
        
    return Upserts

"""
Generates a list of time intervals between two dates, split into chunks of specified hours.  
Returns pairs of timestamps in n-hours (or custom) intervals from start to end date.  
Useful for batch processing over partial days.
"""

def get_part_day_intervals(start_date: str, end_date: str, time_delta_hours: int=12):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    results = []
    current = start
    while current < end:
        next_half_day = current + timedelta(hours=time_delta_hours)
        results.append([current.strftime("%Y-%m-%d %H:%M:%S"), next_half_day.strftime("%Y-%m-%d %H:%M:%S")])
        current = next_half_day
    return results

"""
    Generates a datetime on the given date using a multimodal normal distribution based on input peak hours.
    Example use case: simulating user sign-up times where activity spikes at specific times of the day.

    Parameters:
    - date (datetime.date): The day to generate the time on.
    - peak_hours (list[int]): List of hour values representing the peaks (e.g. [9, 15]).
    - weights (list[float], optional): Probability distribution over the peaks. Must sum to 1.

    Returns:
    - datetime.datetime: Timestamp on the input date with time drawn from one of the peak distributions.
"""

def generate_multimodal_time_on_date(date: date, peak_hours: list[int], weights: list[float] = None) -> datetime:

    if weights is None:
        weights = [1 / len(peak_hours)] * len(peak_hours)

    # Select a peak hour based on weights
    peak_hour = random.choices(peak_hours, weights=weights, k=1)[0]

    # Determine minutes after midnight using a normal distribution centered at the peak
    mean_minutes = peak_hour * 60
    std_dev = 45 if peak_hour < 12 else 60  
    minutes = np.random.normal(loc=mean_minutes, scale=std_dev)

    # Clamp to realistic day time (6 AM to 10 PM)
    minutes = max(6 * 60, min(22 * 60, minutes))

    hour = int(minutes // 60)
    minute = int(minutes % 60)
    second = random.randint(0, 59)

    return datetime.combine(date, time(hour=hour, minute=minute, second=second))


def get_random_date_with_weekday_bias(date: date, weekday_weights=None) -> datetime.date:
    if weekday_weights is None:
        weekday_weights = [1/7] * 7
    target_weekday = random.choices(range(7), weights=weekday_weights)[0]
    candidate_date = date
    while candidate_date.weekday() != target_weekday:
        candidate_date -= timedelta(days=1)
    return candidate_date