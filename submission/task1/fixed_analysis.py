import pandas as pd
import sys

def load_data(filepath):
    """Load CSV file"""
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

def clean_data(df):
    """Clean missing values intelligently
    
    FIXED: Instead of dropping all rows with missing values,
    fill numeric columns with median (preserves more data)
    and drop rows where critical fields are missing.
    """
    df = df.copy()
    
    # Fill numeric columns with median to preserve data
    numeric_cols = ['assessment_score', 'project_score', 'days_since_application']
    for col in numeric_cols:
        if col in df.columns and df[col].dtype in ['float64', 'int64']:
            df[col].fillna(df[col].median(), inplace=True)
    
    # Drop rows where critical identifier columns are missing
    df = df.dropna(subset=['candidate_id', 'name', 'track'])
    
    return df

def calculate_stats(df):
    """Calculate summary statistics
    
    FIXED: Only calculate stats on numeric columns, 
    with explicit column references.
    """
    # Validate input
    if df.empty:
        print("Warning: No data available for statistics")
        return {}
    
    summary = {}
    
    # Only compute for columns that exist and are numeric
    if 'assessment_score' in df.columns:
        summary['assessment_mean'] = df['assessment_score'].mean()
        summary['assessment_count'] = df['assessment_score'].count()
    
    if 'project_score' in df.columns:
        summary['project_mean'] = df['project_score'].mean()
        summary['project_count'] = df['project_score'].count()
    
    if 'days_since_application' in df.columns:
        summary['median_days_pending'] = df['days_since_application'].median()
        summary['max_days_pending'] = df['days_since_application'].max()
    
    return summary

def get_top_tracks(df, n=3):
    """Get top performing tracks
    
    FIXED: Use correct column name 'track' (was 'department'),
    handle inconsistent track values, and validate results.
    """
    # Validate input
    if df.empty:
        print("Warning: No data available for ranking")
        return pd.Series(dtype='float64')
    
    if 'track' not in df.columns:
        print("Error: 'track' column not found")
        return pd.Series(dtype='float64')
    
    if 'assessment_score' not in df.columns:
        print("Error: 'assessment_score' column not found")
        return pd.Series(dtype='float64')
    
    # Group by track and calculate mean assessment score
    track_performance = df.groupby('track')['assessment_score'].agg(['mean', 'count'])
    track_performance = track_performance.sort_values('mean', ascending=False)
    
    return track_performance.head(n)

def main():
    """Main entry point for analysis"""
    try:
        # Load data
        df = load_data('intern_applications.csv')
        print(f"Loaded {len(df)} records")
        
        # Clean data
        df_clean = clean_data(df)
        print(f"After cleaning: {len(df_clean)} records")
        print(f"Rows removed: {len(df) - len(df_clean)}")
        
        # VALIDATION CHECK: Ensure reasonable data ranges
        if df_clean['assessment_score'].max() > 100:
            print("WARNING: Found assessment scores > 100. Check data quality.")
        if (df_clean['assessment_score'] < 0).any():
            print("WARNING: Found negative assessment scores. Check data quality.")
        
        # Calculate statistics
        stats = calculate_stats(df_clean)
        print("\n=== Summary Statistics ===")
        for key, val in stats.items():
            if isinstance(val, float):
                print(f"  {key}: {val:.2f}")
            else:
                print(f"  {key}: {val}")
        
        # Get top performing tracks
        top_tracks = get_top_tracks(df_clean, n=5)
        print("\n=== Top Performing Tracks ===")
        print(top_tracks)
        
        print("\nAnalysis completed successfully!")
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
