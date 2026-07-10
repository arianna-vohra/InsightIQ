import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "openai/gpt-oss-20b:free"


def ask_ai(question, dashboard_data, chat_history):

    history = ""

    recent_messages = chat_history[-8:]

    for message in recent_messages:

        if message["role"] == "user":
            history += f"User: {message['content']}\n"

        elif message["role"] == "assistant":
            history += f"Assistant: {message['content']}\n"

    prompt = f"""
You are a Senior Business Consultant at Bain & Company.

You are helping a business executive analyze a business dashboard.

Conversation History:
{history}

Dashboard Data:
{dashboard_data}

Current User Question:
{question}

Rules:

- If greeted, respond naturally.
- If asked business questions, answer like a Bain consultant.
- Never invent numbers.
- Only use dashboard data.
- Use conversation history for follow-up questions.

For analytical questions use this format:

## Executive Summary

## Key Findings

## Business Impact

## Recommendations
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

    return response.choices[0].message.content


def explain_sql_result(question, dataframe):

    prompt = f"""
You are a Senior Business Consultant.

A business user asked:

{question}

SQL Result:

{dataframe.to_string(index=False)}

Explain the result using this format:

## Executive Summary

## Key Findings

## Business Impact

## Recommendations

Do not invent numbers.
Only use the SQL result provided.
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

    return response.choices[0].message.content