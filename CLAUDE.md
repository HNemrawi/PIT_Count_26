# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Point-in-Time (PIT) Count Application** built with Streamlit for processing and analyzing homeless count data. The application processes survey data from Emergency Shelter (ES), Transitional Housing (TH), and Unsheltered sources, generating standardized HUD (Housing and Urban Development) reports.

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

## Architecture

### Region Support

This is the **New England** implementation of the PIT Count Application. It uses a specific name format for duplication detection:
- **New England**: Uses 1st letter of first name + 1st & 3rd letters of last name

Region selection occurs after authentication (currently defaults to New England).

### Data Flow

1. **Upload** → Raw Excel/CSV files uploaded for ES, TH, and Unsheltered sources
2. **Processing** → Household-level data transformed to person-level records
3. **Validation** → Age, gender, and race/ethnicity values validated
4. **Duplication Detection** → Hierarchical matching identifies potential duplicates
5. **Report Generation** → Standardized HUD reports calculated from processed data
6. **Download** → Excel exports with formatting and color-coding

### Module Structure

The codebase is organized into consolidated modules (recently refactored from nested packages):

- **app.py**: Main entry point with Streamlit UI workflow (login → region selection → upload → validation → reports → download)
- **config.py**: All configuration including region mappings, report templates, and category definitions
- **processor.py**: Core data transformation logic (column mapping → age counting → household classification → flattening → chronic homelessness flagging)
- **reports.py**: Report generation using cached statistics calculation
- **components.py**: UI components for each workflow step
- **utils.py**: Session management, timezone handling, and formatting helpers

### Key Processing Steps

**1. Data Transformation Pipeline** (processor.py):
```
apply_column_mapping()
  → count_age_groups()
  → classify_household_type()
  → flatten_entire_dataset()
  → flag_chronically_homeless()
  → add_age_group_column()
  → process_race()
  → process_gender()
  → standardize_conditions()
```

**2. Household Classification**:
- Household with Children: Adults/youth + children
- Household without Children: Adults/youth only
- Household with Only Children: Children under 18 only (unaccompanied minors)

**3. Duplication Detection** (DuplicationDetector class):
Hierarchical matching with three confidence levels:
- **Likely (High)**: Full name + DOB, Initials + DOB, Full name + exact age
- **Somewhat Likely (Medium)**: Initials + exact age, Full name + age range
- **Possible (Low)**: Initials + age range

**4. Report Generation**:
Reports follow HUD HDX format with five categories:
- HDX_Totals (by household type)
- HDX_Veterans
- HDX_Youth (Unaccompanied and Parenting)
- HDX_Subpopulations
- PIT Summary

All statistics are calculated via `calculate_summary_stats()` which is cached with `@st.cache_data`.

### Session State Management

Critical session state keys:
- `logged_in`, `username`: Authentication state
- `region`: Selected implementation region
- `current_step`: Workflow step ('upload', 'validation', 'reports', 'download')
- `uploaded_data`: Dict of raw DataFrames by source name
- `processed_data`: Dict of processed data (persons_df, households_df, raw_df) by source
- `calculated_reports`: Dict of generated reports

### Authentication

User credentials are stored in Streamlit secrets with SHA-256 hashed passwords. The verification logic is in `verify_credentials()` in app.py.

## Important Implementation Details

### Chronic Homelessness Criteria

Chronic homelessness flagging (processor.py:222) requires disability AND one of:
1. Homeless ≥1 year + first time
2. Homeless this time ≥1 year + not first time
3. Not first time + <1 year this time + 4+ episodes + 12+ months total

**Special Rule**: Transitional Housing (TH) data is excluded from chronic homeless counts in reports (reports.py:296-300).

### Name Handling for New England

The `DuplicationDetector._prepare_name_fields()` method handles the New England name format:
- New England: Combines `first_initial`, `last_initial`, `last_third` (1st letter of first name + 1st & 3rd letters of last name)
- Other regions (fallback): Full first and last names

### Excel Export with Color Coding

Duplication exports use color-coded rows (processor.py:638):
- Red (FF9999): Likely Duplicate
- Orange (FFCC99): Somewhat Likely Duplicate
- Yellow (FFFF99): Possible Duplicate
- Purple (D8BFD8): No name information provided

The `Duplicates_With` column shows Excel row numbers (1-indexed, starting at row 2).

### Multi-Index DataFrames

All reports use pandas MultiIndex with (Category, Subcategory) tuples. The `REPORT_TEMPLATES` define the structure, and `TEMPLATE_MAPPINGS` map template positions to calculation keys.

### Data Validation

Validation (processor.py:709) checks:
- Age Range: Single-select against `VALID_AGE_RANGES`
- Gender: Multi-select against `VALID_GENDERS`
- Race/Ethnicity: Multi-select against `VALID_RACES`

Invalid entries are tracked with row numbers (Excel 1-indexed) and shown in the validation interface.

## Common Operations

### Modifying Report Templates

Report templates are defined in config.py:
- `REPORT_TEMPLATES`: Structure with (Category, Subcategory) tuples
- `TEMPLATE_MAPPINGS`: Maps template positions to calculation keys
- Both must be kept in sync for reports to populate correctly

### Adding New Statistics

1. Add calculation logic to appropriate function in reports.py (`calculate_basic_counts`, `calculate_demographic_info`, etc.)
2. Add key to `TEMPLATE_MAPPINGS` in config.py
3. Ensure template tuple exists in `REPORT_TEMPLATES`

## File Formats

### Input Files
- CSV or Excel (.xlsx) with New England-specific columns
- Excel files support sheet selection in UI
- Expected columns defined in `COLUMN_MAPPINGS['New England']`

### Output Files
- Excel workbooks with multiple sheets (one per report type)
- Color-coded duplication reports
- Formatted headers and auto-adjusted column widths
- Filenames include timestamp: `{ReportType}_{Region}_{Timestamp}.xlsx`

## Recent Changes

The codebase was recently refactored from a nested package structure (components/, config/, core/, utils/) to a flat module structure (components.py, config.py, processor.py, utils.py, reports.py). Git status shows the old structure marked for deletion.
