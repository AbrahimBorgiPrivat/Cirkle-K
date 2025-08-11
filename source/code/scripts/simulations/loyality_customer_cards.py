from faker import Faker
import uuid
import random
from utils import orchestrator
from utils.weights import REGION_WEIGHTS,SEGMENT_WEIGHTS
from collections import defaultdict
from datetime import datetime, timedelta, date
from tqdm import tqdm

def generate_loyalty_id():
    return f"LOYALTY-{uuid.uuid4().hex[:8].upper()}"

def generate_card_number():
    return ''.join([str(random.randint(0, 9)) for _ in range(16)])

def generate_card_type():
    return random.choice(["Visa", "MasterCard", "Dankort", "Amex"])

def build_station_pool() -> dict[str, list[dict]]:
    db_name='circlek'
    sql_stmt = 'SELECT * FROM public.stations_view'
    stations = orchestrator.get_data_from_db(db_name=db_name,
                                        sql_query=sql_stmt)
    
    region_groups = defaultdict(list)
    for row in stations:
        region = row.get("region")
        if region:
            region_groups[region].append(row)
    return region_groups

def get_weighted_home_station(region_pool: dict[str, list[dict]]) -> dict:
    regions = list(REGION_WEIGHTS.keys())
    weights = list(REGION_WEIGHTS.values())
    while True:
        chosen_region = random.choices(regions, weights=weights)[0]
        if region_pool.get(chosen_region):
            return random.choice(region_pool[chosen_region])

def get_segmentationsgroups() -> dict:
    db_name='circlek'
    sql_stmt = 'SELECT * FROM public.segmentationsgroups'
    groups = orchestrator.get_data_from_db(db_name=db_name,
                                        sql_query=sql_stmt)
    return groups

def get_weighted_segmentation(groups: list[dict], weights: dict[int, float]) -> dict:
    group_weights = [weights[g["id"]] for g in groups]
    return random.choices(groups, weights=group_weights, k=1)[0]

def get_random_date_with_weekday_bias(date: date, weekday_weights=None) -> datetime.date:
    if weekday_weights is None:
        weekday_weights = [1/7] * 7
    target_weekday = random.choices(range(7), weights=weekday_weights)[0]
    candidate_date = date
    while candidate_date.weekday() != target_weekday:
        candidate_date -= timedelta(days=1)
    return candidate_date

def generate_customers(num_customers=100):
    customers = []
    cards = []
    fake = Faker("da_DK")
    region_pool  = build_station_pool()
    segmentationsgroups = get_segmentationsgroups()

    for _ in tqdm(range(num_customers)):
        loyalty_id = generate_loyalty_id()
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        country = 'Denmark'
        home_station = get_weighted_home_station(region_pool)
        segment = get_weighted_segmentation(groups=segmentationsgroups,
                                        weights=SEGMENT_WEIGHTS)
        peak_hours = segment['peak_hours']
        hour_weights = segment['hour_weights']
        weekday_weights = segment['weekday_weights']
        base_date = datetime.now() - timedelta(days=random.randint(0, 729))
        base_date = get_random_date_with_weekday_bias(date=base_date,
                                                      weekday_weights=weekday_weights)
        signup_dt = orchestrator.generate_multimodal_time_on_date(base_date, 
                                                                  peak_hours=peak_hours, 
                                                                  weights=hour_weights)
        customer = {
            "loyalty_id": loyalty_id,
            "name": name,
            "phone": phone,
            "email": email,
            "country": country,
            "primary_station": home_station['pno'],
            "segmentationgroup": segment['id'],
            "signed_up": signup_dt,
            "perm_notify": random.choices([True, False], weights=[90, 10])[0],
            "perm_email": random.choices([True, False], weights=[90, 10])[0],
            "perm_sms": random.choices([True, False], weights=[90, 10])[0],
            "perm_survey": random.choices([True, False], weights=[90, 10])[0],
        }

        customers.append(customer)

    # Generate 1–4 payment cards per customer
        for _ in range(random.randint(1, 4)):
            card = {
                "card_id": str(uuid.uuid4()),
                "card_number": generate_card_number(),
                "card_type": generate_card_type(),
                "loyalty_id": loyalty_id
            }
            cards.append(card)

    return customers, cards

def main(num_customers=10000):
    return generate_customers(num_customers=num_customers)

if __name__ == "__main__":
    customers, cards = main(20)
    print("--- Customers ---")
    for c in customers:
        print(c)
    
    
