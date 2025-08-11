from scripts import upserts

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
            print(f"🔄 Running: {name}")
            module.main()
            print(f"✅ Completed: {name}\n")
        except Exception as e:
            print(f"❌ Error in {name}: {e}\n")

if __name__ == "__main__":
    main()