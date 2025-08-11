import uuid
import random
from utils import orchestrator

def build_station_pool() -> list[dict]:
    db_name = 'circlek'
    sql_stmt = 'SELECT pno FROM public.stations'
    stations = orchestrator.get_data_from_db(db_name=db_name, sql_query=sql_stmt)
    return stations

def generate_cashier() -> list[dict]:
    stations = build_station_pool()
    cashiers = []

    for station in stations:
        pno = station["pno"]
        cashier_index = 1  # reset for each station

        def add_cashiers(count, cashier_type):
            nonlocal cashier_index
            for _ in range(count):
                cashiers.append({
                    "cashier_id": f"{pno}-{cashier_index}",
                    "type": cashier_type,
                    "pno": pno
                })
                cashier_index += 1
        add_cashiers(random.randint(2, 4), "cashier")
        add_cashiers(random.randint(1, 2), "service")
        add_cashiers(random.randint(1, 10), "electric")
        add_cashiers(random.choice([i for i in range(2, 13, 2)]), "gas") 
    return cashiers

def main():
    return generate_cashier() 

if __name__ == "__main__":
    all_cashiers = main()
    print(all_cashiers[:5])  
