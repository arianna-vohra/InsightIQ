from utils.ai_helper import ask_ai, explain_sql_result
from utils.sql_agent import generate_sql
from utils.sql_executor import execute_sql


# ==========================================
# Intent Detection (No AI Needed)
# ==========================================

def is_sql_question(question):

    question = question.lower()

    sql_keywords = [
        "top",
        "highest",
        "lowest",
        "customer",
        "customers",
        "product",
        "products",
        "sales rep",
        "sales reps",
        "list",
        "show",
        "display",
        "table",
        "records",
        "orders",
        "profit",
        "revenue"
    ]

    return any(keyword in question for keyword in sql_keywords)


# ==========================================
# Main Copilot
# ==========================================

def copilot(question, dashboard_data, chat_history):

    if is_sql_question(question):

        sql = generate_sql(question)

        try:

            result = execute_sql(sql)

        except Exception as e:

            return {
                "type": "error",
                "message": str(e)
            }

        if result.empty:

            return {
                "type": "empty",
                "message": "No records found."
            }

        insight = explain_sql_result(
            question,
            result
        )

        return {
            "type": "sql",
            "sql": sql,
            "result": result,
            "insight": insight
        }

    else:

        response = ask_ai(
            question,
            dashboard_data,
            chat_history
        )

        return {
            "type": "chat",
            "response": response
        }