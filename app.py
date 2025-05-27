"""
Main application file for PIT Count Application.
Updated to remove sidebar and improve navigation.
"""

import streamlit as st
import warnings
import pandas as pd

# Suppress warnings and set pandas options
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)

# Configure Streamlit page with WIDE layout
st.set_page_config(
    page_title="PIT Count Application",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"  # Collapse sidebar by default
)

# Import application components
from components.auth import create_authentication_interface
from components.workflow import create_workflow_interface
from utils.session import SessionManager
from utils.ui import create_header, create_footer

def main():
    """Main application function with improved UX."""
    
    try:
        # Initialize session
        SessionManager.initialize_session()
        
        # Handle authentication
        is_authenticated, region = create_authentication_interface()
        
        if not is_authenticated:
            return
        
        if not region:
            return
        
        # Show header
        create_header()
        
        # Main workflow (no sidebar)
        create_workflow_interface()
        
        # Show footer
        create_footer()
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        
        with st.expander("🔍 Error Details"):
            st.exception(e)
        
        # Simple reset option
        if st.button("🔄 Reset Application", type="primary"):
            SessionManager.clear_all_session()
            st.rerun()

if __name__ == "__main__":
    main()