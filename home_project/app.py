# app.py
import streamlit as st
from typing import Dict, Type, Optional
from enum import Enum, auto
from dataclasses import dataclass
from ui.pages import LoginPage, SignupPage, MainPage
from ui.page.dashboard import DashboardPage
from core.exceptions import AppException
import logging
from pathlib import Path
from streamlit_navigation_bar import st_navbar

class PageID(Enum):
    """Enum for page identification"""
    LOGIN = auto()
    SIGNUP = auto()
    MAIN = auto()
    DASHBOARD = auto()

@dataclass
class PageConfig:
    """Configuration for each page"""
    title: str
    requires_auth: bool
    icon: Optional[str] = None
    order: Optional[int] = None

class Application:
    """
    Main application class handling routing, state management, and navigation.
    
    Attributes:
        pages (Dict[PageID, Type]): Mapping of page IDs to page classes
        page_configs (Dict[PageID, PageConfig]): Page-specific configurations
    """
    
    # Page configurations
    PAGE_CONFIGS: Dict[PageID, PageConfig] = {
        PageID.LOGIN: PageConfig("Login", False, "🔑", 1),
        PageID.SIGNUP: PageConfig("Sign Up", False, "📝", 2),
        PageID.MAIN: PageConfig("Main", True, "🏠", 3),
        PageID.DASHBOARD: PageConfig("Dashboard", True, "📊", 4)
    }

    def __init__(self):
        """Initialize application state and logging"""
        self._setup_logging()
        self._initialize_session_state()
        self._initialize_pages()
        
    def _setup_logging(self) -> None:
        """Configure application logging"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            filename=log_dir / "app.log",
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _initialize_session_state(self) -> None:
        """Initialize or update session state variables"""
        try:
            default_state = {
                'page_history': [],
                'authenticated': False,
                'current_page': PageID.LOGIN,
                'user_role': None,
                'user_id': None,
                'name': '',
                'signup': False,
                'show_animation': False,
                'animation_complete': False,
                'last_activity': None,
            }
            
            for key, default_value in default_state.items():
                if key not in st.session_state:
                    st.session_state[key] = default_value
                    
        except Exception as e:
            self.logger.error(f"Session state initialization failed: {str(e)}")
            raise AppException("Failed to initialize application state")

    def _initialize_pages(self) -> None:
        """Initialize page mapping with error handling"""
        try:
            self.pages: Dict[PageID, Type] = {
                PageID.LOGIN: LoginPage,
                PageID.SIGNUP: SignupPage,
                PageID.MAIN: MainPage,
                PageID.DASHBOARD: DashboardPage
            }
        except Exception as e:
            self.logger.error(f"Page initialization failed: {str(e)}")
            raise AppException("Failed to initialize application pages")

    def _handle_navigation(self) -> None:
        """Handle page navigation using tabs"""
        try:
            if st.session_state['authenticated'] and not st.session_state.get('show_animation', False):
                # Only show navigation items for authenticated pages
                nav_pages = {
                    page_id: config for page_id, config in self.PAGE_CONFIGS.items()
                    if config.requires_auth
                }
                
                # Sort pages by order
                sorted_pages = sorted(
                    nav_pages.items(),
                    key=lambda x: x[1].order or float('inf')
                )
                
                # Create tabs
                tab_titles = [f"{config.icon} {config.title}" for _, config in sorted_pages]
                tabs = st.tabs(tab_titles)
                
                # Store current tab index
                current_page = st.session_state['current_page']
                current_index = next(
                    (i for i, (page_id, _) in enumerate(sorted_pages) if page_id == current_page),
                    0
                )
                
                # Add settings and logout in a container above the tabs
                with st.container():
                    col1, col2, col3 = st.columns([1, 1, 1])
                    

                    with col3:
                        if st.button("🚪 Logout"):
                            self._handle_logout()
                
                # Handle tab selection
                for i, (page_id, _) in enumerate(sorted_pages):
                    if i == current_index:
                        with tabs[i]:
                            pass  # Content will be rendered by the page class
                    else:
                        with tabs[i]:
                            if st.button(f"Go to {nav_pages[page_id].title}", key=f"tab_{i}"):
                                self._navigate_to(page_id)

        except Exception as e:
            self.logger.error(f"Navigation handling failed: {str(e)}")
            st.error("Navigation system encountered an error")


    def _navigate_to(self, page_id: PageID) -> None:
        """
        Handle navigation to a specific page
        
        Args:
            page_id (PageID): Target page identifier
        """
        config = self.PAGE_CONFIGS.get(page_id)
        if not config:
            self.logger.error(f"Invalid page ID: {page_id}")
            return
            
        if config.requires_auth and not st.session_state['authenticated']:
            st.warning("Please log in to access this page")
            page_id = PageID.LOGIN
            
        st.session_state['current_page'] = page_id
        st.rerun()

    def _handle_logout(self) -> None:
        """Handle user logout and session cleanup"""
        try:
            self.logger.info(f"User logout: {st.session_state.get('user_id')}")
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            self._initialize_session_state()
            st.rerun()
        except Exception as e:
            self.logger.error(f"Logout failed: {str(e)}")
            st.error("Failed to log out properly")

    def _get_current_page(self) -> PageID:
        """
        Determine current page based on application state
        
        Returns:
            PageID: Current page identifier
        """
        if not st.session_state['authenticated']:
            return PageID.SIGNUP if st.session_state['signup'] else PageID.LOGIN
        
        if st.session_state.get('show_animation', False):
            return PageID.MAIN
            
        return st.session_state.get('current_page', PageID.MAIN)

    def run(self) -> None:
        """Run the application with error handling"""
        try:
            current_page = self._get_current_page()
            st.session_state['current_page'] = current_page

            if not st.session_state.get('show_animation', False):
                self._handle_navigation()

            page_class = self.pages.get(current_page)
            if page_class:
                page_instance = page_class()
                page_instance.render()
            else:
                st.error("Page not found!")
                self.logger.error(f"Invalid page requested: {current_page}")

            # Update page history
            if current_page not in st.session_state['page_history']:
                st.session_state['page_history'].append(current_page)
                
        except Exception as e:
            self.logger.error(f"Application runtime error: {str(e)}")
            st.error("An unexpected error occurred. Please try refreshing the page.")

def main():
    """Application entry point with configuration"""
    try:
        st.set_page_config(
            page_title="Company Portfolio Manager",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="collapsed" 
        )

        app = Application()
        app.run()
                
    except Exception as e:
        st.error("Failed to start application. Please contact support.")
        logging.error(f"Application startup failed: {str(e)}")

if __name__ == "__main__":
    main()