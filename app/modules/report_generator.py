import pandas as pd
from typing import Dict, Any, List
import os
from modules.crew_agents import generate_report
from modules.graph_generator import save_graph_images

def generate_markdown_report(df: pd.DataFrame, graphs: Dict[str, Any]) -> str:
    """
    Generate a full markdown report with integrated graphs
    
    Args:
        df: DataFrame containing the dataset
        graphs: Dictionary of matplotlib figures
        
    Returns:
        str: Markdown formatted report with embedded graphs
    """
    # Generate the AI report
    ai_report = generate_report(df)
    
    # Save graphs as base64 encoded strings
    graph_data = save_graph_images(graphs)
    
    # Create headers for different report sections
    report_sections = extract_report_sections(ai_report)
    
    # Build the final markdown report with graphs
    final_report = build_markdown_report(report_sections, graph_data, df)
    
    return final_report

def extract_report_sections(report_text: str) -> Dict[str, str]:
    """
    Extract different sections from the AI generated report
    
    Args:
        report_text: Raw text from the AI report
    
    Returns:
        Dictionary with section name as key and content as value
    """
    # Initialize sections
    sections = {
        "intro": "",
        "insights": "",
        "quality": "",
        "recommendations": "",
    }
    
    # Simple logic to split the report into sections based on common patterns
    lines = report_text.split('\n')
    current_section = "intro"
    
    for line in lines:
        lower_line = line.lower()
        
        if "insight" in lower_line and "#" in line:
            current_section = "insights"
            sections[current_section] += line + "\n"
        elif "quality" in lower_line and "#" in line:
            current_section = "quality"
            sections[current_section] += line + "\n"
        elif "recommend" in lower_line and "#" in line:
            current_section = "recommendations"
            sections[current_section] += line + "\n"
        else:
            sections[current_section] += line + "\n"
    
    return sections

def build_markdown_report(sections: Dict[str, str], graph_data: Dict[str, str], df: pd.DataFrame) -> str:
    """
    Build the final markdown report with embedded graphs
    
    Args:
        sections: Dictionary of report sections
        graph_data: Dictionary of base64 encoded graph images
        df: The dataset DataFrame for summary statistics
        
    Returns:
        str: The final markdown report with embedded graphs
    """
    # Build the final report with added styling and embedded graphs
    markdown = """
    <style>
    .report-container {
        font-family: Arial, sans-serif;
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .report-header {
        text-align: center;
        padding-bottom: 20px;
        border-bottom: 2px solid #2c3e50;
        margin-bottom: 30px;
    }
    .section {
        margin-bottom: 30px;
        padding: 20px;
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .section-title {
        color: #2c3e50;
        border-bottom: 1px solid #eee;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    .graph-container {
        text-align: center;
        margin: 20px 0;
    }
    .graph-caption {
        font-style: italic;
        color: #555;
        text-align: center;
        margin-top: 10px;
        font-size: 0.9em;
    }
    .key-metrics {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        margin: 20px 0;
    }
    .metric-card {
        width: 30%;
        padding: 15px;
        background-color: #e8f4f8;
        border-radius: 5px;
        margin-bottom: 15px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.8em;
        font-weight: bold;
        color: #2980b9;
    }
    .metric-label {
        font-size: 0.9em;
        color: #555;
    }
    </style>
    
    <div class="report-container">
        <div class="report-header">
            <h1>Business Analyst ICP Journal</h1>
            <p>Comprehensive analysis with data visualizations</p>
        </div>
    """
    
    # Add key metrics section
    markdown += """
        <div class="section">
            <h2 class="section-title">Key Metrics Overview</h2>
            <div class="key-metrics">
    """
    
    # Calculate and add key metrics
    metrics = [
        {"label": "Total Customers", "value": len(df)},
        {"label": "Average Monthly Spend", 
         "value": f"${df['MonthlySpend'].mean():.2f}" if 'MonthlySpend' in df.columns else "N/A"},
        {"label": "Average Tenure", 
         "value": f"{df['Tenure'].mean():.1f} months" if 'Tenure' in df.columns else "N/A"},
    ]
    
    if 'Churn' in df.columns:
        churn_rate = df['Churn'].mean() * 100 if df['Churn'].dtype == bool else df['Churn'].value_counts(normalize=True).get(True, 0) * 100
        metrics.append({"label": "Churn Rate", "value": f"{churn_rate:.1f}%"})
    
    for metric in metrics:
        markdown += f"""
                <div class="metric-card">
                    <div class="metric-value">{metric['value']}</div>
                    <div class="metric-label">{metric['label']}</div>
                </div>
        """
    
    markdown += """
            </div>
        </div>
    """
    
    # Add distribution graphs section
    markdown += """
        <div class="section">
            <h2 class="section-title">Distribution Analysis</h2>
    """
    
    # Add Plan Distribution graph if available
    if 'Plan Distribution' in graph_data:
        markdown += f"""
            <div class="graph-container">
                <img src="data:image/png;base64,{graph_data['Plan Distribution']}" alt="Plan Distribution" style="max-width: 100%;">
                <p class="graph-caption">Figure 1: Distribution of customers across different subscription plans</p>
            </div>
        """
    
    # Add Industry Distribution graph if available
    if 'Top 10 Industries' in graph_data:
        markdown += f"""
            <div class="graph-container">
                <img src="data:image/png;base64,{graph_data['Top 10 Industries']}" alt="Industry Distribution" style="max-width: 100%;">
                <p class="graph-caption">Figure 2: Top 10 industries represented in the customer base</p>
            </div>
        """
    
    markdown += """
        </div>
    """
    
    # Add Customer Behavior section
    markdown += """
        <div class="section">
            <h2 class="section-title">Customer Behavior Analysis</h2>
    """
    
    # Add Churn Rate graph if available
    if 'Churn Rate' in graph_data:
        markdown += f"""
            <div class="graph-container">
                <img src="data:image/png;base64,{graph_data['Churn Rate']}" alt="Churn Rate" style="max-width: 100%;">
                <p class="graph-caption">Figure 3: Customer churn rate analysis</p>
            </div>
        """
    
    # Add Spend vs Tenure graph if available
    if 'Spend vs Tenure' in graph_data:
        markdown += f"""
            <div class="graph-container">
                <img src="data:image/png;base64,{graph_data['Spend vs Tenure']}" alt="Spend vs Tenure" style="max-width: 100%;">
                <p class="graph-caption">Figure 4: Relationship between monthly spend and customer tenure</p>
            </div>
        """
    
    markdown += """
        </div>
    """
    
    # Add Financial Insights section
    markdown += """
        <div class="section">
            <h2 class="section-title">Financial Insights</h2>
    """
    
    # Add Monthly Spend Distribution graph if available
    if 'Monthly Spend Distribution' in graph_data:
        markdown += f"""
            <div class="graph-container">
                <img src="data:image/png;base64,{graph_data['Monthly Spend Distribution']}" alt="Monthly Spend Distribution" style="max-width: 100%;">
                <p class="graph-caption">Figure 5: Distribution of monthly spending across customers</p>
            </div>
        """
    
    # Add Tenure Distribution graph if available
    if 'Tenure Distribution' in graph_data:
        markdown += f"""
            <div class="graph-container">
                <img src="data:image/png;base64,{graph_data['Tenure Distribution']}" alt="Tenure Distribution" style="max-width: 100%;">
                <p class="graph-caption">Figure 6: Distribution of customer tenure in months</p>
            </div>
        """
    
    markdown += """
        </div>
    """
    
    # Add AI Analysis section with the AI report content
    markdown += """
        <div class="section">
            <h2 class="section-title">AI Analysis Findings</h2>
    """
    
    # Add insights section if it exists
    if sections["insights"]:
        markdown += """
            <h3>Key Insights</h3>
            <div>{}</div>
        """.format(sections["insights"].replace('\n', '<br>'))
    
    # Add quality section if it exists
    if sections["quality"]:
        markdown += """
            <h3>Data Quality Assessment</h3>
            <div>{}</div>
        """.format(sections["quality"].replace('\n', '<br>'))
    
    # Add recommendations section if it exists
    if sections["recommendations"]:
        markdown += """
            <h3>Strategic Recommendations</h3>
            <div>{}</div>
        """.format(sections["recommendations"].replace('\n', '<br>'))
    
    markdown += """
        </div>
    </div>
    """
    
    return markdown 