"""
PIT Count Application - Main Entry Point
Simplified version maintaining all original functionality
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)

# Import our modules
from config import REGIONS
from processor import process_pit_data, detect_duplicates, validate_data
from reports import generate_all_reports
from components import (
    show_upload_interface, show_validation_interface,
    show_reports_interface, show_download_interface,
    show_combine_interface, show_dv_summation_interface
)
from utils import (
    init_session_state, create_header, create_footer,
    get_current_timestamp, get_timezone_for_region, safe_dataframe_display
)

def main():
    """Main application function"""
    
    # Configure Streamlit page
    st.set_page_config(
        page_title="PIT Count Application",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    init_session_state()
    
    try:
        if 'region' not in st.session_state:
            st.session_state['region'] = None

        create_header()

        step = st.session_state.get('current_step', 'upload')
        show_progress_navigation(step)
        if step == 'upload':
            handle_upload_step()
        elif step == 'validation':
            handle_validation_step()
        elif step == 'reports':
            handle_reports_step()
        elif step == 'download':
            handle_download_step()
        elif step == 'combine':
            handle_combine_step()
        elif step == 'dv_sum':
            handle_dv_sum_step()

        create_footer()
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        
        with st.expander("🔍 Error Details"):
            st.exception(e)
        
        if st.button("🔄 Reset Application", type="primary"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

def show_progress_navigation(current_step):
    """Show progress indicator with clickable navigation"""

    steps = ['upload', 'validation', 'reports', 'download', 'combine', 'dv_sum']
    step_names = ['Data Upload', 'Validation & Duplication', 'View Reports', 'Download Results', 'Combine Data', 'DV Summation']
    step_icons = ['📁', '🔍', '📈', '📥', '🔗', '➕']
    
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
                has_data = bool(st.session_state.get('uploaded_data'))
            elif step == 'reports' or step == 'download':
                has_data = bool(st.session_state.get('calculated_reports'))
            elif step == 'combine':
                has_data = True  # Always accessible - independent tool
            elif step == 'dv_sum':
                has_data = True  # Always accessible - independent tool
            
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
            
            # Create button
            button_disabled = not has_data
            
            if st.button(
                f"{icon}\n{name}",
                key=f"nav_{step}",
                type=button_type,
                width='stretch',
                disabled=button_disabled,
                help=help_text
            ):
                if has_data and not button_disabled:
                    st.session_state['current_step'] = step
                    st.rerun()
    
    # Show current progress
    if current_step in steps:
        current_index = steps.index(current_step)
        progress = (current_index + 1) / len(steps)
        st.progress(progress, text=f"Step {current_index + 1} of {len(steps)}: {step_names[current_index]}")

def handle_upload_step():
    """Handle the upload step"""
    current_region = st.session_state.get('region')
    if current_region is None or current_region == 'Unknown':
        st.warning("⚠️ Region not detected. Please select your region manually:")
        selected_region = st.selectbox(
            "Select Region:",
            REGIONS,
            help="Select the region that matches your data format"
        )
        if st.button("✅ Set Region and Continue", type="primary"):
            st.session_state['region'] = selected_region
            if selected_region == 'New England':
                st.session_state['timezone'] = 'America/New_York'
            else:
                st.session_state['timezone'] = 'America/Chicago'
            st.success(f"✅ Region set to: {selected_region}")
            st.rerun()
        return

    existing_data = st.session_state.get('uploaded_data', {})

    if existing_data:
        show_existing_data_summary(existing_data)

        st.warning("⚠️ Uploading new files will replace the existing data.")
        if st.button("🔄 Upload New Data", type="secondary"):
            # Clear all data and caches
            st.session_state['uploaded_data'] = {}
            st.session_state['processed_data'] = {}
            st.session_state['calculated_reports'] = {}
            # Clear Excel file cache to free memory
            st.session_state['excel_files'] = {}
            st.session_state['temp_files'] = {}
            st.rerun()

        show_navigation_buttons(next_step='validation')
    else:
        uploaded_data = show_upload_interface()

        if uploaded_data:
            st.session_state['uploaded_data'] = uploaded_data

            with st.spinner("🔄 Processing your data..."):
                processed_data = process_all_sources(uploaded_data)
                st.session_state['processed_data'] = processed_data

                st.success("✅ Data processed successfully!")
                st.balloons()

                st.session_state['current_step'] = 'validation'
                st.rerun()

def show_existing_data_summary(data_dict):
    """Show summary of existing uploaded data"""
    st.success(f"✅ You have {len(data_dict)} data source(s) already uploaded.")

    col1, col2, col3 = st.columns(3)
    total_rows = sum(len(df) for df in data_dict.values())

    with col1:
        st.metric("Data Sources", len(data_dict))
    with col2:
        st.metric("Total Households", f"{total_rows:,}")
    with col3:
        st.metric("Status", "✅ Ready")

    st.subheader("📊 Current Data")

    for source_name, df in data_dict.items():
        st.write(f"### {source_name} - {len(df)} rows")
        df_safe = safe_dataframe_display(df.head(20))
        st.dataframe(df_safe, width='stretch')
        st.write("---")

def process_all_sources(uploaded_data):
    """Process all uploaded data sources with progress tracking"""
    processed = {}
    region = st.session_state.get('region')

    if not region:
        st.error("Region not set. Please log in again.")
        return {}

    total_sources = len(uploaded_data)
    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, (source_name, df) in enumerate(uploaded_data.items(), 1):
        progress_pct = idx / total_sources
        progress_bar.progress(progress_pct)
        status_text.text(f"Processing {source_name}... ({idx}/{total_sources})")

        source_data = process_pit_data(df, source_name, region)
        processed[source_name] = source_data

    progress_bar.empty()
    status_text.empty()

    all_persons = []
    all_households = []

    for source_name, source_data in processed.items():
        if not isinstance(source_data, dict):
            st.warning(f"Skipping {source_name}: Invalid data structure")
            continue

        persons_df = source_data.get('persons_df')
        households_df = source_data.get('households_df')

        if persons_df is not None and not persons_df.empty:
            all_persons.append(persons_df)
        if households_df is not None and not households_df.empty:
            all_households.append(households_df)

    if all_persons:
        combined_persons = pd.concat(all_persons, ignore_index=True)
        combined_households = pd.concat(all_households, ignore_index=True)
    else:
        combined_persons = pd.DataFrame()
        combined_households = pd.DataFrame()

    processed['combined'] = {
        'persons_df': combined_persons,
        'households_df': combined_households
    }

    return processed

def handle_validation_step():
    """Handle the validation step"""
    uploaded_data = st.session_state.get('uploaded_data', {})
    processed_data = st.session_state.get('processed_data', {})
    
    if not uploaded_data:
        st.error("No uploaded data found.")
        show_navigation_buttons(previous_step='upload')
        return
    
    st.header("🔍 Data Validation & Duplication Detection")
    
    # Show validation interface
    show_validation_interface(uploaded_data, processed_data)
    
    # Check if we need to calculate statistics
    if processed_data and not st.session_state.get('calculated_reports'):
        if st.button("📊 Generate Reports", type="primary", width='stretch'):
            with st.spinner("🔄 Calculating statistics and generating reports..."):
                calculated_reports = generate_all_reports(processed_data)
                
                if calculated_reports:
                    st.session_state['calculated_reports'] = calculated_reports
                    st.success("✅ Reports generated successfully!")
                    st.balloons()
                    
                    # Auto-navigate to reports
                    st.session_state['current_step'] = 'reports'
                    st.rerun()
    else:
        # Navigation
        show_navigation_buttons(
            previous_step='upload',
            next_step='reports',
            next_enabled=bool(st.session_state.get('calculated_reports'))
        )

def handle_reports_step():
    """Handle the reports step"""
    if not st.session_state.get('calculated_reports'):
        st.error("No reports available. Please calculate reports first.")
        show_navigation_buttons(previous_step='validation')
        return
    
    st.header("📊 View Reports")
    
    # Show reports interface
    show_reports_interface()
    
    # Navigation
    show_navigation_buttons(
        previous_step='validation',
        next_step='download'
    )

def handle_download_step():
    """Handle the download step"""
    if not st.session_state.get('calculated_reports'):
        st.error("No reports available for download.")
        show_navigation_buttons(previous_step='reports')
        return

    st.header("Download Results")

    # Show download interface
    show_download_interface()

    # Navigation - back and next to combine
    show_navigation_buttons(previous_step='reports', next_step='combine')


def handle_combine_step():
    """Handle the combine data step - independent of other workflow steps"""
    st.header("Combine Data")

    # Show combine interface
    show_combine_interface()

    # Navigation - back and next to dv_sum
    show_navigation_buttons(previous_step='download', next_step='dv_sum')


def handle_dv_sum_step():
    """Handle the DV summation step - independent of other workflow steps"""
    st.header("DV Data Summation")

    # Show DV summation interface
    show_dv_summation_interface()

    # Navigation - only back button (no next step)
    show_navigation_buttons(previous_step='combine')


def show_navigation_buttons(previous_step=None, next_step=None, next_enabled=True):
    """Show navigation buttons"""
    st.write("---")
    
    cols = []
    if previous_step:
        cols.append("previous")
    cols.append("center")
    if next_step:
        cols.append("next")
    
    columns = st.columns(len(cols))
    col_index = 0
    
    # Previous button
    if previous_step:
        with columns[col_index]:
            step_names = {
                'upload': 'Upload',
                'validation': 'Validation',
                'reports': 'Reports',
                'download': 'Download',
                'combine': 'Combine',
                'dv_sum': 'DV Summation'
            }
            if st.button(
                f"Back to {step_names.get(previous_step, previous_step)}",
                type="secondary",
                width='stretch'
            ):
                st.session_state['current_step'] = previous_step
                st.rerun()
        col_index += 1

    # Center column
    with columns[col_index]:
        st.empty()
    col_index += 1

    # Next button
    if next_step:
        with columns[col_index]:
            step_names = {
                'upload': 'Upload',
                'validation': 'Validation',
                'reports': 'Reports',
                'download': 'Download',
                'combine': 'Combine',
                'dv_sum': 'DV Summation'
            }
            if st.button(
                f"Continue to {step_names.get(next_step, next_step)}",
                type="primary",
                width='stretch',
                disabled=not next_enabled
            ):
                st.session_state['current_step'] = next_step
                st.rerun()

if __name__ == "__main__":
    main()