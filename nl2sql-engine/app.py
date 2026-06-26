import streamlit as st
import pandas as pd
from nl2sql_engine import nl_to_result

st.set_page_config(page_title="NL2SQL Query Engine", layout="wide")
st.title("🗄️ NL2SQL Query Engine")
st.caption("Ask questions about the company database in plain English.")

with st.expander("📋 View Schema"):
    st.code("""
customers(customer_id, name, city, country, signup_date)
products(product_id, name, category, unit_price)
orders(order_id, customer_id, order_date, status)
order_items(order_item_id, order_id, product_id, quantity)
""")

query = st.text_input("Ask a question:", placeholder="e.g. Show top 5 cities by total revenue")

if st.button("Run Query") and query:
    with st.spinner("Generating SQL and fetching results..."):
        try:
            sql, columns, rows = nl_to_result(query)
            st.subheader("Generated SQL")
            st.code(sql, language="sql")

            if rows:
                df = pd.DataFrame(rows, columns=columns)
                st.subheader("Results")
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Query ran successfully but returned no rows.")
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.subheader("Try these examples:")
examples = [
    "What are the top 5 customers by total spend?",
    "Show monthly order count for 2024",
    "Which product category generates the most revenue?",
    "List customers from India who placed more than 3 orders",
]
for ex in examples:
    if st.button(ex):
        st.session_state["query"] = ex