import sqlite3

def view_inventory():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inventory")
    products = cursor.fetchall()

    print("ID | Name       | Price (₹) | Stock")
    print("--------------------------------------")
    for row in products:
        print(f"{row[0]:<2} | {row[1]:<10} | ₹{row[2]:<8} | {row[3]}")

    conn.close()

view_inventory()