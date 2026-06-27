from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from nl2sql_engine import nl_to_result

app = FastAPI(title="NL2SQL Query Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/api/query")
def query_database(request: QueryRequest):
    try:
        sql, columns, rows = nl_to_result(request.question)
        return {
            "sql": sql,
            "columns": columns,
            "rows": rows
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/schema")
def get_schema():
    return {
        "tables": [
            "customers(customer_id, name, city, country, signup_date)",
            "products(product_id, name, category, unit_price)",
            "orders(order_id, customer_id, order_date, status)",
            "order_items(order_item_id, order_id, product_id, quantity)"
        ]
    }
