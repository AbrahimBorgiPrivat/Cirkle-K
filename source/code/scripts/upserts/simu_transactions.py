from utils.orchestrator import update_insert_dw, ensure_table_structure
from utils.db_types import TEXT, Float, BIGINT, TIMESTAMP, JSONB
from scripts.simulations import transactions

def upsert(create_table_if_not_exist=False):
    transaction, transaction_lines, campaign_transactions = transactions.main()
    db_name='circlek'
    schema_name='public'
    
    ### UPSERT transaction ###
    
    table_name='transactions'
    fields_dict = {
        'transaction_id': {"type": TEXT(), "primary_key": True, "autoincrement": False},
        'timestamp': {"type": TIMESTAMP()},
        'cashier_id': {"type": TEXT()},
        'card_id': {"type": TEXT()},
        'context': {"type": JSONB()},
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
                     new_data=transaction,
                     pk=pk,
                     update_fields=update_fields,
                     not_included_in_update_fields=[])
    
    
    ### UPSERT transaction_lines ###
    
    table_name='transaction_lines'
    fields_dict = {
        'id': {"type": TEXT(), "primary_key": True, "autoincrement": False},
        'transaction_id': {"type": TEXT()},
        'product_id': {"type": BIGINT()},
        'product': {"type": TEXT()},
        'price': {"type": Float()},
        'discount': {"type": Float()},
        'quantity': {"type": BIGINT()},
        'total': {"type": Float()},
        'campaign_transaction_id': {"type": TEXT()},
        'context': {"type": JSONB()}
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
                     new_data=transaction_lines,
                     pk=pk,
                     update_fields=update_fields,
                     not_included_in_update_fields=[])
    
    ### UPSERT campaign_transactions ###
    
    table_name='campaign_transactions'
    fields_dict = {
        'campaign_transaction_id': {"type": TEXT(), "primary_key": True, "autoincrement": False},
        'campaign_id': {"type": BIGINT()},
        'customer_id': {"type": TEXT()},
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
                     new_data=campaign_transactions,
                     pk=pk,
                     update_fields=update_fields,
                     not_included_in_update_fields=[])
    
    return transaction, transaction_lines, campaign_transactions

def main(create_table_if_not_exist=False):
    return upsert(create_table_if_not_exist=create_table_if_not_exist)

if __name__ == "__main__":
    main()