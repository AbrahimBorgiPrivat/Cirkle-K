from utils.orchestrator import load_json_file, select_columns, update_insert_dw, ensure_table_structure
from utils.db_types import TEXT, TIMESTAMP
from tqdm import tqdm
from utils.path_config import JSON_DIR

def convert_upsert(create_table_if_not_exist=False):
    file_path = JSON_DIR
    file_name = "DAR_Husnummer_1.json"
    columns_to_keep = {
        'id_lokalId': 'id',
        'adgangsadressebetegnelse': 'adgangsadressebetegnelse',
        'husnummerretning': 'husnummerretning',
        'husnummertekst': 'husnummertekst',
        'adgangspunkt': 'adgangspunkt_id',
        'vejpunkt': 'vejpunkt_id',
        'jordstykke': 'jordstykke_id',
        'placeretPåForeløbigtJordstykke': 'placeret_paa_foreloebigt_jordstykke',
        'geoDanmarkBygning': 'geo_danmark_bygning_id',
        'adgangTilBygning': 'adgang_til_bygning',
        'adgangTilTekniskAnlæg': 'adgang_til_teknisk_anlaeg',
        'vejmidte': 'vejmidte_id',
        'afstemningsområde': 'afstemningsomraade_id',
        'kommuneinddeling': 'kommuneinddeling_id',
        'supplerendeBynavn': 'supplerende_bynavn',
        'navngivenVej': 'navngiven_vej_id',
        'postnummer': 'postnummer_id',
        'id_namespace': 'id_namespace',
        'status': 'status',
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
    table_name='dar_husnummer'
    fields_dict = {
        'id': {"type": TEXT(), "primary_key": True, "autoincrement": False},
        'adgangsadressebetegnelse': {"type": TEXT()},
        'husnummerretning': {"type": TEXT()},
        'husnummertekst': {"type": TEXT()},
        'adgangspunkt_id': {"type": TEXT()},
        'vejpunkt_id': {"type": TEXT()},
        'jordstykke_id': {"type": TEXT()},
        'placeret_paa_foreloebigt_jordstykke': {"type": TEXT()},
        'geo_danmark_bygning_id': {"type": TEXT()},
        'adgang_til_bygning': {"type": TEXT()},
        'adgang_til_teknisk_anlaeg': {"type": TEXT()},
        'vejmidte_id': {"type": TEXT()},
        'afstemningsomraade_id': {"type": TEXT()},
        'kommuneinddeling_id': {"type": TEXT()},
        'supplerende_bynavn': {"type": TEXT()},
        'navngiven_vej_id': {"type": TEXT()},
        'postnummer_id': {"type": TEXT()},
        'id_namespace': {"type": TEXT()},
        'status': {"type": TEXT()},
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

    chunk_size = 10000  
    total_upserted = 0

    for i in tqdm(range(0, len(data), chunk_size)):
        chunk = data[i:i + chunk_size]
        update_insert_dw(db_name=db_name,
                         schema=schema_name,
                            table=table_name,
                         new_data=chunk,
                         pk=pk,
                         update_fields=update_fields,
                         not_included_in_update_fields=['createdtime'])
        total_upserted += len(chunk)
    print(f"Data from {file_name} has been inserted/updated in {schema_name}.{table_name}.")
    return total_upserted

def main(create_table_if_not_exist=False):
    return convert_upsert(create_table_if_not_exist=create_table_if_not_exist)

if __name__ == "__main__":
    main(True)