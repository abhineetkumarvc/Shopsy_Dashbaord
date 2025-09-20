import streamlit as st

# Initialize login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login function
def login():
    st.title("🔐 Login to Flipkart Dashboard")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if email == "abhineetkumar.vc@flipkart.com" and password == "flipkart@0505":
            st.session_state.logged_in = True
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Access denied. Flipkart credentials only.")

# Logout function
def logout():
    st.session_state.logged_in = False
    st.rerun()

# Main logic
if not st.session_state.logged_in:
    login()
    st.stop()
else:
    st.sidebar.button("Logout", on_click=logout)
    st.title("📊 Welcome to the Flipkart Dashboard")
    st.write("You are now logged in. Upload your file or explore KPIs.")
