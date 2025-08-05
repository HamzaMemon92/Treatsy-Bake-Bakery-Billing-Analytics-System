menu = {
    "cake and pastry": {
        "rasmalaicake": 700,
        "Truffle cake": 600,
        "dutch chocolate": 500,
        "black forest": 300,
        "marble cake": 800,
        "dripping cake": 400,
        "tea time cake": 500
    },
    "brownies": {
        "nutella": 140,
        "walnut": 120,
        "ganache": 110,
        "triple chocolate": 130,
        "crinkle top": 99
    }
}

print("Welcome to Treatsy Bake!")
print("How may I help you?")
print("Click 1. Menu")
print("Click 2. Bill")

order = []
total = 0
c = int(input("Enter your choice: "))

if c == 1:
    while True:
        print("\n----- MENU -----")
        for category, items in menu.items():
            print(f"\n{category.upper()}")
            for item, price in items.items():
                print(f"{item}: ₹{price}")

        o = input("\nEnter your choice of order: ").strip().lower()
        found = False

        for category in menu:
            for item in menu[category]:
                if item.lower() == o:
                    price = menu[category][item]
                    order.append((item, price))
                    total += price
                    print(f"{item} added to your cart - ₹{price}")
                    found = True
                    break
            if found:
                break

        if not found:
            print(" Item not found in menu. Please try again.")

        more = input("Do you want to add more items? (yes/no): ").strip().lower()
        if more != "yes":
            break

    # 🧾 Print final bill
    print(" Printing Bill")
    for item, price in order:
        print(f"{item} - ₹{price}")
    print("---------------------------")
    print(f"Total Amount: ₹{total}")
    print("THANK YOU FOR CHOOSING TREATSY BAKE ")

elif c == 2:
    print("You haven't ordered anything yet.")
else:
    print("Invalid choice.")
