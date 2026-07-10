import pandas as pd
import random
from faker import Faker
import os

# Create a Faker object for Indian data
fake = Faker("en_IN")
state_to_region = {
    "Delhi": "North",
    "Haryana": "North",
    "Punjab": "North",
    "Himachal Pradesh": "North",
    "Jammu and Kashmir": "North",
    "Uttarakhand": "North",
    "Uttar Pradesh": "North",

    "Maharashtra": "West",
    "Gujarat": "West",
    "Goa": "West",
    "Rajasthan": "West",

    "Tamil Nadu": "South",
    "Karnataka": "South",
    "Kerala": "South",
    "Andhra Pradesh": "South",
    "Telangana": "South",

    "West Bengal": "East",
    "Odisha": "East",
    "Bihar": "East",
    "Jharkhand": "East",
    "Assam": "East",

    "Madhya Pradesh": "Central",
    "Chhattisgarh": "Central"
}

# Number of customers we want
NUM_CUSTOMERS = 5000

# Create the output folder if it doesn't exist
os.makedirs("data/raw", exist_ok=True)

# -------------------------------
# Generate Customers
# -------------------------------

customers = []

segments = ["Consumer", "Corporate", "Home Office"]

for i in range(1, NUM_CUSTOMERS + 1):

    state = fake.state()

    region = state_to_region.get(
        state,
        random.choice(["North", "South", "East", "West", "Central"])
    )

    customers.append({
        "Customer_ID": f"CUST{i:05}",
        "Customer_Name": fake.name(),
        "Email": fake.email(),
        "City": fake.city(),
        "State": state,
        "Region": region,
        "Segment": random.choice(segments)
    })

customers_df = pd.DataFrame(customers)

customers_df.to_csv("data/raw/customers.csv", index=False)

print("✅ customers.csv created successfully!")

products = []

categories = {
    "Electronics": ["Laptop", "Mobile", "Headphones", "Monitor", "Keyboard"],
    "Furniture": ["Chair", "Table", "Sofa", "Bed", "Wardrobe"],
    "Fashion": ["Shirt", "Shoes", "Jeans", "Jacket", "Watch"],
    "Sports": ["Football", "Cricket Bat", "Tennis Racket", "Yoga Mat", "Dumbbell"],
    "Home": ["Mixer", "Cookware", "Vacuum Cleaner", "Air Purifier", "Lamp"]
}

product_id = 1

for category, items in categories.items():

    for item in items:

        for i in range(20):

            cost = random.randint(500, 50000)
            selling_price = int(cost * random.uniform(1.15, 1.60))

            products.append({
                "Product_ID": f"PROD{product_id:04}",
                "Product_Name": f"{item} {i+1}",
                "Category": category,
                "Cost": cost,
                "Selling_Price": selling_price
            })

            product_id += 1

products_df = pd.DataFrame(products)

products_df.to_csv("data/raw/products.csv", index=False)

print("✅ products.csv created successfully!")

# -------------------------------
# Generate Sales Representatives
# -------------------------------

sales_reps = []

regions = ["North", "South", "East", "West", "Central"]

for i in range(1, 101):

    sales_reps.append({
        "Rep_ID": f"REP{i:03}",
        "Rep_Name": fake.name(),
        "Region": random.choice(regions)
    })

sales_reps_df = pd.DataFrame(sales_reps)

sales_reps_df.to_csv("data/raw/sales_reps.csv", index=False)

print("✅ sales_reps.csv created successfully!")

# -------------------------------
# Generate Orders
# -------------------------------

orders = []

for i in range(1, 50001):

    customer = random.randint(1, NUM_CUSTOMERS)
    product = random.randint(1, len(products))
    rep = random.randint(1, 100)

    quantity = random.randint(1, 5)
    discount = random.choice([0, 5, 10, 15, 20])

    product_cost = products[product - 1]["Cost"]
    selling_price = products[product - 1]["Selling_Price"]

    sales = quantity * selling_price * (1 - discount / 100)
    profit = sales - (quantity * product_cost)

    orders.append({
        "Order_ID": f"ORD{i:06}",
        "Order_Date": fake.date_between(start_date="-2y", end_date="today"),
        "Customer_ID": f"CUST{customer:05}",
        "Product_ID": f"PROD{product:04}",
        "Rep_ID": f"REP{rep:03}",
        "Quantity": quantity,
        "Discount": discount,
        "Sales": round(sales, 2),
        "Profit": round(profit, 2)
    })

orders_df = pd.DataFrame(orders)

orders_df.to_csv("data/raw/orders.csv", index=False)

print("✅ orders.csv created successfully!")