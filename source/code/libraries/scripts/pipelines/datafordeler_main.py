import logging

from libraries.scripts import api, upserts

logger = logging.getLogger(__name__)

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
            logger.info("Running %s module...", name)
            module.main()
            logger.info("%s module completed successfully.", name)
        except Exception as e:
            logger.exception("Error in %s module: %s", name, e)

if __name__ == "__main__":
    main()
    
