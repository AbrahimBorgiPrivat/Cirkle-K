import logging
from pathlib import Path

import psycopg2

from libraries.utils import path_config

logger = logging.getLogger(__name__)


def main(runtime_vars: dict) -> None:
    client = runtime_vars["client"]
    if client["db_type"] != "postgresql":
        raise ValueError(f"Unsupported db_type: {client['db_type']}")

    connection = psycopg2.connect(
        dbname=client["db_name"],
        user=client["username"],
        password=client["password"],
        host=client["server"],
        port=client["port"],
    )
    connection.autocommit = True

    try:
        for relative_sql_path in runtime_vars["sql_queries"]:
            sql_path = path_config.RUNTIME_DIR / relative_sql_path
            if not sql_path.exists():
                raise FileNotFoundError(f"SQL file not found: {sql_path}")

            sql_text = sql_path.read_text(encoding="utf-8").strip()
            if not sql_text:
                logger.warning("Skipping empty SQL file: %s", sql_path)
                continue

            logger.info("Executing SQL file: %s", sql_path)
            with connection.cursor() as cursor:
                cursor.execute(sql_text)
    finally:
        connection.close()
