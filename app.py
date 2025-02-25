import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, Optional

import streamlit as st
from typing import Dict, Optional

# Menu items and prices (defined as in the original document)
MENU_ITEMS = {
    'Pizza': 6500,
    'Burger': 3000,
    'Noodles': 1300
}

# Initialize session state for the cart and checkout status if they don't exist
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'checkout_complete' not in st.session_state:
    st.session_state.checkout_complete = False

def display_menu():
    """Display the menu options in Streamlit."""
    st.title("Welcome to the Food Ordering App!")
    st.write("### Menu:")
    for item, price in MENU_ITEMS.items():
        st.write(f"{item} - {price} Naira")

def get_user_choice() -> Optional[int]:
    """Get the user's choice from a Streamlit selectbox."""
    choices = list(MENU_ITEMS.keys())
    choices.append("Proceed to Checkout")  # Add proceed option instead of exit
    selected = st.selectbox("Select an item or proceed to checkout:", choices, index=len(choices)-1)
    
    if selected == "Proceed to Checkout":
        return None
    return choices.index(selected) + 1  # Return 1, 2, or 3 for items

def get_quantity() -> int:
    """Get the quantity using a Streamlit text input."""
    quantity = st.text_input("Enter the quantity (must be a positive number):", value="1")
    try:
        quantity = int(quantity)
        if quantity <= 0:
            st.error("Quantity must be greater than 0.")
            return 1  # Default to 1 if invalid
        return quantity
    except ValueError:
        st.error("Invalid input. Please enter a valid number.")
        return 1  # Default to 1 if not a number

def get_item_name(choice: int) -> str:
    """Retrieve the name of a food item based on the choice number."""
    if choice == 1:
        return 'Pizza'
    elif choice == 2:
        return 'Burger'
    elif choice == 3:
        return 'Noodles'
    return ""

def get_item_price(choice: int) -> int:
    """Retrieve the price of a food item based on the choice number."""
    if choice == 1:
        return 6500
    elif choice == 2:
        return 3000
    elif choice == 3:
        return 1300
    return 0

def calculate_total_price(item_price: int, quantity: int) -> int:
    """Calculate the total price for an item based on its price and quantity."""
    return item_price * quantity

def place_order() -> Dict:
    """Manage the process of adding items to the cart using Streamlit buttons."""
    cart = st.session_state.cart
    
    if st.button("Add Item to Cart"):
        choice = get_user_choice()
        if choice is None:
            st.session_state.checkout_complete = True  # Move to checkout
            return cart
        
        quantity = get_quantity()
        if quantity <= 0:  # Ensure valid quantity before proceeding
            st.error("Please enter a valid quantity.")
            return cart
        
        item_name = get_item_name(choice)
        item_price = get_item_price(choice)
        total_price = calculate_total_price(item_price, quantity)
        
        if item_name in cart:
            cart[item_name]['quantity'] += quantity
            cart[item_name]['total_price'] += total_price
        else:
            cart[item_name] = {'quantity': quantity, 'total_price': total_price}
        
        st.session_state.cart = cart  # Update session state
        st.success(f"Added {quantity} {item_name}(s) to cart. Total for this item: {total_price} Naira")
    
    return cart

def check_out(cart: Dict):
    """Display the cart contents, collect user details, and simulate payment in Streamlit."""
    if not cart:
        st.error("Your cart is empty. Please add items before checking out.")
        return
    
    st.write("### Checking out...")
    st.write("#### Your order details:")
    total_order_price = 0
    
    for item_name, details in cart.items():
        quantity = details['quantity']
        total_price = details['total_price']
        st.write(f"**{item_name}:** Quantity - {quantity}, Total Price - {total_price} Naira")
        total_order_price += total_price
    
    st.write(f"**Total Order Price:** {total_order_price} Naira")

    # Collect user details
    st.write("### Please provide your details:")
    name = st.text_input("Name:")
    address = st.text_area("Delivery Address:")
    contact = st.text_input("Contact Number (e.g., +234123456789):")

    # Payment simulation
    st.write("### Payment")
    if st.button("Make Payment"):
        if name and address and contact:
            st.success(f"Payment of {total_order_price} Naira confirmed for {name}!\nDelivery will be arranged to {address}. We will contact you at {contact}.")
            st.session_state.cart = {}  # Clear cart after payment
            st.session_state.checkout_complete = False  # Reset checkout status
        else:
            st.error("Please fill in all your details before making payment.")

    # Option to go back to ordering
    if st.button("Back to Ordering"):
        st.session_state.checkout_complete = False

def food_ordering_app():
    """Main function to run the food ordering app in Streamlit."""
    if not st.session_state.checkout_complete:
        display_menu()
        cart = place_order()
    else:
        check_out(st.session_state.cart)

# Run the app
if __name__ == "__main__":
    food_ordering_app()
