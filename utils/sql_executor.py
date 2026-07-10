import sqlite3
import pandas as pd

DB_PATH = "database/insightiq.db"


def execute_sql(sql_query):

    try:

        conn = sqlite3.connect(DB_PATH)

        df = pd.read_sql_query(sql_query, conn)

        conn.close()

        return df

    except Exception as e:

        return f"Error: {e}"