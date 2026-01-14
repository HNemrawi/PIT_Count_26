"""
UI Components module for PIT Count Application
Contains all interface components for upload, validation, reports, and download
"""

import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from typing import Dict, List, Optional, Tuple
from openpyxl.utils import get_column_letter
from openpyxl.styles import NamedStyle, Font, Alignment, PatternFill


from config import VALID_AGE_RANGES, VALID_GENDERS, VALID_RACES
from processor import detect_duplicates, validate_data, map_name_columns_for_duplication
from utils import get_timezone_for_region, create_download_filename, get_current_timestamp, safe_dataframe_display

def show_upload_interface():
    """Show the data upload interface"""
    region = st.session_state.get('region')

    # Store files in session state if not already there
    if 'temp_files' not in st.session_state:
        st.session_state['temp_files'] = {}
    
    uploaded_data = {}
    
    st.write(f"**Selected Region:** {region}")
    st.write("---")
    
    # Emergency Shelter
    st.subheader("📁 Emergency Shelter (ES) Data")
    es_file = st.file_uploader(
        "Choose Emergency Shelter file",
        type=['csv', 'xlsx'],
        key="es_upload"
    )
    
    if es_file:
        if es_file.name.endswith('.xlsx'):
            # Store file in session state
            st.session_state['temp_files']['es'] = es_file
            
            # Read Excel file to get sheet names
            try:
                excel_file = pd.ExcelFile(es_file)
                sheet_names = excel_file.sheet_names
                
                if len(sheet_names) > 1:
                    selected_sheet = st.selectbox(
                        "Select sheet for Emergency Shelter data:",
                        sheet_names,
                        key="es_sheet_select"
                    )
                else:
                    selected_sheet = sheet_names[0]
                
                # Show preview
                if st.button("Preview ES Data", key="preview_es"):
                    preview_df = pd.read_excel(es_file, sheet_name=selected_sheet, nrows=10, engine='openpyxl')
                    preview_df_safe = safe_dataframe_display(preview_df)
                    st.dataframe(preview_df_safe, width='stretch')
                    
            except Exception as e:
                st.error(f"Error reading Excel file: {str(e)}")
        else:
            # CSV file - no sheet selection needed
            st.session_state['temp_files']['es'] = es_file
    
    st.write("---")
    
    # Transitional Housing
    st.subheader("📁 Transitional Housing (TH) Data")
    th_file = st.file_uploader(
        "Choose Transitional Housing file",
        type=['csv', 'xlsx'],
        key="th_upload"
    )
    
    if th_file:
        if th_file.name.endswith('.xlsx'):
            st.session_state['temp_files']['th'] = th_file
            
            try:
                excel_file = pd.ExcelFile(th_file)
                sheet_names = excel_file.sheet_names
                
                if len(sheet_names) > 1:
                    selected_sheet = st.selectbox(
                        "Select sheet for Transitional Housing data:",
                        sheet_names,
                        key="th_sheet_select"
                    )
                else:
                    selected_sheet = sheet_names[0]
                
                if st.button("Preview TH Data", key="preview_th"):
                    preview_df = pd.read_excel(th_file, sheet_name=selected_sheet, nrows=10, engine='openpyxl')
                    preview_df_safe = safe_dataframe_display(preview_df)
                    st.dataframe(preview_df_safe, width='stretch')
                    
            except Exception as e:
                st.error(f"Error reading Excel file: {str(e)}")
        else:
            st.session_state['temp_files']['th'] = th_file
    
    st.write("---")
    
    # Unsheltered
    st.subheader("📁 Unsheltered Data")
    unsheltered_file = st.file_uploader(
        "Choose Unsheltered file",
        type=['csv', 'xlsx'],
        key="unsheltered_upload"
    )
    
    if unsheltered_file:
        if unsheltered_file.name.endswith('.xlsx'):
            st.session_state['temp_files']['unsheltered'] = unsheltered_file
            
            try:
                excel_file = pd.ExcelFile(unsheltered_file)
                sheet_names = excel_file.sheet_names
                
                if len(sheet_names) > 1:
                    selected_sheet = st.selectbox(
                        "Select sheet for Unsheltered data:",
                        sheet_names,
                        key="unsheltered_sheet_select"
                    )
                else:
                    selected_sheet = sheet_names[0]
                
                if st.button("Preview Unsheltered Data", key="preview_unsheltered"):
                    preview_df = pd.read_excel(unsheltered_file, sheet_name=selected_sheet, nrows=10, engine='openpyxl')
                    preview_df_safe = safe_dataframe_display(preview_df)
                    st.dataframe(preview_df_safe, width='stretch')
                    
            except Exception as e:
                st.error(f"Error reading Excel file: {str(e)}")
        else:
            st.session_state['temp_files']['unsheltered'] = unsheltered_file

    st.write("---")

    # Process button
    if st.button("🔄 Process Uploaded Files", type="primary", width='stretch'):
        # Process files with selected sheets
        files_to_process = st.session_state.get('temp_files', {})
        
        if files_to_process:
            with st.spinner("Processing files..."):
                # Process ES file
                if 'es' in files_to_process:
                    es_file = files_to_process['es']
                    if es_file.name.endswith('.xlsx') and 'es_sheet_select' in st.session_state:
                        es_df = pd.read_excel(es_file, sheet_name=st.session_state['es_sheet_select'], engine='openpyxl')
                    else:
                        es_df = load_file_direct(es_file)
                    
                    if es_df is not None:
                        uploaded_data["Sheltered_ES"] = es_df
                        st.success(f"✅ ES data: {len(es_df)} rows")
                
                # Process TH file
                if 'th' in files_to_process:
                    th_file = files_to_process['th']
                    if th_file.name.endswith('.xlsx') and 'th_sheet_select' in st.session_state:
                        th_df = pd.read_excel(th_file, sheet_name=st.session_state['th_sheet_select'], engine='openpyxl')
                    else:
                        th_df = load_file_direct(th_file)
                    
                    if th_df is not None:
                        uploaded_data["Sheltered_TH"] = th_df
                        st.success(f"✅ TH data: {len(th_df)} rows")
                
                # Process Unsheltered file
                if 'unsheltered' in files_to_process:
                    unsheltered_file = files_to_process['unsheltered']
                    if unsheltered_file.name.endswith('.xlsx') and 'unsheltered_sheet_select' in st.session_state:
                        unsheltered_df = pd.read_excel(unsheltered_file, sheet_name=st.session_state['unsheltered_sheet_select'], engine='openpyxl')
                    else:
                        unsheltered_df = load_file_direct(unsheltered_file)

                    if unsheltered_df is not None:
                        uploaded_data["Unsheltered"] = unsheltered_df
                        st.success(f"✅ Unsheltered data: {len(unsheltered_df)} rows")

            if uploaded_data:
                # Validate data
                valid_data = {}
                for source_name, df in uploaded_data.items():
                    # Clean data
                    df.columns = df.columns.str.strip()
                    df = df.loc[:, ~df.columns.duplicated(keep='first')]
                    
                    # Remove rows without timestamps
                    if 'Timestamp' in df.columns:
                        initial_count = len(df)
                        df = df.dropna(subset=['Timestamp'])
                        dropped = initial_count - len(df)
                        if dropped > 0:
                            st.info(f"{source_name}: Removed {dropped} rows with missing timestamps")
                    
                    # Check essential columns
                    essential = ['Timestamp', 'Gender', 'Race/Ethnicity', 'Age Range']
                    missing = set(essential) - set(df.columns)
                    
                    if missing:
                        st.error(f"❌ {source_name}: Missing columns: {', '.join(missing)}")
                    else:
                        valid_data[source_name] = df
                
                if valid_data:
                    # Clear temp files
                    st.session_state['temp_files'] = {}
                    st.session_state['uploaded_data'] = valid_data
                    return valid_data
                else:
                    st.error("Please fix the issues with your data and try again.")
        else:
            st.info("Please upload at least one data file to continue.")
    
    return {}

def load_file_direct(uploaded_file):
    """Load a file directly without sheet selection (optimized for performance)"""
    try:
        if uploaded_file.name.endswith('.csv'):
            # Use faster CSV reading with low_memory=False for mixed types
            return pd.read_csv(uploaded_file, low_memory=False)
        elif uploaded_file.name.endswith('.xlsx'):
            # Use openpyxl engine explicitly (faster than default)
            return pd.read_excel(uploaded_file, engine='openpyxl')
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

def load_file(uploaded_file):
    """Load a file into a dataframe (optimized for performance)"""
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file, low_memory=False)
        elif uploaded_file.name.endswith('.xlsx'):
            # Handle multiple sheets with optimized engine
            excel_file = pd.ExcelFile(uploaded_file, engine='openpyxl')
            if len(excel_file.sheet_names) > 1:
                sheet_name = st.selectbox(
                    f"Select sheet from {uploaded_file.name}",
                    excel_file.sheet_names
                )
                return pd.read_excel(uploaded_file, sheet_name=sheet_name, engine='openpyxl')
            else:
                return pd.read_excel(uploaded_file, engine='openpyxl')
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

def show_validation_interface(uploaded_data, processed_data):
    """Show the validation and duplication detection interface"""
    region = st.session_state.get('region')
    
    # Create tabs
    tab1, tab2 = st.tabs(["🔍 Duplication Detection", "✅ Data Validation"])
    
    with tab1:
        show_duplication_interface(uploaded_data, region)
    
    with tab2:
        show_data_validation_interface(uploaded_data, region)

def show_duplication_interface(uploaded_data, region):
    """Show duplication detection interface"""
    st.subheader("🔍 Duplication Detection")
    
    with st.expander("ℹ️ How Duplication Detection Works", expanded=False):
        st.markdown(f"""
        ### Detection Logic (Current Region: {region})

        The system uses **region-specific hierarchical matching** to identify potential duplicates.
        Higher priority rules override lower ones - if a pair matches a "Likely" condition,
        it won't be downgraded even if it also matches "Somewhat Likely" or "Possible" conditions.

        ---

        ### New England Rules
        *Uses 3-letter name codes: 1st letter of first name + 1st & 3rd letters of last name*

        | Color | Confidence Level | Matching Conditions |
        |-------|-----------------|---------------------|
        | 🔴 | **Likely Duplicate** | Full Name (3-letter code) + DOB match |
        | 🟠 | **Somewhat Likely** | Full Name (3-letter code) + Age match |
        | 🟡 | **Possible Duplicate** | Full Name (3-letter code) + Age Range match |
        | 🟣 | **No Name Info** | Record has no name information (not matched) |

        **Name Format Example:** "John Smith" → "JSI" (J + S + I, where I is 3rd letter of Smith)

        ---

        ### Great Lakes Rules
        *Uses full names (First Name + Last Name) and initials*

        | Color | Confidence Level | Matching Conditions |
        |-------|-----------------|---------------------|
        | 🔴 | **Likely Duplicate** | Full Name + DOB match |
        | 🔴 | **Likely Duplicate** | Full Name + Age match |
        | 🔴 | **Likely Duplicate** | Initials + DOB match |
        | 🟠 | **Somewhat Likely** | Full Name + Age Range match |
        | 🟠 | **Somewhat Likely** | Initials + Age match |
        | 🟡 | **Possible Duplicate** | Initials + Age Range match |
        | 🟣 | **No Name Info** | Record has no name information (not matched) |

        **Name Format Example:** "John Smith" → Full name: "JOHN SMITH", Initials: "JS"

        ---

        ### Key Differences Between Regions

        | Feature | New England | Great Lakes |
        |---------|-------------|-------------|
        | Name Format | 3-letter code | Full names |
        | Initials Matching | Not used | Used for all confidence levels |
        | Full Name + Age | Somewhat Likely | Likely |
        | Matching Strictness | More strict (fewer rules) | More comprehensive (more rules) |

        ---

        ### Important Notes

        - **Hierarchy Enforcement**: Higher confidence matches prevent downgrading to lower confidence
        - **No Name Records**: Records without name information are flagged with 🟣 but not compared
        - **Heads of Household**: Comparison focuses on heads of household information
        - **Data Priority**: DOB is preferred over Age; Age is preferred over Age Range

        ### Excel Export

        - Color-coded rows (red/orange/yellow/purple)
        - "Duplicates_With" column shows Excel row numbers (starting at row 2)
        - "Duplication_Reason" explains why records matched
        """)
    
    if st.button("🚀 Run Duplication Detection", type="primary"):
        with st.spinner("Analyzing records..."):
            results = {}

            for source_name, df in uploaded_data.items():
                # Map name columns before detection to ensure standardized format
                df_with_mapped_names = map_name_columns_for_duplication(df, region)
                annotated = detect_duplicates(df_with_mapped_names, source_name, region)
                results[source_name] = annotated

            st.session_state['dup_results'] = results
            st.success("✅ Detection complete!")
    
    # Display results
    if 'dup_results' in st.session_state:
        for source_name, annotated in st.session_state['dup_results'].items():
            st.subheader(f"📊 Results: {source_name}")
            
            # Summary stats
            total = len(annotated)
            likely = (annotated['Duplication_Score'].str.contains('Likely Duplicate 🔴', na=False)).sum()
            somewhat = (annotated['Duplication_Score'].str.contains('Somewhat Likely', na=False)).sum()
            possible = (annotated['Duplication_Score'].str.contains('Possible', na=False)).sum()
            no_name = (annotated['Duplication_Score'].str.contains('No name', na=False)).sum()
            not_duplicate = (annotated['Duplication_Score'] == 'Not Duplicate').sum()
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Total", f"{total:,}")
            with col2:
                st.metric("🔴 Likely", likely)
            with col3:
                st.metric("🟠 Somewhat", somewhat)
            with col4:
                st.metric("🟡 Possible", possible)
            with col5:
                st.metric("🟣 No Name", no_name)
            
            # Summary message
            total_flagged = total - not_duplicate
            flagged_pct = (total_flagged / total * 100) if total > 0 else 0
            st.info(f"""
            **Summary**: {total_flagged} records ({flagged_pct:.1f}%) 
            flagged for review out of {total:,} total records.
            """)
            
            # Important note about indices
            st.warning("""
            **📌 Index Reference:**
            - **In this table**: `Duplicates_With` shows zero-based indices (0, 1, 2...)
            - **In Excel download**: Indices are adjusted to match Excel row numbers (2, 3, 4...)
            """)
            
            # Show data
            from utils import safe_dataframe_display
            st.dataframe(safe_dataframe_display(annotated), width='stretch', height=400)
            
            # Download buttons
            col1, col2 = st.columns(2)
            
            with col1:
                # CSV download
                csv_data = annotated.to_csv(index=False)
                st.download_button(
                    "📥 Download CSV",
                    data=csv_data,
                    file_name=f"{source_name}_duplicates.csv",
                    mime="text/csv",
                    key=f"dup_csv_{source_name}"
                )
            
            with col2:
                # Excel download with highlights
                from processor import DuplicationDetector
                # Create a new detector instance to generate Excel
                detector = DuplicationDetector(uploaded_data[source_name], source_name, region)
                excel_buffer = detector.create_excel_with_highlights(annotated)
                
                st.download_button(
                    "📥 Download Excel (with highlights)",
                    data=excel_buffer.getvalue(),
                    file_name=f"{source_name}_duplicates.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"dup_excel_{source_name}",
                    help="Download color-coded Excel file with adjusted row numbers"
                )

def show_data_validation_interface(uploaded_data, region):
    """Show data validation interface"""
    st.subheader("✅ Data Validation")

    with st.expander("ℹ️ About Data Validation", expanded=False):
        st.markdown("""
        ### Validation Rules

        The system validates the following data fields:

        #### 🔢 Age Range (Single-Select)
        - **Valid Values**: Under 18, 18-24, 25-34, 35-44, 45-54, 55-64, 65+
        - **Applies To**: All age range columns (HOH + additional adults)
        - **Empty Values**: Allowed (skipped in validation)

        #### 👤 Sex (Single-Select, Required)
        - **Valid Values**: Male, Female
        - **Applies To**: All sex columns (HOH + additional adults + children)
        - **Empty Values**: Flagged as invalid

        #### 🎭 Gender (Multi-Select, Optional)
        - **Valid Values**: Man, Woman, Non-Binary, Transgender, Questioning, Different Identity
        - **Applies To**: All gender columns (HOH + additional adults + children)
        - **Format**: Comma-separated for multiple selections (e.g., "Woman, Transgender")
        - **Empty Values**: Allowed (optional field)
        - **Note**: Gender columns may not exist in all datasets - this is acceptable

        #### 🌍 Race/Ethnicity (Multi-Select)
        - **Valid Values**:
          - American Indian, Alaska Native, or Indigenous
          - Asian or Asian American
          - Black, African American, or African
          - Hispanic/Latina/e/o
          - Middle Eastern or North African
          - Native Hawaiian or Pacific Islander
          - White
          - Client Doesn't Know
          - Client Prefers Not to Answer
          - Data Not Collected
        - **Format**: Comma-separated for multiple selections
        - **Empty Values**: Allowed (skipped in validation)

        ### How Validation Works

        1. **Run Validation** button scans all uploaded data sources
        2. Invalid entries are flagged with their Excel row numbers
        3. Results show the invalid value and list of valid options
        4. Download options available for each issue type and complete reports

        ### What Gets Flagged

        - **Typos**: "Mal" instead of "Male"
        - **Extra Spaces**: " Male " with leading/trailing spaces
        - **Wrong Format**: "Male,Female" in a single-select field
        - **Invalid Options**: Values not in the approved list
        - **Required Fields**: Missing sex values (when column exists)
        """)

    st.info("Click **Run Validation** to check all uploaded data for invalid entries.")

    
    if st.button("🔍 Run Validation", type="primary", key="validate_btn"):
        all_results = {}
        
        for source_name, df in uploaded_data.items():
            with st.spinner(f"Validating {source_name}..."):
                validation_results = validate_data(df, source_name, region)
                if validation_results:
                    all_results[source_name] = validation_results
        
        st.session_state['validation_results'] = all_results
        
        if all_results:
            st.warning("⚠️ Validation issues found!")
        else:
            st.success("✅ All data is valid!")
    
    # Display results
    if 'validation_results' in st.session_state:
        results = st.session_state['validation_results']
        
        if not results:
            st.success("✅ No validation issues found!")
            return
        
        # Create comprehensive summary metrics
        total_issues = sum(sum(len(df) for df in source_results.values()) for source_results in results.values())

        # Count by type across all sources
        all_age_issues = sum(len(df) for source_results in results.values()
                            for k, df in source_results.items() if k.startswith('age_'))
        all_sex_issues = sum(len(df) for source_results in results.values()
                            for k, df in source_results.items() if k.startswith('sex_'))
        all_gender_issues = sum(len(df) for source_results in results.values()
                               for k, df in source_results.items() if k.startswith('gender_'))
        all_race_issues = sum(len(df) for source_results in results.values()
                             for k, df in source_results.items() if k.startswith('race_'))

        # Top row metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Issues", f"{total_issues:,}")
        with col2:
            st.metric("Sources with Issues", len(results))
        with col3:
            st.metric("Most Common",
                     "🔢 Age" if all_age_issues >= max(all_sex_issues, all_gender_issues, all_race_issues)
                     else "👤 Sex" if all_sex_issues >= max(all_age_issues, all_gender_issues, all_race_issues)
                     else "🎭 Gender" if all_gender_issues >= max(all_age_issues, all_sex_issues, all_race_issues)
                     else "🌍 Race")
        with col4:
            st.metric("Status", "⚠️ Needs Review")

        # Second row - breakdown by type
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🔢 Age Issues", all_age_issues)
        with col2:
            st.metric("👤 Sex Issues", all_sex_issues)
        with col3:
            st.metric("🎭 Gender Issues", all_gender_issues)
        with col4:
            st.metric("🌍 Race Issues", all_race_issues)

        st.write("---")

        # Download all issues across all sources as Excel
        if total_issues > 0:
            from io import BytesIO
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill, Alignment

            # Create workbook with separate sheets per source
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                for source_name, validation_results in results.items():
                    if validation_results:
                        all_issues_df = pd.concat(validation_results.values(), ignore_index=True)
                        # Sort by Row number for easier navigation
                        all_issues_df = all_issues_df.sort_values('Row')
                        all_issues_df.to_excel(writer, sheet_name=source_name[:31], index=False)

            excel_buffer.seek(0)
            st.download_button(
                "📥 Download All Validation Issues (Excel)",
                data=excel_buffer.getvalue(),
                file_name=f"validation_issues_{region}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_all_validation_excel",
                help="Download all validation issues across all sources as an Excel file"
            )

            st.write("---")
        
        for source_name, validation_results in results.items():
            source_issues = sum(len(df) for df in validation_results.values())

            # Group by type
            age_issues = {k: v for k, v in validation_results.items() if k.startswith('age_')}
            sex_issues = {k: v for k, v in validation_results.items() if k.startswith('sex_')}
            gender_issues = {k: v for k, v in validation_results.items() if k.startswith('gender_')}
            race_issues = {k: v for k, v in validation_results.items() if k.startswith('race_')}

            # Count issues by type for this source
            age_count = sum(len(df) for df in age_issues.values())
            sex_count = sum(len(df) for df in sex_issues.values())
            gender_count = sum(len(df) for df in gender_issues.values())
            race_count = sum(len(df) for df in race_issues.values())

            with st.expander(f"📋 {source_name} - {source_issues} issues", expanded=True):
                # Summary for this source - only show categories that exist in data
                breakdown_lines = [
                    f"- 🔢 Age Range: {age_count} issues",
                    f"- 👤 Sex: {sex_count} issues"
                ]

                # Only show Gender if any Gender columns exist in the dataset
                has_gender_columns = any('Gender' in col for col in uploaded_data[source_name].columns)
                if has_gender_columns:
                    breakdown_lines.append(f"- 🎭 Gender: {gender_count} issues")

                breakdown_lines.append(f"- 🌍 Race/Ethnicity: {race_count} issues")

                st.markdown("**Issue Breakdown:**\n" + "\n".join(breakdown_lines))

                st.write("---")

                # Age Range Issues
                if age_issues:
                    st.write("### 🔢 Age Range Issues")
                    for key, df in age_issues.items():
                        if not df.empty:
                            column_name = df['Column'].iloc[0]
                            st.write(f"**{column_name}** ({len(df)} invalid entries)")

                            # Show detailed table
                            display_df = df[['Row', 'Value', 'Valid_Options']].copy()
                            display_df['Row'] = display_df['Row'].apply(lambda x: f"Row {x}")
                            st.dataframe(display_df, use_container_width=True, height=min(300, len(df) * 35 + 50))

                            # Download option for this specific issue
                            csv = df.to_csv(index=False)
                            st.download_button(
                                f"📥 Download CSV",
                                data=csv,
                                file_name=f"{source_name}_{column_name.replace(' ', '_')}_issues.csv",
                                mime="text/csv",
                                key=f"dl_{source_name}_{key}"
                            )
                            st.write("---")

                # Sex Issues
                if sex_issues:
                    st.write("### 👤 Sex Issues (Required Field)")
                    for key, df in sex_issues.items():
                        if not df.empty:
                            column_name = df['Column'].iloc[0]
                            st.write(f"**{column_name}** ({len(df)} invalid entries)")

                            # Show detailed table
                            display_df = df[['Row', 'Value', 'Invalid_Parts', 'Valid_Options']].copy()
                            display_df['Row'] = display_df['Row'].apply(lambda x: f"Row {x}")
                            st.dataframe(display_df, use_container_width=True, height=min(300, len(df) * 35 + 50))

                            # Download option
                            csv = df.to_csv(index=False)
                            st.download_button(
                                f"📥 Download CSV",
                                data=csv,
                                file_name=f"{source_name}_{column_name.replace(' ', '_')}_issues.csv",
                                mime="text/csv",
                                key=f"dl_{source_name}_{key}"
                            )
                            st.write("---")

                # Gender Issues
                if gender_issues:
                    st.write("### 🎭 Gender Issues (Optional Field)")
                    for key, df in gender_issues.items():
                        if not df.empty:
                            column_name = df['Column'].iloc[0]
                            st.write(f"**{column_name}** ({len(df)} invalid entries)")

                            # Show detailed table
                            display_df = df[['Row', 'Value', 'Invalid_Parts', 'Valid_Options']].copy()
                            display_df['Row'] = display_df['Row'].apply(lambda x: f"Row {x}")
                            st.dataframe(display_df, use_container_width=True, height=min(300, len(df) * 35 + 50))

                            # Download option
                            csv = df.to_csv(index=False)
                            st.download_button(
                                f"📥 Download CSV",
                                data=csv,
                                file_name=f"{source_name}_{column_name.replace(' ', '_')}_issues.csv",
                                mime="text/csv",
                                key=f"dl_{source_name}_{key}"
                            )
                            st.write("---")
                
                # Race/Ethnicity Issues
                if race_issues:
                    st.write("### 🌍 Race/Ethnicity Issues")
                    for key, df in race_issues.items():
                        if not df.empty:
                            column_name = df['Column'].iloc[0]
                            st.write(f"**{column_name}** ({len(df)} invalid entries)")

                            # Show detailed table
                            display_df = df[['Row', 'Value', 'Invalid_Parts', 'Valid_Options']].copy()
                            display_df['Row'] = display_df['Row'].apply(lambda x: f"Row {x}")
                            st.dataframe(display_df, use_container_width=True, height=min(300, len(df) * 35 + 50))

                            # Download option
                            csv = df.to_csv(index=False)
                            st.download_button(
                                f"📥 Download CSV",
                                data=csv,
                                file_name=f"{source_name}_{column_name.replace(' ', '_')}_issues.csv",
                                mime="text/csv",
                                key=f"dl_{source_name}_{key}"
                            )
                            st.write("---")

                # Download all issues for this source
                if source_issues > 0:
                    st.write("### 📦 Download All Issues for This Source")
                    all_issues_df = pd.concat(validation_results.values(), ignore_index=True)
                    # Sort by Row for easier navigation
                    all_issues_df = all_issues_df.sort_values('Row')
                    csv_all = all_issues_df.to_csv(index=False)
                    st.download_button(
                        f"📥 Download ALL {source_name} Issues (CSV)",
                        data=csv_all,
                        file_name=f"{source_name}_all_validation_issues.csv",
                        mime="text/csv",
                        key=f"dl_all_{source_name}",
                        type="primary",
                        use_container_width=True
                    )

def show_report_filters():
    """Show filter interface for reports"""
    uploaded_data = st.session_state.get('uploaded_data', {})

    if not uploaded_data:
        return

    # Collect all unique values from all data sources for filter columns
    filter_columns = ['Project Name on HIC', 'County', 'AHS District']
    available_filters = {}

    for col in filter_columns:
        all_values = set()
        col_exists = False

        for source_name, df in uploaded_data.items():
            if col in df.columns:
                col_exists = True
                # Get unique non-null values
                unique_vals = df[col].dropna().unique()
                all_values.update(unique_vals)

        if col_exists and all_values:
            available_filters[col] = sorted(list(all_values))

    if not available_filters:
        return

    # Show filter UI
    with st.expander("🔍 Filter Reports", expanded=False):
        st.info("Filter the data before viewing reports. Select values to include in the reports.")

        # Initialize filter state if not exists
        if 'report_filters' not in st.session_state:
            st.session_state['report_filters'] = {}

        # Create columns for filters
        num_filters = len(available_filters)
        if num_filters == 1:
            cols = [st.container()]
        elif num_filters == 2:
            cols = st.columns(2)
        else:
            cols = st.columns(3)

        filter_changed = False

        for idx, (col_name, values) in enumerate(available_filters.items()):
            with cols[idx % len(cols)]:
                st.write(f"**{col_name}**")

                # Multiselect for each filter column
                selected = st.multiselect(
                    f"Select {col_name}",
                    options=values,
                    default=st.session_state['report_filters'].get(col_name, []),
                    key=f"filter_{col_name}",
                    label_visibility="collapsed"
                )

                # Check if filter changed
                if selected != st.session_state['report_filters'].get(col_name, []):
                    filter_changed = True

                st.session_state['report_filters'][col_name] = selected

        # Apply filters button
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button("🔄 Apply Filters", type="primary", width='stretch'):
                apply_report_filters()

        with col2:
            if st.button("🔁 Reset Filters", width='stretch'):
                st.session_state['report_filters'] = {}
                apply_report_filters()

        with col3:
            # Show active filters count
            active_count = sum(1 for v in st.session_state['report_filters'].values() if v)
            if active_count > 0:
                st.info(f"**{active_count}** filter(s) active")

def apply_report_filters():
    """Apply filters and regenerate reports"""
    from reports import generate_all_reports

    filters = st.session_state.get('report_filters', {})
    uploaded_data = st.session_state.get('uploaded_data', {})

    # Check if any filters are active
    has_active_filters = any(v for v in filters.values())

    if not has_active_filters:
        # No filters, regenerate from original data
        with st.spinner("Regenerating reports without filters..."):
            processed_data = st.session_state.get('processed_data', {})
            calculated_reports = generate_all_reports(processed_data)
            st.session_state['calculated_reports'] = calculated_reports
            st.success("✅ Filters removed, reports regenerated!")
            st.rerun()
        return

    # Apply filters to uploaded data
    filtered_data = {}

    with st.spinner("Applying filters and regenerating reports..."):
        for source_name, df in uploaded_data.items():
            filtered_df = df.copy()

            # Apply each filter
            for col_name, selected_values in filters.items():
                if selected_values and col_name in filtered_df.columns:
                    filtered_df = filtered_df[filtered_df[col_name].isin(selected_values)]

            # Only include if data remains after filtering
            if not filtered_df.empty:
                filtered_data[source_name] = filtered_df

        if not filtered_data:
            st.error("No data matches the selected filters. Please adjust your filter criteria.")
            return

        # Process filtered data
        from processor import process_pit_data
        region = st.session_state.get('region')

        processed_filtered = {}
        for source_name, df in filtered_data.items():
            source_data = process_pit_data(df, source_name, region)
            processed_filtered[source_name] = source_data

        # Combine data for reporting
        all_persons = []
        all_households = []

        for source_name, source_data in processed_filtered.items():
            persons_df = source_data.get('persons_df')
            households_df = source_data.get('households_df')

            if not persons_df.empty:
                all_persons.append(persons_df)
            if not households_df.empty:
                all_households.append(households_df)

        # Create combined dataset
        if all_persons:
            combined_persons = pd.concat(all_persons, ignore_index=True)
            combined_households = pd.concat(all_households, ignore_index=True)
        else:
            combined_persons = pd.DataFrame()
            combined_households = pd.DataFrame()

        processed_filtered['combined'] = {
            'persons_df': combined_persons,
            'households_df': combined_households
        }

        # Generate reports from filtered data
        calculated_reports = generate_all_reports(processed_filtered)
        st.session_state['calculated_reports'] = calculated_reports

        # Show summary
        total_records = sum(len(df) for df in filtered_data.values())
        st.success(f"✅ Filters applied! Reports regenerated with {total_records} filtered records.")
        st.rerun()

def show_reports_interface():
    """Show the reports interface with all tabs preserved"""
    calculated_reports = st.session_state.get('calculated_reports', {})

    if not calculated_reports:
        st.info("No reports available.")
        return

    # Show filter interface
    show_report_filters()

    st.write("---")

    # Create tabs for each report type - PRESERVE EXACT STRUCTURE
    report_types = ['HDX_Totals', 'HDX_Veterans', 'HDX_Youth', 'HDX_Subpopulations', 'PIT Summary']
    tabs = st.tabs([f"📊 {rt}" for rt in report_types])
    
    for tab, report_type in zip(tabs, report_types):
        with tab:
            reports = calculated_reports.get(report_type, {})
            
            if not reports:
                st.info(f"No {report_type} reports available.")
                continue
            
            # Display each report in this category
            for report_name, report_df in reports.items():
                st.subheader(f"📋 {report_name}")
                
                if report_df.empty:
                    st.warning("No data available for this report.")
                    continue
                
                # Prepare display
                display_df = report_df.copy()
                
                # Handle MultiIndex
                if isinstance(display_df.index, pd.MultiIndex):
                    display_df = display_df.reset_index()
                    display_df.columns = ['Category', 'Subcategory'] + list(display_df.columns[2:])
                else:
                    display_df = display_df.reset_index()
                    if 'index' in display_df.columns:
                        display_df.rename(columns={'index': 'Category'}, inplace=True)
                    display_df['Subcategory'] = ''
                
                # Show the table
                from utils import safe_dataframe_display
                st.dataframe(
                    safe_dataframe_display(display_df),
                    width='stretch',
                    height=min(600, len(display_df) * 35 + 100),
                    hide_index=True
                )
                
                # Download button
                csv_data = display_df.to_csv(index=False)
                st.download_button(
                    "📥 Download CSV",
                    data=csv_data,
                    file_name=f"{report_name.replace(' ', '_')}.csv",
                    mime="text/csv",
                    key=f"dl_{report_type}_{report_name}"
                )
                
                st.write("---")

def show_download_interface():
    """Show the download interface with all original options"""
    calculated_reports = st.session_state.get('calculated_reports', {})
    processed_data = st.session_state.get('processed_data', {})
    uploaded_data = st.session_state.get('uploaded_data', {})
    region = st.session_state.get('region', 'Unknown')
    
    if not calculated_reports:
        st.info("No reports available for download.")
        return
    
    st.subheader("Available Reports")
    
    # Display available reports summary
    total_reports = sum(len(reports) for reports in calculated_reports.values())
    st.write(f"**Total Reports:** {total_reports}")
    
    # Show report summary table
    summary_data = []
    for report_type, reports in calculated_reports.items():
        for report_name, report_df in reports.items():
            summary_data.append({
                'Report Type': report_type,
                'Report Name': report_name,
                'Rows': len(report_df),
                'Columns': len(report_df.columns)
            })
    
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, width='stretch')
    
    # Download options
    st.subheader("Download Options")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Download type selection - ALL ORIGINAL OPTIONS
        download_type = st.radio(
            "Select Download Type",
            ["Reports Only", 
             "Reports + Raw Data with IDs", 
             "Reports + Processed Data with IDs",
             "All Data (Reports + Raw + Processed)"],
            help="Choose what data to include in the download"
        )
    
    with col2:
        st.write("**File Information:**")
        timezone = get_timezone_for_region(region)
        timestamp = get_current_timestamp(timezone)
        filename = create_download_filename(region, "Reports", timestamp)
        st.write(f"Filename: `{filename}`")
        st.write(f"Timestamp: {timestamp}")
    
    # Generate and download
    if st.button("Generate Download File", type="primary"):
        generate_download_file(
            filename, 
            download_type,
            calculated_reports,
            uploaded_data,
            processed_data,
            region
        )
    
    st.write("---")
    
    # Individual downloads section
    show_individual_downloads(calculated_reports, region)
    
    st.write("---")
    
    # Raw data downloads section
    show_raw_data_downloads(uploaded_data, processed_data, region)
    
    st.write("---")
    
    # Processed data downloads section
    show_processed_data_downloads(processed_data, region)
    
    st.write("---")
    
    # Additional resources
    show_additional_resources()

def generate_download_file(filename, download_type, calculated_reports, uploaded_data, processed_data, region):
    """Generate download file with selected options"""
    with st.spinner("Generating Excel file..."):
        try:
            # Prepare data based on download type
            include_raw = download_type in ["Reports + Raw Data with IDs", "All Data (Reports + Raw + Processed)"]
            include_processed = download_type in ["Reports + Processed Data with IDs", "All Data (Reports + Raw + Processed)"]
            
            raw_data_with_ids = None
            processed_data_with_ids = None
            
            if include_raw:
                raw_data_with_ids = prepare_raw_data_with_ids(uploaded_data, processed_data)
            
            if include_processed:
                processed_data_with_ids = prepare_processed_data_with_ids(processed_data)
            
            # Create Excel file
            excel_buffer = create_comprehensive_excel_export(
                calculated_reports,
                raw_data_with_ids,
                processed_data_with_ids,
                include_raw,
                include_processed
            )
            
            # Calculate file size
            file_size_mb = len(excel_buffer.getvalue()) / 1024 / 1024
            
            # Provide download
            st.download_button(
                label=f"📥 Download Excel File ({file_size_mb:.1f} MB)",
                data=excel_buffer.getvalue(),
                file_name=filename,
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                type="primary",
                width='stretch'
            )
            
            st.success("Excel file generated successfully!")
            
            # Show file details
            with st.expander("File Details"):
                st.write(f"**Filename:** {filename}")
                st.write(f"**File Size:** {file_size_mb:.2f} MB")
                st.write(f"**Report Sheets:** {len(calculated_reports)}")
                
                for sheet_name, sheet_data in calculated_reports.items():
                    st.write(f"- {sheet_name}: {len(sheet_data)} reports")
                
                if include_raw and raw_data_with_ids:
                    st.write(f"**Raw Data Sheets:** {len(raw_data_with_ids)}")
                    for source_name, raw_df in raw_data_with_ids.items():
                        st.write(f"- Raw_{source_name}: {len(raw_df)} households")
                
                if include_processed and processed_data_with_ids:
                    st.write(f"**Processed Data Sheets:** {len(processed_data_with_ids) * 2}")
                    for source_name, data_dict in processed_data_with_ids.items():
                        if 'persons' in data_dict:
                            st.write(f"- Processed_Persons_{source_name}: {len(data_dict['persons'])} persons")
                        if 'households' in data_dict:
                            st.write(f"- Processed_Households_{source_name}: {len(data_dict['households'])} households")
        
        except Exception as e:
            st.error(f"Error generating Excel file: {str(e)}")

def prepare_raw_data_with_ids(uploaded_data, processed_data):
    """Prepare raw data with Household ID and Person IDs"""
    raw_data_with_ids = {}
    
    for source_name in ['Sheltered_ES', 'Sheltered_TH', 'Unsheltered']:
        raw_df = uploaded_data.get(source_name, pd.DataFrame())
        if raw_df.empty:
            continue
        
        source_data = processed_data.get(source_name, {})
        persons_df = source_data.get('persons_df', pd.DataFrame())
        
        if persons_df.empty:
            continue
        
        # Create enhanced raw data
        enhanced_raw = raw_df.copy()
        
        # Add Household ID
        enhanced_raw.insert(0, 'Household_ID', range(1, len(enhanced_raw) + 1))
        
        # Create Person IDs
        person_ids_list = []
        
        for idx in range(len(enhanced_raw)):
            household_id = idx + 1
            
            # Get all persons in this household
            household_persons = persons_df[persons_df['Household_ID'] == household_id]
            
            if not household_persons.empty:
                person_ids = []
                for _, person in household_persons.iterrows():
                    member_type = person.get('Member_Type', 'Unknown')
                    member_number = person.get('Member_Number', 1)
                    person_id = f"HH{household_id}_{member_type[0]}{member_number}"
                    person_ids.append(person_id)
                
                person_ids_str = ', '.join(sorted(person_ids))
            else:
                person_ids_str = f"HH{household_id}_A1"
            
            person_ids_list.append(person_ids_str)
        
        # Add Person IDs column
        enhanced_raw.insert(1, 'Person_IDs', person_ids_list)
        
        raw_data_with_ids[source_name] = enhanced_raw
    
    return raw_data_with_ids

def prepare_processed_data_with_ids(processed_data):
    """Prepare processed persons and households data"""
    processed_data_with_ids = {}
    
    for source_name in ['Sheltered_ES', 'Sheltered_TH', 'Unsheltered']:
        source_data = processed_data.get(source_name, {})
        persons_df = source_data.get('persons_df', pd.DataFrame())
        households_df = source_data.get('households_df', pd.DataFrame())
        
        if persons_df.empty and households_df.empty:
            continue
        
        # Prepare persons data
        if not persons_df.empty:
            persons_enhanced = persons_df.copy()
            
            # Add Person_ID column
            person_ids = []
            for _, person in persons_enhanced.iterrows():
                household_id = person.get('Household_ID', 0)
                member_type = person.get('Member_Type', 'Unknown')
                member_number = person.get('Member_Number', 1)
                person_id = f"HH{household_id}_{member_type[0]}{member_number}"
                person_ids.append(person_id)
            
            persons_enhanced.insert(0, 'Person_ID', person_ids)
            
            # Reorder columns
            important_cols = ['Person_ID', 'Household_ID', 'Member_Type', 'Member_Number', 
                            'Gender', 'race', 'age_range', 'age_group', 'DV', 'vet', 'CH']
            other_cols = [col for col in persons_enhanced.columns if col not in important_cols]
            persons_enhanced = persons_enhanced[important_cols + other_cols]
        else:
            persons_enhanced = pd.DataFrame()
        
        # Prepare households data
        if not households_df.empty:
            households_enhanced = households_df.copy()
            
            # Add person count and IDs
            person_counts = []
            person_ids_lists = []
            
            for _, household in households_enhanced.iterrows():
                household_id = household.get('household_id', 0)
                
                # Get all persons in this household
                household_persons = persons_df[persons_df['Household_ID'] == household_id]
                
                person_counts.append(len(household_persons))
                
                if not household_persons.empty:
                    person_ids = []
                    for _, person in household_persons.iterrows():
                        member_type = person.get('Member_Type', 'Unknown')
                        member_number = person.get('Member_Number', 1)
                        person_id = f"HH{household_id}_{member_type[0]}{member_number}"
                        person_ids.append(person_id)
                    person_ids_lists.append(', '.join(sorted(person_ids)))
                else:
                    person_ids_lists.append('')
            
            households_enhanced.insert(1, 'Person_Count', person_counts)
            households_enhanced.insert(2, 'Person_IDs', person_ids_lists)
            
            # Reorder columns
            important_cols = ['household_id', 'Person_Count', 'Person_IDs', 'household_type', 
                            'total_persons', 'count_adult', 'count_youth', 'count_child_hoh', 
                            'count_child_hh', 'youth']
            other_cols = [col for col in households_enhanced.columns if col not in important_cols]
            households_enhanced = households_enhanced[important_cols + other_cols]
        else:
            households_enhanced = pd.DataFrame()
        
        processed_data_with_ids[source_name] = {
            'persons': persons_enhanced,
            'households': households_enhanced
        }
    
    return processed_data_with_ids

def create_comprehensive_excel_export(reports_data, raw_data_with_ids, processed_data_with_ids, 
                                    include_raw, include_processed):
    """Create Excel file with all reports and optional data - EXACT ORIGINAL FORMATTING"""
    excel_buffer = BytesIO()
    
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        workbook = writer.book
        
        # Create styles
        cell_style = NamedStyle(
            name="cell_style",
            font=Font(size=11),
            alignment=Alignment(horizontal="left", vertical="center")
        )
        
        title_style = NamedStyle(
            name="title_style",
            font=Font(size=12, bold=True, color="000000"),
            alignment=Alignment(horizontal="center", vertical="center"),
            fill=PatternFill(start_color="e2efe8", end_color="e2efe8", fill_type="solid")
        )
        
        if 'cell_style' not in workbook.named_styles:
            workbook.add_named_style(cell_style)
        if 'title_style' not in workbook.named_styles:
            workbook.add_named_style(title_style)
        
        # Process each report type
        for report_type, reports in reports_data.items():
            if not reports:
                continue
            
            # Create worksheet for this report type
            if report_type not in workbook.sheetnames:
                workbook.create_sheet(report_type)
            
            worksheet = workbook[report_type]
            worksheet.sheet_state = 'visible'
            
            current_row = 1
            
            # Add each report to the worksheet
            for report_name, report_df in reports.items():
                if report_df.empty:
                    continue
                
                # Write the DataFrame to Excel
                report_df.to_excel(
                    writer,
                    sheet_name=report_type,
                    index=True,
                    startrow=current_row
                )
                
                # Format the section
                format_worksheet_section(worksheet, report_df, report_name, current_row)
                
                # Move to next section
                current_row += len(report_df) + 8
        
        # Add raw data sheets if requested
        if include_raw and raw_data_with_ids:
            for source_name, raw_df in raw_data_with_ids.items():
                sheet_name = f"Raw_{source_name}"
                raw_df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Format the raw data sheet
                worksheet = workbook[sheet_name]
                worksheet.sheet_state = 'visible'
                
                # Auto-adjust column widths
                for col_num, column in enumerate(raw_df.columns, 1):
                    max_length = max(
                        len(str(column)),
                        raw_df[column].astype(str).str.len().max() if not raw_df.empty else 0
                    )
                    adjusted_width = min(max(max_length + 2, 10), 50)
                    worksheet.column_dimensions[get_column_letter(col_num)].width = adjusted_width
        
        # Add processed data sheets if requested
        if include_processed and processed_data_with_ids:
            for source_name, data_dict in processed_data_with_ids.items():
                # Add persons sheet
                if 'persons' in data_dict:
                    sheet_name = f"Processed_Persons_{source_name}"
                    data_dict['persons'].to_excel(writer, sheet_name=sheet_name, index=False)
                    
                    worksheet = workbook[sheet_name]
                    worksheet.sheet_state = 'visible'
                    
                    # Auto-adjust column widths
                    for col_num, column in enumerate(data_dict['persons'].columns, 1):
                        max_length = max(
                            len(str(column)),
                            data_dict['persons'][column].astype(str).str.len().max() if not data_dict['persons'].empty else 0
                        )
                        adjusted_width = min(max(max_length + 2, 10), 50)
                        worksheet.column_dimensions[get_column_letter(col_num)].width = adjusted_width
                
                # Add households sheet
                if 'households' in data_dict:
                    sheet_name = f"Processed_Households_{source_name}"
                    data_dict['households'].to_excel(writer, sheet_name=sheet_name, index=False)
                    
                    worksheet = workbook[sheet_name]
                    worksheet.sheet_state = 'visible'
                    
                    # Auto-adjust column widths
                    for col_num, column in enumerate(data_dict['households'].columns, 1):
                        max_length = max(
                            len(str(column)),
                            data_dict['households'][column].astype(str).str.len().max() if not data_dict['households'].empty else 0
                        )
                        adjusted_width = min(max(max_length + 2, 10), 50)
                        worksheet.column_dimensions[get_column_letter(col_num)].width = adjusted_width
        
        # Remove default sheet if it exists and we have other sheets
        if "Sheet" in workbook.sheetnames and len(workbook.sheetnames) > 1:
            del workbook["Sheet"]
    
    excel_buffer.seek(0)
    return excel_buffer

def format_worksheet_section(worksheet, df, title, start_row):
    """Apply formatting to a worksheet section"""
    from openpyxl.utils import get_column_letter
    
    # Add title
    title_cell = worksheet.cell(row=start_row, column=1, value=title)
    title_cell.style = 'title_style'
    
    # Merge title cells
    end_col = df.shape[1] + 2 if not df.empty else 3
    worksheet.merge_cells(
        start_row=start_row,
        start_column=1,
        end_row=start_row,
        end_column=end_col
    )
    
    # Format data cells
    data_start_row = start_row + 1
    data_end_row = data_start_row + df.shape[0] + 1
    
    for row in worksheet.iter_rows(
        min_row=data_start_row,
        max_row=data_end_row,
        min_col=1,
        max_col=end_col
    ):
        for cell in row:
            cell.style = 'cell_style'
    
    # Auto-adjust column widths
    for col_num in range(1, end_col + 1):
        column = worksheet[get_column_letter(col_num)]
        max_length = 0
        
        for cell in column:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        
        # Set minimum width and maximum width
        adjusted_width = min(max(max_length + 2, 10), 50)
        worksheet.column_dimensions[get_column_letter(col_num)].width = adjusted_width

def show_individual_downloads(calculated_reports, region):
    """Show individual report downloads section"""
    st.subheader("Individual Report Downloads")
    
    if not calculated_reports:
        st.info("No reports available.")
        return
    
    # Create report options
    report_options = []
    for report_type, reports in calculated_reports.items():
        for report_name in reports.keys():
            report_options.append(f"{report_type} - {report_name}")
    
    if not report_options:
        st.info("No individual reports available.")
        return
    
    selected_report = st.selectbox(
        "Select Report for Individual Download",
        report_options
    )
    
    if selected_report:
        # Parse selection
        report_type, report_name = selected_report.split(" - ", 1)
        report_df = calculated_reports[report_type][report_name]
        
        # Show preview
        with st.expander(f"Preview: {selected_report}"):
            st.dataframe(report_df, width='stretch')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CSV download
            csv_data = report_df.to_csv()
            csv_filename = f"{region}_{report_type}_{report_name.replace(' ', '_')}.csv"
            
            st.download_button(
                label="📄 Download as CSV",
                data=csv_data,
                file_name=csv_filename,
                mime='text/csv'
            )
        
        with col2:
            # Excel download (single sheet)
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                report_df.to_excel(writer, sheet_name=report_name[:30], index=True)
            
            excel_filename = f"{region}_{report_type}_{report_name.replace(' ', '_')}.xlsx"
            
            st.download_button(
                label="📊 Download as Excel",
                data=excel_buffer.getvalue(),
                file_name=excel_filename,
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

def show_raw_data_downloads(uploaded_data, processed_data, region):
    """Show raw data downloads section"""
    st.subheader("Enhanced Raw Data Downloads")
    
    if not uploaded_data:
        st.info("No raw data available.")
        return
    
    st.info("Raw data downloads include Household ID and Person IDs for verification purposes.")
    
    # Prepare raw data with IDs
    raw_data_with_ids = prepare_raw_data_with_ids(uploaded_data, processed_data)
    
    if not raw_data_with_ids:
        st.warning("No processed data available to generate IDs.")
        return
    
    # Show available sources
    for source_name, enhanced_df in raw_data_with_ids.items():
        st.write(f"### {source_name}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Households", len(enhanced_df))
        
        with col2:
            # Count total persons from Person_IDs column
            total_persons = sum(len(pid.split(', ')) for pid in enhanced_df['Person_IDs'])
            st.metric("Total Persons", total_persons)
        
        with col3:
            # Download button
            csv_data = enhanced_df.to_csv(index=False)
            filename = f"{region}_{source_name}_Raw_with_IDs.csv"
            
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=filename,
                mime='text/csv',
                key=f"raw_{source_name}"
            )
        
        # Preview
        with st.expander(f"Preview first 10 rows"):
            # Show only key columns in preview
            preview_cols = ['Household_ID', 'Person_IDs', 'Timestamp', 'Gender', 'Age Range', 'Race/Ethnicity']
            display_cols = [col for col in preview_cols if col in enhanced_df.columns]
            from utils import safe_dataframe_display
            st.dataframe(safe_dataframe_display(enhanced_df[display_cols].head(10)), width='stretch')

def show_processed_data_downloads(processed_data, region):
    """Show processed data downloads section"""
    st.subheader("Processed Data Downloads")
    
    if not processed_data:
        st.info("No processed data available.")
        return
    
    st.info("Download the fully processed persons and households data with all calculated fields.")
    
    # Prepare processed data
    processed_data_with_ids = prepare_processed_data_with_ids(processed_data)
    
    if not processed_data_with_ids:
        st.warning("No processed data available.")
        return
    
    # Show available sources
    for source_name, data_dict in processed_data_with_ids.items():
        st.write(f"### {source_name}")
        
        # Create tabs for persons and households
        tab1, tab2 = st.tabs(["👥 Persons Data", "🏠 Households Data"])
        
        with tab1:
            if 'persons' in data_dict and not data_dict['persons'].empty:
                persons_df = data_dict['persons']
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Persons", len(persons_df))
                
                with col2:
                    st.metric("Unique Households", persons_df['Household_ID'].nunique())
                
                with col3:
                    # Download button
                    csv_data = persons_df.to_csv(index=False)
                    filename = f"{region}_{source_name}_Processed_Persons.csv"
                    
                    st.download_button(
                        label="📥 Download Persons CSV",
                        data=csv_data,
                        file_name=filename,
                        mime='text/csv',
                        key=f"processed_persons_{source_name}"
                    )
                
                # Preview
                with st.expander("Preview first 20 rows"):
                    st.dataframe(persons_df.head(20), width='stretch')
            else:
                st.info("No persons data available for this source.")
        
        with tab2:
            if 'households' in data_dict and not data_dict['households'].empty:
                households_df = data_dict['households']
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Households", len(households_df))
                
                with col2:
                    avg_size = households_df['total_persons'].mean()
                    st.metric("Avg Household Size", f"{avg_size:.1f}")
                
                with col3:
                    # Download button
                    csv_data = households_df.to_csv(index=False)
                    filename = f"{region}_{source_name}_Processed_Households.csv"
                    
                    st.download_button(
                        label="📥 Download Households CSV",
                        data=csv_data,
                        file_name=filename,
                        mime='text/csv',
                        key=f"processed_households_{source_name}"
                    )
                
                # Preview
                with st.expander("Preview first 20 rows"):
                    st.dataframe(households_df.head(20), width='stretch')
            else:
                st.info("No households data available for this source.")

def show_additional_resources():
    """Show additional resources section"""
    st.subheader("Additional Resources")
    
    st.write("**Related Tools:**")
    st.markdown("- [HMIS and Non-HMIS Combiner](https://combinepit.streamlit.app/)")
    st.markdown("- [Breakdown by Project Name on HIC](https://hic-project.streamlit.app/)")
    
    st.write("**Support:**")
    st.write("For technical support or questions about the PIT Count application, please contact your system administrator.")
