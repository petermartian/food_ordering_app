import streamlit as st
from typing import Dict, Optional

# Menu items and prices (defined as in the original document)
MENU_ITEMS = {
    'Pizza': 6500,
    'Burger': 3000,
    'Noodles': 1300
}

# Initialize session state for the cart if it doesn't exist
if 'cart' not in st.session_state:
    st.session_state.cart = {}

def display_menu():
    """Display the menu options in Streamlit."""
    st.title("Welcome to the Food Ordering App!")
    st.write("### Menu:")
    for item, price in MENU_ITEMS.items():
        st.write(f"{item} - {price} Naira")

def get_user_choice() -> Optional[int]:
    """Get the user's choice from a Streamlit selectbox."""
    choices = list(MENU_ITEMS.keys())
    choices.append("Exit Menu")  # Add exit option
    selected = st.selectbox("Select an item or exit:", choices, index=len(choices)-1)
    
    if selected == "Exit Menu":
        return None
    return choices.index(selected) + 1  # Return 1, 2, or 3 for items

def get_quantity() -> int:
    """Get the quantity using a Streamlit number input."""
    quantity = st.number_input("Enter the quantity:", min_value=1, value=1, step=1)
    return int(quantity)

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
            st.write("Finished adding items.")
            return cart
        
        quantity = get_quantity()
        item_name = get_item_name(choice)
        item_price = get_item_price(choice)
        total_price = calculate_total_price(item_price, quantity)
        
        if item_name in cart:
            cart[item_name]['quantity'] += quantity
            cart[item_name]['total_price'] += total_price
        else:
            cart[item_name] = {'quantity': quantity, 'total_price': total_price}
        
        st.session_state.cart = cart  # Update session state
        st.write(f"Added {quantity} {item_name}(s) to cart. Total for this item: {total_price} Naira")
    
    return cart

def check_out(cart: Dict):
    """Display the cart contents and total price as a receipt in Streamlit."""
    if not cart:
        st.write("Your cart is empty. No items to check out.")
    else:
        st.write("### Checking out...")
        st.write("#### Your order details:")
        total_order_price = 0
        
        for item_name, details in cart.items():
            quantity = details['quantity']
            total_price = details['total_price']
            st.write(f"**{item_name}:** Quantity - {quantity}, Total Price - {total_price} Naira")
            total_order_price += total_price
        
        st.write(f"**Total Order Price:** {total_order_price} Naira")
        st.write("Thank you for ordering!")
        
        # Clear cart after checkout
        if st.button("Confirm Checkout"):
            st.session_state.cart = {}
            st.write("Order confirmed! Cart has been cleared.")

def food_ordering_app():
    """Main function to run the food ordering app in Streamlit."""
    display_menu()
    cart = place_order()
    check_out(cart)

# Run the app
if __name__ == "__main__":
    food_ordering_app()