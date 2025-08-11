from utils.orchestrator import update_insert_dw, ensure_table_structure
from utils.db_types import TEXT, BOOLEAN, BIGINT
from scripts.simulations import cashier

def upsert(create_table_if_not_exist=False):
    cashiers = cashier.main()
    db_name='circlek'
    schema_name='public'
    table_name='cashier'
    fields_dict = {
        'cashier_id': {"type": TEXT(), "primary_key": True, "autoincrement": False},
        'type': {"type": TEXT()},
        'pno': {"type": BIGINT()},
    }
    test_table_structure = ensure_table_structure(db_name=db_name,
                                schema_name=schema_name,
                                table_name=table_name,
                                fields_dict=fields_dict,
                                create_table_if_not_exist=create_table_if_not_exist)
    if not test_table_structure:
        raise RuntimeError(f"Table '{schema_name}.{table_name}' does not exist or has incorrect structure.")
    
    pk = [col for col, config in fields_dict.items() if isinstance(config, dict) and config.get("primary_key", False)]
    update_fields = [col for col in fields_dict if col not in pk]
    update_insert_dw(db_name=db_name,
                     schema=schema_name,
                     table=table_name,
                     new_data=cashiers,
                     pk=pk,
                     update_fields=update_fields,
                     not_included_in_update_fields=[])
    return cashiers

def main(create_table_if_not_exist=False):
    return upsert(create_table_if_not_exist=create_table_if_not_exist)

if __name__ == "__main__":
    main()