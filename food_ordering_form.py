
import streamlit as st

def food_ordering_form():
    st.title("ML6 Food Ordering Form")

    # Food Item Selection
    st.header("1. Select Your Food Items")
    food_items = {
        "Pizza": 12.00,
        "Sushi": 15.50,
        "Salad": 10.00,
        "Sandwich": 8.75,
        "Soup": 7.00
    }
    selected_items = {}
    total_cost = 0.0

    for item, price in food_items.items():
        col1, col2, col3 = st.columns([0.5, 0.2, 0.3])
        with col1:
            st.write(f"{item} (${price:.2f})")
        with col2:
            quantity = st.number_input(f"Quantity for {item}", min_value=0, max_value=10, value=0, key=f"qty_{item}")
        with col3:
            if quantity > 0:
                item_total = quantity * price
                st.write(f"Total: ${item_total:.2f}")
                selected_items[item] = {"quantity": quantity, "price": price, "total": item_total}
                total_cost += item_total

    if not selected_items:
        st.warning("Please select at least one food item.")

    # Location Selection
    st.header("2. Select Pickup Location")
    ml6_locations = [
        "Main Office - Ground Floor",
        "Main Office - First Floor",
        "Annex Building - East Wing",
        "Annex Building - West Wing",
        "Innovation Hub - Level 2"
    ]
    pickup_location = st.selectbox("Choose a pickup location:", ml6_locations)

    # Order Summary
    st.header("3. Order Summary")
    if selected_items:
        st.write("**Selected Items:**")
        for item, details in selected_items.items():
            st.write(f"- {details['quantity']}x {item} @ ${details['price']:.2f} each = ${details['total']:.2f}")
        st.write(f"**Pickup Location:** {pickup_location}")
        st.write(f"**Total Cost:** ${total_cost:.2f}")
    else:
        st.info("Your cart is empty. Please select some food items.")

    # Form Submission
    st.header("4. Complete Your Order")
    customer_name = st.text_input("Your Name:")
    customer_notes = st.text_area("Special Instructions (optional):")

    if st.button("Place Order"):
        if not selected_items:
            st.error("Cannot place an empty order. Please select some food items.")
        elif not customer_name:
            st.error("Please enter your name to place the order.")
        else:
            # In a real application, you would send this data to a backend system or vendor API.
            # For this example, we'll just display a confirmation.
            st.success("Order Placed Successfully!")
            st.balloons()

            st.subheader("Order Confirmation Details:")
            st.write(f"**Name:** {customer_name}")
            st.write(f"**Pickup Location:** {pickup_location}")
            st.write(f"**Items:**")
            for item, details in selected_items.items():
                st.write(f"- {details['quantity']}x {item}")
            if customer_notes:
                st.write(f"**Special Instructions:** {customer_notes}")
            st.write(f"**Total Amount:** ${total_cost:.2f}")
            st.info("Your order has been sent to the vendor. You will receive a notification when it's ready for pickup.")

if __name__ == '__main__':
    food_ordering_form()
