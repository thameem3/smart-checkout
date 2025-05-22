# admin_panel.py
import tkinter as tk
from tkinter import messagebox
import sqlite3
from inventory_db import add_product, update_stock, get_product_info, create_inventory_db

# Initialize DB if not created
create_inventory_db()

def check_password():
    password = password_entry.get()
    if password == "admin123":
        open_admin_panel()
    else:
        messagebox.showerror("Error", "Invalid password!")

def open_admin_panel():
    admin_window.destroy()
    window = tk.Tk()
    window.title("Admin Panel")

    def view_inventory():
        inventory_window = tk.Toplevel(window)
        inventory_window.title("Inventory")
        inventory_listbox = tk.Listbox(inventory_window, width=50, height=15)
        inventory_listbox.pack()
        products = get_all_products()
        for product in products:
            inventory_listbox.insert(tk.END, f"{product[1]} - ₹{product[2]} - Stock: {product[3]}")

    def get_all_products():
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        products = cursor.fetchall()
        conn.close()
        return products

    def add_new_product():
        name = name_entry.get()
        price = float(price_entry.get())
        stock = int(stock_entry.get())
        add_product(name, price, stock)
        messagebox.showinfo("Success", "Product added.")

    def update_product_stock():
        name = name_entry.get()
        quantity = int(stock_entry.get())
        update_stock(name, quantity)
        messagebox.showinfo("Success", "Stock updated.")

    tk.Label(window, text="Product Name").pack()
    name_entry = tk.Entry(window)
    name_entry.pack()

    tk.Label(window, text="Price").pack()
    price_entry = tk.Entry(window)
    price_entry.pack()

    tk.Label(window, text="Stock Quantity").pack()
    stock_entry = tk.Entry(window)
    stock_entry.pack()

    tk.Button(window, text="Add Product", command=add_new_product).pack()
    tk.Button(window, text="Update Stock", command=update_product_stock).pack()
    tk.Button(window, text="View Inventory", command=view_inventory).pack()

    window.mainloop()

# Login window
admin_window = tk.Tk()
admin_window.title("Admin Login")
tk.Label(admin_window, text="Enter Admin Password").pack()
password_entry = tk.Entry(admin_window, show="*")
password_entry.pack()
tk.Button(admin_window, text="Login", command=check_password).pack()
admin_window.mainloop()