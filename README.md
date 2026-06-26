# NL2SQL Query Engine

Ask plain-English questions about a database and get back the SQL query plus the results — no SQL needed.

## How It Works

1. User asks a question in plain English
2. Question + fixed schema sent to Gemini API via a schema-grounded prompt
3. Generated SQL is checked against a safety filter (blocks DROP/DELETE/UPDATE/INSERT/ALTER)
4. Safe queries run against SQLite, results shown alongside the SQL

## Tech Stack

Python 3.11 · Google Gemini API (`gemini-2.5-flash`) · SQLite · Streamlit · pandas

## Schema
customers(customer_id, name, city, country, signup_date)

products(product_id, name, category, unit_price)

orders(order_id, customer_id, order_date, status)

order_items(order_item_id, order_id, product_id, quantity)

Sample data: 200 customers, 50 products, 1000 orders.

## Setup

```bash
git clone https://github.com/Adwika-95/NL2SQL-Query-Engine.git
cd nl2sql-engine
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Add a `.env` file:
GEMINI_API_KEY=your_key_here
Get a free key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

## Run

```bash
python build_db.py
streamlit run app.py
```

Try: *"Top 5 customers by total spend"*, *"Monthly order count for 2024"*, *"Which category generates the most revenue?"*

## Key Design Choices

- **Schema-grounded prompt** — prevents the model from hallucinating tables/columns
- **Safety layer** — LLM-generated SQL is treated as untrusted input; destructive statements are blocked before execution
- **Read-only** — only SELECT queries are supported

## Limitations

- Single fixed schema (no dynamic upload)
- Keyword-based safety check, not full SQL parsing
- No caching — every query hits the API fresh
