import pandas as pd

def extract_findings(df: pd.DataFrame) -> dict:
    """
    Extract key metrics from the DataFrame for analysis.
    """
    findings = {}

    # Plan Distribution
    plan_counts = df['Plan'].value_counts(normalize=True) * 100
    findings['plan_distribution'] = {plan: f"{perc:.1f}%" for plan, perc in plan_counts.items()}

    # Average Spend
    findings['average_spend'] = round(df['Monthly Spend ($)'].mean(), 2)

    # Churn Rate
    churn_rate = df['Churned'].value_counts(normalize=True).get(True, 0) * 100
    findings['churn_rate'] = f"{churn_rate:.1f}%"

    # Average Tenure
    findings['average_tenure'] = round(df['Tenure (Months)'].mean(), 1)

    # Top Countries
    findings['top_countries'] = df['Country'].value_counts().head(5).index.tolist()

    # Top Industries
    findings['top_industries'] = df['Industry'].value_counts().head(5).index.tolist()

    # Signup Sources
    findings['signup_sources'] = df['Signup Source'].value_counts().head(3).index.tolist()

    return findings
