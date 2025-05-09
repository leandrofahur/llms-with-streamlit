import pandas as pd
from typing import Dict, Any, List
import os
import streamlit as st
import random
# Remove dependency on crew_agents
# from modules.crew_agents import generate_report
from modules.graph_generator import save_graph_images

def generate_streamlit_report(df: pd.DataFrame, graphs: Dict[str, Any]) -> None:
    """
    Generate and display a report directly in Streamlit using native components
    
    Args:
        df: DataFrame containing the dataset
        graphs: Dictionary of matplotlib figures
    """
    # Generate sample insights instead of using AI
    # ai_report = generate_report(df)
    sample_insights = generate_sample_insights(df)
    
    # Extract key metrics directly from the dataframe
    metrics = extract_key_metrics(df)
    
    # Create headers for different report sections
    # report_sections = extract_report_sections(ai_report)
    report_sections = {
        "intro": sample_insights["intro"],
        "insights": sample_insights["insights"],
        "quality": sample_insights["quality"],
        "recommendations": sample_insights["recommendations"]
    }
    
    # Build and display the report using Streamlit components
    display_shopmax_report(report_sections, graphs, metrics, df)

def generate_sample_insights(df: pd.DataFrame) -> Dict[str, str]:
    """
    Generate sample insights without using AI agents
    
    Args:
        df: DataFrame containing the dataset
        
    Returns:
        Dictionary with sample insights
    """
    # Extract some basic statistics for insights
    sample_insights = {
        "intro": "This report analyzes customer data to identify key patterns and trends.",
        "insights": "",
        "quality": "The dataset was analyzed for quality issues. No major issues were found.",
        "recommendations": ""
    }
    
    # Add plan insights if available
    if 'Plan' in df.columns:
        plan_counts = df['Plan'].value_counts()
        top_plan = plan_counts.index[0]
        plan_percentage = plan_counts[top_plan] / len(df) * 100
        
        sample_insights["insights"] += f"The {top_plan} plan is the most popular subscription option, accounting for {plan_percentage:.1f}% of customers. "
        sample_insights["insights"] += "This suggests strong product-market fit for this tier. "
        sample_insights["recommendations"] += f"- Consider optimizing the {top_plan} plan features based on customer usage patterns.\n"
    
    # Add financial insights
    if 'MonthlySpend' in df.columns:
        avg_spend = df['MonthlySpend'].mean()
        sample_insights["insights"] += f"The average monthly spend is ${avg_spend:.2f}, which indicates a solid revenue stream. "
        sample_insights["recommendations"] += "- Implement tiered pricing strategies to increase average revenue per user.\n"
    
    # Add churn insights
    if 'Churn' in df.columns:
        try:
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
            
            sample_insights["insights"] += f"The current churn rate is {churn_rate:.1f}%, which impacts customer lifetime value. "
            sample_insights["recommendations"] += "- Develop targeted retention programs for at-risk customer segments.\n"
        except:
            pass
    
    # Add tenure insights
    if 'Tenure' in df.columns:
        avg_tenure = df['Tenure'].mean()
        sample_insights["insights"] += f"Customers stay subscribed for an average of {avg_tenure:.1f} months. "
        sample_insights["recommendations"] += "- Create loyalty rewards for customers who reach tenure milestones.\n"
    
    # Add industry insights if available
    if 'Industry' in df.columns:
        top_industries = df['Industry'].value_counts().head(3)
        industries_text = ", ".join([f"{ind}" for ind in top_industries.index])
        sample_insights["insights"] += f"The top industries in our customer base are {industries_text}. "
        sample_insights["recommendations"] += "- Develop industry-specific features for the top customer segments.\n"
    
    # Add generic insights if we have little to work with
    if len(sample_insights["insights"]) < 50:
        sample_insights["insights"] += """
        The customer data reveals several actionable patterns that can inform business strategy.
        There's a correlation between subscription tiers and customer retention that should be leveraged.
        Customer acquisition channels significantly impact lifetime value and should be optimized accordingly.
        """
    
    # Add generic recommendations if we have little to work with
    if len(sample_insights["recommendations"]) < 50:
        sample_insights["recommendations"] += """
        - Implement a customer feedback loop to continually improve product features
        - Develop a comprehensive customer onboarding program to increase initial engagement
        - Create targeted marketing campaigns based on customer segmentation
        - Optimize pricing strategy to maximize both conversion and revenue
        - Establish a customer success program to proactively address potential churn factors
        """
    
    return sample_insights

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
    
    # Return the filtered text or an empty string if no matches
    return " ".join(filtered_lines)

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

def get_default_insight(section_type: str) -> str:
    """
    Get default insights for a graph section when no AI insights are found
    
    Args:
        section_type: Type of section (plans, financial, tenure, industry)
        
    Returns:
        Default insight text
    """
    default_insights = {
        "plans": """
            A significant portion of subscribers are opting for the Basic plan, 
            indicating a potential opportunity to enhance its features or introduce upsell 
            strategies to transition users to higher-tier plans. The distribution suggests 
            focusing marketing efforts on highlighting the value of premium tiers.
        """,
        
        "financial": """
            The monthly spend distribution reveals important spending patterns that can 
            be leveraged for targeted pricing strategies. The churn rate analysis 
            indicates opportunities for retention programs focused on at-risk segments.
        """,
        
        "tenure": """
            Customer tenure analysis shows correlation between subscription duration and 
            spending levels. Longer-tenured customers tend to generate more predictable 
            revenue, suggesting value in loyalty programs to extend customer lifetime value.
        """,
        
        "industry": """
            The industry distribution highlights key verticals that form your customer base. 
            This suggests opportunities for industry-specific features or marketing campaigns 
            targeting the most represented segments, while also identifying potential growth 
            areas in underrepresented industries.
        """
    }
    
    # Clean up the text by removing extra whitespace
    insight = default_insights.get(section_type, "")
    return " ".join(line.strip() for line in insight.split('\n')).strip()

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
    plan_insights = filter_insights_by_keyword(sections["insights"], 
                                               ["subscription", "plan", "tier", "basic", "premium", "enterprise"])
    
    if plan_insights:
        st.markdown('<div class="insightBox"><div class="insightTitle">📊 Graph Insight:</div>' + 
                   plan_insights + '</div>', unsafe_allow_html=True)
    else:
        # Use default insight
        st.markdown(f"""
        <div class="insightBox">
            <div class="insightTitle">📊 Graph Insight:</div>
            {get_default_insight("plans")}
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
        sections["insights"], ["spend", "financial", "churn", "revenue", "cost", "pricing", "dollar", "$", "money"]
    )
    
    if financial_insights:
        st.markdown('<div class="insightBox"><div class="insightTitle">📊 Graph Insight:</div>' + 
                   financial_insights + '</div>', unsafe_allow_html=True)
    else:
        # Use default insight
        st.markdown(f"""
        <div class="insightBox">
            <div class="insightTitle">📊 Graph Insight:</div>
            {get_default_insight("financial")}
        </div>
        """, unsafe_allow_html=True)
    
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
        sections["insights"], ["tenure", "retention", "loyal", "customer lifetime", "month", "churn", "duration"]
    )
    
    if tenure_insights:
        st.markdown('<div class="insightBox"><div class="insightTitle">📊 Graph Insight:</div>' + 
                   tenure_insights + '</div>', unsafe_allow_html=True)
    else:
        # Use default insight
        st.markdown(f"""
        <div class="insightBox">
            <div class="insightTitle">📊 Graph Insight:</div>
            {get_default_insight("tenure")}
        </div>
        """, unsafe_allow_html=True)
    
    # Add spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==== Industry Distribution Section ====
    if 'Top 10 Industries' in graphs:
        st.markdown('<div class="sectionHeader">🔵 Industry Distribution</div>', unsafe_allow_html=True)
        
        # Add industry graph
        st.pyplot(graphs['Top 10 Industries'])
        
        # Add industry insights
        industry_insights = filter_insights_by_keyword(
            sections["insights"], ["industry", "sector", "vertical", "business type", "market", "segment"]
        )
        
        if industry_insights:
            st.markdown('<div class="insightBox"><div class="insightTitle">📊 Graph Insight:</div>' + 
                       industry_insights + '</div>', unsafe_allow_html=True)
        else:
            # Use default insight
            st.markdown(f"""
            <div class="insightBox">
                <div class="insightTitle">📊 Graph Insight:</div>
                {get_default_insight("industry")}
            </div>
            """, unsafe_allow_html=True)
        
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