from scripts import api, upserts

def main():
    modules = [
        ("API DOWNLOAD AF DATAFORMIDLER", api.dataformidler_download_files),
        ("DAGI Kommuneinddeling", upserts.dagi_kommuneinddeling),
        ("DAGI Landsdel", upserts.dagi_landsdel),
        ("DAGI Postnummerinddeling", upserts.dagi_postnummeriddeling),
        ("DAGI Region", upserts.dagi_region),
        ("DAGI Storkreds", upserts.dagi_storkreds),
        ("DAR Adresse", upserts.dar_adresse),
        ("DAR Adressepunkt", upserts.dar_adressepunkt),
        ("DAR Husnummer", upserts.dar_husnummer),
        ("DAR Navngivenvej", upserts.dar_navngivenvej),
        ("DAR Postnummer", upserts.dar_postnummer)
    ]

    for name, module in modules:
        try:
            print(f"Running {name} module...")
            module.main()
            print(f"{name} module completed successfully.\n")
        except Exception as e:
            print(f"Error in {name} module: {e}\n")

if __name__ == "__main__":
    main()
    