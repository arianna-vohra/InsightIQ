import sqlite3
import pandas as pd

DB_PATH = "database/insightiq.db"


def execute_query(query):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


# ==========================================
# Helper
# ==========================================

def build_where_clause(region="All", category="All"):

    where = []

    if region != "All":
        where.append(f"c.Region = '{region}'")

    if category != "All":
        where.append(f"p.Category = '{category}'")

    if where:
        return "WHERE " + " AND ".join(where)

    return ""


# ==========================================
# KPI
# ==========================================

def get_total_sales(region="All", category="All"):

    where_clause = build_where_clause(region, category)

    query = f"""
    SELECT
        ROUND(SUM(o.Sales),2) AS Total_Sales
    FROM orders o
    JOIN customers c
        ON o.Customer_ID = c.Customer_ID
    JOIN products p
        ON o.Product_ID = p.Product_ID
    {where_clause}
    """

    df = execute_query(query)

    return df.iloc[0]["Total_Sales"]


def get_total_profit(region="All", category="All"):

    where_clause = build_where_clause(region, category)

    query = f"""
    SELECT
        ROUND(SUM(o.Profit),2) AS Total_Profit
    FROM orders o
    JOIN customers c
        ON o.Customer_ID = c.Customer_ID
    JOIN products p
        ON o.Product_ID = p.Product_ID
    {where_clause}
    """

    df = execute_query(query)

    return df.iloc[0]["Total_Profit"]


def get_total_orders(region="All", category="All"):

    where_clause = build_where_clause(region, category)

    query = f"""
    SELECT
        COUNT(*) AS Total_Orders
    FROM orders o
    JOIN customers c
        ON o.Customer_ID = c.Customer_ID
    JOIN products p
        ON o.Product_ID = p.Product_ID
    {where_clause}
    """

    df = execute_query(query)

    return df.iloc[0]["Total_Orders"]


def get_average_order_value(region="All", category="All"):

    where_clause = build_where_clause(region, category)

    query = f"""
    SELECT
        ROUND(AVG(o.Sales),2) AS Avg_Order_Value
    FROM orders o
    JOIN customers c
        ON o.Customer_ID = c.Customer_ID
    JOIN products p
        ON o.Product_ID = p.Product_ID
    {where_clause}
    """

    df = execute_query(query)

    return df.iloc[0]["Avg_Order_Value"]


# ==========================================
# Charts
# ==========================================

def get_sales_by_region(region="All", category="All"):

    where_clause = build_where_clause(region, category)

    query = f"""
    SELECT
        c.Region,
        ROUND(SUM(o.Sales),2) AS Total_Sales
    FROM orders o
    JOIN customers c
        ON o.Customer_ID = c.Customer_ID
    JOIN products p
        ON o.Product_ID = p.Product_ID
    {where_clause}
    GROUP BY c.Region
    ORDER BY Total_Sales DESC
    """

    return execute_query(query)


def get_top_products(region="All", category="All", limit=10):

    where_clause = build_where_clause(region, category)

    query = f"""
    SELECT
        p.Product_Name,
        ROUND(SUM(o.Sales),2) AS Total_Sales
    FROM orders o
    JOIN products p
        ON o.Product_ID = p.Product_ID
    JOIN customers c
        ON o.Customer_ID = c.Customer_ID
    {where_clause}
    GROUP BY p.Product_Name
    ORDER BY Total_Sales DESC
    LIMIT {limit}
    """

    return execute_query(query)


def get_top_customers(region="All", category="All", limit=10):

    where_clause = build_where_clause(region, category)

    query = f"""
    SELECT
        c.Customer_Name,
        ROUND(SUM(o.Sales),2) AS Total_Sales
    FROM orders o
    JOIN customers c
        ON o.Customer_ID = c.Customer_ID
    JOIN products p
        ON o.Product_ID = p.Product_ID
    {where_clause}
    GROUP BY c.Customer_Name
    ORDER BY Total_Sales DESC
    LIMIT {limit}
    """

    return execute_query(query)


def get_monthly_sales(region="All", category="All"):

    where_clause = build_where_clause(region, category)

    query = f"""
    SELECT
        substr(o.Order_Date,1,7) AS Month,
        ROUND(SUM(o.Sales),2) AS Total_Sales
    FROM orders o
    JOIN customers c
        ON o.Customer_ID = c.Customer_ID
    JOIN products p
        ON o.Product_ID = p.Product_ID
    {where_clause}
    GROUP BY Month
    ORDER BY Month
    """

    return execute_query(query)
def get_best_region():

    query = """
    SELECT
        c.Region,
        ROUND(SUM(o.Sales),2) AS Total_Sales
    FROM orders o
    JOIN customers c
        ON o.Customer_ID = c.Customer_ID
    GROUP BY c.Region
    ORDER BY Total_Sales DESC
    LIMIT 1
    """

    return execute_query(query)


def get_best_product():

    query = """
    SELECT
        p.Product_Name,
        ROUND(SUM(o.Sales),2) AS Total_Sales
    FROM orders o
    JOIN products p
        ON o.Product_ID = p.Product_ID
    GROUP BY p.Product_Name
    ORDER BY Total_Sales DESC
    LIMIT 1
    """

    return execute_query(query)


def get_best_category():

    query = """
    SELECT
        p.Category,
        ROUND(SUM(o.Profit),2) AS Profit
    FROM orders o
    JOIN products p
        ON o.Product_ID = p.Product_ID
    GROUP BY p.Category
    ORDER BY Profit DESC
    LIMIT 1
    """

    return execute_query(query)


def get_best_month():

    query = """
    SELECT
        substr(Order_Date,1,7) AS Month,
        ROUND(SUM(Sales),2) AS Sales
    FROM orders
    GROUP BY Month
    ORDER BY Sales DESC
    LIMIT 1
    """

    return execute_query(query)
print("Analytics loaded successfully")