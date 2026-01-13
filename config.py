"""
Configuration file for PIT Count Application
Contains all mappings, templates, and constants
"""

# Region configurations
REGIONS = ['New England', 'Great Lakes']

# Unified Column Mappings with Priority
# Format: 'target_column': [('source_column_1', priority), ('source_column_2', priority), ...]
# Higher priority number = preferred source (used first if present)
UNIFIED_COLUMN_MAPPINGS = {
    # Timestamp
    'Timestamp': [('Timestamp', 100)],

    # Adult 1 - Name fields (region-specific)
    'first_initial': [('1st Letter of First Name', 100)],  # NE only
    'last_initial': [('1st Letter of Last Name', 100)],     # NE only
    'last_third': [('3rd Letter of Last Name', 100)],       # NE only
    'first_name': [('First Name', 100)],                    # GL only
    'first_letter_last': [('First Letter of Last Name', 100)],  # GL only

    # Adult 1 - Core fields
    'Sex': [('Sex', 100)],
    'Gender': [('Gender', 100)],
    'Race/Ethnicity': [('Race/Ethnicity', 100)],
    'age_range': [('Age Range', 100)],
    'age': [('Age', 100)],
    'dob': [('Date of Birth', 100)],

    # Adult 1 - DV Question (regional variations)
    'DV': [
        ('Currently Fleeing Domestic/Sexual/Dating Violence', 100),  # NE
        ('Are you a victim/survivor of domestic violence?', 90),      # GL
    ],

    # Adult 1 - Veteran Status (regional variations)
    'vet': [
        ('Veteran Status', 100),  # NE
        ('Have you ever served on active duty in the Armed Forces of the United States?', 90),  # GL
    ],

    # Adult 1 - Disability
    'disability': [('**SURVEYOR: Does this person have a disabling condition?', 100)],

    # Adult 1 - Homelessness history (regional variations)
    'homeless_long': [
        ('How long have you been literally homeless?', 100),  # NE
        ('How long have you been homeless?', 90),  # GL
    ],
    'homeless_long_this_time': [
        ('How long have you been literally homeless this time?', 100),  # NE
        ('How long have you been homeless this time?', 90),  # GL
    ],
    'homeless_times': [
        ('Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?', 100),
    ],
    'homeless_total': [
        ('In total, how long did you stay in shelters or on the streets for those times?', 100),
    ],
    'first_time': [
        ('Is this the first time you have stayed in a place not meant for human habitation, in an emergency shelter, in a motel/hotel room paid for by an organization, or transitional housing?', 100),  # NE
        ("Is this the first time you've been homeless?", 90),  # GL
    ],
    'chronic_condition': [
        ('Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?', 100),  # NE
        ('Do you have, or have you ever been diagnosed with, any of the following?', 90),  # GL
    ],
    'specific_homeless_long': [
        ('Specific length of time literally homeless:', 100),  # NE
        ('Specific length of time homeless', 90),  # GL
    ],
    'specific_homeless_long_this_time': [
        ('Specific length of time literally homeless this time', 100),  # NE
        ('Specific length of time homeless this time', 90),  # GL
    ],

    # Adult 2 - Name fields
    'adult_2_first_initial': [('Adult/Parent #2: 1st Letter of First Name', 100)],  # NE only
    'adult_2_last_initial': [('Adult/Parent #2: 1st Letter of Last Name', 100)],  # NE only
    'adult_2_last_third': [('Adult/Parent #2: 3rd Letter of Last Name', 100)],     # NE only
    'adult_2_first_name': [('Adult/Parent #2: First Name', 100)],  # GL only
    'adult_2_first_letter_last': [('Adult/Parent #2: First Letter of Last Name', 100)],  # GL only

    # Adult 2 - Core fields
    'adult_2_Sex': [('Adult/Parent #2: Sex', 100)],
    'adult_2_Gender': [('Adult/Parent #2: Gender', 100)],
    'adult_2_Race/Ethnicity': [('Adult/Parent #2: Race/Ethnicity', 100)],
    'adult_2_age_range': [('Adult/Parent #2: Age Range', 100)],
    'adult_2_age': [('Adult/Parent #2: Age', 100)],  # GL only
    'adult_2_dob': [('Adult/Parent #2: Date of Birth', 100)],

    # Adult 2 - DV Question (regional variations)
    'adult_2_DV': [
        ('Adult/Parent #2: Currently Fleeing Domestic/Sexual/Dating Violence', 100),  # NE
        ('Adult/Parent #2: Are you a victim/survivor of domestic violence?', 90),  # GL
    ],

    # Adult 2 - Veteran Status (regional variations)
    'adult_2_vet': [
        ('Adult/Parent #2: Veteran Status', 100),  # NE
        ('Adult/Parent #2: Have you ever served on active duty in the Armed Forces of the United States?', 90),  # GL
    ],

    # Adult 2 - Disability
    'adult_2_disability': [('**SURVEYOR: Does Adult/Parent #2 have a disabling condition?', 100)],

    # Adult 2 - Homelessness history (regional variations)
    'adult_2_homeless_long': [
        ('Adult/Parent #2: How long have you been literally homeless?', 100),  # NE
        ('Adult/Parent #2: How long have you been homeless?', 90),  # GL
    ],
    'adult_2_homeless_long_this_time': [
        ('Adult/Parent #2: How long have you been literally homeless this time?', 100),  # NE
        ('Adult/Parent #2: How long have you been homeless this time?', 90),  # GL
    ],
    'adult_2_homeless_times': [
        ('Adult/Parent #2: Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?', 100),
    ],
    'adult_2_homeless_total': [
        ('Adult/Parent #2: In total, how long did you stay in shelters or on the streets for those times?', 100),
    ],
    'adult_2_first_time': [
        ('Adult/Parent #2: Is this the first time you have stayed in a place not meant for human habitation, in an emergency shelter, in a motel/hotel room paid for by an organization, or transitional housing?', 100),  # NE
        ("Adult/Parent #2: Is this the first time you've been homeless?", 90),  # GL
    ],
    'adult_2_chronic_condition': [
        ('Adult/Parent #2: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?', 100),  # NE
        ('Adult/Parent #2: Do you have, or have you ever been diagnosed with, any of the following?', 90),  # GL
    ],

    # Adult 3 - Name fields (NE only - OPTIONAL)
    'adult_3_first_initial': [('Adult/Parent #3: 1st Letter of First Name', 100)],
    'adult_3_last_initial': [('Adult/Parent #3: 1st Letter of Last Name', 100)],
    'adult_3_last_third': [('Adult/Parent #3: 3rd Letter of Last Name', 100)],

    # Adult 3 - Core fields (NE only - OPTIONAL)
    'adult_3_Sex': [('Adult/Parent #3: Sex', 100)],
    'adult_3_Gender': [('Adult/Parent #3: Gender', 100)],
    'adult_3_Race/Ethnicity': [('Adult/Parent #3: Race/Ethnicity', 100)],
    'adult_3_age_range': [('Adult/Parent #3: Age Range', 100)],
    'adult_3_dob': [('Adult/Parent #3: Date of Birth', 100)],
    'adult_3_DV': [('Adult/Parent #3: Currently Fleeing Domestic/Sexual/Dating Violence', 100)],
    'adult_3_vet': [('Adult/Parent #3: Veteran Status', 100)],
    'adult_3_disability': [('**SURVEYOR: Does Adult/Parent #3 have a disabling condition?', 100)],
    'adult_3_homeless_long': [('Adult/Parent #3: How long have you been literally homeless?', 100)],
    'adult_3_homeless_long_this_time': [('Adult/Parent #3: How long have you been literally homeless this time?', 100)],
    'adult_3_homeless_times': [('Adult/Parent #3: Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?', 100)],
    'adult_3_homeless_total': [('Adult/Parent #3: In total, how long did you stay in shelters or on the streets for those times?', 100)],
    'adult_3_first_time': [('Adult/Parent #3: Is this the first time you have stayed in a place not meant for human habitation, in an emergency shelter, in a motel/hotel room paid for by an organization, or transitional housing?', 100)],
    'adult_3_chronic_condition': [('Adult/Parent #3: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?', 100)],

    # Adult 4 - Name fields (NE only - OPTIONAL)
    'adult_4_first_initial': [('Adult/Parent #4: 1st Letter of First Name', 100)],
    'adult_4_last_initial': [('Adult/Parent #4: 1st Letter of Last Name', 100)],
    'adult_4_last_third': [('Adult/Parent #4: 3rd Letter of Last Name', 100)],

    # Adult 4 - Core fields (NE only - OPTIONAL)
    'adult_4_Sex': [('Adult/Parent #4: Sex', 100)],
    'adult_4_Gender': [('Adult/Parent #4: Gender', 100)],
    'adult_4_Race/Ethnicity': [('Adult/Parent #4: Race/Ethnicity', 100)],
    'adult_4_age_range': [('Adult/Parent #4: Age Range', 100)],
    'adult_4_dob': [('Adult/Parent #4: Date of Birth', 100)],
    'adult_4_DV': [('Adult/Parent #4: Currently Fleeing Domestic/Sexual/Dating Violence', 100)],
    'adult_4_vet': [('Adult/Parent #4: Veteran Status', 100)],
    'adult_4_disability': [('**SURVEYOR: Does Adult/Parent #4 have a disabling condition?', 100)],
    'adult_4_homeless_long': [('Adult/Parent #4: How long have you been literally homeless?', 100)],
    'adult_4_homeless_long_this_time': [('Adult/Parent #4: How long have you been literally homeless this time?', 100)],
    'adult_4_homeless_times': [('Adult/Parent #4: Including this time, how many separate times have you stayed in shelters or on the streets in the past three years?', 100)],
    'adult_4_homeless_total': [('Adult/Parent #4: In total, how long did you stay in shelters or on the streets for those times?', 100)],
    'adult_4_first_time': [('Adult/Parent #4: Is this the first time you have stayed in a place not meant for human habitation, in an emergency shelter, in a motel/hotel room paid for by an organization, or transitional housing?', 100)],
    'adult_4_chronic_condition': [('Adult/Parent #4: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?', 100)],

    # Children - Child 1
    'child_1': [('Do you need to add information for a child in the household?', 100)],
    'child_1_first_initial': [
        ('Child #1: 1st Letter of First Name', 100),  # NE format
        ('Child #1: First Initial of First Name', 90),  # GL format
    ],
    'child_1_last_initial': [
        ('Child #1: 1st Letter of Last Name', 100),  # NE format
        ('Child #1: First Initial of Last Name', 90),  # GL format
    ],
    'child_1_last_third': [('Child #1: 3rd Letter of Last Name', 100)],  # NE only
    'child_1_dob': [('Child #1: Date of Birth', 100)],  # NE only
    'child_1_age': [('Child #1: Age', 100)],  # GL only
    'child_1_chronic_condition': [('Child #1: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?', 100)],  # NE only
    'child_1_Sex': [('Child #1: Sex', 100)],
    'child_1_Gender': [('Child #1: Gender', 100)],
    'child_1_Race/Ethnicity': [('Child #1: Race/Ethnicity', 100)],

    # Child 2
    'child_2': [('Do you need to add information for another child?', 100)],
    'child_2_first_initial': [
        ('Child #2: 1st Letter of First Name', 100),
        ('Child #2: First Initial of First Name', 90),
    ],
    'child_2_last_initial': [
        ('Child #2: 1st Letter of Last Name', 100),
        ('Child #2: First Initial of Last Name', 90),
    ],
    'child_2_last_third': [('Child #2: 3rd Letter of Last Name', 100)],
    'child_2_dob': [('Child #2: Date of Birth', 100)],
    'child_2_age': [('Child #2: Age', 100)],
    'child_2_chronic_condition': [('Child #2: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?', 100)],
    'child_2_Sex': [('Child #2: Sex', 100)],
    'child_2_Gender': [('Child #2: Gender', 100)],
    'child_2_Race/Ethnicity': [('Child #2: Race/Ethnicity', 100)],

    # Child 3
    'child_3': [('Do you need to add information for a third child?', 100)],
    'child_3_first_initial': [
        ('Child #3: 1st Letter of First Name', 100),
        ('Child #3: First Initial of First Name', 90),
    ],
    'child_3_last_initial': [
        ('Child #3: 1st Letter of Last Name', 100),
        ('Child #3: First Initial of Last Name', 90),
    ],
    'child_3_last_third': [('Child #3: 3rd Letter of Last Name', 100)],
    'child_3_dob': [('Child #3: Date of Birth', 100)],
    'child_3_age': [('Child #3: Age', 100)],
    'child_3_chronic_condition': [('Child #3: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?', 100)],
    'child_3_Sex': [('Child #3: Sex', 100)],
    'child_3_Gender': [('Child #3: Gender', 100)],
    'child_3_Race/Ethnicity': [('Child #3: Race/Ethnicity', 100)],

    # Child 4
    'child_4': [('Do you need to add information for a fourth child?', 100)],
    'child_4_first_initial': [
        ('Child #4: 1st Letter of First Name', 100),
        ('Child #4: First Initial of First Name', 90),
    ],
    'child_4_last_initial': [
        ('Child #4: 1st Letter of Last Name', 100),
        ('Child #4: First Initial of Last Name', 90),
    ],
    'child_4_last_third': [('Child #4: 3rd Letter of Last Name', 100)],
    'child_4_dob': [('Child #4: Date of Birth', 100)],
    'child_4_age': [('Child #4: Age', 100)],
    'child_4_chronic_condition': [('Child #4: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?', 100)],
    'child_4_Sex': [('Child #4: Sex', 100)],
    'child_4_Gender': [('Child #4: Gender', 100)],
    'child_4_Race/Ethnicity': [('Child #4: Race/Ethnicity', 100)],

    # Child 5
    'child_5': [('Do you need to add information for a fifth child?', 100)],
    'child_5_first_initial': [
        ('Child #5: 1st Letter of First Name', 100),
        ('Child #5: First Initial of First Name', 90),
    ],
    'child_5_last_initial': [
        ('Child #5: 1st Letter of Last Name', 100),
        ('Child #5: First Initial of Last Name', 90),
    ],
    'child_5_last_third': [('Child #5: 3rd Letter of Last Name', 100)],
    'child_5_dob': [('Child #5: Date of Birth', 100)],
    'child_5_age': [('Child #5: Age', 100)],
    'child_5_chronic_condition': [('Child #5: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?', 100)],
    'child_5_Sex': [('Child #5: Sex', 100)],
    'child_5_Gender': [('Child #5: Gender', 100)],
    'child_5_Race/Ethnicity': [('Child #5: Race/Ethnicity', 100)],

    # Child 6
    'child_6': [('Do you need to add information for a sixth child?', 100)],
    'child_6_first_initial': [
        ('Child #6: 1st Letter of First Name', 100),
        ('Child #6: First Initial of First Name', 90),
    ],
    'child_6_last_initial': [
        ('Child #6: 1st Letter of Last Name', 100),
        ('Child #6: First Initial of Last Name', 90),
    ],
    'child_6_last_third': [('Child #6: 3rd Letter of Last Name', 100)],
    'child_6_dob': [('Child #6: Date of Birth', 100)],
    'child_6_age': [('Child #6: Age', 100)],
    'child_6_chronic_condition': [('Child #6: Do you have, or have you ever been diagnosed with, any of the listed conditions of long duration?', 100)],
    'child_6_Sex': [('Child #6: Sex', 100)],
    'child_6_Gender': [('Child #6: Gender', 100)],
    'child_6_Race/Ethnicity': [('Child #6: Race/Ethnicity', 100)],

    # Optional filter columns
    'Project Name on HIC': [('Project Name on HIC', 100)],
    'County': [('County', 100)],
    'AHS District': [('AHS District', 100)],
}

# Region detection signatures
REGION_SIGNATURES = {
    'New England': {
        'required_columns': [
            '1st Letter of First Name',
            '3rd Letter of Last Name',
            'Currently Fleeing Domestic/Sexual/Dating Violence'
        ],
        'timezone': 'America/New_York',
        'max_adults': 4,
        'child_chronic_conditions': True
    },
    'Great Lakes': {
        'required_columns': [
            'First Name',
            'Are you a victim/survivor of domestic violence?'
        ],
        'optional_name_columns': [
            ['First Letter of Last Name'],  # Option 1: First + Last initial
            ['Last Name']  # Option 2: First + Full Last
        ],
        'timezone': 'America/Chicago',
        'max_adults': 2,
        'child_chronic_conditions': False
    }
}

# Categories
AGE_RANGES = ['25-34', '35-44', '45-54', '55-64', '65+']

SEX_CATEGORIES = {
    'Female': 'Female',
    'Male': 'Male'
}

GENDER_CATEGORIES = {
    'Woman (Girl if child)': 'Woman_Girl',
    'Man (Boy if child)': 'Man_Boy',
    'Culturally Specific Identity': 'Culturally_Specific_Identity',
    'Transgender': 'Transgender',
    'Non-Binary': 'Non_Binary',
    'Questioning': 'Questioning',
    'Different Identity': 'Different_Identity',
    'More Than One Gender': 'More_Than_One_Gender'
}

RACE_CATEGORIES = {
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

CONDITION_CATEGORIES = {
    'Mental Health': 'Serious_Mental_Illness',
    'Substance Use Disorder (Alcohol, Drugs, or Both)': 'Substance_Use_Disorder',
    'Physical Condition': 'Physical_Condition',
    'HIV/AIDS': 'HIV_AIDS',
    'Developmental Condition': 'Developmental_Condition',
    'Other Chronic Health Condition': 'other_Condition'
}

HOUSEHOLD_CATEGORIES = {
    'Household with Children': 'Households_with_Child',
    'Household without Children': 'Households_without_Children',
    'Household with Only Children': 'Households_with_Only_Children'
}

# Condition mapping
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

# Report columns
REPORT_COLUMNS = ["Sheltered_ES", "Sheltered_TH", "Unsheltered", "Total"]

# Report templates
REPORT_TEMPLATES = {
    'TOTAL_with': [
        ("Total number of households", ""),
        ("Total number of persons (adults & children)", ""),
        ("      Number of children (under age 18)", ""),
        ("      Number of young (age 18 to 24)", ""),
        ("      Number of adults (age 25 to 34)", ""),
        ("      Number of adults (age 35 to 44)", ""),
        ("      Number of adults (age 45 to 54)", ""),
        ("      Number of adults (age 55 to 64)", ""),
        ("      Number of adults (age 65 or older)", ""),
        ("Sex (adults and children)", "Female"),
        ("Sex (adults and children)", "Male"),
        ("Gender (adults and children)", "Woman (Girl if child)"),
        ("Gender (adults and children)", "Man (Boy if child)"),
        ("Gender (adults and children)", "Culturally Specific Identity"),
        ("Gender (adults and children)", "Transgender"),
        ("Gender (adults and children)", "Non-Binary"),
        ("Gender (adults and children)", "Questioning"),
        ("Gender (adults and children)", "Different Identity"),
        ("Gender (adults and children)", "More Than One Gender"),
        ("Gender (adults and children)", "      Includes Woman (Girl if child)"),
        ("Gender (adults and children)", "      Includes Man (Boy if child)"),
        ("Gender (adults and children)", "      Includes Culturally Specific Identity"),
        ("Gender (adults and children)", "      Includes Transgender"),
        ("Gender (adults and children)", "      Includes Non-Binary"),
        ("Gender (adults and children)", "      Includes Questioning"),
        ("Gender (adults and children)", "      Includes Different Identity"),
        ("Race and Ethnicity (adults and children)", "Indigenous (American Indian/Alaska Native/Indigenous)"),
        ("Race and Ethnicity (adults and children)", "Indigenous (American Indian/Alaska Native/Indigenous) & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (adults and children)", "Asian/Asian American"),
        ("Race and Ethnicity (adults and children)", "Asian/Asian American & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (adults and children)", "Black/African American/African"),
        ("Race and Ethnicity (adults and children)", "Black/African American/African & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (adults and children)", "Hispanic/Latina/e/o"),
        ("Race and Ethnicity (adults and children)", "Middle Eastern/North African"),
        ("Race and Ethnicity (adults and children)", "Middle Eastern/North African & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (adults and children)", "Native Hawaiian/Pacific Islander"),
        ("Race and Ethnicity (adults and children)", "Native Hawaiian/Pacific Islander & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (adults and children)", "White"),
        ("Race and Ethnicity (adults and children)", "White & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (adults and children)", "Multi-Racial & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (adults and children)", "Multi-Racial (not Hispanic/Latina/e/o)"),
        ("Chronically Homeless", "Total number of households"),
        ("Chronically Homeless", "Total number of persons")
    ],
    
    'TOTAL_without': [
        ("Total number of households", ""),
        ("Total number of persons", ""),
        ("      Number of young (age 18 to 24)", ""),
        ("      Number of adults (age 25 to 34)", ""),
        ("      Number of adults (age 35 to 44)", ""),
        ("      Number of adults (age 45 to 54)", ""),
        ("      Number of adults (age 55 to 64)", ""),
        ("      Number of adults (age 65 or older)", ""),
        ("Sex", "Female"),
        ("Sex", "Male"),
        ("Gender", "Woman (Girl if child)"),
        ("Gender", "Man (Boy if child)"),
        ("Gender", "Culturally Specific Identity"),
        ("Gender", "Transgender"),
        ("Gender", "Non-Binary"),
        ("Gender", "Questioning"),
        ("Gender", "Different Identity"),
        ("Gender", "More Than One Gender"),
        ("Gender", "      Includes Woman (Girl if child)"),
        ("Gender", "      Includes Man (Boy if child)"),
        ("Gender", "      Includes Culturally Specific Identity"),
        ("Gender", "      Includes Transgender"),
        ("Gender", "      Includes Non-Binary"),
        ("Gender", "      Includes Questioning"),
        ("Gender", "      Includes Different Identity"),
        ("Race and Ethnicity", "Indigenous (American Indian/Alaska Native/Indigenous)"),
        ("Race and Ethnicity", "Indigenous (American Indian/Alaska Native/Indigenous) & Hispanic/Latina/e/o"),
        ("Race and Ethnicity", "Asian/Asian American"),
        ("Race and Ethnicity", "Asian/Asian American & Hispanic/Latina/e/o"),
        ("Race and Ethnicity", "Black/African American/African"),
        ("Race and Ethnicity", "Black/African American/African & Hispanic/Latina/e/o"),
        ("Race and Ethnicity", "Hispanic/Latina/e/o"),
        ("Race and Ethnicity", "Middle Eastern/North African"),
        ("Race and Ethnicity", "Middle Eastern/North African & Hispanic/Latina/e/o"),
        ("Race and Ethnicity", "Native Hawaiian/Pacific Islander"),
        ("Race and Ethnicity", "Native Hawaiian/Pacific Islander & Hispanic/Latina/e/o"),
        ("Race and Ethnicity", "White"),
        ("Race and Ethnicity", "White & Hispanic/Latina/e/o"),
        ("Race and Ethnicity", "Multi-Racial & Hispanic/Latina/e/o"),
        ("Race and Ethnicity", "Multi-Racial (not Hispanic/Latina/e/o)"),
        ("Chronically Homeless", "Total number of persons")
    ],
    
    'TOTAL_withonly': [
        ("Total number of households", ""),
        ("Number of children (persons under age 18)", ""),
        ("Sex", "Female"),
        ("Sex", "Male"),
        ("Gender", "Woman (Girl if child)"),
        ("Gender", "Man (Boy if child)"),
        ("Gender", "Culturally Specific Identity"),
        ("Gender", "Transgender"),
        ("Gender", "Non-Binary"),
        ("Gender", "Questioning"),
        ("Gender", "Different Identity"),
        ("Gender", "More Than One Gender"),
        ("Gender", "      Includes Woman (Girl if child)"),
        ("Gender", "      Includes Man (Boy if child)"),
        ("Gender", "      Includes Culturally Specific Identity"),
        ("Gender", "      Includes Transgender"),
        ("Gender", "      Includes Non-Binary"),
        ("Gender", "      Includes Questioning"),
        ("Gender", "      Includes Different Identity"),
        ("Race and Ethnicity", "Indigenous (American Indian/Alaska Native/Indigenous)"),
        ("Race and Ethnicity", "Indigenous (American Indian/Alaska Native/Indigenous) & Hispanic/Latina/e/o"),
        ("Race and Ethnicity", "Asian/Asian American"),
        ("Race and Ethnicity", "Asian/Asian American & Hispanic/Latina/e/o"),
        ("Race and Ethnicity", "Black/African American/African"),
        ("Race and Ethnicity", "Black/African American/African & Hispanic/Latina/e/o"),
        ("Race and Ethnicity", "Hispanic/Latina/e/o"),
        ("Race and Ethnicity", "Middle Eastern/North African"),
        ("Race and Ethnicity", "Middle Eastern/North African & Hispanic/Latina/e/o"),
        ("Race and Ethnicity", "Native Hawaiian/Pacific Islander"),
        ("Race and Ethnicity", "Native Hawaiian/Pacific Islander & Hispanic/Latina/e/o"),
        ("Race and Ethnicity", "White"),
        ("Race and Ethnicity", "White & Hispanic/Latina/e/o"),
        ("Race and Ethnicity", "Multi-Racial & Hispanic/Latina/e/o"),
        ("Race and Ethnicity", "Multi-Racial (not Hispanic/Latina/e/o)"),
        ("Chronically Homeless", "Total number of persons")
    ],
    
    'VET_with': [
        ("Total number of households", ""),
        ("Total number of persons", ""),
        ("Total number of veterans", ""),
        ("Sex (veterans only)", "Female"),
        ("Sex (veterans only)", "Male"),
        ("Gender (veterans only)", "Woman (Girl if child)"),
        ("Gender (veterans only)", "Man (Boy if child)"),
        ("Gender (veterans only)", "Culturally Specific Identity"),
        ("Gender (veterans only)", "Transgender"),
        ("Gender (veterans only)", "Non-Binary"),
        ("Gender (veterans only)", "Questioning"),
        ("Gender (veterans only)", "Different Identity"),
        ("Gender (veterans only)", "More Than One Gender"),
        ("Gender (veterans only)", "      Includes Woman (Girl if child)"),
        ("Gender (veterans only)", "      Includes Man (Boy if child)"),
        ("Gender (veterans only)", "      Includes Culturally Specific Identity"),
        ("Gender (veterans only)", "      Includes Transgender"),
        ("Gender (veterans only)", "      Includes Non-Binary"),
        ("Gender (veterans only)", "      Includes Questioning"),
        ("Gender (veterans only)", "      Includes Different Identity"),
        ("Race and Ethnicity (veterans only)", "Indigenous (American Indian/Alaska Native/Indigenous)"),
        ("Race and Ethnicity (veterans only)", "Indigenous (American Indian/Alaska Native/Indigenous) & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (veterans only)", "Asian/Asian American"),
        ("Race and Ethnicity (veterans only)", "Asian/Asian American & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (veterans only)", "Black/African American/African"),
        ("Race and Ethnicity (veterans only)", "Black/African American/African & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (veterans only)", "Hispanic/Latina/e/o"),
        ("Race and Ethnicity (veterans only)", "Middle Eastern/North African"),
        ("Race and Ethnicity (veterans only)", "Middle Eastern/North African & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (veterans only)", "Native Hawaiian/Pacific Islander"),
        ("Race and Ethnicity (veterans only)", "Native Hawaiian/Pacific Islander & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (veterans only)", "White"),
        ("Race and Ethnicity (veterans only)", "White & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (veterans only)", "Multi-Racial & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (veterans only)", "Multi-Racial (not Hispanic/Latina/e/o)"),
        ("Chronically Homeless", "Total number of households"),
        ("Chronically Homeless", "Total number of persons")
    ],
    
    'VET_without': [
        ("Total number of households", ""),
        ("Total number of persons", ""),
        ("Total number of veterans", ""),
        ("Sex (veterans only)", "Female"),
        ("Sex (veterans only)", "Male"),
        ("Gender (veterans only)", "Woman (Girl if child)"),
        ("Gender (veterans only)", "Man (Boy if child)"),
        ("Gender (veterans only)", "Culturally Specific Identity"),
        ("Gender (veterans only)", "Transgender"),
        ("Gender (veterans only)", "Non-Binary"),
        ("Gender (veterans only)", "Questioning"),
        ("Gender (veterans only)", "Different Identity"),
        ("Gender (veterans only)", "More Than One Gender"),
        ("Gender (veterans only)", "      Includes Woman (Girl if child)"),
        ("Gender (veterans only)", "      Includes Man (Boy if child)"),
        ("Gender (veterans only)", "      Includes Culturally Specific Identity"),
        ("Gender (veterans only)", "      Includes Transgender"),
        ("Gender (veterans only)", "      Includes Non-Binary"),
        ("Gender (veterans only)", "      Includes Questioning"),
        ("Gender (veterans only)", "      Includes Different Identity"),
        ("Race and Ethnicity (veterans only)", "Indigenous (American Indian/Alaska Native/Indigenous)"),
        ("Race and Ethnicity (veterans only)", "Indigenous (American Indian/Alaska Native/Indigenous) & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (veterans only)", "Asian/Asian American"),
        ("Race and Ethnicity (veterans only)", "Asian/Asian American & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (veterans only)", "Black/African American/African"),
        ("Race and Ethnicity (veterans only)", "Black/African American/African & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (veterans only)", "Hispanic/Latina/e/o"),
        ("Race and Ethnicity (veterans only)", "Middle Eastern/North African"),
        ("Race and Ethnicity (veterans only)", "Middle Eastern/North African & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (veterans only)", "Native Hawaiian/Pacific Islander"),
        ("Race and Ethnicity (veterans only)", "Native Hawaiian/Pacific Islander & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (veterans only)", "White"),
        ("Race and Ethnicity (veterans only)", "White & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (veterans only)", "Multi-Racial & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (veterans only)", "Multi-Racial (not Hispanic/Latina/e/o)"),
        ("Chronically Homeless", "Total number of persons")
    ],
    
    'YOUTH_without': [
        ("Total number of unaccompanied youth households", ""),
        ("Total number of unaccompanied youth", ""),
        ("      Number of unaccompanied youth (under age 18)", ""),
        ("      Number of unaccompanied youth (age 18 to 24)", ""),
        ("Sex (unaccompanied youth)", "Female"),
        ("Sex (unaccompanied youth)", "Male"),
        ("Gender (unaccompanied youth)", "Woman (Girl if child)"),
        ("Gender (unaccompanied youth)", "Man (Boy if child)"),
        ("Gender (unaccompanied youth)", "Culturally Specific Identity"),
        ("Gender (unaccompanied youth)", "Transgender"),
        ("Gender (unaccompanied youth)", "Non-Binary"),
        ("Gender (unaccompanied youth)", "Questioning"),
        ("Gender (unaccompanied youth)", "Different Identity"),
        ("Gender (unaccompanied youth)", "More Than One Gender"),
        ("Gender (unaccompanied youth)", "      Includes Woman (Girl if child)"),
        ("Gender (unaccompanied youth)", "      Includes Man (Boy if child)"),
        ("Gender (unaccompanied youth)", "      Includes Culturally Specific Identity"),
        ("Gender (unaccompanied youth)", "      Includes Transgender"),
        ("Gender (unaccompanied youth)", "      Includes Non-Binary"),
        ("Gender (unaccompanied youth)", "      Includes Questioning"),
        ("Gender (unaccompanied youth)", "      Includes Different Identity"),
        ("Race and Ethnicity (unaccompanied youth)", "Indigenous (American Indian/Alaska Native/Indigenous)"),
        ("Race and Ethnicity (unaccompanied youth)", "Indigenous (American Indian/Alaska Native/Indigenous) & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (unaccompanied youth)", "Asian/Asian American"),
        ("Race and Ethnicity (unaccompanied youth)", "Asian/Asian American & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (unaccompanied youth)", "Black/African American/African"),
        ("Race and Ethnicity (unaccompanied youth)", "Black/African American/African & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (unaccompanied youth)", "Hispanic/Latina/e/o"),
        ("Race and Ethnicity (unaccompanied youth)", "Middle Eastern/North African"),
        ("Race and Ethnicity (unaccompanied youth)", "Middle Eastern/North African & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (unaccompanied youth)", "Native Hawaiian/Pacific Islander"),
        ("Race and Ethnicity (unaccompanied youth)", "Native Hawaiian/Pacific Islander & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (unaccompanied youth)", "White"),
        ("Race and Ethnicity (unaccompanied youth)", "White & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (unaccompanied youth)", "Multi-Racial & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (unaccompanied youth)", "Multi-Racial (not Hispanic/Latina/e/o)"),
        ("Chronically Homeless", "Total number of persons")
    ],
    
    'YOUTH_with': [
        ("Total number of parenting youth household", ""),
        ("Total number of persons in parenting youth households", ""),
        ("Total Parenting Youth (youth parents only)", ""),
        ("Total Children in Parenting Youth Households", ""),
        ("   Number of parenting youth under age 18", ""),
        ("      Children in households with parenting youth under age 18", ""),
        ("   Number of parenting youth age 18 to 24", ""),
        ("      Children in households with parenting youth age 18 to 24", ""),
        ("Sex (youth parents only)", "Female"),
        ("Sex (youth parents only)", "Male"),
        ("Gender (youth parents only)", "Woman (Girl if child)"),
        ("Gender (youth parents only)", "Man (Boy if child)"),
        ("Gender (youth parents only)", "Culturally Specific Identity"),
        ("Gender (youth parents only)", "Transgender"),
        ("Gender (youth parents only)", "Non-Binary"),
        ("Gender (youth parents only)", "Questioning"),
        ("Gender (youth parents only)", "Different Identity"),
        ("Gender (youth parents only)", "More Than One Gender"),
        ("Gender (youth parents only)", "      Includes Woman (Girl if child)"),
        ("Gender (youth parents only)", "      Includes Man (Boy if child)"),
        ("Gender (youth parents only)", "      Includes Culturally Specific Identity"),
        ("Gender (youth parents only)", "      Includes Transgender"),
        ("Gender (youth parents only)", "      Includes Non-Binary"),
        ("Gender (youth parents only)", "      Includes Questioning"),
        ("Gender (youth parents only)", "      Includes Different Identity"),
        ("Race and Ethnicity (youth parents only)", "Indigenous (American Indian/Alaska Native/Indigenous)"),
        ("Race and Ethnicity (youth parents only)", "Indigenous (American Indian/Alaska Native/Indigenous) & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (youth parents only)", "Asian/Asian American"),
        ("Race and Ethnicity (youth parents only)", "Asian/Asian American & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (youth parents only)", "Black/African American/African"),
        ("Race and Ethnicity (youth parents only)", "Black/African American/African & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (youth parents only)", "Hispanic/Latina/e/o"),
        ("Race and Ethnicity (youth parents only)", "Middle Eastern/North African"),
        ("Race and Ethnicity (youth parents only)", "Middle Eastern/North African & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (youth parents only)", "Native Hawaiian/Pacific Islander"),
        ("Race and Ethnicity (youth parents only)", "Native Hawaiian/Pacific Islander & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (youth parents only)", "White"),
        ("Race and Ethnicity (youth parents only)", "White & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (youth parents only)", "Multi-Racial & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (youth parents only)", "Multi-Racial (not Hispanic/Latina/e/o)"),
        ("Chronically Homeless", "Total number of households"),
        ("Chronically Homeless", "Total number of persons")
    ],
    
    'INDEX_SUB': [
        ("Adults with a Serious Mental Illness", ""),
        ("Adults with a Substance Use Disorder", ""),
        ("Adults with HIV/AIDS", ""),
        ("Victims of Domestic Violence (fleeing)", "")
    ],
    
    'TOTAL_Summary': [
        ("Total number of households", ""),
        ("Total number of households", "Households with at Least One Adult and One Child"),
        ("Total number of households", "      2 members"),
        ("Total number of households", "      3 members"),
        ("Total number of households", "      4 members"),
        ("Total number of households", "      5+ members"),
        ("Total number of households", "Households without Children"),
        ("Total number of households", "Households with Only Children"),
        ("Total number of persons", ""),
        ("Total number of persons", "Number of children (under age 18)"),
        ("Total number of persons", "Number of young adults (age 18 to 24)"),
        ("Total number of persons", "Adults (25-34)"),
        ("Total number of persons", "Adults (35-44)"),
        ("Total number of persons", "Adults (45-54)"),
        ("Total number of persons", "Adults (55-64)"),
        ("Total number of persons", "Adults (65+)"),
        ("Total number of persons", "Unreported Age"),
        ("Sex (adults and children)", "Female"),
        ("Sex (adults and children)", "Male"),
        ("Gender (adults and children)", "Woman (Girl if child)"),
        ("Gender (adults and children)", "Man (Boy if child)"),
        ("Gender (adults and children)", "Culturally Specific Identity"),
        ("Gender (adults and children)", "Transgender"),
        ("Gender (adults and children)", "Non-Binary"),
        ("Gender (adults and children)", "Questioning"),
        ("Gender (adults and children)", "Different Identity"),
        ("Gender (adults and children)", "More Than One Gender"),
        ("Gender (adults and children)", "      Includes Woman (Girl if child)"),
        ("Gender (adults and children)", "      Includes Man (Boy if child)"),
        ("Gender (adults and children)", "      Includes Culturally Specific Identity"),
        ("Gender (adults and children)", "      Includes Transgender"),
        ("Gender (adults and children)", "      Includes Non-Binary"),
        ("Gender (adults and children)", "      Includes Questioning"),
        ("Gender (adults and children)", "      Includes Different Identity"),
        ("Race and Ethnicity (adults and children)", "Indigenous (American Indian/Alaska Native/Indigenous)"),
        ("Race and Ethnicity (adults and children)", "Indigenous (American Indian/Alaska Native/Indigenous) & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (adults and children)", "Asian/Asian American"),
        ("Race and Ethnicity (adults and children)", "Asian/Asian American & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (adults and children)", "Black/African American/African"),
        ("Race and Ethnicity (adults and children)", "Black/African American/African & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (adults and children)", "Hispanic/Latina/e/o"),
        ("Race and Ethnicity (adults and children)", "Middle Eastern/North African"),
        ("Race and Ethnicity (adults and children)", "Middle Eastern/North African & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (adults and children)", "Native Hawaiian/Pacific Islander"),
        ("Race and Ethnicity (adults and children)", "Native Hawaiian/Pacific Islander & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (adults and children)", "White"),
        ("Race and Ethnicity (adults and children)", "White & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (adults and children)", "Multi-Racial & Hispanic/Latina/e/o"),
        ("Race and Ethnicity (adults and children)", "Multi-Racial (not Hispanic/Latina/e/o)"),
        ("Subpopulations", "Chronically homeless HOUSEHOLDS"),
        ("Subpopulations", "Chronically homeless persons"),
        ("Subpopulations", "Veterans"),
        ("Subpopulations", "DV households"),
        ("Subpopulations", "DV survivors"),
        ("Subpopulations", "Unaccompanied youth households"),
        ("Subpopulations", "Parenting youth households"),
        ("Chronic Health Conditions (Adults)", "Physical Disability"),
        ("Chronic Health Conditions (Adults)", "Developmental Condition"),
        ("Chronic Health Conditions (Adults)", "Mental Health"),
        ("Chronic Health Conditions (Adults)", "Chronic Substance Abuse"),
        ("Chronic Health Conditions (Adults)", "HIV_AIDS"),
        ("Chronic Health Conditions (Adults)", "Other Chronic Health Conditions"),
        ("Chronic Health Conditions (Children)", "Physical Disability"),
        ("Chronic Health Conditions (Children)", "Developmental Condition"),
        ("Chronic Health Conditions (Children)", "Mental Health"),
        ("Chronic Health Conditions (Children)", "Chronic Substance Abuse"),
        ("Chronic Health Conditions (Children)", "HIV_AIDS"),
        ("Chronic Health Conditions (Children)", "Other Chronic Health Conditions"),
        ("History of Homelessness", "First Time Homeless"),
        ("History of Homelessness", "Length of Time Homeless(Less than one month)"),
        ("History of Homelessness", "Length of Time Homeless(One to three months)"),
        ("History of Homelessness", "Length of Time Homeless(Three months to one year)"),
        ("History of Homelessness", "Length of Time Homeless(One year or more)"),
        ("History of Homelessness (HHs)", "First Time Homeless"),
        ("History of Homelessness (HHs)", "Length of Time Homeless(Less than one month)"),
        ("History of Homelessness (HHs)", "Length of Time Homeless(One to three months)"),
        ("History of Homelessness (HHs)", "Length of Time Homeless(Three months to one year)"),
        ("History of Homelessness (HHs)", "Length of Time Homeless(One year or more)")
    ]
}

# Template mappings (maps template indices to calculation keys)
TEMPLATE_MAPPINGS = {
    'mapping_with': [
        (("Total number of households", ""), 'Total_number_of_households'),
        (("Total number of persons (adults & children)", ""), 'Total_number_of_persons'),
        (("      Number of children (under age 18)", ""), 'Number_of_children'),
        (("      Number of young (age 18 to 24)", ""), 'Number_of_young_adults'),
        (("      Number of adults (age 25 to 34)", ""), 'Number_of_adults_25-34'),
        (("      Number of adults (age 35 to 44)", ""), 'Number_of_adults_35-44'),
        (("      Number of adults (age 45 to 54)", ""), 'Number_of_adults_45-54'),
        (("      Number of adults (age 55 to 64)", ""), 'Number_of_adults_55-64'),
        (("      Number of adults (age 65 or older)", ""), 'Number_of_adults_65+'),
        (("Sex (adults and children)", "Female"), 'Female'),
        (("Sex (adults and children)", "Male"), 'Male'),
        (("Gender (adults and children)", "Woman (Girl if child)"), 'Woman_Girl'),
        (("Gender (adults and children)", "Man (Boy if child)"), 'Man_Boy'),
        (("Gender (adults and children)", "Culturally Specific Identity"), 'Culturally_Specific_Identity'),
        (("Gender (adults and children)", "Transgender"), 'Transgender'),
        (("Gender (adults and children)", "Non-Binary"), 'Non_Binary'),
        (("Gender (adults and children)", "Questioning"), 'Questioning'),
        (("Gender (adults and children)", "Different Identity"), 'Different_Identity'),
        (("Gender (adults and children)", "More Than One Gender"), 'More_Than_One_Gender'),
        (("Gender (adults and children)", "      Includes Woman (Girl if child)"), 'Includes_Woman_Girl'),
        (("Gender (adults and children)", "      Includes Man (Boy if child)"), 'Includes_Man_Boy'),
        (("Gender (adults and children)", "      Includes Culturally Specific Identity"), 'Includes_Culturally_Specific_Identity'),
        (("Gender (adults and children)", "      Includes Transgender"), 'Includes_Transgender'),
        (("Gender (adults and children)", "      Includes Non-Binary"), 'Includes_Non_Binary'),
        (("Gender (adults and children)", "      Includes Questioning"), 'Includes_Questioning'),
        (("Gender (adults and children)", "      Includes Different Identity"),'Includes_Different_Identity'),
        (("Race and Ethnicity (adults and children)", "Indigenous (American Indian/Alaska Native/Indigenous)"), 'Indigenous'),
(("Race and Ethnicity (adults and children)", "Indigenous (American Indian/Alaska Native/Indigenous) & Hispanic/Latina/e/o"), 'Indigenous_Hispanic'),
        (("Race and Ethnicity (adults and children)", "Asian/Asian American"), 'Asian'),
        (("Race and Ethnicity (adults and children)", "Asian/Asian American & Hispanic/Latina/e/o"), 'Asian_Hispanic'),
        (("Race and Ethnicity (adults and children)", "Black/African American/African"), 'Black'),
        (("Race and Ethnicity (adults and children)", "Black/African American/African & Hispanic/Latina/e/o"), 'Black_Hispanic'),
        (("Race and Ethnicity (adults and children)", "Hispanic/Latina/e/o"), 'Hispanic'),
        (("Race and Ethnicity (adults and children)", "Middle Eastern/North African"), 'Middle_Eastern_North_African'),
        (("Race and Ethnicity (adults and children)", "Middle Eastern/North African & Hispanic/Latina/e/o"), 'Middle_Eastern_North_African_Hispanic'),
        (("Race and Ethnicity (adults and children)", "Native Hawaiian/Pacific Islander"), 'Native_Hawaiian'),
        (("Race and Ethnicity (adults and children)", "Native Hawaiian/Pacific Islander & Hispanic/Latina/e/o"), 'Native_Hawaiian_Hispanic'),
        (("Race and Ethnicity (adults and children)", "White"), 'White'),
        (("Race and Ethnicity (adults and children)", "White & Hispanic/Latina/e/o"), 'White_Hispanic'),
        (("Race and Ethnicity (adults and children)", "Multi-Racial & Hispanic/Latina/e/o"), 'Multi_Racial_Hispanic'),
        (("Race and Ethnicity (adults and children)", "Multi-Racial (not Hispanic/Latina/e/o)"), 'Multi_Racial_Non_Hispanic'),
        (("Chronically Homeless", "Total number of households"), 'CH_Total_number_of_households'),
        (("Chronically Homeless", "Total number of persons"), 'CH_Total_number_of_persons')
    ],
    
    'mapping_without': [
        (("Total number of households", ""), 'Total_number_of_households'),
        (("Total number of persons", ""), 'Total_number_of_persons'),
        (("      Number of young (age 18 to 24)", ""), 'Number_of_young_adults'),
        (("      Number of adults (age 25 to 34)", ""), 'Number_of_adults_25-34'),
        (("      Number of adults (age 35 to 44)", ""), 'Number_of_adults_35-44'),
        (("      Number of adults (age 45 to 54)", ""), 'Number_of_adults_45-54'),
        (("      Number of adults (age 55 to 64)", ""), 'Number_of_adults_55-64'),
        (("      Number of adults (age 65 or older)", ""), 'Number_of_adults_65+'),
        (("Sex", "Female"), 'Female'),
        (("Sex", "Male"), 'Male'),
        (("Gender", "Woman (Girl if child)"), 'Woman_Girl'),
        (("Gender", "Man (Boy if child)"), 'Man_Boy'),
        (("Gender", "Culturally Specific Identity"), 'Culturally_Specific_Identity'),
        (("Gender", "Transgender"), 'Transgender'),
        (("Gender", "Non-Binary"), 'Non_Binary'),
        (("Gender", "Questioning"), 'Questioning'),
        (("Gender", "Different Identity"), 'Different_Identity'),
        (("Gender", "More Than One Gender"), 'More_Than_One_Gender'),
        (("Gender", "      Includes Woman (Girl if child)"), 'Includes_Woman_Girl'),
        (("Gender", "      Includes Man (Boy if child)"), 'Includes_Man_Boy'),
        (("Gender", "      Includes Culturally Specific Identity"), 'Includes_Culturally_Specific_Identity'),
        (("Gender", "      Includes Transgender"), 'Includes_Transgender'),
        (("Gender", "      Includes Non-Binary"), 'Includes_Non_Binary'),
        (("Gender", "      Includes Questioning"), 'Includes_Questioning'),
        (("Gender", "      Includes Different Identity"),'Includes_Different_Identity'),
        (("Race and Ethnicity", "Indigenous (American Indian/Alaska Native/Indigenous)"), 'Indigenous'),
        (("Race and Ethnicity", "Indigenous (American Indian/Alaska Native/Indigenous) & Hispanic/Latina/e/o"), 'Indigenous_Hispanic'),
        (("Race and Ethnicity", "Asian/Asian American"), 'Asian'),
        (("Race and Ethnicity", "Asian/Asian American & Hispanic/Latina/e/o"), 'Asian_Hispanic'),
        (("Race and Ethnicity", "Black/African American/African"), 'Black'),
        (("Race and Ethnicity", "Black/African American/African & Hispanic/Latina/e/o"), 'Black_Hispanic'),
        (("Race and Ethnicity", "Hispanic/Latina/e/o"), 'Hispanic'),
        (("Race and Ethnicity", "Middle Eastern/North African"), 'Middle_Eastern_North_African'),
        (("Race and Ethnicity", "Middle Eastern/North African & Hispanic/Latina/e/o"), 'Middle_Eastern_North_African_Hispanic'),
        (("Race and Ethnicity", "Native Hawaiian/Pacific Islander"), 'Native_Hawaiian'),
        (("Race and Ethnicity", "Native Hawaiian/Pacific Islander & Hispanic/Latina/e/o"), 'Native_Hawaiian_Hispanic'),
        (("Race and Ethnicity", "White"), 'White'),
        (("Race and Ethnicity", "White & Hispanic/Latina/e/o"), 'White_Hispanic'),
        (("Race and Ethnicity", "Multi-Racial & Hispanic/Latina/e/o"), 'Multi_Racial_Hispanic'),
        (("Race and Ethnicity", "Multi-Racial (not Hispanic/Latina/e/o)"), 'Multi_Racial_Non_Hispanic'),
        (("Chronically Homeless", "Total number of persons"), 'CH_Total_number_of_persons')
    ],
    
    'mapping_withonly': [
        (("Total number of households", ""), 'Total_number_of_households'),
        (("Number of children (persons under age 18)", ""), 'Total_number_of_persons'),
        (("Sex", "Female"), 'Female'),
        (("Sex", "Male"), 'Male'),
        (("Gender", "Woman (Girl if child)"), 'Woman_Girl'),
        (("Gender", "Man (Boy if child)"), 'Man_Boy'),
        (("Gender", "Culturally Specific Identity"), 'Culturally_Specific_Identity'),
        (("Gender", "Transgender"), 'Transgender'),
        (("Gender", "Non-Binary"), 'Non_Binary'),
        (("Gender", "Questioning"), 'Questioning'),
        (("Gender", "Different Identity"), 'Different_Identity'),
        (("Gender", "More Than One Gender"), 'More_Than_One_Gender'),
        (("Gender", "      Includes Woman (Girl if child)"), 'Includes_Woman_Girl'),
        (("Gender", "      Includes Man (Boy if child)"), 'Includes_Man_Boy'),
        (("Gender", "      Includes Culturally Specific Identity"), 'Includes_Culturally_Specific_Identity'),
        (("Gender", "      Includes Transgender"), 'Includes_Transgender'),
        (("Gender", "      Includes Non-Binary"), 'Includes_Non_Binary'),
        (("Gender", "      Includes Questioning"), 'Includes_Questioning'),
        (("Gender", "      Includes Different Identity"),'Includes_Different_Identity'),
        (("Race and Ethnicity", "Indigenous (American Indian/Alaska Native/Indigenous)"), 'Indigenous'),
        (("Race and Ethnicity", "Indigenous (American Indian/Alaska Native/Indigenous) & Hispanic/Latina/e/o"), 'Indigenous_Hispanic'),
        (("Race and Ethnicity", "Asian/Asian American"), 'Asian'),
        (("Race and Ethnicity", "Asian/Asian American & Hispanic/Latina/e/o"), 'Asian_Hispanic'),
        (("Race and Ethnicity", "Black/African American/African"), 'Black'),
        (("Race and Ethnicity", "Black/African American/African & Hispanic/Latina/e/o"), 'Black_Hispanic'),
        (("Race and Ethnicity", "Hispanic/Latina/e/o"), 'Hispanic'),
        (("Race and Ethnicity", "Middle Eastern/North African"), 'Middle_Eastern_North_African'),
        (("Race and Ethnicity", "Middle Eastern/North African & Hispanic/Latina/e/o"), 'Middle_Eastern_North_African_Hispanic'),
        (("Race and Ethnicity", "Native Hawaiian/Pacific Islander"), 'Native_Hawaiian'),
        (("Race and Ethnicity", "Native Hawaiian/Pacific Islander & Hispanic/Latina/e/o"), 'Native_Hawaiian_Hispanic'),
        (("Race and Ethnicity", "White"), 'White'),
        (("Race and Ethnicity", "White & Hispanic/Latina/e/o"), 'White_Hispanic'),
        (("Race and Ethnicity", "Multi-Racial & Hispanic/Latina/e/o"), 'Multi_Racial_Hispanic'),
        (("Race and Ethnicity", "Multi-Racial (not Hispanic/Latina/e/o)"), 'Multi_Racial_Non_Hispanic'),
        (("Chronically Homeless", "Total number of persons"), 'CH_Total_number_of_persons')
    ],
    
    'mapping_vet_with': [
        (("Total number of households", ""), 'Total_number_of_households'),
        (("Total number of persons", ""), 'Total_number_of_persons'),
        (("Total number of veterans", ""), 'Total number of veterans'),
        (("Sex (veterans only)", "Female"), 'Female'),
        (("Sex (veterans only)", "Male"), 'Male'),
        (("Gender (veterans only)", "Woman (Girl if child)"), 'Woman_Girl'),
        (("Gender (veterans only)", "Man (Boy if child)"), 'Man_Boy'),
        (("Gender (veterans only)", "Culturally Specific Identity"), 'Culturally_Specific_Identity'),
        (("Gender (veterans only)", "Transgender"), 'Transgender'),
        (("Gender (veterans only)", "Non-Binary"), 'Non_Binary'),
        (("Gender (veterans only)", "Questioning"), 'Questioning'),
        (("Gender (veterans only)", "Different Identity"), 'Different_Identity'),
        (("Gender (veterans only)", "More Than One Gender"), 'More_Than_One_Gender'),
        (("Gender (veterans only)", "      Includes Woman (Girl if child)"), 'Includes_Woman_Girl'),
        (("Gender (veterans only)", "      Includes Man (Boy if child)"), 'Includes_Man_Boy'),
        (("Gender (veterans only)", "      Includes Culturally Specific Identity"), 'Includes_Culturally_Specific_Identity'),
        (("Gender (veterans only)", "      Includes Transgender"), 'Includes_Transgender'),
        (("Gender (veterans only)", "      Includes Non-Binary"), 'Includes_Non_Binary'),
        (("Gender (veterans only)", "      Includes Questioning"), 'Includes_Questioning'),
        (("Gender (veterans only)", "      Includes Different Identity"),'Includes_Different_Identity'),
        (("Race and Ethnicity (veterans only)", "Indigenous (American Indian/Alaska Native/Indigenous)"), 'Indigenous'),
        (("Race and Ethnicity (veterans only)", "Indigenous (American Indian/Alaska Native/Indigenous) & Hispanic/Latina/e/o"), 'Indigenous_Hispanic'),
        (("Race and Ethnicity (veterans only)", "Asian/Asian American"), 'Asian'),
        (("Race and Ethnicity (veterans only)", "Asian/Asian American & Hispanic/Latina/e/o"), 'Asian_Hispanic'),
        (("Race and Ethnicity (veterans only)", "Black/African American/African"), 'Black'),
        (("Race and Ethnicity (veterans only)", "Black/African American/African & Hispanic/Latina/e/o"), 'Black_Hispanic'),
        (("Race and Ethnicity (veterans only)", "Hispanic/Latina/e/o"), 'Hispanic'),
        (("Race and Ethnicity (veterans only)", "Middle Eastern/North African"), 'Middle_Eastern_North_African'),
        (("Race and Ethnicity (veterans only)", "Middle Eastern/North African & Hispanic/Latina/e/o"), 'Middle_Eastern_North_African_Hispanic'),
        (("Race and Ethnicity (veterans only)", "Native Hawaiian/Pacific Islander"), 'Native_Hawaiian'),
        (("Race and Ethnicity (veterans only)", "Native Hawaiian/Pacific Islander & Hispanic/Latina/e/o"), 'Native_Hawaiian_Hispanic'),
        (("Race and Ethnicity (veterans only)", "White"), 'White'),
        (("Race and Ethnicity (veterans only)", "White & Hispanic/Latina/e/o"), 'White_Hispanic'),
        (("Race and Ethnicity (veterans only)", "Multi-Racial & Hispanic/Latina/e/o"), 'Multi_Racial_Hispanic'),
        (("Race and Ethnicity (veterans only)", "Multi-Racial (not Hispanic/Latina/e/o)"), 'Multi_Racial_Non_Hispanic'),
        (("Chronically Homeless", "Total number of households"), 'CH_Total_number_of_households'),
        (("Chronically Homeless", "Total number of persons"), 'CH_Total_number_of_persons')
    ],
    
    'mapping_vet_without': [
        (("Total number of households", ""), 'Total_number_of_households'),
        (("Total number of persons", ""), 'Total_number_of_persons'),
        (("Total number of veterans", ""), 'Total number of veterans'),
        (("Sex (veterans only)", "Female"), 'Female'),
        (("Sex (veterans only)", "Male"), 'Male'),
        (("Gender (veterans only)", "Woman (Girl if child)"), 'Woman_Girl'),
        (("Gender (veterans only)", "Man (Boy if child)"), 'Man_Boy'),
        (("Gender (veterans only)", "Culturally Specific Identity"), 'Culturally_Specific_Identity'),
        (("Gender (veterans only)", "Transgender"), 'Transgender'),
        (("Gender (veterans only)", "Non-Binary"), 'Non_Binary'),
        (("Gender (veterans only)", "Questioning"), 'Questioning'),
        (("Gender (veterans only)", "Different Identity"), 'Different_Identity'),
        (("Gender (veterans only)", "More Than One Gender"), 'More_Than_One_Gender'),
        (("Gender (veterans only)", "      Includes Woman (Girl if child)"), 'Includes_Woman_Girl'),
        (("Gender (veterans only)", "      Includes Man (Boy if child)"), 'Includes_Man_Boy'),
        (("Gender (veterans only)", "      Includes Culturally Specific Identity"), 'Includes_Culturally_Specific_Identity'),
        (("Gender (veterans only)", "      Includes Transgender"), 'Includes_Transgender'),
        (("Gender (veterans only)", "      Includes Non-Binary"), 'Includes_Non_Binary'),
        (("Gender (veterans only)", "      Includes Questioning"), 'Includes_Questioning'),
        (("Gender (veterans only)", "      Includes Different Identity"),'Includes_Different_Identity'),
        (("Race and Ethnicity (veterans only)", "Indigenous (American Indian/Alaska Native/Indigenous)"), 'Indigenous'),
        (("Race and Ethnicity (veterans only)", "Indigenous (American Indian/Alaska Native/Indigenous) & Hispanic/Latina/e/o"), 'Indigenous_Hispanic'),
        (("Race and Ethnicity (veterans only)", "Asian/Asian American"), 'Asian'),
        (("Race and Ethnicity (veterans only)", "Asian/Asian American & Hispanic/Latina/e/o"), 'Asian_Hispanic'),
        (("Race and Ethnicity (veterans only)", "Black/African American/African"), 'Black'),
        (("Race and Ethnicity (veterans only)", "Black/African American/African & Hispanic/Latina/e/o"), 'Black_Hispanic'),
        (("Race and Ethnicity (veterans only)", "Hispanic/Latina/e/o"), 'Hispanic'),
        (("Race and Ethnicity (veterans only)", "Middle Eastern/North African"), 'Middle_Eastern_North_African'),
        (("Race and Ethnicity (veterans only)", "Middle Eastern/North African & Hispanic/Latina/e/o"), 'Middle_Eastern_North_African_Hispanic'),
        (("Race and Ethnicity (veterans only)", "Native Hawaiian/Pacific Islander"), 'Native_Hawaiian'),
        (("Race and Ethnicity (veterans only)", "Native Hawaiian/Pacific Islander & Hispanic/Latina/e/o"), 'Native_Hawaiian_Hispanic'),
        (("Race and Ethnicity (veterans only)", "White"), 'White'),
        (("Race and Ethnicity (veterans only)", "White & Hispanic/Latina/e/o"), 'White_Hispanic'),
        (("Race and Ethnicity (veterans only)", "Multi-Racial & Hispanic/Latina/e/o"), 'Multi_Racial_Hispanic'),
        (("Race and Ethnicity (veterans only)", "Multi-Racial (not Hispanic/Latina/e/o)"), 'Multi_Racial_Non_Hispanic'),
        (("Chronically Homeless", "Total number of persons"), 'CH_Total_number_of_persons')
    ],
    
    'mapping_youth_without': [
        (("Total number of unaccompanied youth households", ""), 'Total_number_of_households'),
        (("Total number of unaccompanied youth", ""), 'Total_number_of_persons'),
        (("      Number of unaccompanied youth (under age 18)", ""), 'Number_of_children'),
        (("      Number of unaccompanied youth (age 18 to 24)", ""), 'Number_of_young_adults'),
        (("Sex (unaccompanied youth)", "Female"), 'Female'),
        (("Sex (unaccompanied youth)", "Male"), 'Male'),
        (("Gender (unaccompanied youth)", "Woman (Girl if child)"), 'Woman_Girl'),
        (("Gender (unaccompanied youth)", "Man (Boy if child)"), 'Man_Boy'),
        (("Gender (unaccompanied youth)", "Culturally Specific Identity"), 'Culturally_Specific_Identity'),
        (("Gender (unaccompanied youth)", "Transgender"), 'Transgender'),
        (("Gender (unaccompanied youth)", "Non-Binary"), 'Non_Binary'),
        (("Gender (unaccompanied youth)", "Questioning"), 'Questioning'),
        (("Gender (unaccompanied youth)", "Different Identity"), 'Different_Identity'),
        (("Gender (unaccompanied youth)", "More Than One Gender"), 'More_Than_One_Gender'),
        (("Gender (unaccompanied youth)", "      Includes Woman (Girl if child)"), 'Includes_Woman_Girl'),
        (("Gender (unaccompanied youth)", "      Includes Man (Boy if child)"), 'Includes_Man_Boy'),
        (("Gender (unaccompanied youth)", "      Includes Culturally Specific Identity"), 'Includes_Culturally_Specific_Identity'),
        (("Gender (unaccompanied youth)", "      Includes Transgender"), 'Includes_Transgender'),
        (("Gender (unaccompanied youth)", "      Includes Non-Binary"), 'Includes_Non_Binary'),
        (("Gender (unaccompanied youth)", "      Includes Questioning"), 'Includes_Questioning'),
        (("Gender (unaccompanied youth)", "      Includes Different Identity"),'Includes_Different_Identity'),
        (("Race and Ethnicity (unaccompanied youth)", "Indigenous (American Indian/Alaska Native/Indigenous)"), 'Indigenous'),
        (("Race and Ethnicity (unaccompanied youth)", "Indigenous (American Indian/Alaska Native/Indigenous) & Hispanic/Latina/e/o"), 'Indigenous_Hispanic'),
        (("Race and Ethnicity (unaccompanied youth)", "Asian/Asian American"), 'Asian'),
        (("Race and Ethnicity (unaccompanied youth)", "Asian/Asian American & Hispanic/Latina/e/o"), 'Asian_Hispanic'),
        (("Race and Ethnicity (unaccompanied youth)", "Black/African American/African"), 'Black'),
        (("Race and Ethnicity (unaccompanied youth)", "Black/African American/African & Hispanic/Latina/e/o"), 'Black_Hispanic'),
        (("Race and Ethnicity (unaccompanied youth)", "Hispanic/Latina/e/o"), 'Hispanic'),
        (("Race and Ethnicity (unaccompanied youth)", "Middle Eastern/North African"), 'Middle_Eastern_North_African'),
        (("Race and Ethnicity (unaccompanied youth)", "Middle Eastern/North African & Hispanic/Latina/e/o"), 'Middle_Eastern_North_African_Hispanic'),
        (("Race and Ethnicity (unaccompanied youth)", "Native Hawaiian/Pacific Islander"), 'Native_Hawaiian'),
        (("Race and Ethnicity (unaccompanied youth)", "Native Hawaiian/Pacific Islander & Hispanic/Latina/e/o"), 'Native_Hawaiian_Hispanic'),
        (("Race and Ethnicity (unaccompanied youth)", "White"), 'White'),
        (("Race and Ethnicity (unaccompanied youth)", "White & Hispanic/Latina/e/o"), 'White_Hispanic'),
        (("Race and Ethnicity (unaccompanied youth)", "Multi-Racial & Hispanic/Latina/e/o"), 'Multi_Racial_Hispanic'),
        (("Race and Ethnicity (unaccompanied youth)", "Multi-Racial (not Hispanic/Latina/e/o)"), 'Multi_Racial_Non_Hispanic'),
        (("Chronically Homeless", "Total number of persons"), 'CH_Total_number_of_persons')
    ],
    
    'mapping_youth_with': [
        (("Total number of parenting youth household", ""), 'Total_number_of_households'),
        (("Total number of persons in parenting youth households", ""), 'Total_number_of_persons'),
        (("Total Parenting Youth (youth parents only)", ""), 'Total_Parenting_Youth'),
        (("Total Children in Parenting Youth Households", ""), 'Number_of_children'),
        (("   Number of parenting youth under age 18", ""), 'Number_of_parenting_youth_under_age_18'),
        (("      Children in households with parenting youth under age 18", ""), 'Children_with_parenting_youth_under_18'),
        (("   Number of parenting youth age 18 to 24", ""), 'Number_of_young_adults'),
        (("      Children in households with parenting youth age 18 to 24", ""), 'Children_with_parenting_youth_18_24'),
        (("Sex (youth parents only)", "Female"), 'Female'),
        (("Sex (youth parents only)", "Male"), 'Male'),
        (("Gender (youth parents only)", "Woman (Girl if child)"), 'Woman_Girl'),
        (("Gender (youth parents only)", "Man (Boy if child)"), 'Man_Boy'),
        (("Gender (youth parents only)", "Culturally Specific Identity"), 'Culturally_Specific_Identity'),
        (("Gender (youth parents only)", "Transgender"), 'Transgender'),
        (("Gender (youth parents only)", "Non-Binary"), 'Non_Binary'),
        (("Gender (youth parents only)", "Questioning"), 'Questioning'),
        (("Gender (youth parents only)", "Different Identity"), 'Different_Identity'),
        (("Gender (youth parents only)", "More Than One Gender"), 'More_Than_One_Gender'),
        (("Gender (youth parents only)", "      Includes Woman (Girl if child)"), 'Includes_Woman_Girl'),
        (("Gender (youth parents only)", "      Includes Man (Boy if child)"), 'Includes_Man_Boy'),
        (("Gender (youth parents only)", "      Includes Culturally Specific Identity"), 'Includes_Culturally_Specific_Identity'),
        (("Gender (youth parents only)", "      Includes Transgender"), 'Includes_Transgender'),
        (("Gender (youth parents only)", "      Includes Non-Binary"), 'Includes_Non_Binary'),
        (("Gender (youth parents only)", "      Includes Questioning"), 'Includes_Questioning'),
        (("Gender (youth parents only)", "      Includes Different Identity"),'Includes_Different_Identity'),
        (("Race and Ethnicity (youth parents only)", "Indigenous (American Indian/Alaska Native/Indigenous)"), 'Indigenous'),
        (("Race and Ethnicity (youth parents only)", "Indigenous (American Indian/Alaska Native/Indigenous) & Hispanic/Latina/e/o"), 'Indigenous_Hispanic'),
        (("Race and Ethnicity (youth parents only)", "Asian/Asian American"), 'Asian'),
        (("Race and Ethnicity (youth parents only)", "Asian/Asian American & Hispanic/Latina/e/o"), 'Asian_Hispanic'),
        (("Race and Ethnicity (youth parents only)", "Black/African American/African"), 'Black'),
        (("Race and Ethnicity (youth parents only)", "Black/African American/African & Hispanic/Latina/e/o"), 'Black_Hispanic'),
        (("Race and Ethnicity (youth parents only)", "Hispanic/Latina/e/o"), 'Hispanic'),
        (("Race and Ethnicity (youth parents only)", "Middle Eastern/North African"), 'Middle_Eastern_North_African'),
        (("Race and Ethnicity (youth parents only)", "Middle Eastern/North African & Hispanic/Latina/e/o"), 'Middle_Eastern_North_African_Hispanic'),
        (("Race and Ethnicity (youth parents only)", "Native Hawaiian/Pacific Islander"), 'Native_Hawaiian'),
        (("Race and Ethnicity (youth parents only)", "Native Hawaiian/Pacific Islander & Hispanic/Latina/e/o"), 'Native_Hawaiian_Hispanic'),
        (("Race and Ethnicity (youth parents only)", "White"), 'White'),
        (("Race and Ethnicity (youth parents only)", "White & Hispanic/Latina/e/o"), 'White_Hispanic'),
        (("Race and Ethnicity (youth parents only)", "Multi-Racial & Hispanic/Latina/e/o"), 'Multi_Racial_Hispanic'),
        (("Race and Ethnicity (youth parents only)", "Multi-Racial (not Hispanic/Latina/e/o)"), 'Multi_Racial_Non_Hispanic'),
        (("Chronically Homeless", "Total number of households"), 'CH_Total_number_of_households'),
        (("Chronically Homeless", "Total number of persons"), 'CH_Total_number_of_persons')
    ],
    
    'mapping_SUB': [
        (("Adults with a Serious Mental Illness", ""), 'Adults_with_a_Serious_Mental_Illness'),
        (("Adults with a Substance Use Disorder", ""), 'Adults_with_a_Substance_Use_Disorder'),
        (("Adults with HIV/AIDS", ""), 'Adults_with_a_HIV_AIDS'),
        (("Victims of Domestic Violence (fleeing)", ""), 'Victims_of_Domestic_Violence_(fleeing)')
    ],
    
    'mapping_Summary': [
        (("Total number of households", ""), 'Total_number_of_households'),
        (("Total number of households", "Households with at Least One Adult and One Child"), 'Households_with_Child'),
        (("Total number of households", "      2 members"), 'Households_2_members'),
        (("Total number of households", "      3 members"), 'Households_3_members'),
        (("Total number of households", "      4 members"), 'Households_4_members'),
        (("Total number of households", "      5+ members"), 'Households_5+_members'),
        (("Total number of households", "Households without Children"), 'Households_without_Children'),
        (("Total number of households", "Households with Only Children"), 'Households_with_Only_Children'),
        (("Total number of persons", ""), 'Total_number_of_persons'),
        (("Total number of persons", "Number of children (under age 18)"), 'Number_of_children'),
        (("Total number of persons", "Number of young adults (age 18 to 24)"), 'Number_of_young_adults'),
        (("Total number of persons", "Adults (25-34)"), 'Number_of_adults_25-34'),
        (("Total number of persons", "Adults (35-44)"), 'Number_of_adults_35-44'),
        (("Total number of persons", "Adults (45-54)"), 'Number_of_adults_45-54'),
        (("Total number of persons", "Adults (55-64)"), 'Number_of_adults_55-64'),
        (("Total number of persons", "Adults (65+)"), 'Number_of_adults_65+'),
        (("Total number of persons", "Unreported Age"), 'Unreported_Age'),
        (("Sex (adults and children)", "Female"), 'Female'),
        (("Sex (adults and children)", "Male"), 'Male'),
        (("Gender (adults and children)", "Woman (Girl if child)"), 'Woman_Girl'),
        (("Gender (adults and children)", "Man (Boy if child)"), 'Man_Boy'),
        (("Gender (adults and children)", "Culturally Specific Identity"), 'Culturally_Specific_Identity'),
        (("Gender (adults and children)", "Transgender"), 'Transgender'),
        (("Gender (adults and children)", "Non-Binary"), 'Non_Binary'),
        (("Gender (adults and children)", "Questioning"), 'Questioning'),
        (("Gender (adults and children)", "Different Identity"), 'Different_Identity'),
        (("Gender (adults and children)", "More Than One Gender"), 'More_Than_One_Gender'),
        (("Gender (adults and children)", "      Includes Woman (Girl if child)"), 'Includes_Woman_Girl'),
        (("Gender (adults and children)", "      Includes Man (Boy if child)"), 'Includes_Man_Boy'),
        (("Gender (adults and children)", "      Includes Culturally Specific Identity"), 'Includes_Culturally_Specific_Identity'),
        (("Gender (adults and children)", "      Includes Transgender"), 'Includes_Transgender'),
        (("Gender (adults and children)", "      Includes Non-Binary"), 'Includes_Non_Binary'),
        (("Gender (adults and children)", "      Includes Questioning"), 'Includes_Questioning'),
        (("Gender (adults and children)", "      Includes Different Identity"), 'Includes_Different_Identity'),
        (("Race and Ethnicity (adults and children)", "Indigenous (American Indian/Alaska Native/Indigenous)"), 'Indigenous'),
        (("Race and Ethnicity (adults and children)", "Indigenous (American Indian/Alaska Native/Indigenous) & Hispanic/Latina/e/o"), 'Indigenous_Hispanic'),
        (("Race and Ethnicity (adults and children)", "Asian/Asian American"), 'Asian'),
        (("Race and Ethnicity (adults and children)", "Asian/Asian American & Hispanic/Latina/e/o"), 'Asian_Hispanic'),
        (("Race and Ethnicity (adults and children)", "Black/African American/African"), 'Black'),
        (("Race and Ethnicity (adults and children)", "Black/African American/African & Hispanic/Latina/e/o"), 'Black_Hispanic'),
        (("Race and Ethnicity (adults and children)", "Hispanic/Latina/e/o"), 'Hispanic'),
        (("Race and Ethnicity (adults and children)", "Middle Eastern/North African"), 'Middle_Eastern_North_African'),
        (("Race and Ethnicity (adults and children)", "Middle Eastern/North African & Hispanic/Latina/e/o"), 'Middle_Eastern_North_African_Hispanic'),
        (("Race and Ethnicity (adults and children)", "Native Hawaiian/Pacific Islander"), 'Native_Hawaiian'),
        (("Race and Ethnicity (adults and children)", "Native Hawaiian/Pacific Islander & Hispanic/Latina/e/o"), 'Native_Hawaiian_Hispanic'),
        (("Race and Ethnicity (adults and children)", "White"), 'White'),
        (("Race and Ethnicity (adults and children)", "White & Hispanic/Latina/e/o"), 'White_Hispanic'),
        (("Race and Ethnicity (adults and children)", "Multi-Racial & Hispanic/Latina/e/o"), 'Multi_Racial_Hispanic'),
        (("Race and Ethnicity (adults and children)", "Multi-Racial (not Hispanic/Latina/e/o)"), 'Multi_Racial_Non_Hispanic'),
        (("Subpopulations", "Chronically homeless HOUSEHOLDS"), 'CH_Total_number_of_households'),
        (("Subpopulations", "Chronically homeless persons"), 'CH_Total_number_of_persons'),
        (("Subpopulations", "Veterans"), 'Total number of veterans'),
        (("Subpopulations", "DV households"), 'Victims_of_Domestic_Violence_(Household)'),
        (("Subpopulations", "DV survivors"), 'Victims_of_Domestic_Violence_(fleeing)'),
        (("Subpopulations", "Unaccompanied youth households"), 'Total_Unaccompanied_Youth_hh'),
        (("Subpopulations", "Parenting youth households"), 'Total_Parenting_Youth_hh'),
        (("Chronic Health Conditions (Adults)", "Physical Disability"), 'Adults_with_a_Physical_Condition'),
        (("Chronic Health Conditions (Adults)", "Developmental Condition"), 'Adults_with_a_Developmental_Condition'),
        (("Chronic Health Conditions (Adults)", "Mental Health"), 'Adults_with_a_Serious_Mental_Illness'),
        (("Chronic Health Conditions (Adults)", "Chronic Substance Abuse"), 'Adults_with_a_Substance_Use_Disorder'),
        (("Chronic Health Conditions (Adults)", "HIV_AIDS"), 'Adults_with_a_HIV_AIDS'),
        (("Chronic Health Conditions (Adults)", "Other Chronic Health Conditions"), 'Adults_with_a_other_Condition'),
        (("Chronic Health Conditions (Children)", "Physical Disability"), 'childs_with_a_Physical_Condition'),
        (("Chronic Health Conditions (Children)", "Developmental Condition"), 'childs_with_a_Developmental_Condition'),
        (("Chronic Health Conditions (Children)", "Mental Health"), 'childs_with_a_Serious_Mental_Illness'),
        (("Chronic Health Conditions (Children)", "Chronic Substance Abuse"), 'childs_with_a_Substance_Use_Disorder'),
        (("Chronic Health Conditions (Children)", "HIV_AIDS"), 'childs_with_a_HIV_AIDS'),
        (("Chronic Health Conditions (Children)", "Other Chronic Health Conditions"), 'childs_with_a_other_Condition'),
        (("History of Homelessness", "First Time Homeless"), 'History_First_Time_Homeless'),
        (("History of Homelessness", "Length of Time Homeless(Less than one month)"), 'History_Less_than_One_Month'),
        (("History of Homelessness", "Length of Time Homeless(One to three months)"), 'History_One_to_Three_Months'),
        (("History of Homelessness", "Length of Time Homeless(Three months to one year)"), 'History_Three_Months_to_One_Year'),
        (("History of Homelessness", "Length of Time Homeless(One year or more)"), 'History_One_Year_or_More'),
        (("History of Homelessness (HHs)", "First Time Homeless"), 'History_HHs_First_Time_Homeless'),
        (("History of Homelessness (HHs)", "Length of Time Homeless(Less than one month)"), 'History_HHs_Less_than_One_Month'),
        (("History of Homelessness (HHs)", "Length of Time Homeless(One to three months)"), 'History_HHs_One_to_Three_Months'),
        (("History of Homelessness (HHs)", "Length of Time Homeless(Three months to one year)"), 'History_HHs_Three_Months_to_One_Year'),
        (("History of Homelessness (HHs)", "Length of Time Homeless(One year or more)"), 'History_HHs_One_Year_or_More')
    ]
}

# Valid values for validation
VALID_AGE_RANGES = ['Under 18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']

VALID_SEX = ['Male', 'Female']

VALID_GENDERS = [
    'Woman (Girl if child)',
    'Man (Boy if child)',
    'Culturally Specific Identity',
    'Non-Binary',
    'Transgender',
    'Questioning',
    'Different Identity'
]

VALID_RACES = [
    'White',
    'Black/African American/African',
    'Asian/Asian American',
    'Indigenous (American Indian/Alaska Native/Indigenous)',
    'Native Hawaiian/Pacific Islander',
    'Middle Eastern/North African',
    'Hispanic/Latina/e/o'
]

