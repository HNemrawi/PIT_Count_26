"""
Session state management for PIT Count application.
Provides clean initialization and management of Streamlit session state.
Enhanced to store uploaded file buffers for sheet re-selection.
"""

import streamlit as st
from typing import Any, Dict
import pandas as pd
from datetime import datetime


class SessionManager:
    """Manages Streamlit session state for PIT Count application."""
    
    # Default session state values
    DEFAULT_STATE = {
        'logged_in': False,
        'username': None,
        'region': None,
        'uploaded_data': {},
        'uploaded_files': {},  # Store file buffers for re-selection
        'data_quality': [],
        'processed_data': {},
        'calculated_reports': {},
        'current_step': 'login'
    }
    
    @classmethod
    def initialize_session(cls):
        """Initialize session state with default values."""
        for key, default_value in cls.DEFAULT_STATE.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    @classmethod
    def clear_data_session(cls):
        """Clear data-related session state while preserving login and region."""
        preserved_keys = ['logged_in', 'username', 'region', 'current_step']
        preserved_values = {key: st.session_state.get(key) for key in preserved_keys}
        
        # Clear data-related keys
        data_keys = ['uploaded_data', 'uploaded_files', 'data_quality', 'processed_data', 'calculated_reports']
        for key in data_keys:
            if key in st.session_state:
                st.session_state[key] = {} if key != 'data_quality' else []
        
        # Clear sheet selection and mode keys
        keys_to_remove = []
        for key in st.session_state:
            if (key.endswith('_selected_sheet') or 
                key.endswith('_reselect_sheet') or 
                key.endswith('_sheet_change_mode')):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del st.session_state[key]
        
        # Set step back to upload
        st.session_state['current_step'] = 'upload'
    
    @classmethod
    def clear_all_session(cls):
        """Clear all session state."""
        st.session_state.clear()
        cls.initialize_session()
    
    @classmethod
    def get_session_value(cls, key: str, default: Any = None) -> Any:
        """Get value from session state with default."""
        return st.session_state.get(key, default)
    
    @classmethod
    def set_session_value(cls, key: str, value: Any):
        """Set value in session state."""
        st.session_state[key] = value
    
    @classmethod
    def update_current_step(cls, step: str):
        """Update the current processing step."""
        st.session_state['current_step'] = step
    
    @classmethod
    def get_current_step(cls) -> str:
        """Get the current processing step."""
        return st.session_state.get('current_step', 'login')
    
    @classmethod
    def is_logged_in(cls) -> bool:
        """Check if user is logged in."""
        return st.session_state.get('logged_in', False)
    
    @classmethod
    def has_uploaded_data(cls) -> bool:
        """Check if data has been uploaded."""
        uploaded_data = st.session_state.get('uploaded_data', {})
        return bool(uploaded_data)
    
    @classmethod
    def has_processed_data(cls) -> bool:
        """Check if data has been processed."""
        processed_data = st.session_state.get('processed_data', {})
        return bool(processed_data)
    
    @classmethod
    def has_calculated_reports(cls) -> bool:
        """Check if reports have been calculated."""
        calculated_reports = st.session_state.get('calculated_reports', {})
        return bool(calculated_reports)
    
    @classmethod
    def get_uploaded_data(cls) -> Dict[str, pd.DataFrame]:
        """Get uploaded data from session."""
        return st.session_state.get('uploaded_data', {})
    
    @classmethod
    def get_processed_data(cls) -> Dict[str, Dict[str, pd.DataFrame]]:
        """Get processed data from session."""
        return st.session_state.get('processed_data', {})
    
    @classmethod
    def get_calculated_reports(cls) -> Dict[str, Dict[str, pd.DataFrame]]:
        """Get calculated reports from session."""
        return st.session_state.get('calculated_reports', {})
    
    @classmethod
    def get_uploaded_files(cls) -> Dict[str, Dict]:
        """Get uploaded file buffers from session."""
        return st.session_state.get('uploaded_files', {})
    
    @classmethod
    def clear_source_data(cls, source_name: str):
        """Clear data for a specific source to force re-processing."""
        # Clear uploaded data for this source
        uploaded_data = cls.get_uploaded_data()
        if source_name in uploaded_data:
            del uploaded_data[source_name]
            cls.set_session_value('uploaded_data', uploaded_data)
        
        # Clear processed data for this source
        processed_data = cls.get_processed_data()
        if source_name in processed_data:
            del processed_data[source_name]
            cls.set_session_value('processed_data', processed_data)
        
        # Clear calculated reports if all data is cleared
        if not uploaded_data:
            cls.set_session_value('calculated_reports', {})
    
    @classmethod
    def get_session_summary(cls) -> Dict[str, Any]:
        """Get summary of current session state."""
        uploaded_data = cls.get_uploaded_data()
        uploaded_files = cls.get_uploaded_files()
        processed_data = cls.get_processed_data()
        calculated_reports = cls.get_calculated_reports()
        
        return {
            'logged_in': cls.is_logged_in(),
            'username': st.session_state.get('username', 'User'),
            'region': st.session_state.get('region'),
            'current_step': cls.get_current_step(),
            'has_uploaded_data': cls.has_uploaded_data(),
            'has_uploaded_files': bool(uploaded_files),
            'has_processed_data': cls.has_processed_data(),
            'has_calculated_reports': cls.has_calculated_reports(),
            'uploaded_sources': list(uploaded_data.keys()),
            'uploaded_files': list(uploaded_files.keys()),
            'uploaded_rows': sum(len(df) for df in uploaded_data.values()),
            'processed_sources': list(processed_data.keys()),
            'available_reports': list(calculated_reports.keys())
        }
    
    @classmethod
    def display_session_debug(cls):
        """Display session state debug information."""
        if st.checkbox("Show Session Debug Info"):
            summary = cls.get_session_summary()
            st.json(summary)

    @classmethod
    def clear_data_session(cls):
        """Clear data-related session state while preserving login and region."""
        preserved_keys = ['logged_in', 'username', 'region', 'current_step']
        preserved_values = {key: st.session_state.get(key) for key in preserved_keys}
        
        # Clean up temporary files if file manager exists
        if 'file_manager' in st.session_state and 'session_id' in st.session_state:
            try:
                st.session_state.file_manager.delete_session_files(st.session_state.session_id)
            except:
                pass  # Don't fail if cleanup has issues
        
        # Clear data-related keys
        data_keys = ['uploaded_data', 'uploaded_files', 'data_quality', 'processed_data', 'calculated_reports']
        for key in data_keys:
            if key in st.session_state:
                st.session_state[key] = {} if key != 'data_quality' else []
        
        # Clear sheet selection and mode keys
        keys_to_remove = []
        for key in st.session_state:
            if (key.endswith('_selected_sheet') or 
                key.endswith('_reselect_sheet') or 
                key.endswith('_sheet_change_mode')):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del st.session_state[key]
        
        # Set step back to upload
        st.session_state['current_step'] = 'upload'

    @classmethod
    def clear_all_session(cls):
        """Clear all session state."""
        # Clean up temporary files if file manager exists
        if 'file_manager' in st.session_state and 'session_id' in st.session_state:
            try:
                st.session_state.file_manager.delete_session_files(st.session_state.session_id)
            except:
                pass
        
        st.session_state.clear()
        cls.initialize_session()