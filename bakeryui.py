import tkinter as tk
from tkinter import messagebox, ttk
from treatsy_backend import init_db, insert_order_data, fetch_customer_sales, fetch_company_analytics



# Initialize DB
init_db()

menu = {
    "Cake and Pastry": {
        "Rasmalaicake": 700,
        "Truffle cake": 600,
        "Dut ch chocolate": 500,
        "Black forest": 300,
        "Marble cake": 800,
        "Dripping cake": 400,
        "Tea time cake": 500
    },
    "Brownies": {
        "Nutella": 140,
        "Walnut": 120,
        "Ganache": 110,
        "Triple chocolate": 130,
        "Crinkle top": 99
    }
}

order = []
total = 0

def add_to_cart(item, price):
    global total
    order.append((item, price))
    total += price
    cart_listbox.insert(tk.END, f"{item} - ₹{price}")
    total_label.config(text=f"Total: ₹{total}")

def print_bill():
    global order, total
    if not order:
        messagebox.showinfo("🧾 Bill", "🛒 No items in your cart!")
        return

    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()

    if not name or not phone:
        messagebox.showwarning("Missing Info", "Please enter both Name and Phone number.")
        return

    bill_text = "\n".join([f"{item} - ₹{price}" for item, price in order])
    bill_text += f"\n\n🧾 Total Amount: ₹{total}\n\n🎉 THANK YOU FOR CHOOSING TREATSY BAKE 🧁"

    # Save to DB
    insert_order_data(name, phone, email, order, total)

    messagebox.showinfo("🧾 Final Bill", bill_text)

    order.clear()
    total = 0
    cart_listbox.delete(0, tk.END)
    total_label.config(text="Total: ₹0")
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

def show_admin_view():
    admin_win = tk.Toplevel(root)
    admin_win.title("Admin Panel")
    admin_win.geometry("900x500")
    
    def show_customer_sales():
        for row in tree.get_children():
            tree.delete(row)
        tree["columns"] = ("Name", "Phone", "Email", "Items", "Total")
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        rows = fetch_customer_sales()

        for row in rows:
            tree.insert("", tk.END, values=row)

    def show_item_analytics():
        for row in tree.get_children():
            tree.delete(row)
        tree["columns"] = ("Item", "Times Sold")
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor="center")

        stats = fetch_company_analytics()
        for stat in stats:
            tree.insert("", tk.END, values=stat)

    btn_frame = tk.Frame(admin_win)
    btn_frame.pack(pady=10)

    sales_btn = tk.Button(btn_frame, text="📋 Customer Sales Data", font=("Arial", 12, "bold"),
                          command=show_customer_sales, bg="#C8FACC")
    sales_btn.grid(row=0, column=0, padx=10)

    analytics_btn = tk.Button(btn_frame, text="📊 Company Analytics", font=("Arial", 12, "bold"),
                              command=show_item_analytics, bg="#FAC4FF")
    analytics_btn.grid(row=0, column=1, padx=10)

    tree = ttk.Treeview(admin_win, show="headings")
    tree.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

# GUI Layout
root = tk.Tk()
root.title("Treatsy Bake Billing System")
root.geometry("900x600")
root.config(bg="ivory")

top_frame = tk.Frame(root, bg="ivory")
top_frame.pack(fill=tk.X, pady=10, padx=20)

title = tk.Label(top_frame, text="🧁 Welcome to Treatsy Bake 🧁", font=("Arial", 20, "bold"), bg="ivory")
title.pack(side=tk.LEFT)

admin_btn = tk.Button(top_frame, text="👤 Admin Panel", bg="#FDCEDF", fg="black", font=("Arial", 10, "bold"),
                      command=show_admin_view)
admin_btn.pack(side=tk.RIGHT)

main_frame = tk.Frame(root, bg="ivory")
main_frame.pack(fill=tk.BOTH, expand=True, padx=20)

menu_frame = tk.Frame(main_frame, bg="ivory")
menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

menu_label = tk.Label(menu_frame, text="🍰 Menu", font=("Arial", 16, "bold"), bg="ivory")
menu_label.pack(pady=5)

for category, items in menu.items():
    cat_label = tk.Label(menu_frame, text=category, font=("Arial", 14, "underline"), bg="ivory")
    cat_label.pack(pady=(10, 2))
    for item, price in items.items():
        btn = tk.Button(menu_frame, text=f"{item} - ₹{price}", width=30,
                        command=lambda i=item, p=price: add_to_cart(i, p))
        btn.pack(pady=2)

cart_frame = tk.Frame(main_frame, bg="ivory", bd=2, relief=tk.RIDGE)
cart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

cart_label = tk.Label(cart_frame, text="🛒 Your Cart", font=("Arial", 16, "bold"), bg="ivory")
cart_label.pack(pady=10)

cart_listbox = tk.Listbox(cart_frame, width=40, height=15, font=("Arial", 12))
cart_listbox.pack(pady=5)

total_label = tk.Label(cart_frame, text="Total: ₹0", font=("Arial", 14, "bold"), bg="ivory")
total_label.pack(pady=5)

name_label = tk.Label(cart_frame, text="Name:", font=("Arial", 12), bg="ivory")
name_label.pack()
name_entry = tk.Entry(cart_frame, font=("Arial", 12))
name_entry.pack()

phone_label = tk.Label(cart_frame, text="Phone:", font=("Arial", 12), bg="ivory")
phone_label.pack()
phone_entry = tk.Entry(cart_frame, font=("Arial", 12))
phone_entry.pack()

email_label = tk.Label(cart_frame, text="Email (optional):", font=("Arial", 12), bg="ivory")
email_label.pack()
email_entry = tk.Entry(cart_frame, font=("Arial", 12))
email_entry.pack()

checkout_btn = tk.Button(cart_frame, text="✅ Checkout & Final Bill", font=("Arial", 14, "bold"),
                         bg="#ADE8F4", fg="black", padx=10, pady=5, command=print_bill)
checkout_btn.pack(pady=20)

root.mainloop()
