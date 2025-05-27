"""
Reports interface component for PIT Count application.
Simplified version without drill-down functionality.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Optional, List, Tuple, Set

from utils.session import SessionManager

def create_reports_interface():
    """Create reports interface for viewing calculated reports."""
    
    calculated_reports = SessionManager.get_session_value('calculated_reports', {})
    
    if not calculated_reports:
        st.info("📋 No reports available. Please calculate reports first.")
        return
    
    # Header
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 25px; border-radius: 15px; margin-bottom: 25px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h1 style="color: white; margin: 0; text-align: center; font-size: 2.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                📊 PIT Count Reports
            </h1>
            <p style="color: #f0f0f0; margin: 10px 0 0 0; font-size: 1.2rem; text-align: center;">
                View your calculated PIT Count reports
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different report types
    report_types = list(calculated_reports.keys())
    if report_types:
        tabs = st.tabs([f"📊 **{report_type}**" for report_type in report_types])
        
        for tab, report_type in zip(tabs, report_types):
            with tab:
                reports = calculated_reports[report_type]
                
                if not reports:
                    st.info(f"No {report_type} reports available.")
                    continue
                
                # Group reports by category name
                grouped_reports = {}
                for report_name, report_df in reports.items():
                    # Extract category from report name (text before "by" or "for")
                    if " by " in report_name:
                        category = report_name.split(" by ")[0]
                    elif " for " in report_name:
                        category = report_name.split(" for ")[0]
                    else:
                        category = report_name
                    
                    if category not in grouped_reports:
                        grouped_reports[category] = []
                    grouped_reports[category].append((report_name, report_df))
                
                # Display grouped reports
                for category, category_reports in grouped_reports.items():
                    # Category header if there are multiple reports in this category
                    if len(category_reports) > 1:
                        st.markdown(f"### {category}")
                    
                    # Display each report in the category
                    for report_name, report_df in category_reports:
                        _display_single_report(report_type, report_name, report_df)


def _display_single_report(report_type: str, report_name: str, report_df: pd.DataFrame):
    """Display a single report."""
    
    # Report header
    st.markdown(f"""
        <div style="background: #00629b; 
                    padding: 15px; border-radius: 10px; margin: 20px 0;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color: white; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
                📊 {report_name}
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    if report_df.empty:
        st.warning("No data available for this report.")
        return
    
    # Prepare display dataframe
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
    
    # Show the report
    st.dataframe(
        display_df,
        use_container_width=True,
        height=min(600, max(200, len(display_df) * 35 + 50)),
        hide_index=True
    )
    
    # Download option
    csv_data = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Report (CSV)",
        data=csv_data,
        file_name=f"{report_name.replace(' ', '_')}.csv",
        mime="text/csv",
        key=f"download_{report_type}_{report_name}"
    )