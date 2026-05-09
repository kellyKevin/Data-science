import pandas as pd
import sys

# Broken analysis script
def load_data(filepath):
    """Load CSV file"""
    df = pd.read_csv(filepath)
    return df

def clean_data(df):
    """Clean missing values"""
    # BUG 1: Dropping rows with any NaN instead of filling
    df = df.dropna()
    return df

def calculate_stats(df):
    """Calculate summary statistics"""
    # BUG 2: Trying to get mean of non-numeric columns
    summary = {}
    summary['assessment_mean'] = df['assessment_score'].mean()
    summary['project_mean'] = df['project_score'].mean()
    
    # BUG 3: Logic error - days_since_application should be ascending (lower is better), but this treats it as descending
    summary['avg_days'] = df['days_since_application'].mean()
    
    return summary

def get_top_departments(df, n=3):
    """Get top performing departments"""
    # BUG 4: Column name inconsistency - 'track' vs 'department'
    top_depts = df.groupby('department')['assessment_score'].mean().head(n)
    return top_depts

def main():
    try:
        df = load_data('intern_applications.csv')
        print(f"Loaded {len(df)} records")
        
        df_clean = clean_data(df)
        print(f"After cleaning: {len(df_clean)} records")
        
        stats = calculate_stats(df_clean)
        print("Summary Statistics:")
        for key, val in stats.items():
            print(f"  {key}: {val}")
        
        top = get_top_departments(df_clean)
        print("\nTop performing tracks:")
        print(top)
        
        # BUG 5: No validation that output makes sense
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
