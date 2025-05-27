"""
Helper functions for PIT Count application.
General utility functions used across the application.
"""

import pandas as pd
import streamlit as st
from datetime import datetime
import pytz
from typing import Dict, List, Optional, Tuple

def get_current_timestamp(timezone: str = "UTC") -> str:
    """Get current timestamp formatted for filenames."""
    return datetime.now(pytz.timezone(timezone)).strftime('%Y-%m-%d_%H-%M-%S')

def get_timezone_for_region(region: str) -> str:
    """Get appropriate timezone for a region."""
    timezone_mapping = {
        'New England': 'America/New_York',
        'Dashgreatlake': 'America/Chicago'
    }
    return timezone_mapping.get(region, 'UTC')

def format_number(value) -> str:
    """Format number for display with commas."""
    if pd.isna(value) or value == 'N/A':
        return 'N/A'
    
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return str(value)

def calculate_percentage(numerator, denominator, decimal_places: int = 1) -> str:
    """Calculate percentage with error handling."""
    if pd.isna(numerator) or pd.isna(denominator) or denominator == 0:
        return 'N/A'
    
    try:
        percentage = (numerator / denominator) * 100
        return f"{percentage:.{decimal_places}f}%"
    except (ValueError, TypeError, ZeroDivisionError):
        return 'N/A'

def safe_divide(numerator, denominator, default=0):
    """Safely divide two numbers with default for division by zero."""
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ValueError):
        return default

def create_download_filename(region: str, report_type: str, timestamp: str) -> str:
    """Create standardized filename for downloads."""
    # Clean region name for filename
    clean_region = region.replace(' ', '_').replace('/', '_')
    return f"{clean_region}_PIT_{report_type}_{timestamp}.xlsx"

def validate_dataframe_structure(df: pd.DataFrame, required_columns: List[str]) -> Tuple[bool, List[str]]:
    """Validate that DataFrame has required structure."""
    missing_columns = set(required_columns) - set(df.columns)
    is_valid = len(missing_columns) == 0
    return is_valid, list(missing_columns)

def clean_dataframe_for_export(df: pd.DataFrame) -> pd.DataFrame:
    """Clean DataFrame for export by handling problematic values."""
    cleaned_df = df.copy()
    
    # Replace inf and -inf with NaN
    cleaned_df = cleaned_df.replace([float('inf'), float('-inf')], pd.NA)
    
    # Fill NaN with appropriate defaults
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype in ['int64', 'float64']:
            cleaned_df[col] = cleaned_df[col].fillna(0)
        else:
            cleaned_df[col] = cleaned_df[col].fillna('')
    
    return cleaned_df

def create_summary_statistics(df: pd.DataFrame, group_by_col: str = None) -> Dict:
    """Create summary statistics for a DataFrame."""
    summary = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
    }
    
    if group_by_col and group_by_col in df.columns:
        group_counts = df[group_by_col].value_counts().to_dict()
        summary['group_counts'] = group_counts
    
    # Numeric column statistics
    numeric_cols = df.select_dtypes(include=[pd.np.number]).columns
    if len(numeric_cols) > 0:
        summary['numeric_summary'] = df[numeric_cols].describe().to_dict()
    
    return summary

def display_processing_progress(current_step: int, total_steps: int, step_name: str):
    """Display processing progress bar."""
    progress = current_step / total_steps
    st.progress(progress, text=f"Step {current_step}/{total_steps}: {step_name}")

def create_expandable_dataframe(df: pd.DataFrame, title: str, max_rows: int = 100):
    """Create an expandable dataframe display."""
    with st.expander(f"{title} ({len(df)} rows)"):
        if len(df) > max_rows:
            st.dataframe(df.head(max_rows), use_container_width=True)
            st.caption(f"Showing first {max_rows} of {len(df)} rows")
        else:
            st.dataframe(df, use_container_width=True)

def format_currency(value, currency_symbol: str = "$") -> str:
    """Format value as currency."""
    if pd.isna(value):
        return 'N/A'
    
    try:
        return f"{currency_symbol}{value:,.2f}"
    except (ValueError, TypeError):
        return str(value)

def get_file_size_mb(file_obj) -> float:
    """Get file size in MB."""
    try:
        file_obj.seek(0, 2)  # Seek to end
        size = file_obj.tell()
        file_obj.seek(0)  # Reset to beginning
        return size / 1024 / 1024
    except:
        return 0.0

def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """Truncate string with suffix if too long."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def create_color_scale(values: List[float], colors: List[str] = None) -> Dict[float, str]:
    """Create color scale mapping for values."""
    if colors is None:
        colors = ['#ff0000', '#ffff00', '#00ff00']  # Red to Yellow to Green
    
    if not values:
        return {}
    
    min_val, max_val = min(values), max(values)
    if min_val == max_val:
        return {min_val: colors[0]}
    
    color_map = {}
    for i, value in enumerate(sorted(set(values))):
        # Calculate position in color scale (0 to 1)
        position = (value - min_val) / (max_val - min_val)
        
        # Map to color index
        color_index = min(int(position * (len(colors) - 1)), len(colors) - 1)
        color_map[value] = colors[color_index]
    
    return color_map

def safe_json_serialize(obj) -> str:
    """Safely serialize object to JSON string."""
    import json
    
    def json_serializer(obj):
        """Custom JSON serializer for pandas/numpy objects."""
        if pd.isna(obj):
            return None
        if hasattr(obj, 'item'):
            return obj.item()
        if hasattr(obj, 'tolist'):
            return obj.tolist()
        return str(obj)
    
    try:
        return json.dumps(obj, default=json_serializer, indent=2)
    except Exception as e:
        return f"Serialization error: {str(e)}"

def compare_dataframes(df1: pd.DataFrame, df2: pd.DataFrame, 
                      name1: str = "DF1", name2: str = "DF2") -> Dict:
    """Compare two DataFrames and return differences."""
    comparison = {
        'shape_comparison': {
            name1: df1.shape,
            name2: df2.shape,
            'same_shape': df1.shape == df2.shape
        },
        'columns_comparison': {
            f'{name1}_only': list(set(df1.columns) - set(df2.columns)),
            f'{name2}_only': list(set(df2.columns) - set(df1.columns)),
            'common': list(set(df1.columns) & set(df2.columns))
        }
    }
    
    # If same shape and columns, compare values
    if df1.shape == df2.shape and set(df1.columns) == set(df2.columns):
        try:
            # Align DataFrames and compare
            df1_aligned, df2_aligned = df1.align(df2)
            differences = (df1_aligned != df2_aligned).sum().sum()
            comparison['value_differences'] = {
                'total_differences': differences,
                'percentage_different': (differences / df1_aligned.size) * 100 if df1_aligned.size > 0 else 0
            }
        except Exception as e:
            comparison['value_differences'] = {'error': str(e)}
    
    return comparison