import logging

from libraries.utils.db_types import BIGINT, Date, Numeric
from libraries.utils.orchestrator import (
    ensure_table_structure,
    load_csvs_as_dicts,
    update_insert_dw,
)
from libraries.utils.path_config import CSV_DIR

logger = logging.getLogger(__name__)


def upsert_csv(create_table_if_not_exist: bool = False):
    file_names = ["transactions2017.csv", "transactions2018.csv"]
    csv_paths = [CSV_DIR / file_name for file_name in file_names]
    data = load_csvs_as_dicts(
        file_paths=csv_paths,
        delimiter=";",
        with_id=True,
    )

    db_name = "circlek"
    schema_name = "interview"
    table_name = "transactions"
    fields_dict = {
        "id": {"type": BIGINT(), "primary_key": True, "autoincrement": False},
        "site_number": {"type": BIGINT()},
        "trn_transaction_date": {"type": Date()},
        "trn_promotion_id": {"type": BIGINT()},
        "trn_item_number": {"type": BIGINT()},
        "units": {"type": Numeric()},
        "gross_amount": {"type": Numeric()},
        "vat": {"type": Numeric()},
        "cost_price": {"type": Numeric()},
    }
    test_table_structure = ensure_table_structure(
        db_name=db_name,
        schema_name=schema_name,
        table_name=table_name,
        fields_dict=fields_dict,
        create_table_if_not_exist=create_table_if_not_exist,
    )
    if not test_table_structure:
        raise RuntimeError(
            f"Table '{schema_name}.{table_name}' does not exist or has incorrect structure."
        )

    pk = [
        col
        for col, config in fields_dict.items()
        if isinstance(config, dict) and config.get("primary_key", False)
    ]
    update_fields = [col for col in fields_dict if col not in pk]
    update_insert_dw(
        db_name=db_name,
        schema=schema_name,
        table=table_name,
        new_data=data,
        pk=pk,
        update_fields=update_fields,
    )
    logger.info(
        "Data from %s has been inserted/updated in %s.%s.",
        ", ".join(file_names),
        schema_name,
        table_name,
    )
    return data


def main(create_table_if_not_exist: bool = False):
    return upsert_csv(create_table_if_not_exist=create_table_if_not_exist)


if __name__ == "__main__":
    main()
