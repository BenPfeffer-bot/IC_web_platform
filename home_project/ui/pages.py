# ui/pages.py

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
from core.authentication import AuthenticationService
from ui.styles import Styles
from config.settings import Settings
import time


class BasePage:
    def __init__(self):
        self.auth_service = AuthenticationService()
        self.init_session_state()

    def show_error(self, message: str) -> None:
        st.error(message)

    def show_success(self, message: str) -> None:
        st.success(message)

    def init_session_state(self) -> None:
        if 'page_initialized' not in st.session_state:
            st.session_state.update({
                'page_initialized': True,
                'authenticated': False,
                'name': '',
                'signup': False,
                'show_animation': False,
                'animation_complete': False
            })

class LoginPage(BasePage):
    def render(self) -> None:
        st.title("Login")
        
        with st.form("login_form"):
            username = st.text_input("Username").strip()
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                if not username or not password:
                    self.show_error("Please fill in all fields")
                elif self.auth_service.login(username, password):
                    st.session_state.update({
                        'authenticated': True,
                        'name': username,
                        'show_animation': True
                    })
                    st.rerun()
                else:
                    self.show_error("Invalid username or password")

        if st.button("Don't have an account? Sign up"):
            st.session_state['signup'] = True
            st.rerun()

class SignupPage(BasePage):
    def render(self) -> None:
        st.title("Sign Up")
        
        with st.form("signup_form"):
            name = st.text_input("Full Name").strip()
            username = st.text_input("Username").strip()
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submitted = st.form_submit_button("Sign Up")

            if submitted:
                if not username or not password or not name:
                    self.show_error("Please fill in all fields")
                elif len(password) < 6:
                    self.show_error("Password must be at least 6 characters long")
                elif password != confirm_password:
                    self.show_error("Passwords do not match")
                else:
                    try:
                        if self.auth_service.register(username, password, name):
                            self.show_success("Account created successfully!")
                            time.sleep(1)
                            st.session_state['signup'] = False
                            st.rerun()
                        else:
                            self.show_error("Username already exists")
                    except Exception as e:
                        self.show_error(f"Registration failed: {str(e)}")

        if st.button("Already have an account? Login"):
            st.session_state['signup'] = False
            st.rerun()

class MainPage(BasePage):
    def render(self) -> None:
        if st.session_state.get('show_animation', False):
            self.show_animation()
        else:
            self.show_dashboard()

    def show_animation(self) -> None:
        try:
            st.markdown('<div class="stApp">', unsafe_allow_html=True)
            current_dir = Path(__file__).parent.parent
            logo_path = current_dir / "statics" / "image" / "logo_grey.png"
            
            if not logo_path.exists():
                st.error(f"Logo not found at: {logo_path}")
                return
            
            with open(logo_path, "rb") as f:
                logo_contents = f.read()
                logo_data_url = f"data:image/png;base64,{base64.b64encode(logo_contents).decode()}"
            
            st.markdown(Styles.get_animation_css(), unsafe_allow_html=True)
            st.markdown(Styles.get_animation_html(logo_data_url), unsafe_allow_html=True)
            
            time.sleep(Settings.ANIMATION_DURATION)
            
            st.session_state.update({
                'show_animation': False,
                'animation_complete': True
            })
            st.rerun()
            
        except Exception as e:
            st.error(f"Animation error: {str(e)}")
            st.session_state['show_animation'] = False
            st.rerun()

    def show_dashboard(self) -> None:
        # Sidebar with navigation and user info
        with st.sidebar:
            st.write(f"Welcome {st.session_state['name']}!")
            
            # Navigation menu
            st.subheader("Navigation")
            pages = {
                "Dashboard": "dashboard",
                "Companies": "companies",
                "Financial Reports": "financials",
                "Investment Tracking": "investments",
                "Document Center": "documents",
                "Settings": "settings"
            }
            
            selected_page = st.radio("", list(pages.keys()))
            
            if st.button("Logout"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                self.init_session_state()
                st.rerun()

        # Main content area
        if selected_page == "Dashboard":
            # Render the React dashboard component
            components.html(
                f"""
                <div id="dashboard-root"></div>
                <script>
                    const dashboard = document.getElementById('dashboard-root');
                    const root = ReactDOM.createRoot(dashboard);
                    root.render(React.createElement(Dashboard, {{ 
                        userName: "{st.session_state['name']}"
                    }}));
                </script>
                """,
                height=800,
            )
        else:
            st.title(selected_page)
            st.write(f"{selected_page} content coming soon...")
