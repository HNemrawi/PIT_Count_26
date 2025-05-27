"""
Authentication component for PIT Count application.
Handles user login and region selection.
Updated to remove sidebar navigation.
"""

import streamlit as st
import hashlib
from typing import Optional, Tuple

from utils.session import SessionManager
from utils.helpers import get_timezone_for_region, get_current_timestamp

class AuthenticationManager:
    """Manages user authentication and region selection."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA256."""
        if not isinstance(password, str):
            raise ValueError("Password must be a string")
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_credentials(username: str, password: str) -> bool:
        """Verify user credentials against stored secrets."""
        try:
            users = st.secrets.get("users", {})
            hashed_input_password = AuthenticationManager.hash_password(password)
            return users.get(username) == hashed_input_password
        except Exception as e:
            st.error(f"Authentication error: {str(e)}")
            return False
    
    @staticmethod
    def create_login_form() -> bool:
        """Create and handle login form."""
        st.title("PIT Count Application")
        st.subheader("Login")
        
        with st.form("login_form", clear_on_submit=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            with col2:
                st.write("")  # Spacing
                st.write("")  # Spacing
                submit_button = st.form_submit_button("Login", type="primary", use_container_width=True)
            
            if submit_button:
                if username and password:
                    if AuthenticationManager.verify_credentials(username, password):
                        SessionManager.set_session_value('logged_in', True)
                        SessionManager.set_session_value('username', username)
                        SessionManager.update_current_step('region_selection')
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password. Please try again.")
                else:
                    st.warning("Please enter both username and password.")
        
        return False
    
    @staticmethod
    def create_region_selection() -> Optional[str]:
        """Create region selection interface."""
        st.title("PIT Count Application")
        st.subheader("Select Implementation Region")
        
        regions = ['', 'New England', 'Dashgreatlake']
        
        with st.form("region_form"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                selected_region = st.selectbox(
                    'Select an Implementation',
                    regions,
                    index=0,
                    help="Choose the region for your PIT count implementation"
                )
                
                if selected_region:
                    timezone = get_timezone_for_region(selected_region)
                    st.info(f"Selected region: {selected_region} (Timezone: {timezone})")
            
            with col2:
                st.write("")  # Spacing
                submit_button = st.form_submit_button("Continue", type="primary", use_container_width=True)
            
            if submit_button:
                if selected_region:
                    SessionManager.set_session_value('region', selected_region)
                    SessionManager.update_current_step('upload')
                    st.success(f"Region selected: {selected_region}")
                    st.rerun()
                else:
                    st.warning("Please select a region to continue.")
        
        return None
    
    @staticmethod
    def create_header():
        """Create application header with user info."""
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.markdown("### PIT Count Application")
        
        with col2:
            region = SessionManager.get_session_value('region')
            username = SessionManager.get_session_value('username', 'User')
            if region:
                st.info(f"👤 {username} | 📍 {region}")
        
        with col3:
            if st.button("Logout", type="secondary"):
                SessionManager.clear_all_session()
                st.rerun()

def create_authentication_interface() -> Tuple[bool, Optional[str]]:
    """Create complete authentication interface."""
    
    # Initialize session
    SessionManager.initialize_session()
    
    # Check current state
    if not SessionManager.is_logged_in():
        success = AuthenticationManager.create_login_form()
        return False, None
    
    # Check if region is selected
    region = SessionManager.get_session_value('region')
    if not region:
        selected_region = AuthenticationManager.create_region_selection()
        return True, selected_region
    
    # Show header only (no sidebar)
    AuthenticationManager.create_header()
    
    return True, region