from datetime import datetime, timedelta
import random
import uuid

def generate_electric_transaction_line(transaction: dict, products: list[dict]) -> dict:
    product = next(p for p in products if p["product_id"] == 3)

    price = round(random.uniform(3.5, 6.5), 2)
    quantity = max(5, round(random.normalvariate(32, 8), 1))  # clamp to min 5 kWh

    # Simulate charge duration: assume ~1 min per 1 kWh
    duration = timedelta(minutes=int(quantity))
    end_time = datetime.fromisoformat(transaction["timestamp"])
    start_time = end_time - duration

    return {
        "id": str(uuid.uuid4()),
        "transaction_id": transaction["transaction_id"],
        "product_id": product["product_id"],
        "product": product["name"],
        "price": price,
        "discount": 0.0,
        "quantity": quantity,
        "total": round(quantity * price, 2),
        "campaign_transaction_id": None,
        "context": {
            "type": "charge",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        }
    }

def generate_gas_transaction_line(transaction: dict, products: list[dict]) -> dict:
    product_id = random.choice([1, 2])  # 95 or Diesel
    product = next(p for p in products if p["product_id"] == product_id)

    price = round(random.uniform(12.5, 14), 2)
    discount = 0.10  # Fixed per liter
    quantity = max(15, round(random.normalvariate(37, 8), 1))  # clamp to min 15L

    net_price = max(0, price - discount)
    total = round(quantity * net_price, 2)

    return {
        "id": str(uuid.uuid4()),
        "transaction_id": transaction["transaction_id"],
        "product_id": product["product_id"],
        "product": product["name"],
        "price": price,
        "discount": discount,
        "quantity": quantity,
        "total": total,
        "campaign_transaction_id": None,
        "context": None
    }

def generate_service_transaction_line(
    transaction: dict,
    products: list[dict],
    customer_loyalty_id: str,
    service_counter: dict,
    campaign_transactions: list[dict]
) -> dict:
    product_id = random.choice([5, 6])
    product = next(p for p in products if p["product_id"] == product_id)
    price = product["price"]
    quantity = 1
    campaign_id = 8  # Car wash campaign ID

    # Increment service count
    current_count = service_counter.get(customer_loyalty_id, 0) + 1
    service_counter[customer_loyalty_id] = current_count

    is_reward = (current_count % 6 == 0)  # Every 6th is free

    campaign_transaction_id = None
    discount = 1.0 if is_reward else 0.0
    total = 0.0 if is_reward else round(price * quantity, 2)

    if is_reward:
        campaign_transaction_id = str(uuid.uuid4())
        campaign_transactions.append({
            "campaign_transaction_id": campaign_transaction_id,
            "campaign_id": campaign_id,
            "customer_id": customer_loyalty_id
        })

    return {
        "id": str(uuid.uuid4()),
        "transaction_id": transaction["transaction_id"],
        "product_id": product_id,
        "product": product["name"],
        "price": price,
        "discount": discount,
        "quantity": quantity,
        "total": total,
        "campaign_transaction_id": campaign_transaction_id,
        "context": None
    }

def generate_cashier_transaction_lines(
    transaction: dict,
    products: list[dict],
    customer_loyalty_id: str,
    campaigns: list[dict],
    campaign_counts: dict,
    campaign_reward_queue: dict,
    campaign_transactions: list[dict]
) -> list[dict]:
    lines = []

    cashier_products = [p for p in products if p["type"] == "cashier"]
    num_lines = random.choices([1, 2, 3, 4, 5], weights=[0.3, 0.3, 0.2, 0.1, 0.1])[0]

    for _ in range(num_lines):
        product = random.choice(cashier_products)
        price = product["price"]
        product_id = product["product_id"]

        quantity = random.choices(
            population=range(1, 11),
            weights=[0.15, 0.25, 0.25, 0.15, 0.1, 0.05, 0.02, 0.015, 0.01, 0.005]
        )[0]

        # Look for campaign tied to this product
        campaign = next((c for c in campaigns if c["product_id"] == product_id), None)
        free_units = 0
        campaign_transaction_id = None

        if campaign:
            key = (customer_loyalty_id, campaign["id"])
            # Handle previous redemption
            pending_free = campaign_reward_queue.get(key, 0)

            if pending_free > 0:
                free_units = 1
                campaign_reward_queue[key] = pending_free - 1
                campaign_transaction_id = str(uuid.uuid4())
                campaign_transactions.append({
                    "campaign_transaction_id": campaign_transaction_id,
                    "campaign_id": campaign["id"],
                    "customer_id": customer_loyalty_id
                })

            else:
                # Increment count toward threshold
                campaign_counts[key] = campaign_counts.get(key, 0) + quantity
                if campaign_counts[key] >= campaign["number"]:
                    # Earn reward
                    campaign_counts[key] = campaign_counts[key] - campaign["number"]
                    campaign_reward_queue[key] = campaign_reward_queue.get(key, 0) + 1

        # Handle line-level discount
        discounted_quantity = free_units
        paid_quantity = quantity - discounted_quantity
        discount = 1.0 if discounted_quantity > 0 else 0.0

        total = round(paid_quantity * price, 2)

        line = {
            "id": str(uuid.uuid4()),
            "transaction_id": transaction["transaction_id"],
            "product_id": product_id,
            "product": product["name"],
            "price": price,
            "discount": discount,
            "quantity": quantity,
            "total": total,
            "campaign_transaction_id": campaign_transaction_id,
            "context": None
        }
        lines.append(line)

    return lines
