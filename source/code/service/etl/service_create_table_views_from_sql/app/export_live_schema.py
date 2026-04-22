import json
import os
from collections import defaultdict
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


SYSTEM_SCHEMAS = {"pg_catalog", "information_schema"}
INCLUDED_SCHEMAS = ["datafordeler", "default_data", "interview", "public"]
RUNTIME_GROUPS = {
    "all.json": INCLUDED_SCHEMAS,
    "datafordeler.json": ["datafordeler"],
    "default_data.json": ["default_data"],
    "interview.json": ["interview"],
    "public.json": ["public"],
}


def quote_ident(identifier: str) -> str:
    return f'"{identifier.replace("\"", "\"\"")}"'


def schema_sql(schema_name: str) -> str:
    return f"CREATE SCHEMA IF NOT EXISTS {quote_ident(schema_name)};\n"


def load_connection_settings() -> dict[str, str]:
    load_dotenv()

    repo_root = Path(__file__).resolve().parents[6]
    code_env_path = repo_root / "source" / "code" / ".env"
    if code_env_path.exists():
        load_dotenv(code_env_path, override=False)

    return {
        "dbname": os.getenv("POSTGRES_DB", "circlek"),
        "user": os.getenv("POSTGRES_USERNAME", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", ""),
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
    }


def get_extension_owned_relations(cursor) -> set[tuple[str, str, str]]:
    cursor.execute(
        """
        SELECT
            ns.nspname AS schema_name,
            cls.relname AS relation_name,
            cls.relkind AS relation_kind
        FROM pg_depend dep
        JOIN pg_extension ext
          ON dep.refobjid = ext.oid
        JOIN pg_class cls
          ON dep.objid = cls.oid
        JOIN pg_namespace ns
          ON cls.relnamespace = ns.oid
        WHERE dep.deptype = 'e'
        """
    )
    return {(row[0], row[1], row[2]) for row in cursor.fetchall()}


def get_tables(cursor, excluded_relations: set[tuple[str, str, str]]) -> list[tuple[str, str, int]]:
    cursor.execute(
        """
        SELECT
            ns.nspname AS schema_name,
            cls.relname AS table_name,
            cls.oid
        FROM pg_class cls
        JOIN pg_namespace ns
          ON cls.relnamespace = ns.oid
        WHERE cls.relkind = 'r'
          AND ns.nspname NOT IN ('pg_catalog', 'information_schema')
        ORDER BY ns.nspname, cls.relname
        """
    )
    return [
        row
        for row in cursor.fetchall()
        if row[0] in INCLUDED_SCHEMAS and (row[0], row[1], "r") not in excluded_relations
    ]


def get_views(cursor, excluded_relations: set[tuple[str, str, str]]) -> list[tuple[str, str, int]]:
    cursor.execute(
        """
        SELECT
            ns.nspname AS schema_name,
            cls.relname AS view_name,
            cls.oid
        FROM pg_class cls
        JOIN pg_namespace ns
          ON cls.relnamespace = ns.oid
        WHERE cls.relkind = 'v'
          AND ns.nspname NOT IN ('pg_catalog', 'information_schema')
        ORDER BY ns.nspname, cls.relname
        """
    )
    return [
        row
        for row in cursor.fetchall()
        if row[0] in INCLUDED_SCHEMAS and (row[0], row[1], "v") not in excluded_relations
    ]


def build_table_sql(cursor, table_oid: int, schema_name: str, table_name: str) -> str:
    cursor.execute(
        """
        SELECT
            attr.attname AS column_name,
            pg_catalog.format_type(attr.atttypid, attr.atttypmod) AS data_type,
            attr.attnotnull AS not_null,
            pg_get_expr(def.adbin, def.adrelid) AS default_expr
        FROM pg_attribute attr
        LEFT JOIN pg_attrdef def
          ON attr.attrelid = def.adrelid
         AND attr.attnum = def.adnum
        WHERE attr.attrelid = %s
          AND attr.attnum > 0
          AND NOT attr.attisdropped
        ORDER BY attr.attnum
        """,
        (table_oid,),
    )
    column_lines = []
    for column_name, data_type, not_null, default_expr in cursor.fetchall():
        parts = [f"{quote_ident(column_name)} {data_type}"]
        if default_expr:
            parts.append(f"DEFAULT {default_expr}")
        if not_null:
            parts.append("NOT NULL")
        column_lines.append("    " + " ".join(parts))

    cursor.execute(
        """
        SELECT
            con.conname,
            con.contype,
            pg_get_constraintdef(con.oid, true) AS constraint_definition
        FROM pg_constraint con
        WHERE con.conrelid = %s
        ORDER BY
            CASE con.contype
                WHEN 'p' THEN 1
                WHEN 'u' THEN 2
                WHEN 'f' THEN 3
                WHEN 'c' THEN 4
                ELSE 5
            END,
            con.conname
        """,
        (table_oid,),
    )
    constraint_lines = [
        f"    CONSTRAINT {quote_ident(constraint_name)} {constraint_definition}"
        for constraint_name, _, constraint_definition in cursor.fetchall()
    ]

    joined_lines = ",\n".join(column_lines + constraint_lines)
    return (
        f"CREATE TABLE IF NOT EXISTS {quote_ident(schema_name)}.{quote_ident(table_name)}\n"
        "(\n"
        f"{joined_lines}\n"
        ");\n"
    )


def build_view_sql(cursor, view_oid: int, schema_name: str, view_name: str) -> str:
    cursor.execute("SELECT pg_get_viewdef(%s, true)", (view_oid,))
    view_definition = cursor.fetchone()[0].strip().rstrip(";")
    return (
        f"SET search_path TO {quote_ident(schema_name)}, public;\n"
        f"DROP VIEW IF EXISTS {quote_ident(schema_name)}.{quote_ident(view_name)};\n"
        f"CREATE OR REPLACE VIEW {quote_ident(schema_name)}.{quote_ident(view_name)} AS\n"
        f"{view_definition};\n"
        "RESET search_path;\n"
    )


def runtime_payload(sql_queries: list[str]) -> dict:
    return {
        "client": {
            "db_name": "POSTGRES_DB",
            "username": "POSTGRES_USERNAME",
            "password": "POSTGRES_PASSWORD",
            "server": "POSTGRES_HOST",
            "port": "POSTGRES_PORT",
            "db_type": "DB_TYPE",
        },
        "sql_queries": sql_queries,
    }


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    connection_settings = load_connection_settings()
    repo_root = Path(__file__).resolve().parents[6]
    definitions_root = repo_root / "source" / "code" / "runtime_definitions" / "create_table_and_views"
    query_root = definitions_root / "queries"
    runtime_root = definitions_root / "runtime"

    with psycopg2.connect(**connection_settings) as connection:
        with connection.cursor() as cursor:
            excluded_relations = get_extension_owned_relations(cursor)
            tables = get_tables(cursor, excluded_relations)
            views = get_views(cursor, excluded_relations)

            write_text(query_root / "migration" / "001_postgis.sql", "CREATE EXTENSION IF NOT EXISTS postgis;\n")

            table_files_by_schema: dict[str, list[str]] = defaultdict(list)
            view_files_by_schema: dict[str, list[str]] = defaultdict(list)

            for schema_name in INCLUDED_SCHEMAS:
                if schema_name != "public":
                    write_text(query_root / "schema" / f"{schema_name}.sql", schema_sql(schema_name))

            for schema_name, table_name, table_oid in tables:
                file_name = f"{schema_name}__{table_name}.sql"
                relative_path = f"create_table_and_views/queries/table/{file_name}"
                write_text(query_root / "table" / file_name, build_table_sql(cursor, table_oid, schema_name, table_name))
                table_files_by_schema[schema_name].append(relative_path)

            for schema_name, view_name, view_oid in views:
                file_name = f"{schema_name}__{view_name}.sql"
                relative_path = f"create_table_and_views/queries/view/{file_name}"
                write_text(query_root / "view" / file_name, build_view_sql(cursor, view_oid, schema_name, view_name))
                view_files_by_schema[schema_name].append(relative_path)

    schema_files = {
        schema_name: f"create_table_and_views/queries/schema/{schema_name}.sql"
        for schema_name in INCLUDED_SCHEMAS
        if schema_name != "public"
    }

    for runtime_name, schemas in RUNTIME_GROUPS.items():
        sql_queries = ["create_table_and_views/queries/migration/001_postgis.sql"]
        for schema_name in schemas:
            if schema_name in schema_files:
                sql_queries.append(schema_files[schema_name])
        for schema_name in schemas:
            sql_queries.extend(table_files_by_schema.get(schema_name, []))
        for schema_name in schemas:
            sql_queries.extend(view_files_by_schema.get(schema_name, []))
        write_json(runtime_root / runtime_name, runtime_payload(sql_queries))

    print("[export] SQL and runtime files generated successfully.")


if __name__ == "__main__":
    main()
