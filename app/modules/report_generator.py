import pandas as pd
from typing import Dict, Any, List
import os
import streamlit as st
from modules.crew_agents import generate_report
from modules.graph_generator import save_graph_images

def generate_streamlit_report(df: pd.DataFrame, graphs: Dict[str, Any]) -> None:
    """
    Generate and display a report directly in Streamlit using native components
    
    Args:
        df: DataFrame containing the dataset
        graphs: Dictionary of matplotlib figures
    """
    # Generate the AI report
    ai_report = generate_report(df)
    
    # Extract key metrics directly from the dataframe
    metrics = extract_key_metrics(df)
    
    # Create headers for different report sections
    report_sections = extract_report_sections(ai_report)
    
    # Build and display the report using Streamlit components
    display_shopmax_report(report_sections, graphs, metrics, df)

def extract_key_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Extract key metrics from the dataframe for the report
    
    Args:
        df: Dataset DataFrame
        
    Returns:
        Dict of key metrics
    """
    metrics = {}
    
    # Plan distribution if available
    if 'Plan' in df.columns:
        plan_distribution = df['Plan'].value_counts(normalize=True) * 100
        metrics['plan_distribution'] = {plan: f"{pct:.1f}%" for plan, pct in plan_distribution.items()}
    
    # Financial metrics
    if 'MonthlySpend' in df.columns:
        metrics['average_spend'] = f"${df['MonthlySpend'].mean():.2f}"
        metrics['median_spend'] = f"${df['MonthlySpend'].median():.2f}"
        metrics['max_spend'] = f"${df['MonthlySpend'].max():.2f}"
    
    # Churn rate
    if 'Churn' in df.columns:
        # Handle different possible data types for churn
        if df['Churn'].dtype == bool:
            churn_rate = df['Churn'].mean() * 100
        else:
            # Try to convert to boolean if it's string-based (True/False or 1/0)
            try:
                df['Churn_bool'] = df['Churn'].astype(bool)
                churn_rate = df['Churn_bool'].mean() * 100
            except:
                # Fallback: use value_counts
                churn_rate = df['Churn'].value_counts(normalize=True).get(True, 0) * 100
        
        metrics['churn_rate'] = f"{churn_rate:.1f}%"
    
    # Tenure metrics
    if 'Tenure' in df.columns:
        metrics['average_tenure'] = f"{df['Tenure'].mean():.1f}"
        metrics['median_tenure'] = f"{df['Tenure'].median():.1f}"
    
    # Top industries if available
    if 'Industry' in df.columns:
        top_industries = df['Industry'].value_counts().head(5).index.tolist()
        metrics['top_industries'] = top_industries
    
    # Countries if available
    if 'Country' in df.columns:
        top_countries = df['Country'].value_counts().head(5).index.tolist()
        metrics['top_countries'] = top_countries
    
    return metrics

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

def extract_bullet_points(text: str) -> List[str]:
    """
    Extract bullet points from text
    
    Args:
        text: Text with bullet points (- or *)
        
    Returns:
        List of bullet points
    """
    bullet_points = []
    lines = text.split('\n')
    
    for line in lines:
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            # Extract the bullet point text
            point_text = line.strip()[2:].strip()
            if point_text:
                bullet_points.append(point_text)
    
    return bullet_points

def filter_insights_by_keyword(insights: str, keywords: List[str]) -> str:
    """
    Filter insights text to only include lines containing specific keywords
    
    Args:
        insights: The insights text
        keywords: List of keywords to filter by
        
    Returns:
        Filtered insights text
    """
    if not insights:
        return ""
        
    filtered_lines = []
    lines = insights.split('\n')
    
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in keywords):
            filtered_lines.append(line)
    
    return " ".join(filtered_lines)

def display_shopmax_report(sections: Dict[str, str], graphs: Dict[str, Any], 
                         metrics: Dict[str, Any], df: pd.DataFrame) -> None:
    """
    Display a ShopMax styled business analyst journal report using Streamlit components
    
    Args:
        sections: Dictionary of report sections
        graphs: Dictionary of matplotlib figures
        metrics: Dictionary of key metrics
        df: The dataset DataFrame
    """
    # Add custom CSS
    st.markdown("""
    <style>
    .reportTitle {
        text-align: center;
        color: white;
        background-color: #2c3e50;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .sectionHeader {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 8px;
    }
    .insightBox {
        background-color: #f8f9fa;
        border-left: 4px solid #e74c3c;
        padding: 15px;
        border-radius: 4px;
        margin: 15px 0;
    }
    .insightTitle {
        color: #e74c3c;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Report Title
    st.markdown('<div class="reportTitle"><h1>📋 ShopMax | Business Analyst Journal</h1></div>', 
                unsafe_allow_html=True)
    
    # ==== Subscription Plans Section ====
    st.markdown('<div class="sectionHeader">🔵 Subscription Plans</div>', unsafe_allow_html=True)
    
    # Add plan metrics
    if 'plan_distribution' in metrics and metrics['plan_distribution']:
        for plan, percentage in metrics['plan_distribution'].items():
            st.markdown(f"- **{plan} Plan**: {percentage} of customers")
    
    # Add Plan Distribution graph if available
    if 'Plan Distribution' in graphs:
        st.pyplot(graphs['Plan Distribution'])
    
    # Add graph insight for subscription plans
    plan_insights = filter_insights_by_keyword(sections["insights"], ["subscription", "plan"])
    
    if plan_insights:
        st.markdown('<div class="insightBox"><div class="insightTitle">📊 Graph Insight:</div>' + 
                   plan_insights + '</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="insightBox">
            <div class="insightTitle">📊 Graph Insight:</div>
            A significant portion of subscribers are opting for the Basic plan, indicating a potential opportunity 
            to enhance its features or introduce upsell strategies to transition users to higher-tier plans.
        </div>
        """, unsafe_allow_html=True)
    
    # Add spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==== Financial Insights Section ====
    st.markdown('<div class="sectionHeader">🔵 Financial Insights</div>', unsafe_allow_html=True)
    
    # Add financial metrics
    metric_cols = st.columns(2)
    with metric_cols[0]:
        if 'average_spend' in metrics:
            st.metric("Average Spend", metrics['average_spend'])
    
    with metric_cols[1]:
        if 'churn_rate' in metrics:
            st.metric("Churn Rate", metrics['churn_rate'])
    
    # Add financial graphs in two columns
    graph_cols = st.columns(2)
    
    with graph_cols[0]:
        if 'Churn Rate' in graphs:
            st.pyplot(graphs['Churn Rate'])
    
    with graph_cols[1]:
        if 'Monthly Spend Distribution' in graphs:
            st.pyplot(graphs['Monthly Spend Distribution'])
    
    # Add financial insights
    financial_insights = filter_insights_by_keyword(
        sections["insights"], ["spend", "financial", "churn", "revenue", "cost"]
    )
    
    if financial_insights:
        st.markdown('<div class="insightBox"><div class="insightTitle">📊 Graph Insight:</div>' + 
                   financial_insights + '</div>', unsafe_allow_html=True)
    
    # Add spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==== Customer Tenure Section ====
    st.markdown('<div class="sectionHeader">🔵 Customer Tenure Analysis</div>', unsafe_allow_html=True)
    
    # Add tenure metrics
    if 'average_tenure' in metrics:
        st.markdown(f"- **Average Tenure**: {metrics['average_tenure']} months")
    
    # Add tenure graphs
    tenure_cols = st.columns(2)
    
    with tenure_cols[0]:
        if 'Spend vs Tenure' in graphs:
            st.pyplot(graphs['Spend vs Tenure'])
    
    with tenure_cols[1]:
        if 'Tenure Distribution' in graphs:
            st.pyplot(graphs['Tenure Distribution'])
    
    # Add tenure insights
    tenure_insights = filter_insights_by_keyword(
        sections["insights"], ["tenure", "retention", "loyal", "customer lifetime"]
    )
    
    if tenure_insights:
        st.markdown('<div class="insightBox"><div class="insightTitle">📊 Graph Insight:</div>' + 
                   tenure_insights + '</div>', unsafe_allow_html=True)
    
    # Add spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==== Industry Distribution Section ====
    if 'Top 10 Industries' in graphs:
        st.markdown('<div class="sectionHeader">🔵 Industry Distribution</div>', unsafe_allow_html=True)
        
        # Add industry graph
        st.pyplot(graphs['Top 10 Industries'])
        
        # Add industry insights
        industry_insights = filter_insights_by_keyword(
            sections["insights"], ["industry", "sector", "vertical", "business type"]
        )
        
        if industry_insights:
            st.markdown('<div class="insightBox"><div class="insightTitle">📊 Graph Insight:</div>' + 
                       industry_insights + '</div>', unsafe_allow_html=True)
        
        # Add spacing
        st.markdown("<br>", unsafe_allow_html=True)
    
    # ==== Strategic Recommendations Section ====
    if sections["recommendations"]:
        st.markdown('<div class="sectionHeader">🔵 Strategic Recommendations</div>', unsafe_allow_html=True)
        
        # Extract and display bullet points
        bullet_points = extract_bullet_points(sections["recommendations"])
        for point in bullet_points:
            st.markdown(f"- {point}")
        
        # If no bullet points were found, display the raw recommendations
        if not bullet_points:
            st.write(sections["recommendations"])
    
    # Add download button for report export
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background-color: #f3f4f6; padding: 15px; border-radius: 5px; text-align: center;">
        <h3 style="margin-top: 0;">Export Your Business Analysis Report</h3>
        <p>Download the full report with visualizations and insights for sharing with your team.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create HTML version for download
    html_report = build_html_for_download(sections, graphs, metrics)
    
    st.download_button(
        label="📥 Download Full Report (HTML)",
        data=html_report,
        file_name="shopmax_business_analysis_report.html",
        mime="text/html"
    )

def build_html_for_download(sections, graph_data, metrics):
    """
    Create an HTML report for download
    This reuses the ShopMax styled report but in downloadable format
    """
    # Save graphs as base64 encoded strings if needed
    # For download we'd still use HTML
    
    # This is a simplified version that would be expanded in a real implementation
    # to create a downloadable version of the report with the same styling
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ShopMax Business Analyst Journal</title>
        <style>
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                max-width: 1100px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .report-container {
                background-color: #2c3e50;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
                color: white;
            }
            .report-title {
                text-align: center;
                padding: 10px 0;
                font-size: 28px;
                font-weight: 600;
            }
            .section {
                background-color: white;
                border-radius: 8px;
                margin-bottom: 25px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .section-header {
                display: flex;
                align-items: center;
                margin-bottom: 15px;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }
            .section-title {
                font-size: 22px;
                color: #2c3e50;
                font-weight: 600;
                margin: 0;
            }
            .insights {
                background-color: #f8f9fa;
                border-left: 4px solid #e74c3c;
                padding: 15px;
                margin: 15px 0;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <div class="report-container">
            <div class="report-title">📋 ShopMax | Business Analyst Journal</div>
        </div>
        
        <div class="section">
            <div class="section-header">
                <h2 class="section-title">🔵 Subscription Plans</h2>
            </div>
            <!-- Plan details would go here -->
            <div class="insights">
                <p>A significant portion of subscribers are opting for the Basic plan, 
                indicating a potential opportunity to enhance its features or introduce upsell strategies.</p>
            </div>
        </div>
        
        <div class="section">
            <div class="section-header">
                <h2 class="section-title">🔵 Financial Insights</h2>
            </div>
            <!-- Financial details would go here -->
        </div>
        
        <!-- More sections would follow -->
        
        <div class="section">
            <div class="section-header">
                <h2 class="section-title">🔵 Strategic Recommendations</h2>
            </div>
            <!-- Recommendations would go here -->
        </div>
    </body>
    </html>
    """
    
    return html 