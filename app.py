import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, Optional

import streamlit as st
from food_order_app_class import FoodOrderApp  # Assuming your class is in food_order_app_class.py

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
