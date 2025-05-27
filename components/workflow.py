"""
Workflow management component for PIT Count application.
Enhanced to handle Excel sheet re-selection and re-processing.
"""

import streamlit as st
from typing import Dict

from components.upload import create_upload_interface
from components.reports import create_reports_interface
from components.dashboard import create_dashboard_interface
from components.download import create_download_interface
from core.calculator import create_calculation_interface
from core.duplication import create_duplication_interface
from components.validation import create_validation_interface
from config.mappings import ColumnMappings
from utils.session import SessionManager

def create_workflow_interface():
    """Create the main workflow interface based on current step."""
    
    current_step = SessionManager.get_current_step()
    
    # Handle legacy steps by redirecting
    if current_step == 'process':
        SessionManager.update_current_step('validation')
        st.rerun()
    elif current_step == 'calculate':
        SessionManager.update_current_step('reports')
        st.rerun()
    
    # Show progress indicator with navigation
    _show_progress_indicator_with_navigation(current_step)
    
    # Route to appropriate interface
    if current_step == 'upload':
        _handle_upload_step()
    
    elif current_step == 'validation':
        _handle_validation_step()
    
    elif current_step == 'reports':
        _handle_reports_step()
    
    elif current_step == 'download':
        _handle_download_step()
    
    else:
        st.error(f"Unknown step: {current_step}")
        if st.button("Reset to Upload"):
            SessionManager.update_current_step('upload')
            st.rerun()


def _show_progress_indicator_with_navigation(current_step: str):
    """Show progress indicator with clickable navigation."""
    
    steps = ['upload', 'validation', 'reports', 'download']
    step_names = ['Data Upload', 'Validation & Duplication', 'View Reports', 'Download Results']
    step_icons = ['📁', '🔍', '📈', '📥']
    
    # Create navigation buttons
    cols = st.columns(len(steps))
    
    for idx, (step, name, icon) in enumerate(zip(steps, step_names, step_icons)):
        with cols[idx]:
            # Determine button state
            is_current = step == current_step
            
            # Check if step has been completed or data is available
            has_data = False
            if step == 'upload':
                has_data = True  # Always accessible
            elif step == 'validation':
                has_data = SessionManager.has_uploaded_data()
            elif step == 'reports' or step == 'download':
                has_data = SessionManager.has_calculated_reports()
            
            # Style button based on state
            if is_current:
                button_type = "primary"
                help_text = "You are here"
            elif has_data:
                button_type = "secondary"
                help_text = f"Go to {name}"
            else:
                button_type = "secondary"
                help_text = f"Complete previous steps to access {name}"
            
            # Create button - but disable navigation during certain operations
            button_disabled = not has_data
            
            # Check if we're in a verification state
            if 'show_verification' in st.session_state:
                for key in st.session_state:
                    if key.startswith('show_verification_') and st.session_state[key]:
                        button_disabled = True  # Disable navigation during verification
                        break
            
            if st.button(
                f"{icon}\n{name}",
                key=f"nav_{step}",
                type=button_type,
                use_container_width=True,
                disabled=button_disabled,
                help=help_text
            ):
                if has_data and not button_disabled:
                    SessionManager.update_current_step(step)
                    st.rerun()
    
    # Show current progress
    if current_step in steps:
        current_index = steps.index(current_step)
        progress = (current_index + 1) / len(steps)
        st.progress(progress, text=f"Step {current_index + 1} of {len(steps)}: {step_names[current_index]}")


def _handle_upload_step():
    """Handle the upload step of the workflow."""
    
    region = SessionManager.get_session_value('region')
    expected_columns = list(ColumnMappings.get_mapping_for_region(region).keys())
    
    # Check for existing uploaded data
    existing_uploaded_data = SessionManager.get_session_value('uploaded_data', {})
    existing_processed_data = SessionManager.get_session_value('processed_data', {})
    
    # Check if we need to force reprocess due to sheet change
    force_reprocess = SessionManager.get_session_value('force_reprocess', False)
    
    # Create upload interface (it will handle existing data display)
    uploaded_data = create_upload_interface(region, expected_columns)
    
    # If data was just uploaded and we don't have processed data yet, or if force reprocess
    if uploaded_data and (not existing_processed_data or force_reprocess):
        with st.spinner("🔄 Processing your data..."):
            from core.data_processor import DataProcessor
            processor = DataProcessor(region)
            processed_data = processor.process_all_sources(uploaded_data)
            
            if processed_data:
                SessionManager.set_session_value('processed_data', processed_data)
                SessionManager.set_session_value('force_reprocess', False)
                # Clear calculated reports as data has changed
                SessionManager.set_session_value('calculated_reports', {})
                st.success("✅ Data processed successfully!")
                st.balloons()
                # Auto-navigate to validation
                SessionManager.update_current_step('validation')
                st.rerun()
    
    # If we have existing data, show navigation options
    elif existing_uploaded_data and existing_processed_data and not force_reprocess:
        _create_navigation_buttons(
            next_step='validation',
            next_enabled=True
        )


def _handle_validation_step():
    """Handle the validation and duplication step."""
    
    uploaded_data = SessionManager.get_session_value('uploaded_data', {})
    processed_data = SessionManager.get_session_value('processed_data', {})
    region = SessionManager.get_session_value('region')
    
    if not uploaded_data:
        st.error("No uploaded data found.")
        _create_navigation_buttons(previous_step='upload')
        return
    
    st.header("🔍 Data Validation & Duplication Detection")
    
    # Merged validation and duplication in tabs
    tab1, tab2 = st.tabs(["🔍 Duplication Detection", "✅ Data Validation"])
    
    with tab1:
        create_duplication_interface(uploaded_data)
    
    with tab2:
        create_validation_interface(uploaded_data, region)
    
    # Check if we need to calculate statistics
    if processed_data and not SessionManager.has_calculated_reports():
        if st.button("📊 Generate Reports", type="primary", use_container_width=True):
            with st.spinner("🔄 Calculating statistics and generating reports..."):
                from core.calculator import StatisticsCalculator
                calculator = StatisticsCalculator(processed_data)
                calculated_reports = calculator.generate_all_reports()
                
                if calculated_reports:
                    SessionManager.set_session_value('calculated_reports', calculated_reports)
                    st.success("✅ Reports generated successfully!")
                    st.balloons()
                    # Auto-navigate to reports
                    SessionManager.update_current_step('reports')
                    st.rerun()
    else:
        # Navigation - go to reports if already calculated
        _create_navigation_buttons(
            previous_step='upload',
            next_step='reports',
            next_enabled=SessionManager.has_calculated_reports()
        )


def _handle_reports_step():
    """Handle the reports step of the workflow - SIMPLIFIED without tabs."""
    
    if not SessionManager.has_calculated_reports():
        st.error("No reports available. Please calculate reports first.")
        _create_navigation_buttons(previous_step='validation')
        return
    
    # IMPORTANT: Just show reports, no tabs here
    st.header("📊 View Reports")
    
    # Only the reports interface
    create_reports_interface()
    
    # Simple navigation at the bottom
    st.write("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Back to Validation", type="secondary", use_container_width=True):
            SessionManager.update_current_step('validation')
            st.rerun()
    
    with col2:
        st.info("💡 Click on values in the reports above to verify them against raw data")
    
    with col3:
        if st.button("Continue to Download →", type="primary", use_container_width=True):
            SessionManager.update_current_step('download')
            st.rerun()


def _handle_download_step():
    """Handle the download step of the workflow."""
    
    if not SessionManager.has_calculated_reports():
        st.error("No reports available for download.")
        _create_navigation_buttons(previous_step='reports')
        return
    
    st.header("📥 Download Results")
    
    # Create tabs for download, dashboard, etc.
    tab1, tab2 = st.tabs(["📥 Download Reports", "📈 Interactive Dashboard"])
    
    with tab1:
        create_download_interface()
    
    with tab2:
        create_dashboard_interface()
    
    # Navigation - at the end, only back button
    _create_navigation_buttons(
        previous_step='reports'
    )


def _create_navigation_buttons(previous_step: str = None, next_step: str = None, 
                             next_enabled: bool = True, previous_enabled: bool = True):
    """Create consistent navigation buttons at the bottom of each step."""
    st.write("---")
    
    # Determine number of columns based on available navigation options
    nav_cols = []
    if previous_step:
        nav_cols.append("previous")
    nav_cols.append("center")  # For status or action buttons
    if next_step:
        nav_cols.append("next")
    
    cols = st.columns(len(nav_cols))
    col_index = 0
    
    # Previous button
    if previous_step:
        with cols[col_index]:
            step_names = {
                'upload': '📁 Upload',
                'validation': '🔍 Validation',
                'reports': '📈 Reports',
                'download': '📥 Download'
            }
            if st.button(
                f"← Back to {step_names.get(previous_step, previous_step)}", 
                type="secondary", 
                use_container_width=True,
                disabled=not previous_enabled
            ):
                SessionManager.update_current_step(previous_step)
                st.rerun()
        col_index += 1
    
    # Center column for status or special actions
    with cols[col_index]:
        # This can be used for status messages or additional actions
        st.empty()
    col_index += 1
    
    # Next button
    if next_step:
        with cols[col_index]:
            step_names = {
                'upload': '📁 Upload',
                'validation': '🔍 Validation',
                'reports': '📈 Reports',
                'download': '📥 Download'
            }
            if st.button(
                f"Continue to {step_names.get(next_step, next_step)} →", 
                type="primary", 
                use_container_width=True,
                disabled=not next_enabled
            ):
                SessionManager.update_current_step(next_step)
                st.rerun()