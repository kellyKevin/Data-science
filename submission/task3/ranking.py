import json
import pandas as pd
import numpy as np
from pathlib import Path

def load_candidates(json_file):
    """Load candidates from JSON file"""
    with open(json_file, 'r') as f:
        candidates = json.load(f)
    return candidates

def clean_candidates_data(candidates):
    """Clean and normalize candidate data"""
    
    # Convert to DataFrame for easier handling
    df = pd.DataFrame(candidates)
    
    print(f"Loaded {len(df)} candidate records")
    
    # Remove duplicates (keep first)
    df_orig_len = len(df)
    df = df.drop_duplicates(subset=['candidate_id'], keep='first')
    if len(df) < df_orig_len:
        print(f"  Removed {df_orig_len - len(df)} duplicate records")
    
    # Standardize track names (case-insensitive)
    track_mapping = {
        'Data Science': 'Data Science',
        'Data science': 'Data Science',
        'Software Engineering': 'Software Engineering',
        'Software Eng': 'Software Engineering',
        'software engineering': 'Software Engineering',
    }
    df['track'] = df['track'].map(track_mapping)
    
    return df

def normalize_score(value, min_val=0, max_val=100):
    """Normalize a score to 0-1 range"""
    if pd.isna(value) or value is None:
        return 0.0
    
    # Handle outliers (scores > 100 or negative)
    if value > max_val:
        value = max_val
    if value < min_val:
        value = min_val
    
    return (value - min_val) / (max_val - min_val)

def calculate_ranking_score(candidate, weights=None):
    """
    Calculate composite ranking score for a candidate.
    
    Scoring Logic:
    - 40% weight: test_score (primary technical assessment)
    - 35% weight: project_score (practical implementation skills)
    - 20% weight: portfolio_score (demonstrated quality of work)
    - -5 points per missing document (completeness penalty)
    - +2 points if recently applied (< 3 days)
    - +1 point if very recently applied (< 7 days)
    
    All component scores normalized to 0-100 range.
    """
    
    if weights is None:
        weights = {
            'test_score': 0.40,
            'project_score': 0.35,
            'portfolio_score': 0.20
        }
    
    score = 0.0
    
    # Primary assessment (test score)
    test_norm = normalize_score(candidate.get('test_score'), 0, 100)
    score += test_norm * weights['test_score'] * 100
    
    # Project score (practical skills)
    project_norm = normalize_score(candidate.get('project_score'), 0, 100)
    score += project_norm * weights['project_score'] * 100
    
    # Portfolio score (work quality)
    portfolio_norm = normalize_score(candidate.get('portfolio_score'), 0, 100)
    score += portfolio_norm * weights['portfolio_score'] * 100
    
    # Penalty for missing documents (-5 points per missing doc)
    missing_docs = candidate.get('missing_documents', 0)
    if missing_docs:
        score -= missing_docs * 5
    
    # Bonus for recent applications (shows engagement/urgency)
    days = candidate.get('days_since_application', 30)
    if days is not None and days >= 0:
        if days < 3:
            score += 2
        elif days < 7:
            score += 1
    
    # Ensure score stays in reasonable range (0-100 with some allowance for bonuses)
    score = max(0, min(score, 105))
    
    return score

def rank_candidates(df):
    """Rank candidates based on composite score"""
    
    # Calculate ranking score for each candidate
    df['ranking_score'] = df.apply(calculate_ranking_score, axis=1)
    
    # Handle data quality issues in scoring
    # Candidates with invalid data (test_score > 100) get flagged
    invalid_data = df[
        (df['test_score'] > 100) | 
        (df['test_score'].isna()) | 
        (df['project_score'].isna()) |
        (df['days_since_application'] < 0)
    ]
    
    if len(invalid_data) > 0:
        print(f"\n⚠️  WARNING: {len(invalid_data)} candidates have data quality issues:")
        for idx, row in invalid_data.iterrows():
            issues = []
            if row['test_score'] is None or (isinstance(row['test_score'], float) and row['test_score'] > 100):
                issues.append("invalid test score")
            if pd.isna(row['project_score']):
                issues.append("missing project score")
            if row['days_since_application'] < 0:
                issues.append("negative days_since_application")
            print(f"   - {row['name']} ({row['candidate_id']}): {', '.join(issues)}")
    
    # Sort by ranking score descending
    df_ranked = df.sort_values('ranking_score', ascending=False).reset_index(drop=True)
    df_ranked['rank'] = range(1, len(df_ranked) + 1)
    
    return df_ranked

def main():
    # Get path to candidates.json
    current_dir = Path(__file__).parent
    candidates_file = current_dir.parent.parent / 'candidates.json'
    
    print("=" * 80)
    print("CANDIDATE RANKING SYSTEM")
    print("=" * 80)
    
    # Load and clean data
    print("\n[1] Loading candidate data...")
    candidates = load_candidates(candidates_file)
    df = clean_candidates_data(candidates)
    
    # Rank candidates
    print("\n[2] Computing ranking scores...")
    df_ranked = rank_candidates(df)
    
    # Display results
    print("\n" + "=" * 80)
    print("RANKING RESULTS")
    print("=" * 80)
    print(f"\nTotal candidates ranked: {len(df_ranked)}\n")
    
    # Display top 10
    print("TOP 10 CANDIDATES:")
    print("-" * 80)
    
    output_cols = ['rank', 'name', 'track', 'test_score', 'project_score', 
                   'portfolio_score', 'missing_documents', 'ranking_score']
    
    top_10 = df_ranked.head(10)[output_cols].copy()
    
    for idx, row in top_10.iterrows():
        print(f"\n{int(row['rank']):2d}. {row['name']:<20} | {row['track']}")
        print(f"    Track: {row['track']}")
        print(f"    Scores: Test={row['test_score']:.0f}, Project={row['project_score']:.0f}, Portfolio={row['portfolio_score']:.0f}")
        print(f"    Missing Docs: {row['missing_documents']} | Ranking Score: {row['ranking_score']:.2f}")
    
    # Display full ranking
    print("\n" + "=" * 80)
    print("FULL RANKING:")
    print("=" * 80 + "\n")
    
    for idx, row in df_ranked.iterrows():
        status = "✓" if row['missing_documents'] == 0 else "!"
        print(f"{int(row['rank']):2d}. {status} {row['name']:<18} | {row['track']:<20} | Score: {row['ranking_score']:6.2f}")
    
    # Save ranking to CSV
    output_file = current_dir / 'ranking_results.csv'
    df_ranked.to_csv(output_file, index=False)
    print(f"\n✓ Full ranking saved to: {output_file}")
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print(f"\nScoring by Track:")
    track_stats = df_ranked.groupby('track')['ranking_score'].agg(['mean', 'min', 'max', 'count'])
    print(track_stats.round(2))
    
    print(f"\nAverage ranking score: {df_ranked['ranking_score'].mean():.2f}")
    print(f"Standard deviation: {df_ranked['ranking_score'].std():.2f}")
    
    return df_ranked

if __name__ == '__main__':
    ranking = main()
