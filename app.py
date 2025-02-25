import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, Optional

import streamlit as st

# Define the FoodOrderApp class (modified for Streamlit)
class FoodOrderApp:
    def __init__(self):
        self.menu = {
            "Pizza": 6500,
            "Burger": 3500,
            "Noodles": 1500,
            "Shawarma": 2500,
            "Water": 500,
            "Juice": 2000
        }
        # Store order in session state
        if 'order' not in st.session_state:
            st.session_state.order = {}

def main():
    app = FoodOrderApp()
    
    # Sidebar for page navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Order Food", "Checkout"])
    
    if page == "Order Food":
        order_page(app)
    else:
        checkout_page(app)

def order_page(app):
    st.title("🍽️ Food Order App")
    
    # Split into two columns
    col1, col2 = st.columns([2, 3])
    
    # Menu Section (Left Side)
    with col1:
        st.header("Menu")
        st.markdown("---")
        
        # Display menu items with styling
        for item, price in app.menu.items():
            with st.container():
                st.markdown(f"**{item}** - ₦{price:,}")
                if st.button(f"Add {item}", key=f"add_{item}", 
                           help=f"Add {item} to cart"):
                    if item in st.session_state.order:
                        st.session_state.order[item] += 1
                    else:
                        st.session_state.order[item] = 1
                    st.success(f"Added {item} to cart!")
                st.markdown("---")

    # Cart Section (Right Side)
    with col2:
        st.header("Your Cart")
        st.markdown("---")
        
        if not st.session_state.order:
            st.info("Your cart is empty!")
        else:
            total = 0
            for item, quantity in st.session_state.order.items():
                item_total = app.menu[item] * quantity
                total += item_total
                
                with st.expander(f"{item} x{quantity}"):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"Price: ₦{app.menu[item]:,}")
                    with col2:
                        if st.button("➖", key=f"minus_{item}"):
                            if st.session_state.order[item] > 1:
                                st.session_state.order[item] -= 1
                            else:
                                del st.session_state.order[item]
                            st.experimental_rerun()
                    with col3:
                        if st.button("❌", key=f"remove_{item}"):
                            del st.session_state.order[item]
                            st.experimental_rerun()
                st.write(f"Subtotal: ₦{item_total:,}")
                st.markdown("---")
            
            st.markdown(f"**Total: ₦{total:,}**")
        
        # Checkout button
        if st.session_state.order:
            if st.button("🛒 Checkout", 
                        help="Proceed to checkout",
                        key="checkout_btn",
                        use_container_width=True):
                st.session_state.page = "Checkout"
                st.experimental_rerun()

def checkout_page(app):
    st.title("🧾 Checkout")
    
    if not st.session_state.order:
        st.warning("Your cart is empty! Please add items to checkout.")
        if st.button("Back to Menu"):
            st.session_state.page = "Order Food"
            st.experimental_rerun()
        return
    
    # Display receipt
    st.header("Order Receipt")
    total = 0
    
    with st.container():
        for item, quantity in st.session_state.order.items():
            item_total = app.menu[item] * quantity
            total += item_total
            st.markdown(f"""
            <div style='padding: 10px;'>
                <span style='font-size: 18px;'>{item} x{quantity}</span>
                <span style='float: right;'>₦{item_total:,}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f"""
        <div style='padding: 10px;'>
            <span style='font-size: 20px; font-weight: bold;'>Total Amount</span>
            <span style='float: right; font-weight: bold;'>₦{total:,}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Complete Order button
    if st.button("✅ Complete Order", use_container_width=True):
        st.success("Thank you for your order! Your food will be prepared soon.")
        st.session_state.order = {}  # Clear the order
        st.experimental_rerun()
    
    if st.button("⬅ Back to Menu"):
        st.session_state.page = "Order Food"
        st.experimental_rerun()

if __name__ == "__main__":
    # Page config
    st.set_page_config(
        page_title="Food Order App",
        page_icon="🍽️",
        layout="wide"
    )
    main()
