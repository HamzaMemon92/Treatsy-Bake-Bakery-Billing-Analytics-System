# Treatsy-Bake-Bakery-Billing-Analytics-System

Treatsy Bake is a smart bakery billing system with two interfaces:
- A CLI version for quick orders
- A Tkinter GUI version for a user-friendly checkout system with an Admin Dashboard

It allows:
- Efficient customer billing
- Tracking of popular products
- CRM via customer data storage
- Sales analytics via dashboards

---

##  Tech Stack

- **Frontend (GUI)**: Python Tkinter
- **CLI Interface**: Basic Python input/output
- **Backend**: SQLite3
- **Database file**: `treatsy.db`
- **Analytics**: Sales data & item frequency tracking

---

##  Features

###  Customer Interface
- Browse menu (Cake & Brownies)
- Add items to cart
- Enter name, phone, and email
- Generate bill
- Auto-save order to database

###  Admin Panel
- View customer sales history
- Track most sold products (item-wise analytics)

###  Database
- `customers`: Stores name, phone, email
- `orders`: One row per transaction (includes all items & total)
- `sales`: One row per item sold (used for item popularity analytics)

###  Smart Logic
- Prevent duplicate customer records (by phone number)
- Auto-update item frequency
- Centralized data handling
