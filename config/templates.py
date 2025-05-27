"""
Report templates and structures for PIT Count outputs.
Updated to match exact original template_mapping.py structures
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class ReportType(Enum):
    HDX_TOTALS = "HDX_Totals"
    HDX_VETERANS = "HDX_Veterans" 
    HDX_YOUTH = "HDX_Youth"
    HDX_SUBPOPULATIONS = "HDX_Subpopulations"
    PIT_SUMMARY = "PIT Summary"

# Exact column structure from original
COLUMN = [
    "Sheltered_ES",
    "Sheltered_TH", 
    "Unsheltered",
    "Total"
]

# Exact templates from original template_mapping.py
TOTAL_with = [
    ("Total number of households", ""),
    ("Total number of persons (adults & children)", ""),
    ("      Number of children (under age 18)", ""),
    ("      Number of young (age 18 to 24)", ""),
    ("      Number of adults (age 25 to 34)", ""),
    ("      Number of adults (age 35 to 44)", ""),
    ("      Number of adults (age 45 to 54)", ""),
    ("      Number of adults (age 55 to 64)", ""),
    ("      Number of adults (age 65 or older)", ""),
    # Gender Categories
    ("Gender (adults and children)", "Woman (Girl if child)"),
    ("Gender (adults and children)", "Man (Boy if child)"),
    ("Gender (adults and children)", "Culturally Specific Identity"),
    ("Gender (adults and children)", "Transgender"),
    ("Gender (adults and children)", "Non-Binary"),
    ("Gender (adults and children)", "Questioning"),
    ("Gender (adults and children)", "Different Identity"),
    ("Gender (adults and children)", "More Than One Gender"),
    ("Gender (adults and children)","      Includes Woman (Girl if child)"),
    ("Gender (adults and children)","      Includes Man (Boy if child)"),
    ("Gender (adults and children)","      Includes Culturally Specific Identity"),
    ("Gender (adults and children)","      Includes Transgender"),
    ("Gender (adults and children)","      Includes Non-Binary"),
    ("Gender (adults and children)","      Includes Questioning"),
    ("Gender (adults and children)","      Includes Different Identity"),
    # Race and Ethnicity Categories
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
    #CH
    ("Chronically Homeless", "Total number of households"),
    ("Chronically Homeless", "Total number of persons")
]

TOTAL_without = [
    ("Total number of households", ""),
    ("Total number of persons", ""),
    ("      Number of young (age 18 to 24)", ""),
    ("      Number of adults (age 25 to 34)", ""),
    ("      Number of adults (age 35 to 44)", ""),
    ("      Number of adults (age 45 to 54)", ""),
    ("      Number of adults (age 55 to 64)", ""),
    ("      Number of adults (age 65 or older)", ""),
    # Gender Categories
    ("Gender", "Woman (Girl if child)"),
    ("Gender", "Man (Boy if child)"),
    ("Gender", "Culturally Specific Identity"),
    ("Gender", "Transgender"),
    ("Gender", "Non-Binary"),
    ("Gender", "Questioning"),
    ("Gender", "Different Identity"),
    ("Gender", "More Than One Gender"),
    ("Gender","      Includes Woman (Girl if child)"),
    ("Gender","      Includes Man (Boy if child)"),
    ("Gender","      Includes Culturally Specific Identity"),
    ("Gender","      Includes Transgender"),
    ("Gender","      Includes Non-Binary"),
    ("Gender","      Includes Questioning"),
    ("Gender","      Includes Different Identity"),
    # Race and Ethnicity Categories
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
    #CH
    ("Chronically Homeless", "Total number of persons")
]

TOTAL_withonly = [
    ("Total number of households", ""),
    ("Number of children (persons under age 18)", ""),
    # Gender Categories
    ("Gender", "Woman (Girl if child)"),
    ("Gender", "Man (Boy if child)"),
    ("Gender", "Culturally Specific Identity"),
    ("Gender", "Transgender"),
    ("Gender", "Non-Binary"),
    ("Gender", "Questioning"),
    ("Gender", "Different Identity"),
    ("Gender", "More Than One Gender"),
    ("Gender","      Includes Woman (Girl if child)"),
    ("Gender","      Includes Man (Boy if child)"),
    ("Gender","      Includes Culturally Specific Identity"),
    ("Gender","      Includes Transgender"),
    ("Gender","      Includes Non-Binary"),
    ("Gender","      Includes Questioning"),
    ("Gender","      Includes Different Identity"),
    # Race and Ethnicity Categories
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
    #CH
    ("Chronically Homeless", "Total number of persons")
]

VET_with = [
    ("Total number of households", ""),
    ("Total number of persons", ""),
    ("Total number of veterans", ""),
    # Gender Categories
    ("Gender (veterans only)", "Woman (Girl if child)"),
    ("Gender (veterans only)", "Man (Boy if child)"),
    ("Gender (veterans only)", "Culturally Specific Identity"),
    ("Gender (veterans only)", "Transgender"),
    ("Gender (veterans only)", "Non-Binary"),
    ("Gender (veterans only)", "Questioning"),
    ("Gender (veterans only)", "Different Identity"),
    ("Gender (veterans only)", "More Than One Gender"),
    ("Gender (veterans only)","      Includes Woman (Girl if child)"),
    ("Gender (veterans only)","      Includes Man (Boy if child)"),
    ("Gender (veterans only)","      Includes Culturally Specific Identity"),
    ("Gender (veterans only)","      Includes Transgender"),
    ("Gender (veterans only)","      Includes Non-Binary"),
    ("Gender (veterans only)","      Includes Questioning"),
    ("Gender (veterans only)","      Includes Different Identity"),
    # Race and Ethnicity Categories
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
    #CH
    ("Chronically Homeless", "Total number of households"),
    ("Chronically Homeless", "Total number of persons")
]

VET_without = [
    ("Total number of households", ""),
    ("Total number of persons", ""),
    ("Total number of veterans", ""),
    # Gender Categories
    ("Gender (veterans only)", "Woman (Girl if child)"),
    ("Gender (veterans only)", "Man (Boy if child)"),
    ("Gender (veterans only)", "Culturally Specific Identity"),
    ("Gender (veterans only)", "Transgender"),
    ("Gender (veterans only)", "Non-Binary"),
    ("Gender (veterans only)", "Questioning"),
    ("Gender (veterans only)", "Different Identity"),
    ("Gender (veterans only)", "More Than One Gender"),
    ("Gender (veterans only)","      Includes Woman (Girl if child)"),
    ("Gender (veterans only)","      Includes Man (Boy if child)"),
    ("Gender (veterans only)","      Includes Culturally Specific Identity"),
    ("Gender (veterans only)","      Includes Transgender"),
    ("Gender (veterans only)","      Includes Non-Binary"),
    ("Gender (veterans only)","      Includes Questioning"),
    ("Gender (veterans only)","      Includes Different Identity"),
    # Race and Ethnicity Categories
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
    #CH
    ("Chronically Homeless", "Total number of persons")
]

YOUTH_without = [
    ("Total number of unaccompanied youth households", ""),
    ("Total number of unaccompanied youth", ""),
    ("      Number of unaccompanied youth (under age 18)", ""),
    ("      Number of unaccompanied youth (age 18 to 24)", ""),
    # Gender Categories
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
    # Race and Ethnicity Categories
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
    #CH
    ("Chronically Homeless", "Total number of persons")
]

YOUTH_with = [
    ("Total number of parenting youth household", ""),
    ("Total number of persons in parenting youth households", ""),
    ("Total Parenting Youth (youth parents only)", ""),
    ("Total Children in Parenting Youth Households", ""),
    ("   Number of parenting youth under age 18", ""),
    ("      Children in households with parenting youth under age 18", ""),
    ("   Number of parenting youth age 18 to 24", ""),
    ("      Children in households with parenting youth age 18 to 24", ""),
    # Gender Categories
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
    # Race and Ethnicity Categories
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
    #CH
    ("Chronically Homeless", "Total number of households"),
    ("Chronically Homeless", "Total number of persons")
]

INDEX_SUB = [
    ("Adults with a Serious Mental Illness", ""),
    ("Adults with a Substance Use Disorder", ""),
    ("Adults with HIV/AIDS", ""),
    ("Victims of Domestic Violence (fleeing)", "")
]

TOTAL_Summary = [
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

    # Gender Categories
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

    # Race and Ethnicity Categories
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

    # CH
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

def get_report_template(report_type: ReportType, report_name: str) -> List[Tuple[str, str]]:
    """Get the appropriate template for a given report type and name."""
    
    if report_type == ReportType.HDX_TOTALS:
        if "with at Least One Adult and One Child" in report_name:
            return TOTAL_with
        elif "without Children" in report_name:
            return TOTAL_without
        elif "with Only Children" in report_name:
            return TOTAL_withonly
        else:  # Total households
            return TOTAL_with
    
    elif report_type == ReportType.HDX_VETERANS:
        if "with at Least One Adult and One Child" in report_name:
            return VET_with
        else:
            return VET_without
    
    elif report_type == ReportType.HDX_YOUTH:
        if "Unaccompanied" in report_name:
            return YOUTH_without
        else:
            return YOUTH_with
    
    elif report_type == ReportType.HDX_SUBPOPULATIONS:
        return INDEX_SUB
    
    elif report_type == ReportType.PIT_SUMMARY:
        return TOTAL_Summary
    
    return []