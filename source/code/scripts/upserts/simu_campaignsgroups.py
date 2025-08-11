from utils.orchestrator import load_json_file, update_insert_dw, ensure_table_structure
from utils.db_types import BIGINT, TEXT,BOOLEAN, Date
from utils.path_config import JSON_DIR

def convert_upsert(create_table_if_not_exist=False):
    file_path = JSON_DIR
    file_name = "CAMPAIGNS.json"
    segmentationsgroups = load_json_file(file_path,file_name)
    db_name='circlek'
    schema_name='public'
    table_name='campaigns'
    fields_dict = {
        'id': {"type": BIGINT(), "primary_key": True, "autoincrement": False},
        'name': {"type": TEXT()},
        'description': {"type": TEXT()},
        'product_id': {"type": BIGINT()},
        'number': {"type": BIGINT()},
        'start_date': {"type": Date()},
        'end_date': {"type": Date()},
        'active': {"type": BOOLEAN()}, 
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
                    new_data=segmentationsgroups,
                    pk=pk,
                    update_fields=update_fields)
    print(f"Data from {file_name} has been inserted/updated in {schema_name}.{table_name}.")
    return segmentationsgroups

def main(create_table_if_not_exist=False):
    return convert_upsert(create_table_if_not_exist=create_table_if_not_exist)

if __name__ == "__main__":
    main()