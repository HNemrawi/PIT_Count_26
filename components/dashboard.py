"""
Interactive dashboard component for PIT Count application.
Enhanced with accurate calculations, better visualizations, and impressive UI.
Modified to not consider Chronically Homeless (CH) data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Optional
import numpy as np

from utils.session import SessionManager
from utils.helpers import format_number, calculate_percentage

class DashboardManager:
    """Enhanced dashboard functionality with accurate calculations and impressive visualizations."""
    
    def __init__(self):
        """Initialize dashboard with processed data."""
        self.processed_data = SessionManager.get_session_value('processed_data', {})
        self.combined_persons = self.processed_data.get('combined', {}).get('persons_df', pd.DataFrame())
        self.combined_households = self.processed_data.get('combined', {}).get('households_df', pd.DataFrame())
        
        # Define color schemes for consistency
        self.color_schemes = {
            'primary': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'],
            'gradient': ['#0d0887', '#46039f', '#7201a8', '#9c179e', '#bd3786', '#d8576b'],
            'categorical': px.colors.qualitative.Set3,
            'sequential': px.colors.sequential.Viridis
        }
    
    def create_filter_controls(self) -> Dict:
        """Create enhanced filter controls with better UI."""
        if self.combined_persons.empty:
            st.warning("No data available for dashboard")
            return {}
        
        # Create styled filter section
        st.markdown("""
            <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h3 style="margin-top: 0;">📊 Dashboard Filters</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Create filter columns with better organization
        filter_row1 = st.columns([2, 2, 1, 1, 1])
        
        # Data source filter
        with filter_row1[0]:
            available_sources = sorted(self.combined_persons['source'].unique())
            selected_sources = st.multiselect(
                '🏠 Data Sources',
                available_sources,
                default=list(available_sources),
                key="dashboard_sources",
                help="Select one or more data sources to include"
            )
        
        # Household type filter
        with filter_row1[1]:
            available_household_types = sorted(self.combined_households['household_type'].unique())
            selected_household_types = st.multiselect(
                '👨‍👩‍👧‍👦 Household Types',
                available_household_types,
                default=list(available_household_types),
                key="dashboard_household_types",
                help="Filter by household composition"
            )
        
        # Special population toggles
        with filter_row1[2]:
            chronically_homeless = st.selectbox(
                '🏥 Chronically Homeless',
                ['All', 'Yes', 'No'],
                key="dashboard_ch",
                help="Filter chronically homeless individuals (excludes TH data)"
            )
        
        with filter_row1[3]:
            veterans = st.selectbox(
                '🎖️ Veterans',
                ['All', 'Yes', 'No'],
                key="dashboard_veterans",
                help="Filter veteran status"
            )
        
        with filter_row1[4]:
            youth_households = st.selectbox(
                '👶 Youth Households',
                ['All', 'Yes', 'No'],
                key="dashboard_youth",
                help="Filter youth-led households"
            )
        
        # Age range filter (second row)
        filter_row2 = st.columns([3, 3, 2])
        
        with filter_row2[0]:
            age_ranges = ['All', 'Under 18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
            selected_age_ranges = st.multiselect(
                '📅 Age Ranges',
                age_ranges[1:],  # Exclude 'All'
                default=age_ranges[1:],
                key="dashboard_age_ranges",
                help="Filter by age groups"
            )
        
        with filter_row2[1]:
            # Gender filter
            if 'Gender' in self.combined_persons.columns:
                available_genders = sorted(self.combined_persons['Gender'].dropna().unique())
                selected_genders = st.multiselect(
                    '⚥ Gender Identity',
                    available_genders,
                    default=available_genders,
                    key="dashboard_genders",
                    help="Filter by gender identity"
                )
            else:
                selected_genders = []
        
        with filter_row2[2]:
            # DV survivors filter
            dv_survivors = st.selectbox(
                '🛡️ DV Survivors',
                ['All', 'Yes', 'No'],
                key="dashboard_dv",
                help="Filter domestic violence survivors"
            )
        
        return {
            'sources': selected_sources,
            'household_types': selected_household_types,
            'chronically_homeless': chronically_homeless,
            'veterans': veterans,
            'youth_households': youth_households,
            'age_ranges': selected_age_ranges,
            'genders': selected_genders,
            'dv_survivors': dv_survivors
        }
    
    def apply_filters(self, filters: Dict) -> tuple:
        """Apply filters with proper household-person relationship."""
        persons_df = self.combined_persons.copy()
        households_df = self.combined_households.copy()
        
        # Track applied filters for display
        applied_filters = []
        
        # Apply source filter
        if filters.get('sources'):
            persons_df = persons_df[persons_df['source'].isin(filters['sources'])]
            household_id_col = 'Household_ID' if 'Household_ID' in persons_df.columns else 'household_id'
            household_ids = persons_df[household_id_col].unique()
            households_df = households_df[households_df['household_id'].isin(household_ids)]
            if len(filters['sources']) < len(self.combined_persons['source'].unique()):
                applied_filters.append(f"Sources: {', '.join(filters['sources'])}")
        
        # Apply household type filter
        if filters.get('household_types'):
            households_df = households_df[households_df['household_type'].isin(filters['household_types'])]
            household_ids = households_df['household_id'].unique()
            household_id_col = 'Household_ID' if 'Household_ID' in persons_df.columns else 'household_id'
            persons_df = persons_df[persons_df[household_id_col].isin(household_ids)]
            if len(filters['household_types']) < len(self.combined_households['household_type'].unique()):
                applied_filters.append(f"Household Types: {', '.join(filters['household_types'])}")
        
        # Apply age range filter - check both age_range and age_group
        if filters.get('age_ranges') and len(filters['age_ranges']) < 7:
            # Create mask for age filtering
            age_mask = pd.Series([False] * len(persons_df))
            
            for age_range in filters['age_ranges']:
                if age_range == 'Under 18':
                    # Check both age_range and age_group for children
                    age_mask |= (persons_df['age_range'] == 'Under 18')
                    if 'age_group' in persons_df.columns:
                        age_mask |= (persons_df['age_group'] == 'child')
                else:
                    age_mask |= (persons_df['age_range'] == age_range)
            
            persons_df = persons_df[age_mask]
            household_id_col = 'Household_ID' if 'Household_ID' in persons_df.columns else 'household_id'
            household_ids = persons_df[household_id_col].unique()
            households_df = households_df[households_df['household_id'].isin(household_ids)]
            applied_filters.append(f"Age Ranges: {', '.join(filters['age_ranges'])}")
        
        # Apply gender filter
        if filters.get('genders') and 'Gender' in persons_df.columns:
            if len(filters['genders']) < len(self.combined_persons['Gender'].dropna().unique()):
                persons_df = persons_df[persons_df['Gender'].isin(filters['genders'])]
                household_id_col = 'Household_ID' if 'Household_ID' in persons_df.columns else 'household_id'
                household_ids = persons_df[household_id_col].unique()
                households_df = households_df[households_df['household_id'].isin(household_ids)]
                applied_filters.append(f"Genders: {', '.join(filters['genders'][:3])}...")
        
        # Chronically homeless filter - modified to exclude sheltered_TH
        if filters.get('chronically_homeless') != 'All':
            if 'CH' in persons_df.columns:
                if filters['chronically_homeless'] == 'Yes':
                    # For 'Yes', exclude TH sources from CH count
                    ch_persons = persons_df[
                        (persons_df['CH'] == 'Yes') & 
                        (~persons_df['source'].str.lower().str.contains('th', na=False)) &
                        (~persons_df['source'].str.lower().str.contains('transitional', na=False))
                    ]
                else:
                    # For 'No', include all sources but treat TH as 'No' for CH
                    ch_persons = persons_df[
                        (persons_df['CH'] == 'No') | 
                        (persons_df['source'].str.lower().str.contains('th', na=False)) |
                        (persons_df['source'].str.lower().str.contains('transitional', na=False))
                    ]
                
                household_id_col = 'Household_ID' if 'Household_ID' in ch_persons.columns else 'household_id'
                household_ids = ch_persons[household_id_col].unique()
                persons_df = persons_df[persons_df[household_id_col].isin(household_ids)]
                households_df = households_df[households_df['household_id'].isin(household_ids)]
                applied_filters.append(f"Chronically Homeless: {filters['chronically_homeless']} (TH excluded)")
        
        # Veterans
        if filters.get('veterans') != 'All':
            if 'vet' in persons_df.columns:
                vet_persons = persons_df[persons_df['vet'] == filters['veterans']]
                household_id_col = 'Household_ID' if 'Household_ID' in vet_persons.columns else 'household_id'
                household_ids = vet_persons[household_id_col].unique()
                persons_df = persons_df[persons_df[household_id_col].isin(household_ids)]
                households_df = households_df[households_df['household_id'].isin(household_ids)]
                applied_filters.append(f"Veterans: {filters['veterans']}")
        
        # Youth households
        if filters.get('youth_households') != 'All':
            if 'youth' in households_df.columns:
                youth_hh = households_df[households_df['youth'] == filters['youth_households']]
                household_ids = youth_hh['household_id'].unique()
                household_id_col = 'Household_ID' if 'Household_ID' in persons_df.columns else 'household_id'
                persons_df = persons_df[persons_df[household_id_col].isin(household_ids)]
                households_df = households_df[households_df['household_id'].isin(household_ids)]
                applied_filters.append(f"Youth Households: {filters['youth_households']}")
        
        # DV survivors
        if filters.get('dv_survivors') != 'All':
            if 'DV' in persons_df.columns:
                dv_persons = persons_df[persons_df['DV'] == filters['dv_survivors']]
                household_id_col = 'Household_ID' if 'Household_ID' in dv_persons.columns else 'household_id'
                household_ids = dv_persons[household_id_col].unique()
                persons_df = persons_df[persons_df[household_id_col].isin(household_ids)]
                households_df = households_df[households_df['household_id'].isin(household_ids)]
                applied_filters.append(f"DV Survivors: {filters['dv_survivors']}")
        
        # Display applied filters
        if applied_filters:
            st.info(f"🔍 **Active Filters:** {' | '.join(applied_filters)}")
        
        return persons_df, households_df
    
    def create_summary_metrics(self, persons_df: pd.DataFrame, households_df: pd.DataFrame):
        """Create enhanced summary metrics with visual indicators."""
        st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 15px; margin-bottom: 25px;">
                <h2 style="color: white; margin: 0; text-align: center;">📊 Key Metrics Overview</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Calculate metrics
        total_households = len(households_df)
        total_persons = len(persons_df)
        avg_household_size = total_persons / total_households if total_households > 0 else 0
        
        # Count children accurately - check both age_group and age_range
        children_count = 0
        
        # Method 1: Count from age_group
        if 'age_group' in persons_df.columns:
            children_count = len(persons_df[persons_df['age_group'] == 'child'])
        
        # Method 2: If age_group doesn't have children, check age_range directly
        if children_count == 0 and 'age_range' in persons_df.columns:
            children_count = len(persons_df[persons_df['age_range'] == 'Under 18'])
        
        # Method 3: If still 0, check Member_Type for children
        if children_count == 0 and 'Member_Type' in persons_df.columns:
            children_count = len(persons_df[persons_df['Member_Type'] == 'Child'])
            
        children_pct = (children_count / total_persons * 100) if total_persons > 0 else 0
        
        # Create metric cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; 
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
                    <h3 style="color: #1f77b4; margin: 0;">🏠 Total Households</h3>
                    <h1 style="color: #333; margin: 10px 0;">{format_number(total_households)}</h1>
                    <p style="color: #666; margin: 0;">Family units counted</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; 
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
                    <h3 style="color: #ff7f0e; margin: 0;">👥 Total Persons</h3>
                    <h1 style="color: #333; margin: 10px 0;">{format_number(total_persons)}</h1>
                    <p style="color: #666; margin: 0;">Individuals experiencing homelessness</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; 
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
                    <h3 style="color: #2ca02c; margin: 0;">📏 Avg Household Size</h3>
                    <h1 style="color: #333; margin: 10px 0;">{avg_household_size:.1f}</h1>
                    <p style="color: #666; margin: 0;">Persons per household</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; 
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;">
                    <h3 style="color: #d62728; margin: 0;">👶 Children</h3>
                    <h1 style="color: #333; margin: 10px 0;">{format_number(children_count)}</h1>
                    <p style="color: #666; margin: 0;">{children_pct:.1f}% of population</p>
                </div>
            """, unsafe_allow_html=True)
    
    def create_household_composition_chart(self, households_df: pd.DataFrame):
        """Create enhanced household composition donut chart."""
        if households_df.empty:
            return None
        
        household_counts = households_df['household_type'].value_counts()
        
        # Create donut chart
        fig = go.Figure(data=[go.Pie(
            labels=household_counts.index,
            values=household_counts.values,
            hole=.4,
            marker_colors=self.color_schemes['categorical'][:len(household_counts)]
        )])
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>' +
                         'Count: %{value}<br>' +
                         'Percentage: %{percent}<br>' +
                         '<extra></extra>'
        )
        
        fig.update_layout(
            title={
                'text': "Household Composition",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#333'}
            },
            showlegend=True,
            height=400,
            margin=dict(t=60, b=20, l=20, r=20)
        )
        
        # Add center text
        fig.add_annotation(
            text=f"{len(households_df)}<br>Households",
            x=0.5, y=0.5,
            font=dict(size=20, color="#666"),
            showarrow=False
        )
        
        return fig
    
    def create_age_distribution_chart(self, persons_df: pd.DataFrame):
        """Create enhanced age distribution chart with proper grouping."""
        if persons_df.empty:
            return None
        
        # Define age groups in order
        age_order = ['Under 18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
        age_colors = {
            'Under 18': '#FF6B6B',
            '18-24': '#4ECDC4',
            '25-34': '#45B7D1',
            '35-44': '#5C7CFA',
            '45-54': '#845EC2',
            '55-64': '#FFA502',
            '65+': '#FF6348'
        }
        
        # Count by age range
        age_data = []
        for age_range in age_order:
            count = len(persons_df[persons_df['age_range'] == age_range])
            if count > 0:
                age_data.append({
                    'Age Group': age_range,
                    'Count': count,
                    'Color': age_colors.get(age_range, '#999')
                })
        
        # Also check for children if age_range doesn't have 'Under 18'
        if not any(d['Age Group'] == 'Under 18' for d in age_data):
            # Check age_group column for children
            if 'age_group' in persons_df.columns:
                child_count = len(persons_df[persons_df['age_group'] == 'child'])
                if child_count > 0:
                    age_data.insert(0, {
                        'Age Group': 'Under 18',
                        'Count': child_count,
                        'Color': age_colors['Under 18']
                    })
        
        if not age_data:
            return None
        
        age_df = pd.DataFrame(age_data)
        
        # Create bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=age_df['Age Group'],
                y=age_df['Count'],
                marker_color=age_df['Color'],
                text=age_df['Count'],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>' +
                             'Count: %{y}<br>' +
                             'Percentage: %{customdata:.1f}%<br>' +
                             '<extra></extra>',
                customdata=(age_df['Count'] / age_df['Count'].sum() * 100)
            )
        ])
        
        fig.update_layout(
            title={
                'text': "Age Distribution",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#333'}
            },
            xaxis_title="Age Group",
            yaxis_title="Number of Persons",
            height=400,
            showlegend=False,
            xaxis={'tickangle': -45},
            yaxis={'gridcolor': '#f0f0f0'},
            plot_bgcolor='white'
        )
        
        return fig
    
    def create_gender_distribution_chart(self, persons_df: pd.DataFrame):
        """Create enhanced gender distribution chart."""
        if persons_df.empty or 'Gender' not in persons_df.columns:
            return None
        
        # Process gender data
        gender_data = []
        
        # Single gender selections
        single_gender = persons_df[persons_df['gender_count'] == 'one']
        gender_counts = single_gender['Gender'].value_counts()
        
        for gender, count in gender_counts.items():
            gender_data.append({
                'Gender': gender,
                'Count': count,
                'Type': 'Single Selection'
            })
        
        # Multiple gender selections
        multi_gender_count = len(persons_df[persons_df['gender_count'] == 'more'])
        if multi_gender_count > 0:
            gender_data.append({
                'Gender': 'Multiple Genders',
                'Count': multi_gender_count,
                'Type': 'Multiple Selection'
            })
        
        if not gender_data:
            return None
        
        gender_df = pd.DataFrame(gender_data)
        
        # Create horizontal bar chart
        fig = go.Figure()
        
        # Add bars for each type
        for gender_type in gender_df['Type'].unique():
            type_data = gender_df[gender_df['Type'] == gender_type]
            fig.add_trace(go.Bar(
                y=type_data['Gender'],
                x=type_data['Count'],
                name=gender_type,
                orientation='h',
                text=type_data['Count'],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>' +
                             'Count: %{x}<br>' +
                             'Type: ' + gender_type + '<br>' +
                             '<extra></extra>'
            ))
        
        fig.update_layout(
            title={
                'text': "Gender Identity Distribution",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#333'}
            },
            xaxis_title="Count",
            yaxis_title="Gender Identity",
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis={'gridcolor': '#f0f0f0'},
            plot_bgcolor='white',
            barmode='stack'
        )
        
        return fig
    
    def create_race_ethnicity_chart(self, persons_df: pd.DataFrame):
        """Create enhanced race/ethnicity distribution chart."""
        if persons_df.empty or 'race' not in persons_df.columns:
            return None
        
        # Get top 10 categories
        race_counts = persons_df['race'].value_counts().head(10)
        
        if race_counts.empty:
            return None
        
        # Create treemap for better visualization
        fig = go.Figure(go.Treemap(
            labels=race_counts.index,
            parents=[""] * len(race_counts),
            values=race_counts.values,
            text=[f"{label}<br>{count:,} ({count/race_counts.sum()*100:.1f}%)" 
                  for label, count in zip(race_counts.index, race_counts.values)],
            textinfo="text",
            marker=dict(
                colorscale='Viridis',
                line=dict(width=2, color='white')
            ),
            hovertemplate='<b>%{label}</b><br>' +
                         'Count: %{value}<br>' +
                         'Percentage: %{percentRoot}<br>' +
                         '<extra></extra>'
        ))
        
        fig.update_layout(
            title={
                'text': "Race/Ethnicity Distribution (Top 10)",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#333'}
            },
            height=500,
            margin=dict(t=60, b=20, l=20, r=20)
        )
        
        return fig
    
    def create_source_comparison_chart(self, persons_df: pd.DataFrame):
        """Create source comparison with household breakdown."""
        if persons_df.empty:
            return None
        
        source_stats = []
        household_id_col = 'Household_ID' if 'Household_ID' in persons_df.columns else 'household_id'
        
        for source in persons_df['source'].unique():
            source_data = persons_df[persons_df['source'] == source]
            
            # Calculate statistics
            # For CH: 0 for sheltered_TH, normal count for others
            # Check for case variations and partial matches
            ch_count = 0
            source_lower = source.lower()
            if 'CH' in source_data.columns and 'th' not in source_lower and 'transitional' not in source_lower:
                ch_count = len(source_data[source_data['CH'] == 'Yes'])
            
            # Count children - check multiple columns
            children_count = 0
            if 'age_group' in source_data.columns:
                children_count = len(source_data[source_data['age_group'] == 'child'])
            if children_count == 0 and 'age_range' in source_data.columns:
                children_count = len(source_data[source_data['age_range'] == 'Under 18'])
            if children_count == 0 and 'Member_Type' in source_data.columns:
                children_count = len(source_data[source_data['Member_Type'] == 'Child'])
            
            stats = {
                'Source': source,
                'Total Persons': len(source_data),
                'Total Households': source_data[household_id_col].nunique(),
                'Children': children_count,
                'Veterans': len(source_data[source_data['vet'] == 'Yes']) if 'vet' in source_data.columns else 0,
                'Chronically Homeless': ch_count
            }
            source_stats.append(stats)
        
        if not source_stats:
            return None
        
        stats_df = pd.DataFrame(source_stats)
        
        # Create grouped bar chart
        fig = go.Figure()
        
        categories = ['Total Persons', 'Total Households', 'Children', 'Veterans', 'Chronically Homeless']
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        
        for i, category in enumerate(categories):
            fig.add_trace(go.Bar(
                name=category,
                x=stats_df['Source'],
                y=stats_df[category],
                text=stats_df[category],
                textposition='outside',
                marker_color=colors[i],
                hovertemplate='<b>%{x}</b><br>' +
                             f'{category}: %{{y}}<br>' +
                             '<extra></extra>'
            ))
        
        fig.update_layout(
            title={
                'text': "Population Distribution by Data Source",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#333'}
            },
            xaxis_title="Data Source",
            yaxis_title="Count",
            barmode='group',
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            yaxis={'gridcolor': '#f0f0f0'},
            plot_bgcolor='white'
        )
        
        return fig
    
    def create_special_populations_metrics(self, persons_df: pd.DataFrame, households_df: pd.DataFrame):
        """Create special populations metrics with visual indicators."""
        if persons_df.empty:
            return
        
        st.markdown("""
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #333; margin-top: 0;">🎯 Special Populations</h3>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        household_id_col = 'Household_ID' if 'Household_ID' in persons_df.columns else 'household_id'
        
        with col1:
            # Chronically Homeless - Exclude sheltered_TH
            ch_count = 0
            ch_households = 0
            if 'CH' in persons_df.columns:
                # Only count CH from sources other than sheltered_TH (case insensitive)
                ch_persons = persons_df[
                    (persons_df['CH'] == 'Yes') & 
                    (~persons_df['source'].str.lower().str.contains('th', na=False)) &
                    (~persons_df['source'].str.lower().str.contains('transitional', na=False))
                ]
                ch_count = len(ch_persons)
                ch_households = ch_persons[household_id_col].nunique()
            
            ch_pct = (ch_count / len(persons_df) * 100) if len(persons_df) > 0 else 0
            
            st.markdown(f"""
                <div style="background-color: #fff3cd; padding: 15px; border-radius: 8px; 
                            border-left: 4px solid #ffc107; text-align: center;">
                    <h4 style="color: #856404; margin: 0;">🏥 Chronically Homeless</h4>
                    <h2 style="color: #333; margin: 10px 0;">{format_number(ch_count)}</h2>
                    <p style="color: #666; margin: 0;">{ch_pct:.1f}% of population</p>
                    <p style="color: #666; margin: 0; font-size: 0.9em;">{ch_households} households</p>
                    <p style="color: #999; margin: 5px 0 0 0; font-size: 0.8em;"><i>Excludes TH</i></p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Veterans
            vet_count = 0
            vet_households = 0
            if 'vet' in persons_df.columns:
                vet_persons = persons_df[persons_df['vet'] == 'Yes']
                vet_count = len(vet_persons)
                vet_households = vet_persons[household_id_col].nunique()
            
            vet_pct = (vet_count / len(persons_df) * 100) if len(persons_df) > 0 else 0
            
            st.markdown(f"""
                <div style="background-color: #d1ecf1; padding: 15px; border-radius: 8px; 
                            border-left: 4px solid #17a2b8; text-align: center;">
                    <h4 style="color: #0c5460; margin: 0;">🎖️ Veterans</h4>
                    <h2 style="color: #333; margin: 10px 0;">{format_number(vet_count)}</h2>
                    <p style="color: #666; margin: 0;">{vet_pct:.1f}% of population</p>
                    <p style="color: #666; margin: 0; font-size: 0.9em;">{vet_households} households</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # DV Survivors
            dv_count = 0
            dv_households = 0
            if 'DV' in persons_df.columns:
                dv_persons = persons_df[persons_df['DV'] == 'Yes']
                dv_count = len(dv_persons)
                dv_households = dv_persons[household_id_col].nunique()
            
            dv_pct = (dv_count / len(persons_df) * 100) if len(persons_df) > 0 else 0
            
            st.markdown(f"""
                <div style="background-color: #f8d7da; padding: 15px; border-radius: 8px; 
                            border-left: 4px solid #dc3545; text-align: center;">
                    <h4 style="color: #721c24; margin: 0;">🛡️ DV Survivors</h4>
                    <h2 style="color: #333; margin: 10px 0;">{format_number(dv_count)}</h2>
                    <p style="color: #666; margin: 0;">{dv_pct:.1f}% of population</p>
                    <p style="color: #666; margin: 0; font-size: 0.9em;">{dv_households} households</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Youth Households
            youth_hh_count = 0
            youth_persons = 0
            if 'youth' in households_df.columns:
                youth_households = households_df[households_df['youth'] == 'Yes']
                youth_hh_count = len(youth_households)
                # Count all persons in youth households
                youth_hh_ids = youth_households['household_id'].unique()
                youth_persons = len(persons_df[persons_df[household_id_col].isin(youth_hh_ids)])
            
            youth_hh_pct = (youth_hh_count / len(households_df) * 100) if len(households_df) > 0 else 0
            
            st.markdown(f"""
                <div style="background-color: #d4edda; padding: 15px; border-radius: 8px; 
                            border-left: 4px solid #28a745; text-align: center;">
                    <h4 style="color: #155724; margin: 0;">👶 Youth Households</h4>
                    <h2 style="color: #333; margin: 10px 0;">{format_number(youth_hh_count)}</h2>
                    <p style="color: #666; margin: 0;">{youth_hh_pct:.1f}% of households</p>
                    <p style="color: #666; margin: 0; font-size: 0.9em;">{youth_persons} persons</p>
                </div>
            """, unsafe_allow_html=True)
    
    def create_household_size_distribution(self, households_df: pd.DataFrame):
        """Create household size distribution chart."""
        if households_df.empty or 'total_persons' not in households_df.columns:
            return None
        
        # Get size distribution
        size_counts = households_df['total_persons'].value_counts().sort_index()
        
        # Group 5+ together
        size_data = []
        for size, count in size_counts.items():
            if size < 5:
                size_data.append({'Size': f"{size} person{'s' if size > 1 else ''}", 'Count': count, 'Order': size})
            else:
                existing_5plus = next((item for item in size_data if item['Size'] == '5+ persons'), None)
                if existing_5plus:
                    existing_5plus['Count'] += count
                else:
                    size_data.append({'Size': '5+ persons', 'Count': count, 'Order': 5})
        
        if not size_data:
            return None
        
        size_df = pd.DataFrame(size_data).sort_values('Order')
        
        # Create donut chart
        fig = go.Figure(data=[go.Pie(
            labels=size_df['Size'],
            values=size_df['Count'],
            hole=.4,
            marker_colors=px.colors.sequential.Blues_r[:len(size_df)]
        )])
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>' +
                         'Households: %{value}<br>' +
                         'Percentage: %{percent}<br>' +
                         '<extra></extra>'
        )
        
        fig.update_layout(
            title={
                'text': "Household Size Distribution",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#333'}
            },
            showlegend=True,
            height=400,
            margin=dict(t=60, b=20, l=20, r=20)
        )
        
        # Add center text
        avg_size = households_df['total_persons'].mean()
        fig.add_annotation(
            text=f"Avg: {avg_size:.1f}<br>persons",
            x=0.5, y=0.5,
            font=dict(size=18, color="#666"),
            showarrow=False
        )
        
        return fig
    
    def create_trends_chart(self, persons_df: pd.DataFrame):
        """Create a mock trends visualization (placeholder for future time-series data)."""
        # This is a placeholder for when time-series data is available
        st.info("📈 Trends analysis will be available when historical data is integrated.")
        
        # For now, show distribution by source as a proxy
        if 'source' in persons_df.columns:
            source_counts = persons_df.groupby('source').size().reset_index(name='Count')
            
            fig = go.Figure(data=[
                go.Scatter(
                    x=source_counts['source'],
                    y=source_counts['Count'],
                    mode='lines+markers',
                    line=dict(color='#1f77b4', width=3),
                    marker=dict(size=10),
                    fill='tozeroy',
                    fillcolor='rgba(31, 119, 180, 0.2)'
                )
            ])
            
            fig.update_layout(
                title={
                    'text': "Population by Data Source",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20, 'color': '#333'}
                },
                xaxis_title="Data Source",
                yaxis_title="Number of Persons",
                height=400,
                showlegend=False,
                yaxis={'gridcolor': '#f0f0f0'},
                plot_bgcolor='white'
            )
            
            return fig
        
        return None


def create_dashboard_interface():
    """Create the complete interactive dashboard with enhanced UI."""
    
    if not SessionManager.has_processed_data():
        st.info("📊 Please process data first to view the dashboard.")
        return
    
    # Dashboard header
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 15px; margin-bottom: 30px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h1 style="color: white; margin: 0; text-align: center; font-size: 2.5rem;">
                📊 Interactive PIT Count Dashboard
            </h1>
            <p style="color: #f0f0f0; margin: 10px 0 0 0; font-size: 1.2rem; text-align: center;">
                Explore and analyze your Point-in-Time count data with interactive visualizations
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize dashboard manager
    dashboard = DashboardManager()
    
    # Create filter controls
    filters = dashboard.create_filter_controls()
    
    if not filters:
        return
    
    # Apply filters
    filtered_persons, filtered_households = dashboard.apply_filters(filters)
    
    if filtered_persons.empty:
        st.warning("⚠️ No data matches the selected filters. Please adjust your filter criteria.")
        return
    
    # Summary metrics
    dashboard.create_summary_metrics(filtered_persons, filtered_households)
    
    # Special populations metrics
    dashboard.create_special_populations_metrics(filtered_persons, filtered_households)
    
    # Visualizations section
    st.markdown("""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h2 style="color: #333; margin-top: 0;">📈 Data Visualizations</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different visualization categories
    viz_tabs = st.tabs(["📊 Demographics", "🏠 Households", "📍 Sources", "📈 Analysis"])
    
    with viz_tabs[0]:  # Demographics
        col1, col2 = st.columns(2)
        
        with col1:
            # Age distribution
            age_chart = dashboard.create_age_distribution_chart(filtered_persons)
            if age_chart:
                st.plotly_chart(age_chart, use_container_width=True)
        
        with col2:
            # Gender distribution
            gender_chart = dashboard.create_gender_distribution_chart(filtered_persons)
            if gender_chart:
                st.plotly_chart(gender_chart, use_container_width=True)
        
        # Race/ethnicity (full width)
        race_chart = dashboard.create_race_ethnicity_chart(filtered_persons)
        if race_chart:
            st.plotly_chart(race_chart, use_container_width=True)
    
    with viz_tabs[1]:  # Households
        col1, col2 = st.columns(2)
        
        with col1:
            # Household composition
            household_chart = dashboard.create_household_composition_chart(filtered_households)
            if household_chart:
                st.plotly_chart(household_chart, use_container_width=True)
        
        with col2:
            # Household size distribution
            size_chart = dashboard.create_household_size_distribution(filtered_households)
            if size_chart:
                st.plotly_chart(size_chart, use_container_width=True)
    
    with viz_tabs[2]:  # Sources
        # Source comparison
        source_chart = dashboard.create_source_comparison_chart(filtered_persons)
        if source_chart:
            st.plotly_chart(source_chart, use_container_width=True)
    
    with viz_tabs[3]:  # Analysis
        # Trends placeholder
        trends_chart = dashboard.create_trends_chart(filtered_persons)
        if trends_chart:
            st.plotly_chart(trends_chart, use_container_width=True)
    
    # Data tables section
    st.markdown("""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h2 style="color: #333; margin-top: 0;">📋 Detailed Data Tables</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Data preview with better formatting
    with st.expander("🔍 View Filtered Data", expanded=False):
        data_tabs = st.tabs(["👥 Persons Data", "🏠 Households Data", "📊 Summary Statistics"])
        
        with data_tabs[0]:  # Persons
            if not filtered_persons.empty:
                st.info(f"Showing {min(100, len(filtered_persons))} of {len(filtered_persons)} persons")
                
                # Select key columns for display
                display_cols = []
                key_columns = ['source', 'Household_ID', 'household_id', 'Member_Type', 'Gender', 
                              'age_group', 'age_range', 'race', 'vet', 'DV', 'CH', 'household_type']
                
                for col in key_columns:
                    if col in filtered_persons.columns:
                        display_cols.append(col)
                
                # Configure display
                st.dataframe(
                    filtered_persons[display_cols].head(100),
                    use_container_width=True,
                    height=600,
                    column_config={
                        "Household_ID": st.column_config.NumberColumn("Household ID", format="%d"),
                        "household_id": st.column_config.NumberColumn("Household ID", format="%d"),
                        "Member_Type": "Member Type",
                        "age_group": "Age Group",
                        "age_range": "Age Range",
                        "household_type": "Household Type"
                    }
                )
                
                # Download button
                csv = filtered_persons.to_csv(index=False)
                st.download_button(
                    label="📥 Download Persons Data (CSV)",
                    data=csv,
                    file_name="filtered_persons_data.csv",
                    mime="text/csv"
                )
        
        with data_tabs[1]:  # Households
            if not filtered_households.empty:
                st.info(f"Showing {min(100, len(filtered_households))} of {len(filtered_households)} households")
                
                st.dataframe(
                    filtered_households.head(100),
                    use_container_width=True,
                    height=600,
                    column_config={
                        "household_id": st.column_config.NumberColumn("Household ID", format="%d"),
                        "total_persons": st.column_config.NumberColumn("Total Persons", format="%d"),
                        "household_type": "Household Type"
                    }
                )
                
                # Download button
                csv = filtered_households.to_csv(index=False)
                st.download_button(
                    label="📥 Download Households Data (CSV)",
                    data=csv,
                    file_name="filtered_households_data.csv",
                    mime="text/csv"
                )
        
        with data_tabs[2]:  # Summary Statistics
            # Create summary statistics
            summary_stats = {
                "Metric": [],
                "Value": [],
                "Percentage": []
            }
            
            total_persons = len(filtered_persons)
            total_households = len(filtered_households)
            
            # Basic counts
            summary_stats["Metric"].extend(["Total Households", "Total Persons"])
            summary_stats["Value"].extend([total_households, total_persons])
            summary_stats["Percentage"].extend(["-", "-"])
            
            # Age groups
            for age_group in ['child', 'youth', 'adult']:
                count = len(filtered_persons[filtered_persons['age_group'] == age_group])
                pct = (count / total_persons * 100) if total_persons > 0 else 0
                summary_stats["Metric"].append(f"{age_group.capitalize()}s")
                summary_stats["Value"].append(count)
                summary_stats["Percentage"].append(f"{pct:.1f}%")
            
            # Special populations
            if 'vet' in filtered_persons.columns:
                vet_count = len(filtered_persons[filtered_persons['vet'] == 'Yes'])
                vet_pct = (vet_count / total_persons * 100) if total_persons > 0 else 0
                summary_stats["Metric"].append("Veterans")
                summary_stats["Value"].append(vet_count)
                summary_stats["Percentage"].append(f"{vet_pct:.1f}%")
            
            # Chronically Homeless - exclude sheltered_TH
            if 'CH' in filtered_persons.columns:
                ch_count = len(filtered_persons[
                    (filtered_persons['CH'] == 'Yes') & 
                    (~filtered_persons['source'].str.lower().str.contains('th', na=False)) &
                    (~filtered_persons['source'].str.lower().str.contains('transitional', na=False))
                ])
                ch_pct = (ch_count / total_persons * 100) if total_persons > 0 else 0
                summary_stats["Metric"].append("Chronically Homeless (excl. TH)")
                summary_stats["Value"].append(ch_count)
                summary_stats["Percentage"].append(f"{ch_pct:.1f}%")
            else:
                summary_stats["Metric"].append("Chronically Homeless (excl. TH)")
                summary_stats["Value"].append(0)
                summary_stats["Percentage"].append("0.0%")
            
            summary_df = pd.DataFrame(summary_stats)
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
            
            # Download summary
            csv = summary_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Summary Statistics (CSV)",
                data=csv,
                file_name="summary_statistics.csv",
                mime="text/csv"
            )