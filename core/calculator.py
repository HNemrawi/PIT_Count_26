"""
Complete Statistics calculation engine for PIT Count application.
Updated to match exact original calculate_stats.py and template_mapping.py logic.
"""

import pandas as pd
import streamlit as st
from typing import Dict, List, Any, Optional, Tuple
import numpy as np

from config.templates import (
    ReportType, get_report_template, COLUMN,
    TOTAL_with, TOTAL_without, TOTAL_withonly,
    VET_with, VET_without, YOUTH_without, YOUTH_with,
    INDEX_SUB, TOTAL_Summary
)
from config.template_mappings import get_all_mappings
from config.categories import age_ranges,household_categories,gender_categories,race_categories,condition_categories
from core.validator import DataValidator

class OriginalStatisticsCalculator:
    """Calculates statistics using exact original logic from calculate_stats.py"""
    def __init__(self, processed_data: Dict[str, Dict[str, pd.DataFrame]]):
        """Initialize calculator with processed data."""
        self.processed_data = processed_data
        self.full_persons_df = pd.DataFrame()
        self.current_full_persons = pd.DataFrame()
    
    def calculate_basic_counts(self, df: pd.DataFrame, unique_households_df: pd.DataFrame) -> Dict[str, int]:
        """Calculate basic counts - exact copy from original calculate_stats.py"""
        result = {
            'Total_number_of_households': df['Household_ID'].nunique(),
            'Total_number_of_persons': unique_households_df['total_person_in_household'].sum(),
        }
        
        for household, key in household_categories.items():
            result[key] = unique_households_df[unique_households_df['household_type'] == household].shape[0]
        
        return result

    def calculate_household_composition(self, df: pd.DataFrame, unique_households_df: pd.DataFrame) -> Dict[str, int]:
        """Calculate household composition - exact copy from original calculate_stats.py"""        
        result = {}
        
        for n in range(2, 5):
            result[f'Households_{n}_members'] = unique_households_df[
                (unique_households_df['household_type'] == 'Household with Children') & 
                (unique_households_df['total_person_in_household'] == n)
            ].shape[0]
        
        result['Households_5+_members'] = unique_households_df[
            (unique_households_df['household_type'] == 'Household with Children') & 
            (unique_households_df['total_person_in_household'] >= 5)
        ].shape[0]
        
        result['Number_of_children'] = unique_households_df[['count_child_hh', 'count_child_hoh']].sum().sum()
        result['Number_of_young_adults'] = unique_households_df['count_youth'].sum()
        
        for age_range in age_ranges:
            result[f'Number_of_adults_{age_range.replace("-", "-")}'] = df[df['age_range'] == age_range].shape[0]
        
        result['Unreported_Age'] = df[(df['Member_Type'] == 'Adult') & (pd.isnull(df['age_range']))].shape[0]
        
        return result

    def calculate_demographic_info(self, df: pd.DataFrame, unique_households_df: pd.DataFrame) -> Dict[str, int]:
        """Calculate demographic info - FIXED to exclude TH from CH counts"""
 
        # Check if source column exists, use it if available
        if 'source' in df.columns:
            # Exclude TH sources from CH calculation
            ch_mask = (
                (df['CH'] == 'Yes') & 
                (~df['source'].str.lower().str.contains('th', na=False)) &
                (~df['source'].str.lower().str.contains('transitional', na=False))
            )
            ch_persons = df[ch_mask]
            ch_households = ch_persons['Household_ID'].nunique()
            ch_persons_count = ch_persons.drop_duplicates(subset='Household_ID')['total_person_in_household'].sum()
        else:
            # Fallback to original logic if no source column
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
        for condition, key in condition_categories.items():
            result[f'Adults_with_a_{key}'] = df[
                (df['chronic_condition'].str.contains(condition, na=False, regex=False)) & 
                (df['age_group'].isin(['adult', 'youth']))
            ].shape[0]
            
            result[f'childs_with_a_{key}'] = df[
                (df['chronic_condition'].str.contains(condition, na=False, regex=False)) & 
                (df['age_group'].isin(['child', 'unknown']))
            ].shape[0]
        
        # Gender statistics
        for gender, key in gender_categories.items():
            result[key] = df[
                (df['gender_count'] == 'one') & (df['Gender'] == gender)
            ].shape[0]
            
            result[f'Includes_{key}'] = df[
                (df['gender_count'] == 'more') & 
                (df['Gender'].str.contains(gender, na=False, regex=False))
            ].shape[0]
        
        # Race statistics
        for race, key in race_categories.items():
            result[key] = df[df['race'] == race].shape[0]
        
        return result

    def calculate_youth_numbers(self, df: pd.DataFrame, unique_households_df: pd.DataFrame) -> Dict[str, int]:
        """Calculate youth statistics - exact copy from original calculate_stats.py"""
        return {
            'Total_Parenting_Youth': df[(df['youth'] == 'Yes') & (df['Member_Type'] == 'Adult')].shape[0],
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

    def calculate_history_homelessness(self, df: pd.DataFrame, unique_households_df: pd.DataFrame) -> Dict[str, int]:
        """Calculate homelessness history - exact copy from original calculate_stats.py"""
        def sum_total_persons(condition):
            return unique_households_df[condition]['total_person_in_household'].sum()

        def count_households(condition):
            return unique_households_df[condition].shape[0]

        first_time_condition = unique_households_df['first_time'] == 'Yes'
        less_than_one_month_conditions = (
            unique_households_df['specific_homeless_long'].isin(['1 day or less', '2 days - 1 week', 'More than 1 week - Less than 1 month']) | 
            unique_households_df['specific_homeless_long_this_time'].isin(['1 day or less', '2 days - 1 week', 'More than 1 week - Less than 1 month'])
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

    @st.cache_data
    def calculate_summary_stats(_self, df: pd.DataFrame, condition_column: Optional[str] = None, condition: Optional[str] = None) -> Dict[str, Any]:
        """Calculate summary statistics - exact copy from original calculate_stats.py"""
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

            # List of calculation functions
            calculations = [
                (_self.calculate_basic_counts, "Basic Counts"),
                (_self.calculate_household_composition, "Household Composition"),
                (_self.calculate_demographic_info, "Demographic Info"),
                (_self.calculate_youth_numbers, "Youth Numbers"),
                (_self.calculate_history_homelessness, "History of Homelessness")
            ]

            # Perform each calculation
            for calc_func, description in calculations:
                try:
                    summary_stats.update(calc_func(df, unique_households_df))
                except Exception as e:
                    st.error(f"Error in {description}: {e}")

            return summary_stats

        except Exception as e:
            st.error(f"Error in setting up calculate_summary_stats: {e}")
            return {}


class StatisticsCalculator:
    """Updated calculator that uses original logic with exact template matching."""
    
    def __init__(self, processed_data: Dict[str, Dict[str, pd.DataFrame]]):
        """Initialize calculator with processed data."""
        self.processed_data = processed_data
        self.original_calc = OriginalStatisticsCalculator(processed_data)
        
        # Get combined data for calculations
        combined_data = processed_data.get('combined', {})
        self.combined_persons = combined_data.get('persons_df', pd.DataFrame())
        self.combined_households = combined_data.get('households_df', pd.DataFrame())
        
    def get_empty_template(self, index_tuples: List[Tuple[str, str]]) -> pd.DataFrame:
        """Create empty template - exact copy from original populate_temp.py"""
        return pd.DataFrame(0, index=pd.MultiIndex.from_tuples(index_tuples), columns=COLUMN)

    def populate_template(self, df_template: pd.DataFrame, summary_stats: Dict[str, Any], 
                         mapping: List[Tuple[Tuple[str, str], str]], column_name: str):
        """Populate template - exact copy from original populate_temp.py"""
        for index_tuple, key in mapping:
            # Special conditions for 'Sheltered_TH' column - exact from original
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

    def calculate_and_store_stats(self, input_df: pd.DataFrame, name: str, stored_dfs: Dict[str, pd.DataFrame], 
                                 column_name: str, index_tuples: List[Tuple[str, str]], 
                                 mapping: List[Tuple[Tuple[str, str], str]], 
                                 condition_column: Optional[str] = None, condition: Optional[str] = None):
        """Calculate and store stats - exact copy from original populate_temp.py"""
        summary_stats = self.original_calc.calculate_summary_stats(input_df, condition_column, condition)
        if name not in stored_dfs:
            stored_dfs[name] = self.get_empty_template(index_tuples)
        self.populate_template(stored_dfs[name], summary_stats, mapping, column_name)

    def generate_all_reports(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """Generate all PIT Count reports using exact original handle_tabs logic."""
        
        if self.combined_persons.empty:
            st.error("No processed data available for report generation")
            return {}
        
        st.subheader("Generating Reports using Original Logic")
        
        # Initialize report dictionaries exactly like original session state
        all_reports = {
            'HDX_Totals': {},
            'HDX_Veterans': {},
            'HDX_Youth': {},
            'HDX_Subpopulations': {},
            'PIT Summary': {}
        }
        
        # Get all mappings from the new module
        mappings = get_all_mappings()
        
        # Process each source exactly like original handle_tabs_for_households
        for source_name in ["Sheltered_ES", "Sheltered_TH", "Unsheltered"]:
            source_data = self.processed_data.get(source_name)
            if source_data is None:
                continue
                
            source_persons = source_data.get('persons_df', pd.DataFrame())
            if source_persons.empty:
                continue
            
            # Filter datasets by household type - exact like original
            household_with_children = source_persons[source_persons['household_type'] == 'Household with Children']
            household_without_children = source_persons[source_persons['household_type'] == 'Household without Children'] 
            household_with_only_children = source_persons[source_persons['household_type'] == 'Household with Only Children']
            
            # HDX_Totals Reports - exact original handle_tab calls
            self.calculate_and_store_stats(
                household_with_children, "Households with at Least One Adult and One Child",
                all_reports['HDX_Totals'], source_name, TOTAL_with, mappings["mapping_with"]
            )
            
            self.calculate_and_store_stats(
                household_without_children, "Households without Children", 
                all_reports['HDX_Totals'], source_name, TOTAL_without, mappings["mapping_without"]
            )
            
            self.calculate_and_store_stats(
                household_with_only_children, "Households with Only Children (under age 18)",
                all_reports['HDX_Totals'], source_name, TOTAL_withonly, mappings["mapping_withonly"]
            )
            
            self.calculate_and_store_stats(
                source_persons, "Total Households and Persons",
                all_reports['HDX_Totals'], source_name, TOTAL_with, mappings["mapping_with"]
            )
            
            # HDX_Veterans Reports - exact original handle_tab calls
            self.calculate_and_store_stats(
                household_with_children, "Veteran Households with at Least One Adult and One Child",
                all_reports['HDX_Veterans'], source_name, VET_with, mappings["mapping_vet_with"],
                'vet', 'Yes'
            )
            
            self.calculate_and_store_stats(
                household_without_children, "Veteran Households without Children",
                all_reports['HDX_Veterans'], source_name, VET_without, mappings["mapping_vet_without"],
                'vet', 'Yes'
            )
            
            self.calculate_and_store_stats(
                source_persons, "Veteran Total Households and Persons",
                all_reports['HDX_Veterans'], source_name, VET_with, mappings["mapping_vet_with"],
                'vet', 'Yes'
            )
            
            # HDX_Youth Reports - exact original handle_tab calls
            self.calculate_and_store_stats(
                source_persons, "Unaccompanied Youth Households",
                all_reports['HDX_Youth'], source_name, YOUTH_without, mappings["mapping_youth_without"],
                'youth', 'Yes'
            )
            
            # Apply filter for unaccompanied (count_child_hh == 0)
            unaccompanied_youth = source_persons.query("(count_child_hh == 0)") if 'count_child_hh' in source_persons.columns else source_persons
            self.calculate_and_store_stats(
                unaccompanied_youth, "Unaccompanied Youth Households",
                all_reports['HDX_Youth'], source_name, YOUTH_without, mappings["mapping_youth_without"],
                'youth', 'Yes'
            )
            
            # Parenting youth - filter for adults only
            parenting_youth = household_with_children.query("(Member_Type == 'Adult')") if 'Member_Type' in household_with_children.columns else household_with_children
            self.calculate_and_store_stats(
                parenting_youth, "Parenting Youth Households",
                all_reports['HDX_Youth'], source_name, YOUTH_with, mappings["mapping_youth_with"],
                'youth', 'Yes'
            )
            
            # HDX_Subpopulations - exact original handle_tab call
            adults_and_youth = source_persons.query("(age_group.isin(['adult', 'youth']))") if 'age_group' in source_persons.columns else source_persons
            self.calculate_and_store_stats(
                adults_and_youth, "Homeless Subpopulations",
                all_reports['HDX_Subpopulations'], source_name, INDEX_SUB, mappings["mapping_SUB"]
            )
            
            # PIT Summary - exact original handle_tab call
            self.calculate_and_store_stats(
                source_persons, "PIT Summary",
                all_reports['PIT Summary'], source_name, TOTAL_Summary, mappings["mapping_Summary"]
            )
        
        # Calculate totals for all reports - exact like original
        for report_type, reports in all_reports.items():
            for report_name, report_df in reports.items():
                if not report_df.empty:
                    numeric_columns = ['Sheltered_ES', 'Sheltered_TH', 'Unsheltered']
                    report_df[numeric_columns] = report_df[numeric_columns].apply(pd.to_numeric, errors='coerce').fillna(0)
                    report_df['Total'] = report_df[numeric_columns].sum(axis=1)
        
        st.success("All reports generated successfully using original logic!")
        return all_reports


def create_calculation_interface(processed_data: Dict[str, Dict[str, pd.DataFrame]]) -> Dict[str, Dict[str, pd.DataFrame]]:
   """Create the statistics calculation interface using original logic."""
   
   if not processed_data:
       st.info("Please process data first.")
       return {}
   
   st.header("Statistics Calculation")
   
   # Initialize calculator
   calculator = StatisticsCalculator(processed_data)
   
   # Generate all reports
   with st.spinner("Calculating statistics using original logic..."):
       all_reports = calculator.generate_all_reports()
   
   # Store in session state
   st.session_state['calculated_reports'] = all_reports
   
   # Display report summary
   st.subheader("Report Generation Summary")
   
   summary_data = []
   for report_type, reports in all_reports.items():
       for report_name, report_df in reports.items():
           non_zero_values = (report_df.select_dtypes(include=[np.number]) != 0).sum().sum()
           total_values = report_df.select_dtypes(include=[np.number]).size
           
           summary_data.append({
               'Report Type': report_type,
               'Report Name': report_name,
               'Rows': len(report_df),
               'Non-Zero Values': non_zero_values,
               'Total Values': total_values,
               'Data Coverage': f"{(non_zero_values/total_values*100):.1f}%" if total_values > 0 else "0%"
           })
   
   if summary_data:
       summary_df = pd.DataFrame(summary_data)
       st.dataframe(summary_df, use_container_width=True)
   else:
       st.warning("No reports were generated.")
   
   return all_reports