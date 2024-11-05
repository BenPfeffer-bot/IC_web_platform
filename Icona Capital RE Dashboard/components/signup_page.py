# pages/signup.py

import streamlit as st
from utils.session_manager import initialize_session_state
from utils.authentication import AuthenticationService
import time

def show_signup_page(auth_service):
    initialize_session_state()

    if st.session_state.get('authenticated', False):
        st.warning("You are already logged in.")
        st.session_state['current_page'] = 'Landing'
        st.rerun()

    st.title("Sign Up")

    with st.form("signup_form"):
        name = st.text_input("Full Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Sign Up")

        if submitted:
            if not username or not password or not name:
                st.error("Please fill in all fields")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long")
            elif password != confirm_password:
                st.error("Passwords do not match")
            else:
                try:
                    if auth_service.register(username, password, name):
                        st.success("Account created successfully!")
                        time.sleep(1)
                        st.session_state['current_page'] = 'Login'
                        st.rerun()
                    else:
                        st.error("Username already exists")
                except Exception as e:
                    st.error(f"Registration failed: {str(e)}")

    if st.button("Already have an account? Login"):
        st.session_state['current_page'] = 'Login'
        st.rerun()
