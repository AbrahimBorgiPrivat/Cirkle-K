from utils.orchestrator import update_insert_dw, ensure_table_structure
from utils.db_types import TEXT, BOOLEAN, BIGINT, TIMESTAMP
from scripts.simulations import loyality_customer_cards

def upsert(create_table_if_not_exist=False, n_simulations = 10000):
    customers, cards =loyality_customer_cards.main(num_customers=n_simulations)
    db_name='circlek'
    schema_name='public'
    
    ### UPSERT loyality_customers ###
    
    table_name='loyality_customers'
    fields_dict = {
        'loyalty_id': {"type": TEXT(), "primary_key": True, "autoincrement": False},
        'name': {"type": TEXT()},
        'phone': {"type": TEXT()},
        'email': {"type": TEXT()},
        'country': {"type": TEXT()},
        'primary_station': {"type": BIGINT()},
        'segmentationgroup': {"type": BIGINT()},
        'signed_up': {"type": TIMESTAMP()},
        'perm_notify': {"type": BOOLEAN()},
        'perm_email': {"type": BOOLEAN()},
        'perm_sms': {"type": BOOLEAN()},
        'perm_survey': {"type": BOOLEAN()},
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
                     new_data=customers,
                     pk=pk,
                     update_fields=update_fields,
                     not_included_in_update_fields=[])
    
    
    ### UPSERT cards ###
    
    table_name='cards'
    fields_dict = {
        'card_id': {"type": TEXT(), "primary_key": True, "autoincrement": False},
        'card_number': {"type": TEXT()},
        'card_type': {"type": TEXT()},
        'loyalty_id': {"type": TEXT()}
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
                     new_data=cards,
                     pk=pk,
                     update_fields=update_fields,
                     not_included_in_update_fields=[])
    
    return customers, cards

def main(create_table_if_not_exist=False, n_simulations = 10000):
    return upsert(create_table_if_not_exist=create_table_if_not_exist,
                  n_simulations = n_simulations)

if __name__ == "__main__":
    main()