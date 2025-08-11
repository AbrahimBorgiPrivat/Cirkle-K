import random
import uuid
from datetime import timedelta, datetime
from utils import orchestrator, simulations_helper_functions
from collections import defaultdict
from tqdm import tqdm

def get_customers() -> list[dict]:
    db_name='circlek'
    sql_stmt = '''SELECT cust.loyalty_id,
                            cust.primary_station,
                            sta.region,
                            cust.segmentationgroup,
                            cust.signed_up,
                            seggroup.avg_txn_per_month,
                            seggroup.weekday_weights,
                            seggroup.peak_hours,
                            seggroup.hour_weights,
                            seggroup.product_types
                    FROM public.loyality_customers cust
                    LEFT JOIN public.segmentationsgroups seggroup ON seggroup.id = cust.segmentationgroup
                    LEFT JOIN public.stations_view sta ON sta.pno = cust.primary_station'''
    customers = orchestrator.get_data_from_db(db_name=db_name,
                                        sql_query=sql_stmt)
    return customers

def get_cards() -> list[dict]:
    db_name='circlek'
    sql_stmt = 'SELECT * FROM public.cards'
    customers = orchestrator.get_data_from_db(db_name=db_name,
                                        sql_query=sql_stmt)
    return customers

def get_products() -> list[dict]:
    db_name='circlek'
    sql_stmt = 'SELECT * FROM public.products'
    products = orchestrator.get_data_from_db(db_name=db_name,
                                        sql_query=sql_stmt)
    return products

def get_campaigns() -> list[dict]:
    db_name='circlek'
    sql_stmt = 'SELECT * FROM public.campaigns'
    campaigns = orchestrator.get_data_from_db(db_name=db_name,
                                        sql_query=sql_stmt)
    return campaigns

def get_cashiers_by_station() -> dict[int, list[dict]]:
    db_name = 'circlek'
    sql_stmt = 'SELECT * FROM public.cashier'
    cashiers = orchestrator.get_data_from_db(db_name=db_name, sql_query=sql_stmt)
    cashiers_by_station = defaultdict(list)
    for c in cashiers:
        pno = c["pno"]
        cashiers_by_station[pno].append(c)
    return cashiers_by_station

def get_station_pool_by_region() -> dict[str, list[dict]]:
    db_name = 'circlek'
    sql_stmt = 'SELECT * FROM public.stations_view'
    stations = orchestrator.get_data_from_db(db_name=db_name, sql_query=sql_stmt)
    station_pool_by_region = defaultdict(list)
    for c in stations:
        region = c["region"]
        station_pool_by_region[region].append(c)
    return station_pool_by_region

def generate_transactions_for_customer(customer, cards, cashiers_by_station, station_pool_by_region):
    transactions = []
    card_ids = [card['card_id'] for card in cards if card['loyalty_id'] == customer['loyalty_id']]
    region = customer['region']
    primary_pno = customer['primary_station']
    signup_date = customer['signed_up'].date()

    # Estimate number of transactions for this user
    months_since_signup = (datetime.now().date().year - signup_date.year) * 12 + (datetime.now().date().month - signup_date.month)
    txn_count = int(round(random.gauss(customer["avg_txn_per_month"], 1.5) * months_since_signup))
    txn_count = max(txn_count, 1)

    for _ in range(txn_count):
        transaction_id = str(uuid.uuid4())

        # --- TIME ---
        base_day = signup_date + timedelta(days=random.randint(0, (datetime.now().date() - signup_date).days))
        weekday_weights = customer["weekday_weights"]
        txn_date = orchestrator.get_random_date_with_weekday_bias(base_day, weekday_weights)
        txn_time = orchestrator.generate_multimodal_time_on_date(txn_date, customer["peak_hours"], customer["hour_weights"])

        # --- CARD ---
        card_id = random.choice(card_ids)

        # --- CASHIER & TYPE ---
        cashier_type = random.choices(
            list(customer["product_types"].keys()),
            weights=list(customer["product_types"].values())
        )[0]

        if random.random() < 0.5:
            possible_cashiers = cashiers_by_station.get(primary_pno, [])
        else:
            region_stations = station_pool_by_region.get(region, [])
            alt_station = random.choice(region_stations)
            possible_cashiers = cashiers_by_station.get(alt_station["pno"], [])

        cashier_options = [c for c in possible_cashiers if c["type"] == cashier_type]
        if not cashier_options:
            continue  # Skip if no matching cashier type

        cashier = random.choice(cashier_options)

        # --- Build transaction ---
        txn = {
            "transaction_id": transaction_id,
            "timestamp": txn_time.isoformat(),
            "cashier_id": cashier["cashier_id"],
            "card_id": card_id,
            "context": None
        }
        transactions.append(txn)

        # --- Conditional extra transaction logic ---
        # Rule: EV Commuter -> buys in shop before charging
        if customer["segmentationgroup"] == 1 and cashier_type == "cashier":
            if random.random() < customer["product_types"].get("electric", 0):
                electric_cashiers = [c for c in possible_cashiers if c["type"] == "electric"]
                if electric_cashiers:
                    electric_cashier = random.choice(electric_cashiers)
                    offset = timedelta(minutes=random.randint(5, 30))
                    new_txn_time = txn_time + offset
                    new_txn = {
                        "transaction_id": str(uuid.uuid4()),
                        "timestamp": new_txn_time.isoformat(),
                        "cashier_id": electric_cashier["cashier_id"],
                        "card_id": card_id,
                        "context": {
                            "context": "bought in shop before",
                            "former_transaction_id": transaction_id
                        }
                    }
                    transactions.append(new_txn)

        # Rule: Gas or service -> shop after
        if cashier_type in ["gas", "service"]:
            if random.random() < customer["product_types"].get("cashier", 0):
                cashier_cashiers = [c for c in possible_cashiers if c["type"] == "cashier"]
                if cashier_cashiers:
                    cashier_after = random.choice(cashier_cashiers)
                    offset = timedelta(minutes=random.randint(1, 5))
                    new_txn_time = txn_time + offset
                    new_txn = {
                        "transaction_id": str(uuid.uuid4()),
                        "timestamp": new_txn_time.isoformat(),
                        "cashier_id": cashier_after["cashier_id"],
                        "card_id": card_id,
                        "context": {
                            "context": "bought in shop after",
                            "former_transaction_id": transaction_id
                        }
                    }
                    transactions.append(new_txn)

    return transactions

def simulate_transactions() -> tuple[list[dict], list[dict], list[dict]]:
    customers = get_customers()
    cards = get_cards()
    cashiers_by_station = get_cashiers_by_station()
    station_pool_by_region = get_station_pool_by_region()
    products = get_products()
    campaigns = get_campaigns()

    transactions = []
    transaction_lines = []
    campaign_transactions = []

    # Trackers for cashier/service campaign logic
    service_counter = defaultdict(int)
    campaign_counts = defaultdict(int)
    campaign_reward_queue = defaultdict(int)

    for customer in tqdm(customers):
        customer_txns = generate_transactions_for_customer(
            customer,
            cards,
            cashiers_by_station,
            station_pool_by_region
        )

        transactions.extend(customer_txns)

        for txn in customer_txns:
            cashier_id = txn["cashier_id"]
            pno = int(cashier_id.split("-")[0])
            cashier_list = cashiers_by_station.get(pno, [])
            cashier = next((c for c in cashier_list if c["cashier_id"] == cashier_id), None)

            if not cashier:
                continue  # skip if cashier is not found (shouldn't happen)

            cashier_type = cashier["type"]
            loyalty_id = customer["loyalty_id"]

            # Dispatch by type
            if cashier_type == "gas":
                line = simulations_helper_functions.generate_gas_transaction_line(txn, products)
                transaction_lines.append(line)

            elif cashier_type == "electric":
                line = simulations_helper_functions.generate_electric_transaction_line(txn, products)
                transaction_lines.append(line)

            elif cashier_type == "service":
                line = simulations_helper_functions.generate_service_transaction_line(
                    txn, products, loyalty_id,
                    service_counter,
                    campaign_transactions
                )
                transaction_lines.append(line)

            elif cashier_type == "cashier":
                lines = simulations_helper_functions.generate_cashier_transaction_lines(
                    txn, products, loyalty_id,
                    campaigns,
                    campaign_counts,
                    campaign_reward_queue,
                    campaign_transactions
                )
                transaction_lines.extend(lines)

    return transactions, transaction_lines, campaign_transactions

def main():
    return simulate_transactions()

if __name__ == "__main__":
    transaction, transaction_lines, campaign_transactions = main()
    print(transaction_lines[0:2])
    print(campaign_transactions[0:2])
    