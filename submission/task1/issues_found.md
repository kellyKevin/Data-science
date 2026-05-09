# Issues Found in broken_analysis.py

## Issue 1: Data Loss from Aggressive Cleaning

**The Issue:**
```python
df = df.dropna()
```
The script uses `dropna()` without parameters, which removes ANY row with ANY missing value. This is overly aggressive and results in excessive data loss.

**Why It Matters:**
- In the provided dataset, legitimate records have missing assessment or project scores
- Dropping entire rows wastes usable data
- With only ~15 records, losing rows significantly impacts analysis
- Missing values can be handled intelligently (filled, imputed, or handled selectively)

**How I Fixed It:**
- Changed to selective imputation: fill numeric columns with their median value
- Only drop rows where critical identifier columns (candidate_id, name, track) are missing
- Added data preservation while maintaining data integrity

---

## Issue 2: Column Name Mismatch

**The Issue:**
```python
def get_top_departments(df, n=3):
    top_depts = df.groupby('department')['assessment_score'].mean().head(n)
```
The column is actually named 'track' in the CSV, not 'department'. This causes a KeyError at runtime.

**Why It Matters:**
- Script will crash with "KeyError: 'department'"
- Code won't run successfully
- Indicates lack of data exploration before implementation

**How I Fixed It:**
- Changed to correct column name: `df.groupby('track')`
- Added validation to check if column exists before using it
- Renamed function to `get_top_tracks()` for clarity

---

## Issue 3: Missing Input Validation and Error Handling

**The Issue:**
- No checks for empty DataFrames before processing
- No validation that statistics make sense
- Minimal error handling beyond try/except wrapper
- No verification of data ranges

**Why It Matters:**
- If data is unexpectedly empty or corrupted, script produces meaningless output
- Assessment scores of 999 or negative days should be flagged as anomalies
- Users can't tell if results are reliable

**How I Fixed It:**
- Added explicit checks for empty DataFrames
- Added validation for reasonable data ranges (assessment scores 0-100)
- Added row count tracking to show what was cleaned
- Improved error messages with traceback for debugging

---

## Issue 4: No Counting of Records in Groupby Results

**The Issue:**
```python
top_depts = df.groupby('department')['assessment_score'].mean().head(n)
```
Returns only the mean, but doesn't show how many records are in each group.

**Why It Matters:**
- A track with mean=85 from 1 person is different from mean=85 from 10 people
- Makes it hard to assess reliability of aggregates
- Could mislead decision-making

**How I Fixed It:**
- Added `.agg(['mean', 'count'])` to show both metrics
- Results now display mean AND number of records per track

---

## Issue 5: Inadequate Error Handling for File I/O

**The Issue:**
```python
df = pd.read_csv(filepath)
```
No specific error handling for common file issues (missing file, permission denied, corrupted data).

**Why It Matters:**
- Generic exception in main() catches everything but doesn't distinguish issues
- Users don't know what went wrong
- Makes debugging harder

**How I Fixed It:**
- Separated file loading into dedicated function with specific error messages
- Checks for FileNotFoundError specifically
- Provides helpful message if file is missing

---

## Additional Improvements Made

1. **Added docstrings** to all functions explaining what they do and what was fixed
2. **Consistent formatting** of numeric output (2 decimal places)
3. **Better variable names** (e.g., `median_days_pending` instead of `avg_days`)
4. **Expanded output** to show records removed during cleaning
5. **Explicit data type checks** before computing statistics
