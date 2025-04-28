import pandas as pd
import matplotlib.pyplot as plt

def generate_graphs(df: pd.DataFrame) -> dict:
    """
    Generate important graphs from the dataset.
    Returns a dictionary where keys are graph titles and values are matplotlib figure objects.
    """

    graphs = {}

    # Plan Distribution:
    if 'Plan' in df.columns:
        fig1, ax1 = plt.subplots()
        df['Plan'].value_counts().plot(kind='bar', ax=ax1)
        ax1.set_title('Plan Distribution')
        ax1.set_xlabel('Subscription Plan')
        ax1.set_ylabel('Number of Customers')
        graphs['Plan Distribution'] = fig1

    # Churn Rate:
    if 'Churn' in df.columns:
        fig2, ax2 = plt.subplots()
        df['Churn'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax2)
        ax2.set_ylabel('')  # Hide y-label
        ax2.set_title('Churn Rate')
        graphs['Churn Rate'] = fig2

    # Spend vs Tenure:
    if 'MonthlySpend' in df.columns and 'Tenure' in df.columns:
        fig3, ax3 = plt.subplots()
        ax3.scatter(df['MonthlySpend'], df['Tenure'], alpha=0.7)
        ax3.set_title('Spend vs Tenure')
        ax3.set_xlabel('Monthly Spend ($)')
        ax3.set_ylabel('Tenure (Months)')
        graphs['Spend vs Tenure'] = fig3

    # Industry Distribution:
    if 'Industry' in df.columns:
        fig4, ax4 = plt.subplots()
        df['Industry'].value_counts().head(10).plot(kind='bar', ax=ax4)
        ax4.set_title('Top 10 Industries')
        ax4.set_xlabel('Industry')
        ax4.set_ylabel('Number of Customers')
        graphs['Top 10 Industries'] = fig4

    return graphs
