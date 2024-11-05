# utils/session_manager.py

import streamlit as st

def initialize_session_state():
    default_state = {
        'authenticated': False,
        'name': '',
        'current_page': 'Login',
        'show_animation': False,
        'landing_viewed': False,  # Flag to track if landing page has been viewed
    }
    for key, default_value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
