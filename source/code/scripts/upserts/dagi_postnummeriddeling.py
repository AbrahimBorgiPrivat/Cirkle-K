from utils.orchestrator import load_json_file, select_columns, update_insert_dw, ensure_table_structure
from utils.db_types import BIGINT, TEXT, TIMESTAMP, BOOLEAN
from utils.path_config import JSON_DIR

def convert_upsert(create_table_if_not_exist=False):
    file_path = JSON_DIR
    file_name = "DAGI_Postnummerinddeling_1.json"
    columns_to_keep = {
        'id_lokalId': 'id',
        'navn': 'navn',
        'postnummer': 'postnr',
        'gmlId': 'gml_id',
        'DAGIid': 'dag_id',
        'id_namespace': 'id_namespace',
        'dataspecifikation': 'dataspecifikation',
        'erGadepostnummer': 'er_gadepostnummer',
        'status': 'status',
        'landekode': 'landekode',
        'geometristatus': 'geometristatus',
        'skala': 'skala',
        'geometri': 'geometri',
        'virkningFra': 'virkning_fra',
        'virkningTil': 'virkning_til',
        'virkningsaktoer': 'virkningsaktoer',
        'registreringFra': 'registrering_fra',
        'registreringTil': 'registrering_til',
        'registreringsaktoer': 'registreringsaktoer',
        'datafordelerOpdateringstid': 'datafordeler_opdateringstid'
    }

    data = load_json_file(file_path, 
                          file_name)
    data = select_columns(data_list=data, 
                                 selected_keys_with_rename=columns_to_keep,
                                 with_update_and_created_time=True)
    db_name='circlek'
    schema_name='datafordeler'
    table_name='dagi_postnummerinddeling'
    fields_dict = {
        'id': {"type": BIGINT(), "primary_key": True, "autoincrement": False},
        'navn': {"type": TEXT()},
        'postnr': {"type": TEXT()},
        'gml_id': {"type": TEXT()},
        'dag_id': {"type": TEXT()},
        'id_namespace': {"type": TEXT()},
        'dataspecifikation': {"type": TEXT()},
        'er_gadepostnummer': {"type": BOOLEAN()},
        'status': {"type": TEXT()},
        'landekode': {"type": TEXT()},
        'geometristatus': {"type": TEXT()},
        'skala': {"type": TEXT()},
        'geometri': {"type": TEXT()},
        'virkning_fra': {"type": TIMESTAMP()},
        'virkning_til': {"type": TIMESTAMP()},
        'virkningsaktoer': {"type": TEXT()},
        'registrering_fra': {"type": TIMESTAMP()},
        'registrering_til': {"type": TIMESTAMP()},
        'registreringsaktoer': {"type": TEXT()},
        'datafordeler_opdateringstid': {"type": TIMESTAMP()},
        'updatetime': {"type": TIMESTAMP()},
        'createdtime': {"type": TIMESTAMP()}
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
                     new_data=data,
                     pk=pk,
                     update_fields=update_fields,
                    not_included_in_update_fields=['createdtime'])
    number_of_rows_upserted = len(data)
    print(f"Data from {file_name} has been inserted/updated in {schema_name}.{table_name}.")
    return number_of_rows_upserted

def main(create_table_if_not_exist=False):
    return convert_upsert(create_table_if_not_exist=create_table_if_not_exist)

if __name__ == "__main__":
    main(True)