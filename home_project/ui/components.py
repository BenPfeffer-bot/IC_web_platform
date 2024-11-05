
# ui/components.py
import streamlit as st
from typing import Callable
from ui.styles import Styles

class UIComponent:
    """Base class for UI components"""
    @staticmethod
    def create_columns(num_columns: int):
        return st.columns([1] * num_columns)

class LoginForm(UIComponent):
    """Login form component"""
    def render(self, on_login: Callable, on_signup: Callable) -> None:
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        
        col1, col2 = self.create_columns(2)
        
        if col1.button("Login"):
            on_login(username, password)
        if col2.button("Sign Up"):
            on_signup()

class SignupForm(UIComponent):
    """Signup form component"""
    def render(self, on_signup: Callable, on_back: Callable) -> None:
        st.title("Sign Up")
        username = st.text_input("Choose a Username")
        name = st.text_input("Your Name")
        password = st.text_input("Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password')
        
        col1, col2 = self.create_columns(2)
        
        if col1.button("Create Account"):
            if password == confirm_password:
                on_signup(username, password, name)
            else:
                st.error("Passwords do not match")
        
        if col2.button("Back to Login"):
            on_back()