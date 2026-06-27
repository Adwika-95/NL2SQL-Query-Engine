import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("company.db")
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_items;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT,
    country TEXT,
    signup_date TEXT
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    unit_price REAL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    status TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
""")

cities = [("Bengaluru","India"),("Chennai","India"),("Mumbai","India"),
          ("New York","USA"),("London","UK"),("Berlin","Germany")]
categories = ["Electronics","Apparel","Groceries","Furniture","Books"]
statuses = ["Completed","Pending","Cancelled","Shipped"]

# Customers
for i in range(1, 201):
    city, country = random.choice(cities)
    signup = (datetime(2023,1,1) + timedelta(days=random.randint(0,700))).strftime("%Y-%m-%d")
    cur.execute("INSERT INTO customers VALUES (?,?,?,?,?)",
                (i, f"Customer_{i}", city, country, signup))

# Products
for i in range(1, 51):
    cat = random.choice(categories)
    price = round(random.uniform(5, 500), 2)
    cur.execute("INSERT INTO products VALUES (?,?,?,?)",
                (i, f"Product_{i}", cat, price))

# Orders + order_items
order_item_id = 1
for i in range(1, 1001):
    cust_id = random.randint(1, 200)
    order_date = (datetime(2024,1,1) + timedelta(days=random.randint(0,500))).strftime("%Y-%m-%d")
    status = random.choice(statuses)
    cur.execute("INSERT INTO orders VALUES (?,?,?,?)", (i, cust_id, order_date, status))

    for _ in range(random.randint(1, 4)):
        prod_id = random.randint(1, 50)
        qty = random.randint(1, 5)
        cur.execute("INSERT INTO order_items VALUES (?,?,?,?)",
                    (order_item_id, i, prod_id, qty))
        order_item_id += 1

conn.commit()
conn.close()
print("Database built: company.db")