# inventory_db.py
import sqlite3

def create_inventory_db():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        price REAL,
                        stock INTEGER)''')
    conn.commit()
    conn.close()

def add_product(name, price, stock):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO inventory (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
    conn.commit()
    conn.close()

def update_stock(name, quantity_sold):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET stock = stock - ? WHERE name = ?", (quantity_sold, name))
    conn.commit()
    conn.close()

def get_product_info(name):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory WHERE name = ?", (name,))
    product = cursor.fetchone()
    conn.close()
    return product