import os

from dotenv import load_dotenv

# Keep container-provided env vars as the source of truth.
load_dotenv(override=False, verbose=True)


def _missing_env(values: dict[str, str | None]) -> list[str]:
    return [name for name, value in values.items() if not value]


def require_postgres_env() -> None:
    missing = _missing_env(
        {
            "POSTGRES_HOST": POSTGRES_HOST,
            "POSTGRES_PORT": POSTGRES_PORT,
            "POSTGRES_USERNAME": POSTGRES_USERNAME,
            "POSTGRES_PASSWORD": POSTGRES_PASSWORD,
        }
    )
    if missing:
        missing_values = ", ".join(missing)
        raise RuntimeError(
            f"Missing required PostgreSQL environment variables: {missing_values}"
        )


def require_datafordeler_env() -> None:
    missing = _missing_env(
        {
            "DATAFORDELER_USER": DATAFORDELER_USER,
            "DATAFORDELER_PASSWORD": DATAFORDELER_PASSWORD,
        }
    )
    if missing:
        missing_values = ", ".join(missing)
        raise RuntimeError(
            f"Missing required Datafordeler environment variables: {missing_values}"
        )


# POSTGRESQL DATABASE
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME") or os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB", "circlek")

# DATAFORDELER
DATAFORDELER_USER = os.getenv("DATAFORDELER_USER")
DATAFORDELER_PASSWORD = os.getenv("DATAFORDELER_PASSWORD")
DATAFORDELER_API_KEY = os.getenv("DATAFORDELER_API_KEY")
