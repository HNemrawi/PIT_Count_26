"""
Data categories and classifications for PIT Count application.
Updated to match exact original predefined_lists_dicts.py
"""

from enum import Enum
from typing import Dict, List

class AgeGroup(Enum):
    CHILD = "child"
    YOUTH = "youth" 
    ADULT = "adult"
    UNKNOWN = "unknown"

class HouseholdType(Enum):
    WITH_CHILDREN = "Household with Children"
    WITHOUT_CHILDREN = "Household without Children"
    ONLY_CHILDREN = "Household with Only Children"

class MemberType(Enum):
    ADULT = "Adult"
    CHILD = "Child"

# Exact from original predefined_lists_dicts.py
age_ranges = ['25-34', '35-44', '45-54', '55-64', '65+']

gender_categories = {
    'Woman (Girl if child)': 'Woman_Girl',
    'Man (Boy if child)': 'Man_Boy',
    'Culturally Specific Identity': 'Culturally_Specific_Identity',
    'Transgender': 'Transgender',
    'Non-Binary': 'Non_Binary',
    'Questioning': 'Questioning',
    'Different Identity': 'Different_Identity',
    'More Than One Gender': 'More_Than_One_Gender'
}

race_categories = {
    'Indigenous (American Indian/Alaska Native/Indigenous)': 'Indigenous',
    'Indigenous (American Indian/Alaska Native/Indigenous) & Hispanic/Latina/e/o': 'Indigenous_Hispanic',
    'Asian/Asian American': 'Asian',
    'Asian/Asian American & Hispanic/Latina/e/o': 'Asian_Hispanic',
    'Black/African American/African': 'Black',
    'Black/African American/African & Hispanic/Latina/e/o': 'Black_Hispanic',
    'Hispanic/Latina/e/o': 'Hispanic',
    'Middle Eastern/North African': 'Middle_Eastern_North_African',
    'Middle Eastern/North African & Hispanic/Latina/e/o': 'Middle_Eastern_North_African_Hispanic',
    'Native Hawaiian/Pacific Islander': 'Native_Hawaiian',
    'Native Hawaiian/Pacific Islander & Hispanic/Latina/e/o': 'Native_Hawaiian_Hispanic',
    'White': 'White',
    'White & Hispanic/Latina/e/o': 'White_Hispanic',
    'Multi-Racial & Hispanic/Latina/e/o': 'Multi_Racial_Hispanic',
    'Multi-Racial (not Hispanic/Latina/e/o)': 'Multi_Racial_Non_Hispanic'
}

condition_categories = {
    'Mental Health': 'Serious_Mental_Illness',
    'Substance Use Disorder (Alcohol, Drugs, or Both)': 'Substance_Use_Disorder',
    'Physical Condition': 'Physical_Condition',
    'HIV/AIDS': 'HIV_AIDS',
    'Developmental Condition': 'Developmental_Condition',
    'Other Chronic Health Condition': 'other_Condition'
}

household_categories = {
    'Household with Children': 'Households_with_Child',
    'Household without Children': 'Households_without_Children',
    'Household with Only Children': 'Households_with_Only_Children'
}

# Condition mapping from original
CONDITION_MAPPING = {
    'Physical disability': 'Physical Condition',
    'Psychiatric or emotional conditions such as depression or schizophrenia': 'Mental Health',
    'PTSD (Post Traumatic Stress Disorder)': 'Mental Health',
    'Mental Health': 'Mental Health',
    'Substance Use Disorder (Alcohol, Drugs, or Both)': 'Substance Use Disorder (Alcohol, Drugs, or Both)',
    'AIDS or HIV-related illness': 'HIV/AIDS',
    'Ongoing health problems or medical conditions such as diabetes, cancer, o': 'Other Chronic Health Condition',
    'Traumatic brain or head injury': 'Other Chronic Health Condition',
    "Don't Know/Refused": "Don't Know/Refused",
    'None of the above': 'None of the above'
}

# Homeless duration categories
HOMELESS_DURATION_SHORT = ['1 day or less', '2 days - 1 week', 'More than 1 week - Less than 1 month']
HOMELESS_DURATION_1_3_MONTHS = ['1-3 Months']
HOMELESS_DURATION_3_12_MONTHS = ['More than 3 months - Less than 1 year']
HOMELESS_DURATION_1_YEAR_PLUS = ['1 year or more', 'One year or more']

def get_age_group(age_range: str) -> AgeGroup:
    """Get age group enum from age range string."""
    age_ranges_mapping = {
        'adult': ['25-34', '35-44', '45-54', '55-64', '65+', '25-59', '60+'],
        'youth': ['18-24'],
        'child': ['Under 18']
    }
    
    for group, ranges in age_ranges_mapping.items():
        if age_range in ranges:
            return AgeGroup(group)
    
    return AgeGroup.UNKNOWN

def standardize_condition(condition: str) -> str:
    """Standardize condition names using exact original mapping."""
    if not condition or condition != condition:  # Check for NaN
        return condition
    
    conditions = condition.split(', ')
    standardized = [CONDITION_MAPPING.get(cond.strip(), cond.strip()) for cond in conditions]
    return ', '.join(standardized)

def categorize_race(race_ethnicity: str) -> str:
    """Categorize race/ethnicity based on selection rules - exact from original."""
    if not race_ethnicity or race_ethnicity != race_ethnicity:  # Check for NaN
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

def get_gender_count(gender: str) -> str:
    """Count the number of gender selections - exact from original."""
    if not gender or gender != gender:  # Check for NaN
        return 'unknown'
    return 'one' if len(gender.split(',')) == 1 else 'more'