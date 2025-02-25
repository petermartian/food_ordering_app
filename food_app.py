class FoodOrderApp:
    def __init__(self):
        # Define menu with items and prices in Naira
        self.menu = {
            "Pizza": 6500,
            "Burger": 3500,
            "Noodles": 1500,
            "Shawarma": 2500,
            "Water": 500,
            "Juice": 2000
        }
        self.order = {}  # Dictionary to store user's order

    def display_menu(self):
        """Display the available menu items and their prices"""
        print("\n=== Welcome to Our Food Vendor ===")
        print("Menu Items (Prices in Naira):")
        for item, price in self.menu.items():
            print(f"{item}: {price} Naira")
        print("================================\n")

    def take_order(self):
        """Capture user's order with multiple items and quantities"""
        self.order.clear()  # Clear previous order
        while True:
            self.display_menu()
            item = input("Enter the item you want to order (or 'done' to finish): ").capitalize()
            
            if item.lower() == 'done':
                break
                
            if item in self.menu:
                try:
                    quantity = int(input(f"How many {item}(s) would you like? "))
                    if quantity > 0:
                        if item in self.order:
                            self.order[item] += quantity
                        else:
                            self.order[item] = quantity
                        print(f"Added {quantity} {item}(s) to your order!")
                    else:
                        print("Please enter a valid quantity greater than 0.")
                except ValueError:
                    print("Please enter a numeric quantity.")
            else:
                print("Sorry, that item is not on the menu. Please check the menu and try again.")
            
            continue_order = input("Would you like to add another item? (yes/no): ").lower()
            if continue_order != 'yes':
                break

    def display_receipt(self):
        """Display the order summary and total cost"""
        if not self.order:
            print("No items in your order!")
            return

        print("\n=== Order Receipt ===")
        total = 0
        for item, quantity in self.order.items():
            item_total = self.menu[item] * quantity
            total += item_total
            print(f"{item} x{quantity}: {item_total} Naira")
        
        print(f"\nTotal Amount: {total} Naira")
        print("Thank you for your order!")
        print("====================")

def main():
    app = FoodOrderApp()
    
    while True:
        print("\n1. View Menu")
        print("2. Place Order")
        print("3. View Receipt")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            app.display_menu()
        elif choice == '2':
            app.take_order()
        elif choice == '3':
            app.display_receipt()
        elif choice == '4':
            print("Thank you for visiting! Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
