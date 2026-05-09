import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("INTERN APPLICATIONS DATA CLEANING AND ANALYSIS")
print("=" * 80)

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================
print("\n[1] Loading data...")
import os
# Get path to source data
data_file = os.path.join(os.path.dirname(__file__), '..', '..', 'intern_applications.csv')
df = pd.read_csv(data_file)
print(f"Loaded {len(df)} records with {len(df.columns)} columns")
print(f"Initial columns: {list(df.columns)}")

# ============================================================================
# STEP 2: INSPECT DATA QUALITY ISSUES
# ============================================================================
print("\n[2] INITIAL DATA QUALITY ASSESSMENT")
print("-" * 80)

# Missing values
print("\nMissing values:")
print(df.isnull().sum())

# Duplicates
print(f"\nDuplicate rows: {df.duplicated().sum()}")
print(f"Duplicate candidate_ids: {df['candidate_id'].duplicated().sum()}")
if df['candidate_id'].duplicated().any():
    print("Duplicated IDs:", df[df['candidate_id'].duplicated(keep=False)].to_string())

# Data type issues
print("\nData types:")
print(df.dtypes)

# Value range issues
print("\nAssessment score range:")
print(f"  Min: {df['assessment_score'].min()}, Max: {df['assessment_score'].max()}")
print(f"  Count > 100: {(df['assessment_score'] > 100).sum()}")

print("\nDays since application range:")
print(f"  Min: {df['days_since_application'].min()}, Max: {df['days_since_application'].max()}")
print(f"  Negative values: {(df['days_since_application'] < 0).sum()}")

print("\nTrack values (inconsistencies):")
print(df['track'].value_counts())

print("\nGender values (inconsistencies):")
print(df['gender'].value_counts(dropna=False))

print("\nUniversity values (outliers):")
print(df['university'].value_counts())

# Email format issues
print("\nEmail format issues:")
invalid_emails = df[~df['email'].str.contains('@', regex=False, na=False)]['email']
print(f"  Emails without @: {len(invalid_emails)}")
if len(invalid_emails) > 0:
    print(f"  Examples: {invalid_emails.values[:3]}")

# ============================================================================
# STEP 3: DATA CLEANING
# ============================================================================
print("\n[3] PERFORMING DATA CLEANING")
print("-" * 80)

df_clean = df.copy()

# 3.1: Remove duplicates (keep first occurrence)
print("\n3.1: Removing duplicates...")
before = len(df_clean)
df_clean = df_clean.drop_duplicates(subset=['candidate_id'], keep='first')
after = len(df_clean)
print(f"    Removed {before - after} duplicate records")

# 3.2: Standardize track names (case-insensitive, map variations)
print("\n3.2: Standardizing track names...")
track_mapping = {
    'Data Science': 'Data Science',
    'Data science': 'Data Science',
    'Software Engineering': 'Software Engineering',
    'Software Eng': 'Software Engineering',
    'software engineering': 'Software Engineering',
}
df_clean['track'] = df_clean['track'].map(track_mapping)
print(f"    Standardized tracks to: {df_clean['track'].unique()}")

# 3.3: Standardize gender values
print("\n3.3: Standardizing gender values...")
gender_mapping = {
    'M': 'M',
    'F': 'F',
    'Male': 'M',
    'Female': 'F',
}
df_clean['gender'] = df_clean['gender'].map(gender_mapping)
print(f"    Standardized to: {df_clean['gender'].unique()}")

# 3.4: Fix invalid university names
print("\n3.4: Fixing invalid university names...")
df_clean.loc[df_clean['university'] == 'Unknown', 'university'] = np.nan
print(f"    Marked 'Unknown' university as missing")

# 3.5: Fix email format issues
print("\n3.5: Fixing email format issues...")
def fix_email(email):
    if pd.isna(email):
        return email
    email = str(email).strip()
    if '@' in email and '.' not in email.split('@')[1]:
        # Missing domain extension
        if email.endswith('example'):
            return email + '.com'
    return email

df_clean['email'] = df_clean['email'].apply(fix_email)
print(f"    Fixed email format issues")

# 3.6: Handle invalid score values
print("\n3.6: Handling invalid assessment scores...")
# John Doe has score of 999 - likely data entry error
# Replace with NaN so it can be handled as missing
df_clean.loc[df_clean['assessment_score'] > 100, 'assessment_score'] = np.nan
print(f"    Replaced scores > 100 with NaN")

# 3.7: Handle negative days_since_application
print("\n3.7: Handling negative days_since_application...")
count_negative = (df_clean['days_since_application'] < 0).sum()
df_clean.loc[df_clean['days_since_application'] < 0, 'days_since_application'] = np.nan
print(f"    Replaced {count_negative} negative values with NaN")

# 3.8: Fill missing numeric values with appropriate statistics
print("\n3.8: Filling missing numeric values...")
# Fill with median (more robust than mean to outliers)
numeric_cols = ['assessment_score', 'project_score']
for col in numeric_cols:
    null_count = df_clean[col].isnull().sum()
    if null_count > 0:
        median_val = df_clean[col].median()
        df_clean[col].fillna(median_val, inplace=True)
        print(f"    {col}: filled {null_count} missing values with median ({median_val:.1f})")

# 3.9: Fill missing university with "Other"
print("\n3.9: Filling missing categorical values...")
df_clean['university'].fillna('Other', inplace=True)
df_clean['gender'].fillna('Unknown', inplace=True)
print(f"    Filled missing university and gender values")

# 3.10: Validate graduation year (should be future or current year)
print("\n3.10: Checking graduation year validity...")
current_year = 2025
future_years = df_clean[df_clean['graduation_year'] < current_year]
if len(future_years) > 0:
    print(f"    WARNING: {len(future_years)} records with graduation year < {current_year}")
    print(f"    Examples: {future_years[['name', 'graduation_year']].head()}")
else:
    print(f"    All graduation years are >= {current_year}")

# ============================================================================
# STEP 4: VALIDATION CHECKS
# ============================================================================
print("\n[4] VALIDATION CHECKS ON CLEANED DATA")
print("-" * 80)

# Check for remaining nulls
remaining_nulls = df_clean.isnull().sum()
if remaining_nulls.sum() == 0:
    print("✓ No remaining null values")
else:
    print("✗ Remaining null values:")
    print(remaining_nulls[remaining_nulls > 0])

# Check data types and ranges
print("\nScore ranges (should be 0-100):")
print(f"  Assessment: {df_clean['assessment_score'].min():.1f} - {df_clean['assessment_score'].max():.1f}")
print(f"  Project: {df_clean['project_score'].min():.1f} - {df_clean['project_score'].max():.1f}")

print("\nDays since application (should be >= 0):")
print(f"  Min: {df_clean['days_since_application'].min()}")
print(f"  Max: {df_clean['days_since_application'].max()}")

print(f"\nRecord count: {len(df_clean)} (removed {len(df) - len(df_clean)} rows)")

# ============================================================================
# STEP 5: SAVE CLEANED DATA
# ============================================================================
print("\n[5] Saving cleaned data...")
output_file = os.path.join(os.path.dirname(__file__), 'cleaned_intern_applications.csv')
df_clean.to_csv(output_file, index=False)
print(f"✓ Saved to: {output_file}")

# ============================================================================
# STEP 6: ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS OF CLEANED DATA")
print("=" * 80)

print(f"\nTotal candidates: {len(df_clean)}")
print(f"Males: {(df_clean['gender'] == 'M').sum()}")
print(f"Females: {(df_clean['gender'] == 'F').sum()}")

print("\n--- Performance by Track ---")
track_stats = df_clean.groupby('track').agg({
    'assessment_score': ['mean', 'std', 'min', 'max', 'count'],
    'project_score': ['mean', 'count']
}).round(2)
print(track_stats)

print("\n--- Performance by University ---")
univ_stats = df_clean.groupby('university').agg({
    'assessment_score': ['mean', 'count']
}).round(2)
univ_stats.columns = ['_'.join(col).strip() for col in univ_stats.columns.values]
univ_stats = univ_stats.sort_values('assessment_score_mean', ascending=False)
print(univ_stats)

print("\n--- Time to Application Completion ---")
print(f"Average days since application: {df_clean['days_since_application'].mean():.1f}")
print(f"Median days since application: {df_clean['days_since_application'].median():.1f}")
print(f"Longest pending: {df_clean['days_since_application'].max():.0f} days")

print("\n--- Missing Documents ---")
missing_docs_dist = df_clean['missing_documents'].value_counts().sort_index()
print(missing_docs_dist)
print(f"Candidates with missing docs: {(df_clean['missing_documents'] > 0).sum()}")

print("\n--- Top 10 Candidates by Assessment Score ---")
top_10 = df_clean.nlargest(10, 'assessment_score')[['name', 'track', 'assessment_score', 'project_score', 'university']]
print(top_10.to_string(index=False))

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
