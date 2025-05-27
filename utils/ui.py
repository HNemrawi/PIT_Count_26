"""
UI utility functions for PIT Count application.
Handles common UI elements like headers and footers.
Updated to remove sidebar functions.
"""

import streamlit as st
from utils.session import SessionManager

def create_header():
    """Create application header with logo and title."""
    
    with st.container():
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            st.markdown("""
                <div style="text-align: left;">
                    <a href="https://icalliances.org/" target="_blank">
                        <img src="https://images.squarespace-cdn.com/content/v1/54ca7491e4b000c4d5583d9c/eb7da336-e61c-4e0b-bbb5-1a7b9d45bff6/Dash+Logo+2.png?format=750w" width="200">
                    </a>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <h1 style="color:#00629b; text-align:center; margin-top: 20px; font-size: 2.5rem;">
                    Point in Time Count Application
                </h1>
            """, unsafe_allow_html=True)
        
        with col3:
            # Quick status info
            if SessionManager.is_logged_in():
                summary = SessionManager.get_session_summary()
                status_html = "<div style='text-align: right; font-size: 0.9em; color: #666;'>"
                
                if summary['has_uploaded_data']:
                    status_html += "✅ Data Uploaded<br>"
                if summary['has_processed_data']:
                    status_html += "✅ Data Processed<br>"
                if summary['has_calculated_reports']:
                    status_html += "✅ Reports Ready<br>"
                
                status_html += "</div>"
                st.markdown(status_html, unsafe_allow_html=True)


def create_footer():
    """Create application footer."""
    st.markdown("---")
    
    st.markdown("""
        <div style="text-align: center; color: #808080; font-style: italic; padding: 20px;">
            <a href="https://icalliances.org/" target="_blank">
                <img src="https://images.squarespace-cdn.com/content/v1/54ca7491e4b000c4d5583d9c/eb7da336-e61c-4e0b-bbb5-1a7b9d45bff6/Dash+Logo+2.png?format=750w" width="80">
            </a><br>
            DASH™ is a trademark of Institute for Community Alliances.<br>
            <a href="https://icalliances.org/" target="_blank">
                <img src="https://images.squarespace-cdn.com/content/v1/54ca7491e4b000c4d5583d9c/1475614371395-KFTYP42QLJN0VD5V9VB1/ICA+Official+Logo+PNG+%28transparent%29.png?format=1500w" width="80">
            </a><br>
            © 2024 Institute for Community Alliances (ICA). All rights reserved.
        </div>
    """, unsafe_allow_html=True)


def create_step_header(step_name: str, description: str = ""):
    """Create a consistent header for each workflow step."""
    st.header(step_name)
    if description:
        st.markdown(f"*{description}*")
    st.markdown("---")