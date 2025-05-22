import tkinter as tk
from tkinter import ttk
import json
import qrcode
from PIL import Image, ImageTk

class SmartCheckoutGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Checkout")
        self.root.geometry("400x550")
        self.root.configure(bg="white")

        # Title
        tk.Label(root, text="SMART CHECKOUT", font=("Helvetica", 18, "bold"), bg="white").pack(pady=10)

        # Treeview for product list
        self.tree = ttk.Treeview(root, columns=("Product", "Price"), show="headings", height=10)
        self.tree.heading("Product", text="Product")
        self.tree.heading("Price", text="Price (₹)")
        self.tree.pack(pady=10)

        # Total label
        self.total_label = tk.Label(root, text="Total: ₹0", font=("Helvetica", 14), bg="white")
        self.total_label.pack(pady=5)

        # Button to generate QR
        self.qr_button = tk.Button(root, text="Complete Purchase", command=self.show_qr, bg="#28a745", fg="white", font=("Helvetica", 12, "bold"))
        self.qr_button.pack(pady=10)

        # QR code display
        self.qr_label = tk.Label(root, bg="white")
        self.qr_label.pack()

        # Store last items
        self.last_items = []

        # Refresh item list every 1 second
        self.update_items()

    def update_items(self):
        try:
            with open("checkout_data.json", "r") as f:
                items = json.load(f)

            if items != self.last_items:
                self.last_items = items
                self.refresh_tree(items)

        except Exception as e:
            print("Error reading JSON:", e)

        self.root.after(1000, self.update_items)

    def refresh_tree(self, items):
        for i in self.tree.get_children():
            self.tree.delete(i)

        total = 0
        for item in items:
            self.tree.insert("", "end", values=(item["name"].capitalize(), f"₹{item['price']}"))
            total += item["price"]

        self.total_label.config(text=f"Total: ₹{total}")

    def show_qr(self):
        # Calculate total from current items
        total = sum(item["price"] for item in self.last_items)

        # UPI QR code data (replace with your own UPI ID)
        payment_data = f"upi://pay?pa=yourupi@bank&pn=SmartStore&am={total}&cu=INR"

        img = qrcode.make(payment_data)
        img = img.resize((200, 200))
        img = ImageTk.PhotoImage(img)
        self.qr_label.config(image=img)
        self.qr_label.image = img

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartCheckoutGUI(root)
    root.mainloop()