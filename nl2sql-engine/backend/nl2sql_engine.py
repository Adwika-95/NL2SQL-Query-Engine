import os
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

SCHEMA = """
Tables:
1. customers(customer_id, name, city, country, signup_date)
2. products(product_id, name, category, unit_price)
3. orders(order_id, customer_id, order_date, status)
4. order_items(order_item_id, order_id, product_id, quantity)

Relationships:
- orders.customer_id -> customers.customer_id
- order_items.order_id -> orders.order_id
- order_items.product_id -> products.product_id
"""

SYSTEM_PROMPT = f"""You are a SQL generation engine for a SQLite database.
Schema:
{SCHEMA}

Rules:
- Output ONLY valid SQLite SQL. No explanations, no markdown fences.
- Use only the tables/columns listed above.
- Never use destructive statements (DROP, DELETE, UPDATE, INSERT, ALTER).
- If the question cannot be answered with this schema, output: SELECT 'UNSUPPORTED_QUERY' AS error;
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

def generate_sql(natural_language_query: str) -> str:
    response = model.generate_content(natural_language_query)
    sql = response.text.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

def is_safe_query(sql: str) -> bool:
    forbidden = ["drop", "delete", "update", "insert", "alter", "attach", "pragma"]
    lowered = sql.lower()
    return not any(word in lowered for word in forbidden)

def run_query(sql: str, db_path="company.db"):
    if not is_safe_query(sql):
        raise ValueError("Unsafe SQL detected — query blocked.")
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute(sql)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        return columns, rows
    finally:
        conn.close()

def nl_to_result(natural_language_query: str, db_path="company.db"):
    sql = generate_sql(natural_language_query)
    columns, rows = run_query(sql, db_path)
    return sql, columns, rows