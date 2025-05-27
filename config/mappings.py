"""
Column mappings for different regions/implementations.
Updated to include 4th adult support and match exact original mappings.
"""

from typing import Dict

# Updated mappings with 4th adult support
NE_mapping = {
    'Timestamp': 'Timestamp',
    #adult_1
    'Gender': 'Gender',
    'Race/Ethnicity': 'Race/Ethnicity',
    'Age Range': 'age_range',
    'Currently Fleeing Domestic/Sexual/Dating Violence': 'DV',
    'Veteran Status': 'vet',
    '**SURVEYOR: Does this person have a disabling condition?': 'disability',
    # Name fields for New England format
    '1st Letter of First Name': 'first_initial',
    '1st Letter of Last Name': 'last_initial', 
    '3rd Letter of Last Name': 'last_third',
    'Age': 'age',
    'How long have you been literally homeless?': 'homeless_long',
    'How long have you been literally homeless this time?': 'homeless_long_this_time',
    'Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?': 'homeless_times',
    'In total, how long did you stay in shelters or on the streets for those times?' : 'homeless_total',
    'Is this the first time you have stayed in a place not meant for human habitation, in an emergency shelter, in a motel/hotel room paid for by an organization, or transitional housing?': 'first_time',
    'Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'chronic_condition',
    'Specific length of time literally homeless:' : 'specific_homeless_long',
    'Specific length of time literally homeless this time' : 'specific_homeless_long_this_time',
    'Date of Birth': 'dob',
    
    #adult_2
    'Adult/Parent #2: Gender': 'adult_2_Gender',
    'Adult/Parent #2: Race/Ethnicity': 'adult_2_Race/Ethnicity',
    'Adult/Parent #2: Age Range': 'adult_2_age_range',
    'Adult/Parent #2: Currently Fleeing Domestic/Sexual/Dating Violence': 'adult_2_DV',
    'Adult/Parent #2: Veteran Status': 'adult_2_vet',
    '**SURVEYOR: Does Adult/Parent #2 have a disabling condition?' : 'adult_2_disability',
    'Adult/Parent #2: Date of Birth': 'adult_2_dob',
    'Adult/Parent #2: Date of Birth': 'adult_2_dob',
    'Adult/Parent #2: How long have you been literally homeless?' : 'adult_2_homeless_long',
    'Adult/Parent #2: How long have you been literally homeless this time?': 'adult_2_homeless_long_this_time',
    'Adult/Parent #2: Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?': 'adult_2_homeless_times',
    'Adult/Parent #2: In total, how long did you stay in shelters or on the streets for those times?' : 'adult_2_homeless_total',
    'Adult/Parent #2: Is this the first time you have stayed in a place not meant for human habitation, in an emergency shelter, in a motel/hotel room paid for by an organization, or transitional housing?' : 'adult_2_first_time',
    'Adult/Parent #2: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'adult_2_chronic_condition',
    
    #adult_3
    'Adult/Parent #3: Gender': 'adult_3_Gender',
    'Adult/Parent #3: Race/Ethnicity': 'adult_3_Race/Ethnicity',
    'Adult/Parent #3: Age Range': 'adult_3_age_range',
    'Adult/Parent #3: Currently Fleeing Domestic/Sexual/Dating Violence': 'adult_3_DV',
    'Adult/Parent #3: Veteran Status': 'adult_3_vet',
    '**SURVEYOR: Does Adult/Parent #3 have a disabling condition?' : 'adult_3_disability',
    'Adult/Parent #3: Date of Birth': 'adult_3_dob',
    'Adult/Parent #3: Date of Birth': 'adult_3_dob',
    'Adult/Parent #3: How long have you been literally homeless?' : 'adult_3_homeless_long',
    'Adult/Parent #3: How long have you been literally homeless this time?': 'adult_3_homeless_long_this_time',
    'Adult/Parent #3: Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?': 'adult_3_homeless_times',
    'Adult/Parent #3: In total, how long did you stay in shelters or on the streets for those times?' : 'adult_3_homeless_total',
    'Adult/Parent #3: Is this the first time you have stayed in a place not meant for human habitation, in an emergency shelter, in a motel/hotel room paid for by an organization, or transitional housing?' : 'adult_3_first_time',
    'Adult/Parent #3: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'adult_3_chronic_condition',
    
    #adult_4 (NEW)
    'Adult/Parent #4: Gender': 'adult_4_Gender',
    'Adult/Parent #4: Race/Ethnicity': 'adult_4_Race/Ethnicity',
    'Adult/Parent #4: Age Range': 'adult_4_age_range',
    'Adult/Parent #4: Currently Fleeing Domestic/Sexual/Dating Violence': 'adult_4_DV',
    'Adult/Parent #4: Veteran Status': 'adult_4_vet',
    '**SURVEYOR: Does Adult/Parent #4 have a disabling condition?' : 'adult_4_disability',
    'Adult/Parent #4: Date of Birth': 'adult_4_dob',
    'Adult/Parent #4: Date of Birth': 'adult_4_dob',
    'Adult/Parent #4: How long have you been literally homeless?' : 'adult_4_homeless_long',
    'Adult/Parent #4: How long have you been literally homeless this time?': 'adult_4_homeless_long_this_time',
    'Adult/Parent #4: Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?': 'adult_4_homeless_times',
    'Adult/Parent #4: In total, how long did you stay in shelters or on the streets for those times?' : 'adult_4_homeless_total',
    'Adult/Parent #4: Is this the first time you have stayed in a place not meant for human habitation, in an emergency shelter, in a motel/hotel room paid for by an organization, or transitional housing?' : 'adult_4_first_time',
    'Adult/Parent #4: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'adult_4_chronic_condition',
    
    #children
    'Do you need to add information for a child in the household?': 'child_1',
    'Child #1: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'child_1_chronic_condition',
    'Child #1: Gender': 'child_1_Gender',
    'Child #1: Race/Ethnicity': 'child_1_Race/Ethnicity',
    
    'Do you need to add information for another child?': 'child_2',
    'Child #2: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'child_2_chronic_condition',
    'Child #2: Gender': 'child_2_Gender',
    'Child #2: Race/Ethnicity': 'child_2_Race/Ethnicity',
    
    'Do you need to add information for a third child?': 'child_3',
    'Child #3: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'child_3_chronic_condition',
    'Child #3: Gender': 'child_3_Gender',
    'Child #3: Race/Ethnicity': 'child_3_Race/Ethnicity',
    
    'Do you need to add information for a fourth child?': 'child_4',
    'Child #4: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'child_4_chronic_condition',
    'Child #4: Gender': 'child_4_Gender',
    'Child #4: Race/Ethnicity': 'child_4_Race/Ethnicity',
    
    'Do you need to add information for a fifth child?': 'child_5',
    'Child #5: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'child_5_chronic_condition',
    'Child #5: Gender': 'child_5_Gender',
    'Child #5: Race/Ethnicity': 'child_5_Race/Ethnicity',
    
    'Do you need to add information for a sixth child?': 'child_6',
    'Child #6: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?' : 'child_6_chronic_condition',
    'Child #6: Gender': 'child_6_Gender',
    'Child #6: Race/Ethnicity': 'child_6_Race/Ethnicity'
}

WI_mapping = {
    'Timestamp': 'Timestamp',
    #adult_1
    'Gender': 'Gender',
    'Race/Ethnicity': 'Race/Ethnicity',
    'Age Range': 'age_range',
    'Are you a victim/survivor of domestic violence?': 'DV',
    'Have you ever served on active duty in the Armed Forces of the United States?': 'vet',
    '**SURVEYOR: Does this person have a disabling condition?': 'disability',
    # Name fields for Dashgreatlake format
    'First Name': 'first_name',
    'First Letter of Last Name': 'last_initial',
    'Date of Birth': 'dob',
    'Age': 'age',
    'How long have you been homeless?': 'homeless_long',
    'How long have you been homeless this time?': 'homeless_long_this_time',
    'Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?': 'homeless_times',
    'In total, how long did you stay in shelters or on the streets for those times?' : 'homeless_total',
    "Is this the first time you've been homeless?": 'first_time',
    'Do you have, or have you ever been diagnosed with, any of the following?' : 'chronic_condition',
    'Specific length of time homeless' : 'specific_homeless_long',
    'Specific length of time homeless this time' : 'specific_homeless_long_this_time',
    
    #adult_2
    'Adult/Parent #2: Gender': 'adult_2_Gender',
    'Adult/Parent #2: Race/Ethnicity': 'adult_2_Race/Ethnicity',
    'Adult/Parent #2: Age Range': 'adult_2_age_range',
    'Adult/Parent #2: Are you a victim/survivor of domestic violence?': 'adult_2_DV',
    'Adult/Parent #2: Have you ever served on active duty in the Armed Forces of the United States?': 'adult_2_vet',
    '**SURVEYOR: Does Adult/Parent #2 have a disabling condition?' : 'adult_2_disability',
    'Adult/Parent #2: How long have you been homeless?' : 'adult_2_homeless_long',
    'Adult/Parent #2: How long have you been homeless this time?': 'adult_2_homeless_long_this_time',
    'Adult/Parent #2: Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?': 'adult_2_homeless_times',
    'Adult/Parent #2: In total, how long did you stay in shelters or on the streets for those times?' : 'adult_2_homeless_total',
    "Adult/Parent #2: Is this the first time you've been homeless?" : 'adult_2_first_time',
    'Adult/Parent #2: Do you have, or have you ever been diagnosed with, any of the following?' : 'adult_2_chronic_condition',
    
    #adult_3 (NEW for WI mapping)
    'Adult/Parent #3: Gender': 'adult_3_Gender',
    'Adult/Parent #3: Race/Ethnicity': 'adult_3_Race/Ethnicity',
    'Adult/Parent #3: Age Range': 'adult_3_age_range',
    'Adult/Parent #3: Are you a victim/survivor of domestic violence?': 'adult_3_DV',
    'Adult/Parent #3: Have you ever served on active duty in the Armed Forces of the United States?': 'adult_3_vet',
    '**SURVEYOR: Does Adult/Parent #3 have a disabling condition?' : 'adult_3_disability',
    'Adult/Parent #3: How long have you been homeless?' : 'adult_3_homeless_long',
    'Adult/Parent #3: How long have you been homeless this time?': 'adult_3_homeless_long_this_time',
    'Adult/Parent #3: Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?': 'adult_3_homeless_times',
    'Adult/Parent #3: In total, how long did you stay in shelters or on the streets for those times?' : 'adult_3_homeless_total',
    "Adult/Parent #3: Is this the first time you've been homeless?" : 'adult_3_first_time',
    'Adult/Parent #3: Do you have, or have you ever been diagnosed with, any of the following?' : 'adult_3_chronic_condition',
    
    #adult_4 (NEW for WI mapping)
    'Adult/Parent #4: Gender': 'adult_4_Gender',
    'Adult/Parent #4: Race/Ethnicity': 'adult_4_Race/Ethnicity',
    'Adult/Parent #4: Age Range': 'adult_4_age_range',
    'Adult/Parent #4: Are you a victim/survivor of domestic violence?': 'adult_4_DV',
    'Adult/Parent #4: Have you ever served on active duty in the Armed Forces of the United States?': 'adult_4_vet',
    '**SURVEYOR: Does Adult/Parent #4 have a disabling condition?' : 'adult_4_disability',
    'Adult/Parent #4: How long have you been homeless?' : 'adult_4_homeless_long',
    'Adult/Parent #4: How long have you been homeless this time?': 'adult_4_homeless_long_this_time',
    'Adult/Parent #4: Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?': 'adult_4_homeless_times',
    'Adult/Parent #4: In total, how long did you stay in shelters or on the streets for those times?' : 'adult_4_homeless_total',
    "Adult/Parent #4: Is this the first time you've been homeless?" : 'adult_4_first_time',
    'Adult/Parent #4: Do you have, or have you ever been diagnosed with, any of the following?' : 'adult_4_chronic_condition',
    
    #children
    'Do you need to add information for a child in the household?': 'child_1',
    'Child #1: Gender': 'child_1_Gender',
    'Child #1: Race/Ethnicity': 'child_1_Race/Ethnicity',
    
    'Do you need to add information for another child?': 'child_2',
    'Child #2: Gender': 'child_2_Gender',
    'Child #2: Race/Ethnicity': 'child_2_Race/Ethnicity',
    
    'Do you need to add information for a third child?': 'child_3',
    'Child #3: Gender': 'child_3_Gender',
    'Child #3: Race/Ethnicity': 'child_3_Race/Ethnicity',
    
    'Do you need to add information for a fourth child?': 'child_4',
    'Child #4: Gender': 'child_4_Gender',
    'Child #4: Race/Ethnicity': 'child_4_Race/Ethnicity',
    
    'Do you need to add information for a fifth child?': 'child_5',
    'Child #5: Gender': 'child_5_Gender',
    'Child #5: Race/Ethnicity': 'child_5_Race/Ethnicity',
    
    'Do you need to add information for a sixth child?': 'child_6',
    'Child #6: Gender': 'child_6_Gender',
    'Child #6: Race/Ethnicity': 'child_6_Race/Ethnicity'
}

# Condition mapping from original
condition_mapping = {
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

class ColumnMappings:
    """Centralized column mappings for different regions."""
    
    @classmethod
    def get_mapping_for_region(cls, region: str) -> Dict[str, str]:
        """Get appropriate mapping for the specified region."""
        region_mappings = {
            'New England': NE_mapping,
            'Dashgreatlake': WI_mapping
        }
        
        return region_mappings.get(region, {})

def get_person_columns() -> list:
    """Get list of columns that represent person-level data."""
    return [
        'Gender', 'Race/Ethnicity', 'age_range', 'DV', 'vet', 'disability',
        'homeless_long', 'homeless_long_this_time', 'homeless_times',
        'homeless_total', 'first_time', 'chronic_condition',
        'specific_homeless_long', 'specific_homeless_long_this_time',
        'first_name', 'last_name', 'dob'  # Added name fields
    ]

def get_child_presence_columns() -> list:
    """Get list of columns that indicate child presence."""
    return [f'child_{i}' for i in range(1, 7)]

def get_adult_age_columns() -> list:
    """Get list of adult age range columns including 4th adult."""
    return ['age_range', 'adult_2_age_range', 'adult_3_age_range', 'adult_4_age_range']

def get_adult_name_columns() -> list:
    """Get list of adult name columns for duplication detection."""
    return [
        ('first_name', 'last_name', 'dob'),
        ('adult_2_first_name', 'adult_2_last_name', 'adult_2_dob'),
        ('adult_3_first_name', 'adult_3_last_name', 'adult_3_dob'),
        ('adult_4_first_name', 'adult_4_last_name', 'adult_4_dob')
    ]