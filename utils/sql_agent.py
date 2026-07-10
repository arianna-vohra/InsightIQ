import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "openai/gpt-oss-20b:free"
def generate_sql(question):

    prompt = f"""
You are an expert SQL developer.

Database Schema:

Customers(
Customer_ID,
Customer_Name,
Region
)

Products(
Product_ID,
Product_Name,
Category
)

Orders(
Order_ID,
Customer_ID,
Product_ID,
Order_Date,
Quantity,
Sales,
Profit
)

Rules:

- Return ONLY SQL.
- Use SQLite syntax.
- Never explain anything.
- Never use markdown.
- Use JOIN when required.

Examples:

Question:
Top 5 customers

SQL:
SELECT
c.Customer_Name,
ROUND(SUM(o.Sales),2) AS Total_Sales
FROM orders o
JOIN customers c
ON o.Customer_ID = c.Customer_ID
GROUP BY c.Customer_Name
ORDER BY Total_Sales DESC
LIMIT 5;

Question:
Top products

SQL:
SELECT
p.Product_Name,
ROUND(SUM(o.Sales),2) AS Total_Sales
FROM orders o
JOIN products p
ON o.Product_ID = p.Product_ID
GROUP BY p.Product_Name
ORDER BY Total_Sales DESC
LIMIT 10;

Generate SQL for:

{question}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    sql = response.choices[0].message.content.strip()

    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql