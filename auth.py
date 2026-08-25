import streamlit as st
from db import get_connection

def login():
    """Handle user login."""
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            # Here you would typically check the credentials against a database
            st.session_state['authenticated'] = True
            st.success("Logged in successfully!")
        else:
            st.error("Please enter both username and password.")

def signup():
    """Handle user signup."""
    st.subheader("Sign Up")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")

    if st.button("Sign Up"):
        if username and password:
            # Here you would typically save the new user to a database
            st.session_state['authenticated'] = True
            st.success("Account created successfully!")
        else:
            st.error("Please fill in all fields.")

def auth():
    """Manage authentication state."""
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if st.session_state['authenticated']:
        st.success("You are logged in.")
    else:
        option = st.selectbox("Select an option", ["Login", "Sign Up"])
        if option == "Login":
            login()
        else:
            signup()

def main():
    """Main function to run the authentication."""
    st.title("Authentication")
    auth()

if __name__ == "__main__":
    main()