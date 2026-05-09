# Data Cleaning and Analysis Summary

## 1. Data Quality Issues Found

### Initial Assessment
- **Total records loaded**: 21
- **Records after cleaning**: 20 (removed 1 duplicate)

### Quality Issues Identified

| Issue | Count | Severity | Example |
|-------|-------|----------|---------|
| **Duplicate records** | 1 | High | Noah Korir (candidate_id 1014) appears twice |
| **Missing assessment score** | 1 | Medium | Ethan Mwangi (id 1005) |
| **Missing project score** | 1 | Medium | Faiza Noor (id 1006) |
| **Invalid assessment score** | 1 | High | John Doe scored 999 (clearly erroneous) |
| **Negative days_since_application** | 1 | High | Peter Ndegwa has -1 days (impossible) |
| **Invalid university** | 1 | Low | "Unknown" university name |
| **Inconsistent track names** | 3 | Medium | Mix of "Data Science", "Data science", "Software Eng", "Software Engineering", "software engineering" |
| **Inconsistent gender format** | 1 | Low | One record has "Male" instead of "M" |
| **Email format issue** | 0 | N/A | John Doe's email was incomplete (fixed) |

## 2. Cleaning Steps Taken

### Step 1: Duplicate Removal
- Removed 1 exact duplicate row (Noah Korir, id 1014)
- Kept first occurrence, removed second

### Step 2: Standardize Track Names
- Standardized all variations to: "Data Science" or "Software Engineering"
- Mapping applied:
  - "Data science" → "Data Science"
  - "Software Eng" → "Software Engineering"
  - "software engineering" → "Software Engineering"

### Step 3: Standardize Gender Values
- Normalized all gender values to "M" or "F"
- Mapping applied:
  - "Male" → "M"

### Step 4: Fix Invalid University Names
- Replaced "Unknown" with missing value (marked for categorization)

### Step 5: Handle Invalid Email
- Fixed incomplete email addresses (added missing domain extension)

### Step 6: Identify and Flag Invalid Scores
- Assessment score of 999 (John Doe) → marked as missing
- All scores > 100 → marked as missing

### Step 7: Handle Invalid Time Values
- Negative days_since_application (-1 for Peter Ndegwa) → marked as missing

### Step 8: Fill Missing Numeric Values
- Used **median imputation** for assessment_score and project_score
  - Assessment score median: 81.5
  - Project score median: 81.0
- Median was chosen over mean to be robust to outliers

### Step 9: Fill Missing Categorical Values
- Filled missing university with "Other"
- Filled missing gender with "Unknown"

### Step 10: Validation Check
- Identified record with graduation year < 2025 (John Doe, 2024)
- Flagged as warning but retained (may represent edge case)

## 3. Key Insights from Cleaned Data

### Insight 1: Data Science and Software Engineering Track Performance
- **Data Science**: Average assessment score = 80.33 (11 candidates)
- **Software Engineering**: Average assessment score = 78.78 (9 candidates)
- **Finding**: Data Science track candidates score slightly higher on average, but the difference is modest (~1.5 points)
- **Implication**: Both tracks have comparable talent quality

### Insight 2: University Performance Rankings
1. **JKUAT**: 82.5 average (4 candidates)
2. **USIU**: 82.4 average (5 candidates)
3. **Strathmore**: 76.8 average (5 candidates)
4. **University of Nairobi**: 76.5 average (4 candidates)
- **Finding**: JKUAT and USIU consistently produce top performers
- **Note**: University performance could be biased by selection effects (different recruitment channels)

### Insight 3: Application Processing Efficiency
- **Average days pending**: 7.1 days
- **Median days pending**: 6.0 days
- **Range**: 1 to 17 days
- **Finding**: Most applications are reviewed within a week, but some are pending for extended periods
- **Observation**: 75% of applications completed within ~14 days

### Insight 4: Documentation Completeness
- **Complete applications** (0 missing docs): 15 candidates (75%)
- **Applications with missing docs**: 5 candidates (25%)
  - 3 candidates missing 1 document
  - 1 candidate missing 2 documents
  - 1 candidate missing 3 documents
- **Finding**: Most candidates are well-organized, but completion quality varies

### Insight 5: Top Performers
- **Grace Wambui** (Data Science): 92 assessment, 95 project score
- **Brian Otieno** (Software Engineering): 91 assessment, 88 project score
- **Raj Singh** (Software Engineering): 90 assessment, 92 project score
- **Finding**: Top tier shows exceptional consistency across both metrics

## 4. Analysis Limitations

### Data Limitations
1. **Small Sample Size**: Only 20 records is insufficient for robust statistical inference
   - Confidence intervals are wide
   - Cannot control for confounding variables effectively
   
2. **Selection Bias**: Dataset represents only applicants who reached evaluation stage
   - Excludes candidates filtered out earlier
   - University rankings may reflect recruitment patterns, not actual candidate quality
   
3. **Temporal Bias**: Data is static snapshot
   - Does not account for hiring success rate or candidate retention
   - Unknown how assessment scores correlate with job performance
   
4. **Missing Context**: No information on:
   - Whether candidates were hired
   - Why certain documents were missing
   - Interview outcomes or feedback
   - Candidate self-reported skills or experience

### Methodological Limitations
1. **Imputation Assumptions**: 
   - Used median to fill missing scores
   - Assumes data is missing at random (may not be true)
   - Artificial values don't reflect true candidate ability
   
2. **Duplicate Handling**: 
   - Removed duplicate without investigating cause
   - Could have been data entry error or intentional re-application
   
3. **Score Interpretation**:
   - Unknown how assessment_score and project_score are calculated
   - Unknown whether they are comparable across candidates
   - Unknown weighting in hiring decisions

### Validation Limitations
1. Cannot verify "correctness" of cleaned data without:
   - Source system checks
   - Manual review sample
   - Cross-reference with other records
   
2. Remaining data quality issues:
   - Some records still have missing values (1 university, 2 assessment scores, 1 project score, 1 days value)
   - These were filled with medians/placeholders, not verified as correct

## 5. Recommendations for Future Work
1. Collect additional context (hiring outcomes, start dates, retention)
2. Increase sample size for statistical validity
3. Implement real-time data quality checks at source
4. Create data dictionary documenting score calculations
5. Investigate causes of missing documents before application submission
