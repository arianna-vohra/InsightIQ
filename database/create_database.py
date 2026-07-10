import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("database/insightiq.db")

# Read CSV files
customers = pd.read_csv("data/raw/customers.csv")
products = pd.read_csv("data/raw/products.csv")
sales_reps = pd.read_csv("data/raw/sales_reps.csv")
orders = pd.read_csv("data/raw/orders.csv")

# Load data into SQLite tables
customers.to_sql("customers", conn, if_exists="replace", index=False)
products.to_sql("products", conn, if_exists="replace", index=False)
sales_reps.to_sql("sales_reps", conn, if_exists="replace", index=False)
orders.to_sql("orders", conn, if_exists="replace", index=False)

print("✅ Database created successfully!")

conn.close()