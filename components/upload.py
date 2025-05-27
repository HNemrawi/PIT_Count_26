"""
Upload component for PIT Count application.
Enhanced with temporary file storage for better memory management.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional, Tuple
from io import BytesIO
from datetime import datetime
import uuid

from core.validator import DataValidator, ValidationResult
from utils.session import SessionManager
from utils.helpers import get_file_size_mb, format_number
from utils.file_manager import FileManager  # NEW IMPORT

class UploadManager:
    """Manages the upload workflow with enhanced Excel sheet selection."""
    
    def __init__(self, region: str, expected_columns: List[str]):
        """Initialize upload manager with region and expected columns."""
        self.region = region
        self.expected_columns = expected_columns
        
        # Initialize file manager
        if 'file_manager' not in st.session_state:
            st.session_state.file_manager = FileManager()
        self.file_manager = st.session_state.file_manager
        
        # Ensure session ID exists
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
        self.session_id = st.session_state.session_id
    
    def create_upload_instructions(self):
        """Create simplified upload instructions."""
        with st.expander("📋 Upload Instructions", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**What to Upload:**")
                st.write("• Emergency Shelter (ES) data")
                st.write("• Transitional Housing (TH) data")
                st.write("• Unsheltered data")
                st.write("• File formats: CSV or Excel (.xlsx)")
            
            with col2:
                st.write("**Data Structure:**")
                st.write("• Each row = one household")
                st.write("• Include all family members")
                st.write("• Timestamp column required")
                st.write("• Rows without timestamps will be removed")
    
    def create_file_upload_section(self, source_name: str, label: str, 
                                 help_text: str, key: str) -> Optional[pd.DataFrame]:
        """Create enhanced file upload section with sheet re-selection capability."""
        
        st.subheader(f"📁 {label}")
        
        # Check if we have a stored file for this source
        stored_files = SessionManager.get_session_value('uploaded_files', {})
        stored_file_info = stored_files.get(source_name, {})
        has_stored_file = bool(stored_file_info.get('file_path'))  # CHANGED: Check file_path instead of file_buffer
        
        # File uploader
        uploaded_file = st.file_uploader(
            f"Choose {label} file",
            type=['csv', 'xlsx'],
            key=key,
            help=help_text
        )
        
        # If a new file is uploaded, store it
        if uploaded_file:
            # Read file content
            file_content = uploaded_file.read()
            uploaded_file.seek(0)  # Reset for getting size
            file_size = len(file_content) / 1024 / 1024  # MB
            
            # Save to temporary storage
            try:
                file_path = self.file_manager.save_file(
                    file_content, 
                    source_name, 
                    self.session_id
                )
                
                # Store metadata only (not the buffer itself)
                stored_files[source_name] = {
                    'file_path': file_path,
                    'file_name': uploaded_file.name,
                    'file_size': file_size,
                    'upload_time': datetime.now()
                }
                SessionManager.set_session_value('uploaded_files', stored_files)
                
                # Update stored file info
                stored_file_info = stored_files[source_name]
                has_stored_file = True
                
            except Exception as e:
                st.error(f"Failed to save file: {str(e)}")
                return None
        
        # If we have a stored file (either just uploaded or from before)
        if has_stored_file:
            file_name = stored_file_info['file_name']
            file_size = stored_file_info['file_size']
            file_path = stored_file_info['file_path']
            
            st.success(f"✅ **{file_name}** ({file_size:.1f} MB)")
            
            # Check file size
            if file_size > 100:
                st.error("⚠️ File size exceeds 100 MB limit. Please reduce file size and try again.")
                return None
            
            # Load file when needed
            try:
                file_buffer = self.file_manager.load_file(file_path)
                
                # Handle Excel sheet selection
                sheet_name = None
                if file_name.endswith('.xlsx'):
                    try:
                        # Reset buffer position
                        file_buffer.seek(0)
                        excel_file = pd.ExcelFile(file_buffer)
                        sheet_names = excel_file.sheet_names
                        
                        if len(sheet_names) > 1:
                            # Get previously selected sheet if any
                            previous_sheet = SessionManager.get_session_value(f'{source_name}_selected_sheet')
                            default_index = 0
                            if previous_sheet in sheet_names:
                                default_index = sheet_names.index(previous_sheet)
                            
                            # Sheet selector
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                sheet_name = st.selectbox(
                                    f"Select sheet from {file_name}",
                                    sheet_names,
                                    index=default_index,
                                    key=f"{key}_sheet"
                                )
                            
                            with col2:
                                st.info("Sheet will update on form submission")
                            
                            # Store selected sheet
                            SessionManager.set_session_value(f'{source_name}_selected_sheet', sheet_name)
                        else:
                            sheet_name = sheet_names[0]
                            SessionManager.set_session_value(f'{source_name}_selected_sheet', sheet_name)
                            
                    except Exception as e:
                        st.error(f"❌ Error reading Excel file: {str(e)}")
                        return None
                
                # Load the data
                file_buffer.seek(0)  # Reset buffer position
                
                if file_name.endswith('.csv'):
                    df = pd.read_csv(file_buffer)
                elif file_name.endswith('.xlsx'):
                    df = pd.read_excel(file_buffer, sheet_name=sheet_name)
                else:
                    st.error(f"Unsupported file format: {file_name}")
                    return None
                
                if df.empty:
                    st.error("❌ The uploaded file contains no data.")
                    return None
                
                # Basic file info
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Households", format_number(len(df)))
                with col2:
                    st.metric("Columns", len(df.columns))
                
                return df
                
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
                # If file is corrupted or inaccessible, remove it from stored files
                if source_name in stored_files:
                    del stored_files[source_name]
                    SessionManager.set_session_value('uploaded_files', stored_files)
                return None
        
        return None
    
    def validate_uploaded_data(self, data_dict: Dict[str, pd.DataFrame]) -> Tuple[Dict[str, pd.DataFrame], bool]:
        """Validate uploaded data and return cleaned data with status."""
        all_valid = True
        cleaned_data = {}
        
        for source_name, df in data_dict.items():
            # Clean the data first
            df.columns = df.columns.str.strip()
            df = df.loc[:, ~df.columns.duplicated(keep='first')]
            
            # Remove rows with missing timestamps
            if 'Timestamp' in df.columns:
                initial_count = len(df)
                df = df.dropna(subset=['Timestamp'])
                dropped_count = initial_count - len(df)
                if dropped_count > 0:
                    st.info(f"🧹 {source_name}: Removed {dropped_count} rows with missing timestamps")
            
            # Check essential columns
            essential_columns = ['Timestamp', 'Gender', 'Race/Ethnicity', 'Age Range']
            missing_essential = set(essential_columns) - set(df.columns)
            
            if missing_essential:
                st.error(f"❌ {source_name}: Missing essential columns: {', '.join(missing_essential)}")
                all_valid = False
            else:
                cleaned_data[source_name] = df
                st.success(f"✅ {source_name}: Valid data with {len(df)} households")
        
        return cleaned_data, all_valid
    
    def create_data_preview_section(self, data_dict: Dict[str, pd.DataFrame]):
        """Create simplified data preview section."""
        st.subheader("👀 Data Preview")
        
        # Create tabs for each source
        if len(data_dict) > 1:
            tabs = st.tabs(list(data_dict.keys()))
            for tab, (source_name, df) in zip(tabs, data_dict.items()):
                with tab:
                    st.dataframe(df.head(20), use_container_width=True)
                    st.caption(f"Showing first 20 of {len(df)} rows")
        elif data_dict:
            # Single source - no tabs needed
            source_name, df = list(data_dict.items())[0]
            st.dataframe(df.head(20), use_container_width=True)
            st.caption(f"Showing first 20 of {len(df)} rows")
    
    def create_upload_summary(self, data_dict: Dict[str, pd.DataFrame]) -> bool:
        """Create simplified upload summary."""
        st.subheader("📋 Upload Summary")
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        total_rows = sum(len(df) for df in data_dict.values())
        
        with col1:
            st.metric("Data Sources", len(data_dict))
        with col2:
            st.metric("Total Households", format_number(total_rows))
        with col3:
            st.metric("Status", "✅ Ready" if total_rows > 0 else "❌ No Data")
        
        return total_rows > 0


def create_upload_interface(region: str, expected_columns: List[str]) -> Dict[str, pd.DataFrame]:
    """Create the enhanced upload interface with sheet re-selection."""
    
    # Update current step
    SessionManager.update_current_step('upload')
    
    # Check if we already have uploaded data in session
    existing_data = SessionManager.get_session_value('uploaded_data', {})
    stored_files = SessionManager.get_session_value('uploaded_files', {})
    
    # Check if we're in sheet change mode for any source
    sheet_change_mode = {}
    for source_name in stored_files:
        sheet_change_mode[source_name] = SessionManager.get_session_value(f'{source_name}_sheet_change_mode', False)
    
    # Handle sheet change mode OUTSIDE of any form
    if any(sheet_change_mode.values()):
        # Initialize file manager for sheet changes
        if 'file_manager' not in st.session_state:
            st.session_state.file_manager = FileManager()
        file_manager = st.session_state.file_manager
        
        for source_name, is_changing in sheet_change_mode.items():
            if is_changing and source_name in stored_files:
                file_info = stored_files[source_name]
                if file_info['file_name'].endswith('.xlsx'):
                    st.write(f"### 🔄 Change Sheet for {source_name}")
                    st.info(f"📄 File: {file_info['file_name']}")
                    
                    try:
                        # Load file from temp storage
                        file_buffer = file_manager.load_file(file_info['file_path'])
                        file_buffer.seek(0)
                        excel_file = pd.ExcelFile(file_buffer)
                        sheet_names = excel_file.sheet_names
                        
                        # Get current sheet
                        current_sheet = SessionManager.get_session_value(f'{source_name}_selected_sheet')
                        default_index = 0
                        if current_sheet in sheet_names:
                            default_index = sheet_names.index(current_sheet)
                        
                        # Sheet selector
                        new_sheet = st.selectbox(
                            f"Select new sheet for {source_name}:",
                            sheet_names,
                            index=default_index,
                            key=f"reselect_sheet_{source_name}"
                        )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Confirm Sheet Change", type="primary", key=f"confirm_{source_name}"):
                                # Update the selected sheet
                                SessionManager.set_session_value(f'{source_name}_selected_sheet', new_sheet)
                                
                                # Reload data with new sheet
                                file_buffer.seek(0)
                                try:
                                    new_df = pd.read_excel(file_buffer, sheet_name=new_sheet)
                                    
                                    # Update uploaded data
                                    existing_data[source_name] = new_df
                                    SessionManager.set_session_value('uploaded_data', existing_data)
                                    
                                    # Clear processed data to force reprocessing
                                    SessionManager.set_session_value('processed_data', {})
                                    SessionManager.set_session_value('calculated_reports', {})
                                    
                                    # Exit sheet change mode
                                    SessionManager.set_session_value(f'{source_name}_sheet_change_mode', False)
                                    
                                    st.success(f"✅ Sheet changed to '{new_sheet}'. Data will be reprocessed.")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error loading sheet: {str(e)}")
                        
                        with col2:
                            if st.button("❌ Cancel", key=f"cancel_{source_name}"):
                                SessionManager.set_session_value(f'{source_name}_sheet_change_mode', False)
                                st.rerun()
                    
                    except Exception as e:
                        st.error(f"Error accessing file: {str(e)}")
                        # Clear the problematic file reference
                        if source_name in stored_files:
                            del stored_files[source_name]
                            SessionManager.set_session_value('uploaded_files', stored_files)
                        SessionManager.set_session_value(f'{source_name}_sheet_change_mode', False)
                        st.rerun()
                    
                    return existing_data  # Don't show the rest of the interface
    
    # Normal mode - show existing data or upload form
    if existing_data:
        st.success(f"✅ You have {len(existing_data)} data source(s) already uploaded.")
        
        # Show summary of existing data
        col1, col2, col3 = st.columns(3)
        total_rows = sum(len(df) for df in existing_data.values())
        
        with col1:
            st.metric("Data Sources", len(existing_data))
        with col2:
            st.metric("Total Households", format_number(total_rows))
        with col3:
            st.metric("Status", "✅ Ready")
        
        # Show existing data preview with sheet change option
        st.subheader("📊 Current Data")
        
        for source_name, df in existing_data.items():
            st.write(f"### {source_name} - {len(df)} rows")
            
            # Show sheet change option if Excel file
            if source_name in stored_files:
                file_info = stored_files[source_name]
                if file_info['file_name'].endswith('.xlsx'):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        st.info(f"📄 File: {file_info['file_name']}")
                    with col2:
                        current_sheet = SessionManager.get_session_value(f'{source_name}_selected_sheet', 'Default')
                        st.info(f"📊 Current Sheet: {current_sheet}")
                    with col3:
                        if st.button(f"🔄 Change Sheet", key=f"change_sheet_{source_name}"):
                            # Enter sheet change mode
                            SessionManager.set_session_value(f'{source_name}_sheet_change_mode', True)
                            st.rerun()
            
            # Show data preview
            st.dataframe(df.head(20), use_container_width=True)
            st.write("---")
        
        # Option to re-upload
        st.warning("⚠️ Uploading new files will replace the existing data.")
        if st.button("🔄 Upload New Data", type="secondary"):
            SessionManager.clear_data_session()
            st.rerun()
        
        return existing_data
    
    # Initialize upload manager
    upload_manager = UploadManager(region, expected_columns)
    
    # Show upload instructions
    upload_manager.create_upload_instructions()
    
    # Create upload form
    uploaded_data = {}
    
    with st.form("data_upload_form", clear_on_submit=False):
        st.write(f"**Selected Region:** {region}")
        st.write("---")
        
        # Upload sections for each data source
        es_df = upload_manager.create_file_upload_section(
            "Sheltered_ES",
            "Emergency Shelter (ES) Data",
            "Upload data for emergency shelters",
            "es_upload"
        )
        
        st.write("---")
        
        th_df = upload_manager.create_file_upload_section(
            "Sheltered_TH", 
            "Transitional Housing (TH) Data",
            "Upload data for transitional housing",
            "th_upload"
        )
        
        st.write("---")
        
        unsheltered_df = upload_manager.create_file_upload_section(
            "Unsheltered",
            "Unsheltered Data", 
            "Upload data for unsheltered individuals",
            "unsheltered_upload"
        )
        
        st.write("---")
        
        # Form submission
        submitted = st.form_submit_button(
            "🔄 Process Uploaded Files", 
            type="primary",
            use_container_width=True
        )
        
        if submitted:
            # Collect uploaded data
            sources = [
                ("Sheltered_ES", es_df),
                ("Sheltered_TH", th_df),
                ("Unsheltered", unsheltered_df)
            ]
            
            temp_data = {}
            for source_name, df in sources:
                if df is not None and not df.empty:
                    temp_data[source_name] = df
            
            if not temp_data:
                st.error("❌ No valid data files were uploaded. Please select at least one file.")
                return {}
            
            # Validate the data
            st.write("---")
            st.subheader("🔍 Validating Data")
            
            uploaded_data, all_valid = upload_manager.validate_uploaded_data(temp_data)
            
            if not uploaded_data:
                st.error("❌ No valid data after validation. Please check your files.")
                return {}
            
            # Store in session if valid
            if all_valid:
                # Store the validated data in session
                SessionManager.set_session_value('uploaded_data', uploaded_data)
                
                # Show preview
                st.write("---")
                upload_manager.create_data_preview_section(uploaded_data)
                
                # Show summary
                st.write("---")
                ready = upload_manager.create_upload_summary(uploaded_data)
                
                if ready:
                    st.success("🎉 All data sources are valid and ready for processing!")
                
                return uploaded_data
            else:
                st.warning("⚠️ Some data sources have validation issues. Please fix and re-upload.")
                return {}
    
    return {}