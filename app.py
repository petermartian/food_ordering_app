import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, Optional

# Define the FoodOrderApp class
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
        print("=====================")

# Initialize the app session state
if 'app' not in st.session_state:
    st.session_state.app = FoodOrderApp()
if 'page' not in st.session_state:
    st.session_state.page = 'menu'

# Custom CSS for styling
st.markdown("""
    <style>
    .big-button {
        font-size: 20px;
        padding: 10px 20px;
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        border: none;
        cursor: pointer;
    }
    .big-button:hover {
        background-color: #45a049;
    }
    .menu-item {
        background-color: #f9f9f9;
        padding: 10px;
        margin: 5px;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    .cart-item {
        background-color: #e6f7e6;
        padding: 10px;
        margin: 5px;
        border-radius: 5px;
        border: 1px solid #b3e0b3;
    }
    </style>
""", unsafe_allow_html=True)

# Page 1: Menu and Ordering
if st.session_state.page == 'menu':
    st.title("Welcome to Our Food Vendor")
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])  # Left for menu (1 part), right for cart (1 part)
    
    with col1:
        st.subheader("Menu (Prices in Naira)")
        for item, price in st.session_state.app.menu.items():
            if st.button(f"{item} - {price} Naira", key=f"btn_{item}", help=f"Add {item} to your order"):
                quantity = st.number_input(f"How many {item}(s)?", min_value=1, value=1, key=f"qty_{item}")
                if st.button("Add to Cart", key=f"add_{item}"):
                    if item in st.session_state.app.order:
                        st.session_state.app.order[item] += quantity
                    else:
                        st.session_state.app.order[item] = quantity
                    st.success(f"Added {quantity} {item}(s) to your cart!")

    with col2:
        st.subheader("Your Cart")
        if st.session_state.app.order:
            total = 0
            for item, quantity in st.session_state.app.order.items():
                item_total = st.session_state.app.menu[item] * quantity
                total += item_total
                st.markdown(f"""
                    <div class="cart-item">
                        {item} x{quantity}: {item_total} Naira
                    </div>
                """, unsafe_allow_html=True)
            st.markdown(f"<h3>Total: {total} Naira</h3>", unsafe_allow_html=True)
        else:
            st.write("Your cart is empty.")

        # Checkout button
        if st.button("Checkout", key="checkout", help="Proceed to view receipt and checkout"):
            st.session_state.page = 'receipt'

# Page 2: Receipt and Checkout
if st.session_state.page == 'receipt':
    st.title("Order Receipt")
    
    if not st.session_state.app.order:
        st.write("No items in your order!")
    else:
        st.subheader("Your Order Summary")
        total = 0
        for item, quantity in st.session_state.app.order.items():
            item_total = st.session_state.app.menu[item] * quantity
            total += item_total
            st.markdown(f"""
                <div class="cart-item">
                    {item} x{quantity}: {item_total} Naira
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"<h2>Total Amount: {total} Naira</h2>", unsafe_allow_html=True)
        st.write("Thank you for your order!")

        if st.button("Back to Menu", key="back", help="Return to the menu to order more"):
            st.session_state.app.order.clear()  # Clear order to start fresh
            st.session_state.page = 'menu'
        if st.button("Confirm Checkout", key="confirm_checkout", help="Finalize your order"):
            st.success("Order confirmed! Thank you for shopping with us!")
            st.session_state.app.order.clear()  # Clear order after checkout
            if st.button("Back to Menu", key="back_after_checkout"):
                st.session_state.page = 'menu'

# Run the app
if __name__ == "__main__":
    st.write("Run this app with: `streamlit run food_order_app.py`")
