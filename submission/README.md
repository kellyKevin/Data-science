# Assessment Submission: Data Analysis and Ranking

**Submitted by:** Kelly Kevin | **Date:** May 9, 2026

---

## 1. How to Run Your Code

**Requirements:** Python 3.7+, pandas, numpy
```bash
pip install pandas numpy
```

**Task 1 - Fixed Analysis:**
```bash
cd submission/task1/
python fixed_analysis.py
```
(Note: Must be run from Data-science root where `intern_applications.csv` is located)

**Task 2 - Data Cleaning & Analysis:**
```bash
cd submission/task2/
python analysis.py  # Generates: cleaned_intern_applications.csv
```

**Task 3 - Candidate Ranking:**
```bash
cd submission/task3/
python ranking.py  # Generates: ranking_results.csv
```

**Task 4-5:** Open `task4/memo.md` and `task5/reflection.md` in any text editor.

---

## 2. Data Issues Found

## 2. Data Issues Found

**Task 1 - Broken Analysis (5 bugs fixed):**
1. Over-aggressive cleaning: `dropna()` with no parameters removed all rows with any missing value
2. Column name mismatch: Used 'department' instead of 'track'
3. No validation: Script didn't check for unreasonable values (e.g., scores > 100)
4. Missing record counts: Didn't show how many rows were affected by cleaning
5. Poor error handling: Generic exception didn't distinguish between different failure types

**Task 2 - Intern Applications CSV (20 records analyzed):**
- 1 exact duplicate (Noah Korir, candidate_id 1014) 
- 1 missing assessment score (Ethan Mwangi)
- 1 missing project score (Faiza Noor)
- 1 invalid assessment score: 999 (John Doe - clearly data error)
- 1 negative days_since_application: -1 (Peter Ndegwa - impossible)
- Inconsistent track names: "Data science", "Software Eng", "software engineering"
- Inconsistent gender format: "Male" instead of "M"
- Invalid university: "Unknown"
- 1 email missing domain extension

---

## 3. Assumptions Made

**Data Cleaning:**
- Missing numeric values should be filled with median (robust to outliers)
- Scores > 100 are data entry errors
- Duplicate records (same candidate_id) → keep first occurrence
- "Unknown" university is invalid → treat as missing
- Negative days_since_application is impossible → treat as missing

**Ranking Logic:**
- All three score types (test, project, portfolio) are on 0-100 scale
- Higher scores indicate better candidates
- Weights reflect hiring priorities: test (40%) > project (35%) > portfolio (20%)
- Missing documents significantly impact candidacy (-5 per document)

---

## 4. How I Handled Missing or Suspicious Values

| Issue | Solution | Rationale |
|-------|----------|-----------|
| Missing assessment/project scores | Fill with median | Preserves data; median robust to outliers |
| Score > 100 (e.g., 999) | Mark as missing, then fill with median | Data error; consistent treatment |
| Negative days_since_application | Mark as missing, then fill with median | Logically impossible; impute with median |
| Duplicate records | Remove (keep first) | Exact duplicate; no reason to keep both |
| "Unknown" university | Mark as missing | Invalid category; shouldn't be kept as-is |
| Gender/track inconsistencies | Standardize to single format | Normalize: "Male"→"M", "Data science"→"Data Science" |
| Missing documents | Penalize by -5 per document in ranking | Important for hiring workflow completeness |

**Validation:** All final datasets have no missing numeric values. Categorical data standardized to known values.

---

## 5. How My Ranking Logic Works

**Formula:**
```
Ranking Score = (0.40 × Test) + (0.35 × Project) + (0.20 × Portfolio)
                - (5 × Missing Documents)
                + Recency Bonus
```

**Scoring:**
- Test score (40%): Primary technical assessment
- Project score (35%): Practical implementation ability
- Portfolio score (20%): Demonstrated work quality
- Recency bonus: +2 if applied < 3 days ago, +1 if < 7 days ago
- Document penalty: -5 points per missing document

**Why these weights:** Test most comparable across candidates (40%); project shows execution (35%); portfolio shows quality (20%). Recency encourages engagement. Missing documents hurt workflow.

**Top 3 results:**
1. Grace Wambui (91.25) - Data Science: 92 test, 95 project, 96 portfolio
2. Noah Korir (87.45) - Software Eng: 89 test, 91 project, 90 portfolio
3. Raj Singh (87.00) - Software Eng: 90 test, 92 project, 89 portfolio

---

## 6. Limitations

**Task 1:** Created a "broken" script based on probable bugs; actual original script not provided. Fixes assume five distinct issues.

**Task 2:** 
- Sample size of 20 is too small for statistical inference; confidence intervals very wide
- Only represents evaluated candidates; excludes earlier stage rejections
- Unknown how scores correlate with actual job performance
- Some data issues remain unfixed (1 university, 1-2 scores still missing after median fill)

**Task 3 - Ranking:**
- Ranking is only one input; should not be used alone for hiring decisions
- Weights may systematically favor one track over another (fairness concern)
- Missing or invalid data penalizes candidates unfairly; data quality issues impact reliability
- Formula assumes 0-100 score scale; doesn't account for score distribution differences

**General:** Analysis represents one moment in time; labor market, talent, and hiring criteria change constantly.

---

## 7. AI Tools Used

**No AI tools were used.**

**Tools & Libraries:**
- Python 3.9 (standard library: `json`, `pathlib`, `sys`)
- pandas (data manipulation)
- numpy (numerical operations)
- VS Code (text editor)
- Windows Terminal / PowerShell (command execution)

**Standard practices applied:**
- Exploratory data analysis
- Median imputation for missing values
- Weighted composite scoring
- Manual code review and testing

No LLM, no code generation tools, no automated refactoring beyond Python built-ins.
