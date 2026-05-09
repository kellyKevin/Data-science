# Candidate Ranking Logic Explanation

## 1. Ranking Formula

### Scoring Components
The ranking system uses a **weighted composite score** that combines four key factors:

| Component | Weight | Scale | Purpose |
|-----------|--------|-------|---------|
| Test Score | 40% | 0-100 | Primary technical assessment |
| Project Score | 35% | 0-100 | Practical implementation skills |
| Portfolio Score | 20% | 0-100 | Demonstrated work quality |
| Adjustments | ±5% | Variable | Penalties and bonuses |

### Formula
```
Ranking Score = (0.40 × Test) + (0.35 × Project) + (0.20 × Portfolio) 
                - (5 × Missing Documents)
                + Recency Bonus
```

Where:
- All scores normalized to 0-100 range
- **Recency Bonus**: 
  - +2 points if application submitted < 3 days ago
  - +1 point if application submitted < 7 days ago
- **Missing Documents Penalty**: -5 points per missing document

### Rationale for Weights
1. **Test Score (40%)**: Represents structured technical assessment; most comparable across candidates
2. **Project Score (35%)**: Demonstrates ability to execute; nearly as important as test
3. **Portfolio Score (20%)**: Shows real-world quality; weighted lower due to potential variability in assessment criteria
4. **Documents (−5 each)**: Completeness is important for hiring workflow; 3 missing docs severely impacts score
5. **Recency (+1-2)**: Recent applicants may be more motivated or engaged

### Top Ranking Results
1. **Grace Wambui** (91.25) - Data Science
   - Exceptional across all metrics: Test=92, Project=95, Portfolio=96
   
2. **Noah Korir** (87.45) - Software Engineering
   - Consistent high performer: Test=89, Project=91, Portfolio=90
   
3. **Raj Singh** (87.00) - Software Engineering
   - Strong all-around: Test=90, Project=92, Portfolio=89

## 2. Benefit of This Approach

### **Transparency and Auditability**
This approach provides clear, explainable rankings that hiring teams can understand and defend:

- **Understandable Logic**: Each recruiter can see exactly why a candidate ranks where they do
- **No Black Box**: Unlike machine learning models, there's no mysterious "AI decision"
- **Defensible in Review**: If a candidate questions their ranking, the formula can be explained clearly
- **Easy to Adjust**: If leadership decides portfolio should be weighted differently, the formula can be updated and all rankings recalculated instantly
- **Reduced Bias Risk**: Documented weighting is easier to review for fairness compared to unstated human judgment

**Practical Example**: If questioned, you can say: "Grace scored 91.25 because she scored 92 on tests (40% weight), 95 on projects (35%), and 96 on portfolio (20%). This combination places her at the top."

---

## 3. Limitation/Risk of This Approach

### **Vulnerability to Data Quality Issues**
This ranking system is vulnerable to corruption from poor or missing input data:

**Current Issues Observed:**
- John Doe has test_score of 999 (clearly invalid data entry)
- Ethan Mwangi missing test_score entirely
- Faiza Noor missing project_score
- Peter Ndegwa has negative days_since_application (-1)

**Why This Is a Problem:**
- The formula treats missing values as 0, which may not be fair
- An invalid score of 999 gets capped at 100, but doesn't penalize John Doe for providing bad data
- Can't distinguish between "candidate didn't take test" vs. "data wasn't recorded"

**Impact on Rankings:**
- Ethan Mwangi placed #20 (lowest) partly due to missing test score being treated as 0
- However, Ethan's project_score (79) is decent - he might deserve higher ranking if test score were available
- This shows the system can unfairly penalize candidates with incomplete data

**Mitigation**: Before using this ranking in production, require data validation:
- All candidates must have complete test, project, and portfolio scores
- Use imputation or require test retakes for missing values
- Flag candidates with data anomalies for manual review

---

## 4. Fairness and Practical Concern

### **Track-Specific Performance Standards**

**The Concern:**
The current formula applies identical weight and scale to all tracks (Data Science and Software Engineering), but these roles may have fundamentally different skill profiles.

**Current Observation:**
- Data Science avg score: 70.38 (range: 43.45 - 91.25)
- Software Engineering avg score: 71.64 (range: 44.60 - 87.45)
- Very similar distributions, but with different underlying skills

**Why This Matters:**
- A Data Science candidate's "portfolio score" might represent different work (models, analysis) vs. a Software Engineer's portfolio (code projects, system design)
- Test_score might measure different competencies across tracks
- By using identical weights, we might inadvertently penalize one track over the other

**Potential Unfairness:**
- If one track historically has higher test scores due to test difficulty, that track gets systematically ranked higher
- If project scores are easier to achieve in one track, candidates from that track get boosted
- This could create path dependencies where one track dominates hiring

**Practical Concern:**
- After hiring using this formula, you might notice one track is overrepresented compared to business needs
- Retrospectively discovering bias after making offers is expensive and damaging to employer brand

### **Recommendation Before Using**
1. **Stratify analysis by track** - Verify score distributions are comparable
2. **Conduct hiring retrospective** - If you've used past ranking data, see if one track was systematically favored
3. **Consider track-specific thresholds** - Might need different minimum scores for each track
4. **Include domain experts in review** - Have track-specific hiring managers review top candidates before offers

---

## 5. Ranking Interpretation Guide

### What the Score Means
- **85+**: Exceptional candidates, interview immediately
- **75-84**: Strong candidates, likely good hires with proper vetting
- **65-74**: Competitive candidates, interview with alternatives
- **55-64**: Below average, only consider if short on candidates
- **<55**: Likely not competitive without significant development

### How to Use Results
1. **First Pass**: Review top 15-20 candidates for interviews
2. **Track Balance**: Ensure both tracks are represented in interview pool
3. **Manual Review**: Candidates with data quality issues (marked with "!") need manual assessment
4. **Offer Stage**: Don't rank candidates who haven't completed onboarding (background check, reference validation, etc.)

### Candidates with Data Issues (Flagged with "!")
These candidates need special attention:
- **Chao Li** (#8): Missing 1 document - otherwise strong profile (score 78.90)
- **Lila Patel** (#12): Missing 1 document - borderline competency
- **Sarah Chebet** (#15): Missing 3 documents - indicates organizational issues
- **Olivia Tan** (#17): Missing 1 document - low scores and incomplete application
- **Henry Kimani** (#19): Missing 2 documents - lowest tier overall

---

## 6. System Parameters and Adjustments

If different business priorities emerge, these parameters can be adjusted:

```
# Adjust these weights based on hiring needs:
weights = {
    'test_score': 0.40,      # Change to 0.30 if project experience more important
    'project_score': 0.35,   # Change to 0.45 if execution history matters more
    'portfolio_score': 0.20  # Change to 0.25 if quality samples crucial
}

# Adjust penalties/bonuses:
missing_doc_penalty = -5     # -3 if you tolerate incomplete applications
recent_app_bonus_3d = +2    # +1 if urgency doesn't matter
recent_app_bonus_7d = +1    # +0 if speed is irrelevant
```

---

## Summary

| Aspect | Value |
|--------|-------|
| **Total Candidates Ranked** | 20 |
| **Data Quality Issues** | 4 candidates flagged |
| **Top Candidate** | Grace Wambui (91.25) |
| **Average Rank Score** | 70.95 |
| **Standard Deviation** | 14.16 |
| **Track with Highest Avg** | Software Engineering (71.64) |

This ranking provides a good starting point for manual review but should not be used as the sole hiring criterion without addressing data quality and fairness concerns outlined above.
