"""
Report generation module for PIT Count Application
Generates all required reports with exact original structure
"""

import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Tuple, Optional, Any

from config import (
    REPORT_TEMPLATES, TEMPLATE_MAPPINGS, REPORT_COLUMNS,
    AGE_RANGES, SEX_CATEGORIES, GENDER_CATEGORIES, RACE_CATEGORIES,
    CONDITION_CATEGORIES, HOUSEHOLD_CATEGORIES
)

def generate_all_reports(processed_data: Dict[str, Dict[str, pd.DataFrame]]) -> Dict[str, Dict[str, pd.DataFrame]]:
    """Generate all PIT Count reports using exact original logic"""
    
    # Initialize report dictionaries
    all_reports = {
        'HDX_Totals': {},
        'HDX_Veterans': {},
        'HDX_Youth': {},
        'HDX_Subpopulations': {},
        'PIT Summary': {}
    }
    
    # Process each source
    for source_name in ["Sheltered_ES", "Sheltered_TH", "Unsheltered"]:
        source_data = processed_data.get(source_name)
        if not source_data or not isinstance(source_data, dict):
            continue

        source_persons = source_data.get('persons_df', pd.DataFrame())
        if source_persons is None or source_persons.empty:
            continue
        
        # Filter datasets by household type
        household_with_children = source_persons[
            source_persons['household_type'] == 'Household with Children'
        ]
        household_without_children = source_persons[
            source_persons['household_type'] == 'Household without Children'
        ]
        household_with_only_children = source_persons[
            source_persons['household_type'] == 'Household with Only Children'
        ]
        
        # HDX_Totals Reports
        calculate_and_store_stats(
            household_with_children, 
            "Households with at Least One Adult and One Child",
            all_reports['HDX_Totals'], 
            source_name, 
            REPORT_TEMPLATES['TOTAL_with'], 
            TEMPLATE_MAPPINGS['mapping_with']
        )
        
        calculate_and_store_stats(
            household_without_children, 
            "Households without Children",
            all_reports['HDX_Totals'], 
            source_name, 
            REPORT_TEMPLATES['TOTAL_without'], 
            TEMPLATE_MAPPINGS['mapping_without']
        )
        
        calculate_and_store_stats(
            household_with_only_children, 
            "Households with Only Children (under age 18)",
            all_reports['HDX_Totals'], 
            source_name, 
            REPORT_TEMPLATES['TOTAL_withonly'], 
            TEMPLATE_MAPPINGS['mapping_withonly']
        )
        
        calculate_and_store_stats(
            source_persons, 
            "Total Households and Persons",
            all_reports['HDX_Totals'], 
            source_name, 
            REPORT_TEMPLATES['TOTAL_with'], 
            TEMPLATE_MAPPINGS['mapping_with']
        )
        
        # HDX_Veterans Reports
        calculate_and_store_stats(
            household_with_children, 
            "Veteran Households with at Least One Adult and One Child",
            all_reports['HDX_Veterans'], 
            source_name, 
            REPORT_TEMPLATES['VET_with'], 
            TEMPLATE_MAPPINGS['mapping_vet_with'],
            'vet', 'Yes'
        )
        
        calculate_and_store_stats(
            household_without_children, 
            "Veteran Households without Children",
            all_reports['HDX_Veterans'], 
            source_name, 
            REPORT_TEMPLATES['VET_without'], 
            TEMPLATE_MAPPINGS['mapping_vet_without'],
            'vet', 'Yes'
        )
        
        calculate_and_store_stats(
            source_persons, 
            "Veteran Total Households and Persons",
            all_reports['HDX_Veterans'], 
            source_name, 
            REPORT_TEMPLATES['VET_with'], 
            TEMPLATE_MAPPINGS['mapping_vet_with'],
            'vet', 'Yes'
        )
        
        # HDX_Youth Reports
        # Unaccompanied youth
        unaccompanied_youth = source_persons.query("(count_child_hh == 0)") if 'count_child_hh' in source_persons.columns else source_persons
        calculate_and_store_stats(
            unaccompanied_youth, 
            "Unaccompanied Youth Households",
            all_reports['HDX_Youth'], 
            source_name, 
            REPORT_TEMPLATES['YOUTH_without'], 
            TEMPLATE_MAPPINGS['mapping_youth_without'],
            'youth', 'Yes'
        )
        
        # Parenting youth
        parenting_youth = household_with_children.query("(Member_Type == 'Adult')") if 'Member_Type' in household_with_children.columns else household_with_children
        calculate_and_store_stats(
            parenting_youth, 
            "Parenting Youth Households",
            all_reports['HDX_Youth'], 
            source_name, 
            REPORT_TEMPLATES['YOUTH_with'], 
            TEMPLATE_MAPPINGS['mapping_youth_with'],
            'youth', 'Yes'
        )
        
        # HDX_Subpopulations
        adults_and_youth = source_persons.query("(age_group.isin(['adult', 'youth']))") if 'age_group' in source_persons.columns else source_persons
        calculate_and_store_stats(
            adults_and_youth, 
            "Homeless Subpopulations",
            all_reports['HDX_Subpopulations'], 
            source_name, 
            REPORT_TEMPLATES['INDEX_SUB'], 
            TEMPLATE_MAPPINGS['mapping_SUB']
        )
        
        # PIT Summary
        calculate_and_store_stats(
            source_persons, 
            "PIT Summary",
            all_reports['PIT Summary'], 
            source_name, 
            REPORT_TEMPLATES['TOTAL_Summary'], 
            TEMPLATE_MAPPINGS['mapping_Summary']
        )
    
    # Calculate totals for all reports
    for report_type, reports in all_reports.items():
        for report_name, report_df in reports.items():
            if not report_df.empty:
                numeric_columns = ['Sheltered_ES', 'Sheltered_TH', 'Unsheltered']
                report_df[numeric_columns] = report_df[numeric_columns].apply(
                    pd.to_numeric, errors='coerce'
                ).fillna(0)
                report_df['Total'] = report_df[numeric_columns].sum(axis=1)
    
    return all_reports

def calculate_and_store_stats(input_df: pd.DataFrame, name: str, stored_dfs: Dict,
                             column_name: str, index_tuples: List[Tuple[str, str]], 
                             mapping: List[Tuple[Tuple[str, str], str]], 
                             condition_column: Optional[str] = None, 
                             condition: Optional[str] = None):
    """Calculate and store statistics for a report"""
    
    # Calculate summary statistics
    summary_stats = calculate_summary_stats(input_df, condition_column, condition)
    
    # Create empty template if not exists
    if name not in stored_dfs:
        stored_dfs[name] = get_empty_template(index_tuples)
    
    # Populate template
    populate_template(stored_dfs[name], summary_stats, mapping, column_name)

def get_empty_template(index_tuples: List[Tuple[str, str]]) -> pd.DataFrame:
    """Create empty template with MultiIndex"""
    return pd.DataFrame(0, index=pd.MultiIndex.from_tuples(index_tuples), columns=REPORT_COLUMNS)

def populate_template(df_template: pd.DataFrame, summary_stats: Dict[str, Any], 
                     mapping: List[Tuple[Tuple[str, str], str]], column_name: str):
    """Populate template with calculated statistics"""
    
    for index_tuple, key in mapping:
        # Special conditions for 'Sheltered_TH' column
        special_conditions = [
            (("Chronically Homeless", "Total number of households"), 'CH_Total_number_of_households'),
            (("Chronically Homeless", "Total number of persons"), 'CH_Total_number_of_persons')
        ]
        
        if column_name == "Sheltered_TH" and (index_tuple, key) in special_conditions:
            df_template.at[index_tuple, column_name] = 0  # Override with 0
        elif key in summary_stats:
            df_template.at[index_tuple, column_name] = summary_stats[key]
        else:
            df_template.at[index_tuple, column_name] = 'N/A'

@st.cache_data
def calculate_summary_stats(df: pd.DataFrame, condition_column: Optional[str] = None, 
                           condition: Optional[str] = None) -> Dict[str, Any]:
    """Calculate summary statistics - exact copy from original"""
    
    summary_stats = {}
    
    try:
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input is not a pandas DataFrame.")
        
        # Optional filtering based on condition
        if condition_column and condition:
            if condition_column not in df.columns:
                raise ValueError(f"'{condition_column}' column is missing in the DataFrame.")
            df = df[df[condition_column] == condition]
        
        unique_households_df = df.drop_duplicates(subset='Household_ID')
        
        # Calculate all statistics
        summary_stats.update(calculate_basic_counts(df, unique_households_df))
        summary_stats.update(calculate_household_composition(df, unique_households_df))
        summary_stats.update(calculate_demographic_info(df, unique_households_df))
        summary_stats.update(calculate_youth_numbers(df, unique_households_df))
        summary_stats.update(calculate_history_homelessness(df, unique_households_df))
        
        return summary_stats
        
    except Exception as e:
        st.error(f"Error in calculate_summary_stats: {e}")
        return {}

def calculate_basic_counts(df: pd.DataFrame, unique_households_df: pd.DataFrame) -> Dict[str, int]:
    """Calculate basic counts"""
    result = {
        'Total_number_of_households': df['Household_ID'].nunique(),
        'Total_number_of_persons': unique_households_df['total_person_in_household'].sum(),
    }
    
    for household, key in HOUSEHOLD_CATEGORIES.items():
        result[key] = unique_households_df[
            unique_households_df['household_type'] == household
        ].shape[0]
    
    return result

def calculate_household_composition(df: pd.DataFrame, unique_households_df: pd.DataFrame) -> Dict[str, int]:
    """Calculate household composition statistics"""
    result = {}
    
    # Household sizes
    for n in range(2, 5):
        result[f'Households_{n}_members'] = unique_households_df[
            (unique_households_df['household_type'] == 'Household with Children') & 
            (unique_households_df['total_person_in_household'] == n)
        ].shape[0]
    
    result['Households_5+_members'] = unique_households_df[
        (unique_households_df['household_type'] == 'Household with Children') & 
        (unique_households_df['total_person_in_household'] >= 5)
    ].shape[0]
    
    # Age groups
    result['Number_of_children'] = unique_households_df[['count_child_hh', 'count_child_hoh']].sum().sum()
    result['Number_of_young_adults'] = unique_households_df['count_youth'].sum()
    
    for age_range in AGE_RANGES:
        result[f'Number_of_adults_{age_range.replace("-", "-")}'] = df[
            df['age_range'] == age_range
        ].shape[0]
    
    result['Unreported_Age'] = df[
        (df['Member_Type'] == 'Adult') & (pd.isnull(df['age_range']))
    ].shape[0]
    
    return result

def calculate_demographic_info(df: pd.DataFrame, unique_households_df: pd.DataFrame) -> Dict[str, int]:
    """Calculate demographic information"""
    
    # Check for source column to exclude TH from CH counts
    if 'source' in df.columns:
        ch_mask = (
            (df['CH'] == 'Yes') & 
            (~df['source'].str.lower().str.contains('th', na=False)) &
            (~df['source'].str.lower().str.contains('transitional', na=False))
        )
        ch_persons = df[ch_mask]
        ch_households = ch_persons['Household_ID'].nunique()
        ch_persons_count = ch_persons.drop_duplicates(subset='Household_ID')['total_person_in_household'].sum()
    else:
        ch_persons = df[df['CH'] == 'Yes']
        ch_households = ch_persons['Household_ID'].nunique()
        ch_persons_count = ch_persons.drop_duplicates(subset='Household_ID')['total_person_in_household'].sum()
    
    result = {
        'Total number of veterans': df[df['vet'] == 'Yes'].shape[0],
        'CH_Total_number_of_households': ch_households,
        'CH_Total_number_of_persons': ch_persons_count,
        'Victims_of_Domestic_Violence_(fleeing)': df[df['DV'] == 'Yes'].shape[0],
        'Victims_of_Domestic_Violence_(Household)': df[df['DV'] == 'Yes']['Household_ID'].nunique(),
        'More_Than_One_Gender': df[df['gender_count'] == 'more'].shape[0]
    }
    
    # Condition statistics
    for condition, key in CONDITION_CATEGORIES.items():
        result[f'Adults_with_a_{key}'] = df[
            (df['chronic_condition'].str.contains(condition, na=False, regex=False)) & 
            (df['age_group'].isin(['adult', 'youth']))
        ].shape[0]
        
        result[f'childs_with_a_{key}'] = df[
            (df['chronic_condition'].str.contains(condition, na=False, regex=False)) & 
            (df['age_group'].isin(['child', 'unknown']))
        ].shape[0]
    
    # Sex statistics (required field)
    for sex, key in SEX_CATEGORIES.items():
        result[key] = df[df['Sex'] == sex].shape[0]

    # Gender statistics (optional field)
    for gender, key in GENDER_CATEGORIES.items():
        result[key] = df[
            (df['gender_count'] == 'one') & (df['Gender'] == gender)
        ].shape[0]

        result[f'Includes_{key}'] = df[
            (df['gender_count'] == 'more') &
            (df['Gender'].str.contains(gender, na=False, regex=False))
        ].shape[0]

    # Race statistics
    for race, key in RACE_CATEGORIES.items():
        result[key] = df[df['race'] == race].shape[0]

    return result

def calculate_youth_numbers(df: pd.DataFrame, unique_households_df: pd.DataFrame) -> Dict[str, int]:
    """Calculate youth-specific statistics"""
    return {
        'Total_Parenting_Youth': df[
            (df['youth'] == 'Yes') & (df['Member_Type'] == 'Adult')
        ].shape[0],
        'Total_Parenting_Youth_hh': unique_households_df[
            (unique_households_df['youth'] == 'Yes') & 
            (unique_households_df['Member_Type'] == 'Adult') & 
            (unique_households_df['household_type'] == 'Household with Children')
        ].shape[0],
        'Total_Unaccompanied_Youth_hh': df[
            (df['youth'] == 'Yes') & 
            (df['Member_Type'] == 'Adult') & 
            (df['count_child_hh'] == 0)
        ]['Household_ID'].nunique(),
        'Number_of_parenting_youth_under_age_18': df[
            (df['Member_Type'] == 'Adult') & (df['age_group'] == 'child')
        ].shape[0],
        'Children_with_parenting_youth_under_18': unique_households_df[
            unique_households_df['age_group'] == 'child'
        ]['count_child_hh'].sum(),
        'Number_of_parenting_youth_18_24': df[
            (df['Member_Type'] == 'Adult') & (df['age_group'] == 'youth')
        ].shape[0],
        'Children_with_parenting_youth_18_24': unique_households_df[
            unique_households_df['age_group'] == 'youth'
        ]['count_child_hh'].sum(),
    }

def calculate_history_homelessness(df: pd.DataFrame, unique_households_df: pd.DataFrame) -> Dict[str, int]:
    """Calculate homelessness history statistics"""
    
    def sum_total_persons(condition):
        return unique_households_df[condition]['total_person_in_household'].sum()
    
    def count_households(condition):
        return unique_households_df[condition].shape[0]
    
    # Define conditions
    first_time_condition = unique_households_df['first_time'] == 'Yes'
    
    less_than_one_month_conditions = (
        unique_households_df['specific_homeless_long'].isin([
            '1 day or less', '2 days - 1 week', 'More than 1 week - Less than 1 month'
        ]) | 
        unique_households_df['specific_homeless_long_this_time'].isin([
            '1 day or less', '2 days - 1 week', 'More than 1 week - Less than 1 month'
        ])
    )
    
    one_to_three_months_condition = (
        unique_households_df['specific_homeless_long'].isin(['1-3 Months']) | 
        unique_households_df['specific_homeless_long_this_time'].isin(['1-3 Months'])
    )
    
    three_months_to_one_year_condition = (
        unique_households_df['specific_homeless_long'].isin(['More than 3 months - Less than 1 year']) | 
        unique_households_df['specific_homeless_long_this_time'].isin(['More than 3 months - Less than 1 year'])
    )
    
    one_year_or_more_condition = (
        unique_households_df['specific_homeless_long'].isin(['1 year or more']) | 
        unique_households_df['specific_homeless_long_this_time'].isin(['1 year or more'])
    )
    
    return {
        'History_First_Time_Homeless': sum_total_persons(first_time_condition),
        'History_Less_than_One_Month': sum_total_persons(less_than_one_month_conditions),
        'History_One_to_Three_Months': sum_total_persons(one_to_three_months_condition),
        'History_Three_Months_to_One_Year': sum_total_persons(three_months_to_one_year_condition),
        'History_One_Year_or_More': sum_total_persons(one_year_or_more_condition),
        
        'History_HHs_First_Time_Homeless': count_households(first_time_condition),
        'History_HHs_Less_than_One_Month': count_households(less_than_one_month_conditions),
        'History_HHs_One_to_Three_Months': count_households(one_to_three_months_condition),
        'History_HHs_Three_Months_to_One_Year': count_households(three_months_to_one_year_condition),
        'History_HHs_One_Year_or_More': count_households(one_year_or_more_condition),
    }