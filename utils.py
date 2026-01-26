"""
Utilities module for PIT Count Application
Contains helper functions and session management
"""

import streamlit as st
from datetime import datetime
import pytz

def init_session_state():
    """Initialize session state with default values"""
    defaults = {
        'logged_in': False,
        'username': None,
        'region': None,
        'uploaded_data': {},
        'processed_data': {},
        'calculated_reports': {},
        'current_step': 'upload',
        # Combiner-specific state
        'combiner_output': None,
        'combiner_filename': None
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def create_header():
    """Create application header"""
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
        if st.session_state.get('logged_in'):
            username = st.session_state.get('username', 'User')
            region = st.session_state.get('region', '')
            
            st.markdown(f"""
                <div style='text-align: right; font-size: 0.9em; color: #666;'>
                    👤 {username}<br>
                    📍 {region}
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Logout", type="secondary"):
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.rerun()

def create_footer():
    """Create application footer"""
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
            © 2026 Institute for Community Alliances (ICA). All rights reserved.
        </div>
    """, unsafe_allow_html=True)

def get_current_timestamp(timezone='UTC'):
    """Get current timestamp formatted for filenames"""
    tz = pytz.timezone(timezone)
    return datetime.now(tz).strftime('%Y-%m-%d_%H-%M-%S')

def get_timezone_for_region(region):
    """Get timezone for a region"""
    timezone_mapping = {
        'New England': 'America/New_York',
        'Great Lakes': 'America/Chicago',
        'Unknown': 'UTC'
    }
    return timezone_mapping.get(region, 'UTC')

def format_number(value):
    """Format number with commas"""
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return str(value) if value is not None else "N/A"

def calculate_percentage(numerator, denominator, decimal_places=1):
    """Calculate percentage safely"""
    if denominator == 0:
        return "0%"
    try:
        percentage = (numerator / denominator) * 100
        return f"{percentage:.{decimal_places}f}%"
    except (TypeError, ValueError, ZeroDivisionError):
        return "N/A"

def safe_dataframe_display(df):
    """
    Safely convert dataframe for display to avoid Arrow serialization errors.
    Converts columns with mixed types to strings.
    """
    if df is None or df.empty:
        return df

    df_display = df.copy()

    # Convert object columns with mixed types to strings
    for col in df_display.columns:
        if df_display[col].dtype == 'object':
            # Convert all values to strings to avoid mixed type issues
            try:
                # Handle NaN values first, then convert everything to string
                df_display[col] = df_display[col].fillna('').astype(str)
            except Exception as e:
                # If conversion still fails, try element-wise conversion
                try:
                    df_display[col] = df_display[col].apply(lambda x: str(x) if x is not None else '')
                except:
                    pass

    return df_display

def create_summary_metrics(data_dict):
    """Create summary metrics for uploaded data"""
    total_sources = len(data_dict)
    total_rows = sum(len(df) for df in data_dict.values())

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Data Sources", total_sources)
    with col2:
        st.metric("Total Households", format_number(total_rows))
    with col3:
        st.metric("Status", "✅ Ready" if total_rows > 0 else "❌ No Data")

    return total_rows > 0

def display_data_preview(data_dict, max_rows=20):
    """Display preview of uploaded data"""
    if not data_dict:
        return

    if len(data_dict) == 1:
        # Single source
        source_name, df = list(data_dict.items())[0]
        df_safe = safe_dataframe_display(df.head(max_rows))
        st.dataframe(df_safe, width='stretch')
        st.caption(f"Showing first {min(max_rows, len(df))} of {len(df)} rows")
    else:
        # Multiple sources - use tabs
        tabs = st.tabs(list(data_dict.keys()))
        for tab, (source_name, df) in zip(tabs, data_dict.items()):
            with tab:
                df_safe = safe_dataframe_display(df.head(max_rows))
                st.dataframe(df_safe, width='stretch')
                st.caption(f"Showing first {min(max_rows, len(df))} of {len(df)} rows")

def get_progress_text(current_step):
    """Get progress text for current step"""
    steps = {
        'upload': 'Step 1 of 4: Data Upload',
        'validation': 'Step 2 of 4: Validation & Duplication',
        'reports': 'Step 3 of 4: View Reports',
        'download': 'Step 4 of 4: Download Results'
    }
    return steps.get(current_step, '')

def safe_divide(numerator, denominator, default=0):
    """Safely divide two numbers"""
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ValueError, ZeroDivisionError):
        return default

def get_report_icon(report_type):
    """Get icon for report type"""
    icons = {
        'HDX_Totals': '📊',
        'HDX_Veterans': '🎖️',
        'HDX_Youth': '👶',
        'HDX_Subpopulations': '🎯',
        'PIT Summary': '📋'
    }
    return icons.get(report_type, '📊')

def clean_dataframe_for_export(df):
    """Clean DataFrame for export"""
    cleaned_df = df.copy()
    
    # Replace inf and -inf with NaN
    import numpy as np
    cleaned_df = cleaned_df.replace([np.inf, -np.inf], np.nan)
    
    # Fill NaN appropriately
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype in ['int64', 'float64']:
            cleaned_df[col] = cleaned_df[col].fillna(0)
        else:
            cleaned_df[col] = cleaned_df[col].fillna('')
    
    return cleaned_df

def validate_file_size(file_obj, max_size_mb=100):
    """Validate file size"""
    try:
        file_obj.seek(0, 2)  # Seek to end
        size = file_obj.tell()
        file_obj.seek(0)  # Reset to beginning
        size_mb = size / 1024 / 1024

        if size_mb > max_size_mb:
            return False, f"File size ({size_mb:.1f} MB) exceeds limit ({max_size_mb} MB)"
        return True, f"{size_mb:.1f} MB"
    except (AttributeError, OSError, IOError) as e:
        return False, f"Unable to determine file size: {str(e)}"

def create_download_filename(region, report_type, timestamp=None):
    """Create standardized filename for downloads"""
    if timestamp is None:
        timestamp = get_current_timestamp()

    # Clean region name
    clean_region = region.replace(' ', '_').replace('/', '_')

    return f"{clean_region}_PIT_{report_type}_{timestamp}.xlsx"

# ============================================================================
# NEW HELPER FUNCTIONS FOR UNIFIED COLUMN MAPPING SYSTEM
# ============================================================================

def detect_region_and_format(df, signatures=None):
    """
    Auto-detect region and data format from column presence.

    Algorithm:
    1. Score each region based on presence of signature columns
    2. Check optional column groups
    3. Validate detected region has minimum requirements
    4. Return region metadata including timezone

    Args:
        df: Input DataFrame with original column names
        signatures: Region signature definitions (uses REGION_SIGNATURES from config if None)

    Returns:
        Dict with keys:
        - 'region': Detected region name or None
        - 'confidence': Match confidence (0.0 to 1.0)
        - 'timezone': Appropriate timezone for region
        - 'max_adults': Maximum adults supported
        - 'child_chronic_conditions': Whether child chronic conditions are tracked
        - 'missing_optional': List of optional columns not found
        - 'detected_format': Description of detected format
    """
    from config import REGION_SIGNATURES
    import streamlit as st

    if signatures is None:
        signatures = REGION_SIGNATURES

    # Normalize column names
    df_cols = set(df.columns.str.strip())

    # Score each region
    region_scores = {}

    for region_name, signature in signatures.items():
        required = signature.get('required_columns', [])
        optional_groups = signature.get('optional_name_columns', [])

        # Check required columns
        required_matches = sum(1 for col in required if col in df_cols)
        required_total = len(required)

        # Check optional column groups (at least one group must be satisfied)
        optional_satisfied = False
        if optional_groups:
            for group in optional_groups:
                if all(col in df_cols for col in group):
                    optional_satisfied = True
                    break
        else:
            optional_satisfied = True  # No optional requirements

        # Calculate score
        if required_total > 0:
            base_score = required_matches / required_total
        else:
            base_score = 0.0

        # Bonus for optional groups
        final_score = base_score
        if optional_satisfied and base_score > 0:
            final_score = min(base_score + 0.2, 1.0)

        region_scores[region_name] = {
            'score': final_score,
            'required_matches': required_matches,
            'required_total': required_total,
            'optional_satisfied': optional_satisfied
        }

    # Select best match
    if not region_scores:
        return {
            'region': None,
            'confidence': 0.0,
            'error': 'No region signatures defined'
        }

    best_region = max(region_scores.items(), key=lambda x: x[1]['score'])
    region_name, score_info = best_region

    # Require minimum confidence threshold
    MIN_CONFIDENCE = 0.75

    if score_info['score'] < MIN_CONFIDENCE:
        return {
            'region': None,
            'confidence': score_info['score'],
            'error': f'Low confidence in region detection ({score_info["score"]:.1%}). '
                    f'Best match was {region_name} but required columns may be missing.',
            'scores': region_scores
        }

    # Get region metadata
    signature = signatures[region_name]

    # Check for missing optional fields
    missing_optional = []
    if region_name == 'New England':
        # Check for adult 3 & 4 columns
        if 'Adult/Parent #3: Sex' not in df_cols:
            missing_optional.append('Adult #3 data')
        if 'Adult/Parent #4: Sex' not in df_cols:
            missing_optional.append('Adult #4 data')

    return {
        'region': region_name,
        'confidence': score_info['score'],
        'timezone': signature['timezone'],
        'max_adults': signature['max_adults'],
        'child_chronic_conditions': signature['child_chronic_conditions'],
        'missing_optional': missing_optional,
        'detected_format': f"{region_name} format (confidence: {score_info['score']:.1%})",
        'name_format': _describe_name_format(region_name, df_cols)
    }

def _describe_name_format(region: str, columns: set) -> str:
    """Describe the name field format detected."""
    if region == 'New England':
        has_all = all(c in columns for c in [
            '1st Letter of First Name',
            '1st Letter of Last Name',
            '3rd Letter of Last Name'
        ])
        return 'Initials (1st first + 1st & 3rd last)' if has_all else 'Initials (partial)'

    elif region == 'Great Lakes':
        has_full_last = 'Last Name' in columns
        has_initial_last = 'First Letter of Last Name' in columns
        has_first = 'First Name' in columns

        if has_first and has_full_last:
            return 'Full names (First + Last)'
        elif has_first and has_initial_last:
            return 'Hybrid (First + Last initial)'
        else:
            return 'Partial name data'

    return 'Unknown format'

def validate_name_fields_completeness(df, detected_region):
    """
    Validate that sufficient name fields exist for duplication detection.

    Returns:
        Dict with 'is_valid', 'warnings', 'missing_fields'
    """
    import streamlit as st

    warnings = []
    missing_fields = []

    if detected_region == 'New England':
        required_name_fields = [
            '1st Letter of First Name',
            '1st Letter of Last Name',
            '3rd Letter of Last Name'
        ]
        missing = [f for f in required_name_fields if f not in df.columns]

        if missing:
            missing_fields.extend(missing)
            warnings.append(
                f"Missing New England name fields: {', '.join(missing)}. "
                "Duplication detection may be less accurate."
            )

    elif detected_region == 'Great Lakes':
        has_first = 'First Name' in df.columns
        has_last_full = 'Last Name' in df.columns
        has_last_initial = 'First Letter of Last Name' in df.columns

        if not has_first:
            missing_fields.append('First Name')
            warnings.append("Missing 'First Name' field. Duplication detection will be limited.")

        if not has_last_full and not has_last_initial:
            missing_fields.append('Last Name or First Letter of Last Name')
            warnings.append(
                "Missing both 'Last Name' and 'First Letter of Last Name'. "
                "Duplication detection will not work properly."
            )

    is_valid = len(missing_fields) == 0 or (
        # Allow if we have at least first name + some last name info
        'First Name' in df.columns and ('Last Name' in df.columns or 'First Letter of Last Name' in df.columns)
    )

    return {
        'is_valid': is_valid,
        'warnings': warnings,
        'missing_fields': missing_fields
    }

def handle_mixed_format_data(df, mapping_log):
    """
    Handle cases where data might have mixed format columns.

    Strategy:
    1. Prefer higher-priority mappings
    2. For name fields, synthesize missing initials from full names if needed
    3. Log any data synthesis performed
    """
    import streamlit as st

    # Check if we have full first name but need first initial
    if 'First Name' in df.columns and '1st Letter of First Name' not in df.columns:
        # Synthesize first initial
        df['1st Letter of First Name'] = df['First Name'].str[0].str.upper()
        st.info("ℹ️ Synthesized '1st Letter of First Name' from 'First Name'")

    # Check if we have full last name but need last initial
    if 'Last Name' in df.columns and '1st Letter of Last Name' not in df.columns:
        df['1st Letter of Last Name'] = df['Last Name'].str[0].str.upper()
        st.info("ℹ️ Synthesized '1st Letter of Last Name' from 'Last Name'")

    # Check if we have full last name but need 3rd letter
    if 'Last Name' in df.columns and '3rd Letter of Last Name' not in df.columns:
        df['3rd Letter of Last Name'] = df['Last Name'].apply(lambda x: x[2].upper() if len(str(x)) > 2 else '')
        st.info("ℹ️ Synthesized '3rd Letter of Last Name' from 'Last Name'")

    return df

def log_column_mapping_analysis(df_original, df_mapped, mapping_log, detected_region):
    """
    Comprehensive logging for debugging column mapping issues.

    Creates an expandable section with:
    - Original columns found
    - Target columns mapped
    - Priority decisions made
    - Warnings about missing columns
    - Suggestions for format issues
    """
    import streamlit as st

    with st.expander("🔬 Detailed Column Mapping Analysis"):
        st.write("### Original Columns")
        st.write(f"Found {len(df_original.columns)} columns in source data:")
        st.code(", ".join(sorted(df_original.columns)))

        st.write("### Mapped Columns")
        st.write(f"Successfully mapped {len(df_mapped.columns)} target columns:")

        # Group by mapping success
        mapped_successfully = [k for k, v in mapping_log.items() if v['source'] is not None]
        not_mapped = [k for k, v in mapping_log.items() if v['source'] is None]

        st.write(f"✅ **Mapped ({len(mapped_successfully)}):**")
        for target in sorted(mapped_successfully):
            info = mapping_log[target]
            alt_text = f" ({info['alternatives_available']} alternatives available)" if info['alternatives_available'] > 0 else ""
            st.write(f"- `{target}` ← `{info['source']}`{alt_text}")

        if not_mapped:
            st.write(f"⚠️ **Not Mapped ({len(not_mapped)}):**")
            for target in sorted(not_mapped):
                st.write(f"- `{target}` (no source column found)")

        st.write("### Region Detection")
        st.write(f"**Detected Region:** {detected_region}")

        st.write("### Recommendations")
        if len(not_mapped) > 10:
            st.warning("Many columns were not mapped. Verify your data format matches the expected structure.")
        elif len(not_mapped) > 0:
            st.info(f"{len(not_mapped)} optional columns were not found. This may be expected for your region.")