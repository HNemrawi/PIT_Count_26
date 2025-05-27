"""
Core data processing functionality for PIT Count application.
Simplified to run in background without display.
"""

import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Tuple
import warnings

from config.mappings import ColumnMappings, condition_mapping

# Disable pandas warnings
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)

class DataProcessor:
    """Processes raw PIT survey data into standardized format using original logic."""
    
    def __init__(self, region: str):
        """Initialize processor with region-specific mappings."""
        self.region = region
        self.column_mapping = ColumnMappings.get_mapping_for_region(region)
    
    def preprocess_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Renames specified columns in a DataFrame based on a mapping and retains only those columns."""
        # Strip whitespace from column names and remove duplicate columns
        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.duplicated(keep='first')]

        # Filter and rename valid columns
        valid_columns = {k: v for k, v in self.column_mapping.items() if k in df.columns}
        df = df[valid_columns.keys()]
        df.rename(columns=valid_columns, inplace=True)

        return df
    
    def initialize_count_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Initialize count columns for different age groups in the DataFrame."""
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input is not a pandas DataFrame.")

        age_group_columns = ['count_adult', 'count_youth', 'count_child_hoh', 'count_child_hh']
        for column in age_group_columns:
            df[column] = 0

        return df
    
    def update_age_group_counts(self, df: pd.DataFrame, age_related_cols: List[str], child_related_cols: List[str]) -> pd.DataFrame:
        """Update count columns based on age group categories present in the DataFrame."""
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input is not a pandas DataFrame.")

        adult_ages = ['25-34', '35-44', '45-54', '55-64', '65+']
        youth_ages = ['18-24']
        child_age = ['Under 18']

        for col in age_related_cols:
            if col not in df.columns:
                continue

            df[col] = df[col].fillna('')
            df['count_adult'] += df[col].isin(adult_ages).astype(int)
            df['count_youth'] += df[col].isin(youth_ages).astype(int)
            df['count_child_hoh'] += df[col].isin(child_age).astype(int)

        for col in child_related_cols:
            if col not in df.columns:
                continue

            df[col] = df[col].fillna('No')
            df['count_child_hh'] += (df[col] == 'Yes').astype(int)

        return df
    
    def count_age_groups(self, df: pd.DataFrame) -> pd.DataFrame:
        """Count the number of adults, youth, and children in each household."""
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input is not a pandas DataFrame.")

        age_related_cols = [col for col in ['age_range', 'adult_2_age_range', 'adult_3_age_range', 'adult_4_age_range'] if col in df.columns]
        child_related_cols = [f'child_{i}' for i in range(1, 7) if f'child_{i}' in df.columns]

        df = self.initialize_count_columns(df)
        df = self.update_age_group_counts(df, age_related_cols, child_related_cols)

        df['total_person_in_household'] = df['count_adult'] + df['count_youth'] + df['count_child_hoh'] + df['count_child_hh']
        df['youth'] = df['count_adult'].apply(lambda x: 'Yes' if x == 0 else 'No')

        return df
    
    def classify_household_type(self, df: pd.DataFrame) -> pd.DataFrame:
        """Classify the household based on the age groups present."""
        required_columns = ['count_adult', 'count_youth', 'count_child_hh', 'count_child_hoh']
        if not all(column in df.columns for column in required_columns):
            missing_cols = [col for col in required_columns if col not in df.columns]
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

        # Define conditions for classifying households
        has_adults_or_youth = df['count_adult'] + df['count_youth'] > 0
        has_children = df['count_child_hh'] > 0
        only_children = df['count_child_hoh'] > 0

        # Set up the conditions and choices for classification
        conditions = [
            has_adults_or_youth & has_children,
            has_adults_or_youth & ~has_children,
            only_children
        ]
        choices = ['Household with Children', 'Household without Children', 'Household with Only Children']
        
        # Apply conditions to classify households
        df['household_type'] = np.select(conditions, choices, default='Unknown')

        return df
    
    def flatten_entire_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
            """Transforms a household-based DataFrame into a member-based DataFrame."""
            if not isinstance(df, pd.DataFrame):
                raise ValueError("Input is not a pandas DataFrame.")

            # Reset index and create a Household_ID column
            df.reset_index(drop=True, inplace=True)
            df['Household_ID'] = df.index + 1

            def create_member(row, member_type, member_number):
                """Create a dictionary representing a member with household and individual attributes."""
                # Set prefix based on member type and define columns
                prefix = f'child_{member_number}_' if member_type == 'Child' else (f'adult_{member_number}_' if member_number != 1 else '')
                member_attrs = ['Gender', 'Race/Ethnicity', 'age_range', 'DV', 'vet', 'chronic_condition', 'disability', 'first_time', 'homeless_long', 'homeless_long_this_time', 'homeless_times', 'homeless_total','specific_homeless_long_this_time', 'specific_homeless_long']
                household_attrs = ['count_adult', 'count_youth', 'count_child_hoh', 'count_child_hh', 'total_person_in_household', 'household_type', 'youth']

                # Initialize and populate member dictionary
                # Keep Member_Number as just the number for consistency
                member = {'Household_ID': row['Household_ID'], 'Member_Type': member_type, 'Member_Number': member_number}
                member.update({attr: row.get(f'{prefix}{attr}', None) for attr in member_attrs})
                member.update({attr: row.get(attr) for attr in household_attrs})

                # Check if the member exists based on key attributes
                return member if any(pd.notnull(member[attr]) for attr in ['Gender', 'Race/Ethnicity']) else None

            # Create flattened list of member dictionaries
            members = [member for _, row in df.iterrows() for member_type in ['Adult', 'Child'] for i in range(1, 5 if member_type == 'Adult' else 7) if (member := create_member(row, member_type, i))]

            return pd.DataFrame(members)

    def flag_chronically_homeless(self, df: pd.DataFrame) -> pd.DataFrame:
        """Flags chronically homeless individuals in a DataFrame based on specific criteria."""
        required_columns = ['homeless_long', 'first_time', 'homeless_long_this_time', 'homeless_times', 'homeless_total', 'disability']
        if not all(column in df.columns for column in required_columns):
            missing_cols = [col for col in required_columns if col not in df.columns]
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

        # Define conditions for chronic homelessness
        cond1 = (df['homeless_long'] == 'One year or more') & (df['first_time'] == 'Yes')
        cond2 = (df['homeless_long_this_time'] == 'One year or more') & (df['first_time'] == 'No')
        cond3 = (df['first_time'] == 'No') & (df['homeless_long_this_time'] == 'Less than one year') & (df['homeless_times'] == '4 or more times') & (df['homeless_total'] == '12 months or more')
        
        # Combine conditions and apply them along with disability status
        chronic_homeless_condition = cond1 | cond2 | cond3
        df['CH'] = np.where(chronic_homeless_condition & (df['disability'] == 'Yes'), 'Yes', 'No')

        return df
    
    def add_age_group_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adds a new column 'age_group' to the DataFrame to categorize individuals into age groups."""
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input is not a pandas DataFrame.")

        if 'age_range' not in df.columns:
            raise ValueError("'age_range' column is missing in the DataFrame.")

        # Define age ranges and create a mapping from age range to group
        age_ranges = {
            'adult': ['25-34', '35-44', '45-54', '55-64', '65+', '25-59', '60+'],
            'youth': ['18-24'],
            'child': ['Under 18']
        }
        age_range_to_group = {ar: grp for grp, ranges in age_ranges.items() for ar in ranges}

        # Map age ranges to groups and fill non-matching entries with 'unknown'
        df['age_group'] = df['age_range'].map(age_range_to_group).fillna('unknown')

        return df
    
    def process_race(self, df: pd.DataFrame) -> pd.DataFrame:
        """Processes the 'Race/Ethnicity' column of the DataFrame, creating a new 'race' column."""
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input is not a pandas DataFrame.")

        if 'Race/Ethnicity' not in df.columns:
            raise ValueError("'Race/Ethnicity' column is missing in the DataFrame.")

        def categorize_race(race_ethnicity):
            """Categorize the race/ethnicity based on the specified rules."""
            if pd.isnull(race_ethnicity):
                return 'Unknown'

            selected_races = race_ethnicity.split(', ')
            hispanic_selected = "Hispanic/Latina/e/o" in selected_races

            # Handle the case where only 'Hispanic/Latina/e/o' is selected
            if hispanic_selected and len(selected_races) == 1:
                return "Hispanic/Latina/e/o"

            if hispanic_selected:
                selected_races.remove("Hispanic/Latina/e/o")

            if len(selected_races) > 1:
                return "Multi-Racial & Hispanic/Latina/e/o" if hispanic_selected else "Multi-Racial (not Hispanic/Latina/e/o)"
            elif selected_races:
                return f"{selected_races[0]} & Hispanic/Latina/e/o" if hispanic_selected else selected_races[0]
            else:
                return "Unknown"

        # Apply the categorization and drop the original column
        df['race'] = df['Race/Ethnicity'].apply(categorize_race)
        df.drop('Race/Ethnicity', axis=1, inplace=True)

        return df
    
    def process_gender(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adds a 'gender_count' column to the DataFrame."""
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input is not a pandas DataFrame.")

        if 'Gender' not in df.columns:
            raise ValueError("'Gender' column is missing in the DataFrame.")

        def count_gender(gender):
            """Counts the number of gender selections and categorizes the count."""
            if pd.isnull(gender):
                return 'unknown'  
            return 'one' if len(gender.split(',')) == 1 else 'more'

        # Apply the counting function to the 'Gender' column
        df['gender_count'] = df['Gender'].apply(count_gender)
        
        return df
    
    def standardize_conditions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardizes the 'chronic_condition' values in the DataFrame using condition mapping."""
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input is not a pandas DataFrame.")

        def map_conditions(conditions, mapping):
            """Maps each condition to its standardized form based on the provided mapping."""
            if isinstance(conditions, str):
                return ', '.join(mapping.get(condition.strip(), condition.strip()) for condition in conditions.split(','))
            return conditions

        # Apply the mapping to the 'chronic_condition' column if it exists
        if 'chronic_condition' in df.columns:
            df['chronic_condition'] = df['chronic_condition'].apply(lambda x: map_conditions(x, condition_mapping))

        return df
    
    def process_data_original(self, flat_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Processes the data through various steps using exact original logic."""
        try:
            # Step-by-step data processing using exact original functions
            flat_df = self.preprocess_df(flat_df)  # Preprocess DataFrame
            flat_df = self.count_age_groups(flat_df)  # Count age groups
            flat_df = self.classify_household_type(flat_df)  # Classify household types
            flat_df = self.flatten_entire_dataset(flat_df)  # Flatten dataset
            flat_df = self.flag_chronically_homeless(flat_df)  # Flag chronically homeless individuals
            flat_df = self.add_age_group_column(flat_df)  # Add age group column
            flat_df = self.process_race(flat_df)  # Process race data
            flat_df = self.process_gender(flat_df)  # Process gender data
            flat_df = self.standardize_conditions(flat_df)  # Standardize conditions

            # Filter dataframes based on household types
            household_with_children = flat_df[flat_df['household_type'] == 'Household with Children']
            household_without_children = flat_df[flat_df['household_type'] == 'Household without Children']
            household_with_only_children = flat_df[flat_df['household_type'] == 'Household with Only Children']

            return flat_df, household_with_children, household_without_children, household_with_only_children

        except Exception as e:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()  # Return empty DataFrames on error
    
    def process_source_data(self, df: pd.DataFrame, source_name: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Process a single data source using original logic."""
        
        # Use original processing logic
        processed_df, household_with_children, household_without_children, household_with_only_children = self.process_data_original(df)
        
        if processed_df.empty:
            return pd.DataFrame(), pd.DataFrame()
        
        # Add source column
        processed_df['source'] = source_name
        
        # Create persons and households using the processed dataframe
        persons_df = processed_df.copy()
        
        # Standardize column names for consistency
        if 'Household_ID' in persons_df.columns:
            persons_df['household_id'] = persons_df['Household_ID']
        
        # Create households summary from unique household IDs
        unique_households = processed_df.drop_duplicates(subset='Household_ID')
        households_df = unique_households[['Household_ID', 'household_type', 'total_person_in_household', 
                                         'count_adult', 'count_youth', 'count_child_hoh', 'count_child_hh', 'youth']].copy()
        households_df.rename(columns={'Household_ID': 'household_id'}, inplace=True)
        households_df['source'] = source_name
        households_df['total_persons'] = households_df['total_person_in_household']
        
        return persons_df, households_df
    
    def process_all_sources(self, source_data: Dict[str, pd.DataFrame]) -> Dict[str, Dict[str, pd.DataFrame]]:
        """Process all data sources and return organized results."""
        
        processed_data = {}
        all_persons = []
        all_households = []
        
        # Process each source
        for source_name, df in source_data.items():
            # Process the source
            persons_df, households_df = self.process_source_data(df, source_name)
            
            # Store individual source results
            processed_data[source_name] = {
                'raw_df': df,
                'persons_df': persons_df,
                'households_df': households_df
            }
            
            # Accumulate for combined dataset
            if not persons_df.empty:
                all_persons.append(persons_df)
            if not households_df.empty:
                all_households.append(households_df)
        
        # Create combined datasets
        if all_persons:
            combined_persons = pd.concat(all_persons, ignore_index=True)
            combined_households = pd.concat(all_households, ignore_index=True)
        else:
            combined_persons = pd.DataFrame()
            combined_households = pd.DataFrame()
        
        # Store combined results
        processed_data['combined'] = {
            'persons_df': combined_persons,
            'households_df': combined_households
        }
        
        return processed_data