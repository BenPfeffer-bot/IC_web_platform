# pages/dashboard.py

import streamlit as st
from utils.session_manager import initialize_session_state

def show_dashboard():
    initialize_session_state()

    if not st.session_state.get('authenticated', False):
        st.warning("Please log in to access this page.")
        st.session_state['current_page'] = 'Login'
        st.rerun()

    st.title("Dashboard")

    # Your dashboard content goes here
    st.write("This is the dashboard page.")

    if st.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        initialize_session_state()
        st.rerun()
