import json
import random
import os
import datetime
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

# Constants
NUM_SUPPLIERS = 10
NUM_USERS = 15 
DOMAIN_DIR = "envs/retail" 
DATA_DIR = f"{DOMAIN_DIR}/data"

os.makedirs(DATA_DIR, exist_ok=True)


def get_id(n):
    """Constraint 3 & 17: IDs must be strings, incremental, starting from '1'."""
    return str(n)

def get_timestamps():
    """Constraint 10: created_at < updated_at."""
    created = fake.date_time_between(start_date="-2y", end_date="-1m")
    updated = fake.date_time_between(start_date=created, end_date="now")
    return created.isoformat(), updated.isoformat()

def generate_realistic_email(first_name, last_name):
    """Constraint 12: Realistic emails with domains and random numbers."""
    domains = ["gmail.com", "yahoo.com", "outlook.com", "retail-store.com", "provider.net"]
    domain = random.choice(domains)
    separator = random.choice(["", ".", "_", "-"])
    number = str(random.randint(1, 999)) if random.random() > 0.5 else ""
    email = f"{first_name.lower()}{separator}{last_name.lower()}{number}@{domain}"
    return email

def generate_phone():
    """Constraint 13: Consistent phone format."""
    area_code = random.randint(200, 999)
    part1 = random.randint(200, 999)
    part2 = random.randint(1000, 9999)
    return f"({area_code}) {part1}-{part2}"


print("Generating Suppliers...")
suppliers = {}
for i in range(1, NUM_SUPPLIERS + 1):
    s_id = get_id(i)
    created, updated = get_timestamps()
    suppliers[s_id] = {
        "supplier_id": s_id,
        "name": fake.company(),
        "contact_email": fake.company_email(),
        "address": fake.street_address(),
        "city": fake.city(),
        "state": fake.state_abbr(),
        "zip_code": fake.zipcode(),
        "country": "USA",
        "created_at": created,
        "updated_at": updated
    }

with open(f"{DATA_DIR}/suppliers.json", "w") as f:
    json.dump(suppliers, f, indent=2)


print("Generating Products...")
products = {}
product_counter = 1
categories = ["Electronics", "Home", "Clothing", "Sports", "Toys"]

# Constraint 1: Loop through Suppliers (Parents) to ensure max 3 products per supplier
for s_id in suppliers:
    # 0 to 3 products per supplier
    num_products = random.randint(1, 3) 
    
    for _ in range(num_products):
        p_id = get_id(product_counter)
        product_counter += 1
        created, updated = get_timestamps()
        
        # Constraint 5: Description can be empty (free-form)
        description = fake.sentence() if random.random() > 0.2 else ""
        
        products[p_id] = {
            "product_id": p_id,
            "name": f"{random.choice(categories)} {fake.word().capitalize()}",
            "description": description,
            "supplier_id": s_id,  # Constraint 8: Valid FK
            "unit_price": round(random.uniform(10.0, 500.0), 2),
            "created_at": created,
            "updated_at": updated
        }

with open(f"{DATA_DIR}/products.json", "w") as f:
    json.dump(products, f, indent=2)


print("Generating Users...")
users = {}
staff_roles = ["Store Manager", "Fulfillment Specialist"]
for i in range(1, NUM_USERS + 1):
    u_id = get_id(i)
    created, updated = get_timestamps()
    first = fake.first_name()
    last = fake.last_name()
    
    if i <= len(staff_roles):
        role = staff_roles[i-1]
        email = generate_realistic_email(first, last)
    else:
        role = "customer"
        email = generate_realistic_email(first, last)

    users[u_id] = {
        "user_id": u_id,
        "first_name": first,
        "last_name": last,
        "email": email,
        "role": role, 
        "address": fake.street_address(),
        "city": fake.city(),
        "state": fake.state_abbr(),
        "zip_code": fake.zipcode(),
        "country": "USA",
        "created_at": created,
        "updated_at": updated
    }

with open(f"{DATA_DIR}/users.json", "w") as f:
    json.dump(users, f, indent=2)


print("Generating Purchase Orders & Items...")
purchase_orders = {}
po_items = {}
po_counter = 1
po_item_counter = 1

# Constraint 1: Loop through Suppliers (Parents) -> Max 3 POs per supplier
for s_id in suppliers:
    num_pos = random.randint(0, 3)
    
    for _ in range(num_pos):
        po_id = get_id(po_counter)
        po_counter += 1
        created, updated = get_timestamps()
        
        purchase_orders[po_id] = {
            "purchase_order_id": po_id,
            "supplier_id": s_id,
            "order_date": fake.date_between(start_date="-1y", end_date="today").isoformat(),
            "status": random.choice(["pending", "received", "cancelled"]),
            "created_at": created,
            "updated_at": updated
        }
        
        # Items for this PO (Constraint 1: Max 3 items)
        num_items = random.randint(1, 3)
        # Find products belonging to THIS supplier (Constraint 7: Coherence)
        # Only select products from the current supplier to make sense
        supplier_products = [p for p in products.values() if p["supplier_id"] == s_id]
        
        if not supplier_products:
            continue # Skip adding items if supplier has no products
            
        for _ in range(num_items):
            poi_id = get_id(po_item_counter)
            po_item_counter += 1
            
            prod = random.choice(supplier_products)
            
            po_items[poi_id] = {
                "po_item_id": poi_id,
                "purchase_order_id": po_id,
                "product_id": prod["product_id"],
                "quantity": random.randint(10, 100),
                "unit_cost": round(prod["unit_price"] * 0.7, 2), 
                "created_at": created, 
                "updated_at": updated
            }

with open(f"{DATA_DIR}/purchase_orders.json", "w") as f:
    json.dump(purchase_orders, f, indent=2)
with open(f"{DATA_DIR}/purchase_order_items.json", "w") as f:
    json.dump(po_items, f, indent=2)


print("Generating Sales Orders, Items & Shipping...")
sales_orders = {}
so_items = {}
shipping = {}
so_counter = 1
so_item_counter = 1
shipping_counter = 1

all_product_ids = list(products.keys())

# Constraint 1: Loop through Users -> Max 3 SOs per user
for u_id, u_data in users.items():
    if u_data['role'] != "customer":
        continue # Only customers make orders
        
    num_sos = random.randint(0, 3)
    
    for _ in range(num_sos):
        so_id = get_id(so_counter)
        so_counter += 1
        created, updated = get_timestamps()
        status = random.choice(["placed", "processing", "shipped", "delivered", "cancelled", "returned"])
        
        # Constraint 5: cancel_reason is free-form, can be empty
        cancel_reason = ""
        if status == "cancelled":
            cancel_reason = random.choice(["Changed mind", "Found cheaper", "Wait too long"])
        
        sales_orders[so_id] = {
            "sales_order_id": so_id,
            "user_id": u_id,
            "order_date": fake.date_between(start_date="-6m", end_date="today").isoformat(),
            "status": status,
            "payment_method": random.choice(["Credit Card", "PayPal", "Debit"]),
            "cancel_reason": cancel_reason,
            "created_at": created,
            "updated_at": updated
        }
        
        # Items (Constraint 1: Max 3 items)
        num_items = random.randint(1, 3)
        for _ in range(num_items):
            soi_id = get_id(so_item_counter)
            so_item_counter += 1
            
            prod_id = random.choice(all_product_ids)
            
            so_items[soi_id] = {
                "so_item_id": soi_id,
                "sales_order_id": so_id,
                "product_id": prod_id,
                "quantity": random.randint(1, 5),
                "created_at": created,
                "updated_at": updated
            }
            
        # Shipping (Constraint 1: Max 1 shipping record per order)
        # Logic: Shipping exists if status implies movement
        if status in ["shipped", "delivered", "returned"]:
            ship_id = get_id(shipping_counter)
            shipping_counter += 1
            
            est_date = fake.date_between(start_date="today", end_date="+1w").isoformat()
            real_date = fake.date_between(start_date="-1w", end_date="today").isoformat() if status == "delivered" else ""
            
            shipping[ship_id] = {
                "shipping_id": ship_id,
                "sales_order_id": so_id,
                "address": f"{u_data['address']}, {u_data['city']}, {u_data['state']}",
                "estimate_deliver_date": est_date,
                "real_deliver_date": real_date, # Constraint 15: Empty string if not applicable, not null
                "method": "Standard",
                "tracking_number": f"TRK-{fake.uuid4()[:8].upper()}",
                "status": status,
                "created_at": created,
                "updated_at": updated
            }

with open(f"{DATA_DIR}/sales_orders.json", "w") as f:
    json.dump(sales_orders, f, indent=2)
with open(f"{DATA_DIR}/sales_order_items.json", "w") as f:
    json.dump(so_items, f, indent=2)
with open(f"{DATA_DIR}/shipping.json", "w") as f:
    json.dump(shipping, f, indent=2)


print(f"Done! Database seeded in '{DATA_DIR}/' with {product_counter-1} products, {so_counter-1} sales orders.")