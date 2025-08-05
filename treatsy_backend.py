import sqlite3
from datetime import datetime

DB_NAME = "treatsy.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Customers table
    c.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT
        )
    ''')

    # Orders table (one row per transaction — not per item)
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            items TEXT,
            total_price INTEGER,
            order_time TEXT,
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )
    ''')

    # Sales table (tracks each item sold — for analytics)
    c.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT,
            quantity INTEGER DEFAULT 1
        )
    ''')

    conn.commit()
    conn.close()


def insert_order_data(name, phone, email, order_list, total_price):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Get or insert customer
    c.execute("SELECT id FROM customers WHERE phone = ?", (phone,))
    result = c.fetchone()
    if result:
        customer_id = result[0]
    else:
        c.execute("INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
        customer_id = c.lastrowid

    # Prepare single order record
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item_summary = ", ".join([f"{item}" for item, _ in order_list])
    c.execute("INSERT INTO orders (customer_id, items, total_price, order_time) VALUES (?, ?, ?, ?)",
              (customer_id, item_summary, total_price, now))

    # Update analytics: one row per item
    for item, _ in order_list:
        c.execute("SELECT id FROM sales WHERE item = ?", (item,))
        existing = c.fetchone()
        if existing:
            c.execute("UPDATE sales SET quantity = quantity + 1 WHERE id = ?", (existing[0],))
        else:
            c.execute("INSERT INTO sales (item, quantity) VALUES (?, ?)", (item, 1))

    conn.commit()
    conn.close()


def fetch_customer_sales():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''
        SELECT customers.name, customers.phone, customers.email,
               orders.items, orders.total_price, orders.order_time
        FROM orders
        JOIN customers ON orders.customer_id = customers.id
        ORDER BY orders.order_time DESC
    ''')

    rows = c.fetchall()
    conn.close()
    return rows


def fetch_company_analytics():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''
        SELECT item, SUM(quantity) as total_sold
        FROM sales
        GROUP BY item
        ORDER BY total_sold DESC
    ''')

    analytics = c.fetchall()
    conn.close()
    return analytics
