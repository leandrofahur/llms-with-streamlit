import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io
import base64
from matplotlib.figure import Figure
import numpy as np
from typing import Dict, Tuple, List, Any

def generate_graphs(df: pd.DataFrame) -> dict:
    """
    Generate important graphs from the dataset.
    Returns a dictionary where keys are graph titles and values are matplotlib figure objects.
    """
    # Set seaborn style for better aesthetics
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)
    
    graphs = {}

    # Plan Distribution:
    if 'Plan' in df.columns:
        fig1, ax1 = plt.subplots()
        plan_counts = df['Plan'].value_counts()
        sns.barplot(x=plan_counts.index, y=plan_counts.values, palette="viridis", ax=ax1)
        ax1.set_title('Plan Distribution', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Subscription Plan', fontsize=12)
        ax1.set_ylabel('Number of Customers', fontsize=12)
        for i, v in enumerate(plan_counts.values):
            ax1.text(i, v + 5, str(v), ha='center', fontsize=10)
        plt.tight_layout()
        graphs['Plan Distribution'] = fig1

    # Churn Rate:
    if 'Churn' in df.columns:
        fig2, ax2 = plt.subplots()
        churn_counts = df['Churn'].value_counts()
        ax2.pie(churn_counts, labels=churn_counts.index, autopct='%1.1f%%', 
                startangle=90, colors=sns.color_palette("viridis", len(churn_counts)), 
                wedgeprops=dict(width=0.5, edgecolor='w'))
        ax2.set_title('Churn Rate', fontsize=14, fontweight='bold')
        plt.tight_layout()
        graphs['Churn Rate'] = fig2

    # Spend vs Tenure:
    if 'MonthlySpend' in df.columns and 'Tenure' in df.columns:
        fig3, ax3 = plt.subplots()
        if 'Churn' in df.columns:
            # Color by churn status
            scatter = sns.scatterplot(
                x='MonthlySpend', 
                y='Tenure', 
                hue='Churn',
                palette=["#2ecc71", "#e74c3c"],
                alpha=0.7, 
                s=100,
                data=df,
                ax=ax3
            )
            plt.legend(title='Churned', loc='upper right')
        else:
            scatter = sns.scatterplot(
                x='MonthlySpend', 
                y='Tenure', 
                alpha=0.7, 
                s=100,
                data=df,
                ax=ax3
            )
        
        ax3.set_title('Monthly Spend vs Tenure', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Monthly Spend ($)', fontsize=12)
        ax3.set_ylabel('Tenure (Months)', fontsize=12)
        plt.tight_layout()
        graphs['Spend vs Tenure'] = fig3

    # Industry Distribution:
    if 'Industry' in df.columns:
        fig4, ax4 = plt.subplots()
        industry_counts = df['Industry'].value_counts().head(10)
        sns.barplot(x=industry_counts.values, y=industry_counts.index, palette="viridis", ax=ax4)
        ax4.set_title('Top 10 Industries', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Number of Customers', fontsize=12)
        ax4.set_ylabel('Industry', fontsize=12)
        for i, v in enumerate(industry_counts.values):
            ax4.text(v + 0.5, i, str(v), va='center', fontsize=10)
        plt.tight_layout()
        graphs['Top 10 Industries'] = fig4

    # Monthly Spend Distribution:
    if 'MonthlySpend' in df.columns:
        fig5, ax5 = plt.subplots()
        sns.histplot(df['MonthlySpend'], bins=20, kde=True, color='skyblue', ax=ax5)
        ax5.set_title('Monthly Spend Distribution', fontsize=14, fontweight='bold')
        ax5.set_xlabel('Monthly Spend ($)', fontsize=12)
        ax5.set_ylabel('Frequency', fontsize=12)
        ax5.axvline(df['MonthlySpend'].mean(), color='red', linestyle='--', 
                   label=f'Mean: ${df["MonthlySpend"].mean():.2f}')
        ax5.axvline(df['MonthlySpend'].median(), color='green', linestyle='--', 
                   label=f'Median: ${df["MonthlySpend"].median():.2f}')
        ax5.legend()
        plt.tight_layout()
        graphs['Monthly Spend Distribution'] = fig5
    
    # Tenure Distribution:
    if 'Tenure' in df.columns:
        fig6, ax6 = plt.subplots()
        sns.histplot(df['Tenure'], bins=20, kde=True, color='lightgreen', ax=ax6)
        ax6.set_title('Customer Tenure Distribution', fontsize=14, fontweight='bold')
        ax6.set_xlabel('Tenure (Months)', fontsize=12)
        ax6.set_ylabel('Frequency', fontsize=12)
        ax6.axvline(df['Tenure'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {df["Tenure"].mean():.2f} months')
        ax6.axvline(df['Tenure'].median(), color='green', linestyle='--', 
                   label=f'Median: {df["Tenure"].median():.2f} months')
        ax6.legend()
        plt.tight_layout()
        graphs['Tenure Distribution'] = fig6

    return graphs

def fig_to_base64(fig):
    """
    Convert a matplotlib figure to a base64 encoded string
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return img_str

def save_graph_images(graphs: Dict[str, Figure], output_dir: str = 'app/static/images') -> Dict[str, str]:
    """
    Save graph figures as images and return a dictionary of file paths
    
    Args:
        graphs: Dictionary of graph figures
        output_dir: Directory to save images to
        
    Returns:
        Dictionary mapping graph titles to their base64 encoded string representations
    """
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save each graph as an image and store the path
    graph_data = {}
    
    for title, fig in graphs.items():
        # Convert fig to base64 string
        img_str = fig_to_base64(fig)
        graph_data[title] = img_str
        
        # Also save to disk
        file_path = os.path.join(output_dir, f"{title.lower().replace(' ', '_')}.png")
        fig.savefig(file_path, bbox_inches='tight', dpi=100)
    
    return graph_data
