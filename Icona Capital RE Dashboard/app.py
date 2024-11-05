# app.py

import streamlit as st
from utils.session_manager import initialize_session_state
from utils.authentication import AuthenticationService
from components import landing_page, dashboard, signup_page
import time

def main():
    st.set_page_config(
        page_title="Company Portfolio Manager",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    initialize_session_state()
    auth_service = AuthenticationService()

    # Handle page navigation
    if st.session_state['current_page'] == 'Login':
        show_login_page(auth_service)
    elif st.session_state['current_page'] == 'Signup':
        signup_page.show_signup_page(auth_service)
    elif st.session_state['current_page'] == 'Landing':
        landing_page.show_landing_page()
    elif st.session_state['current_page'] == 'Dashboard':
        dashboard.show_dashboard()
    else:
        st.error("Page not found")

def show_login_page(auth_service):
    st.title("Login")

    if st.session_state.get('authenticated', False):
        st.session_state['current_page'] = 'Landing'
        st.rerun()

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            success, name = auth_service.login(username, password)
            if success:
                st.session_state['authenticated'] = True
                st.session_state['name'] = name
                st.session_state['current_page'] = 'Landing'
                st.session_state['show_animation'] = True
                st.rerun()
            else:
                st.error("Invalid username or password")

    if st.button("Don't have an account? Sign up"):
        st.session_state['current_page'] = 'Signup'
        st.rerun()

if __name__ == "__main__":
    main()
