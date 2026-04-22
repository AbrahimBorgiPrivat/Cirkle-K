import logging

from libraries.scripts import upserts

logger = logging.getLogger(__name__)

# Define which modules to run — just comment/uncomment to control flow
run_modules = [
    ("Simulate Products", upserts.simu_products),
    ("Simulate Campaign Groups", upserts.simu_campaignsgroups),
    ("Upsert Stations", upserts.stations),
    ("Simulate Cashiers", upserts.simu_cashier),
    ("Simulate Segmentation Groups", upserts.simu_segmentationgroups),
    ("Simulate Customers & Cards", upserts.simu_customer_cards),
    ("Simulate Transactions", upserts.simu_transactions)
]

def main():
    for name, module in run_modules:
        try:
            logger.info("Running: %s", name)
            module.main()
            logger.info("Completed: %s", name)
        except Exception as e:
            logger.exception("Error in %s: %s", name, e)

if __name__ == "__main__":
    main()
