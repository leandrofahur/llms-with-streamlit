import streamlit as st
import pandas as pd
from config import get_openai_api_key
from modules.graph_generator import generate_graphs
from modules.report_generator import generate_streamlit_report
import os

# Create static directory for images if it doesn't exist
os.makedirs('app/static/images', exist_ok=True)

# Load OpenAI API key:
openai_api_key = get_openai_api_key()

st.set_page_config(
    page_title="📋 Business Analyst ICP Journal",
    page_icon="🧠",
    layout="wide",  # Wide layout for better report display
    initial_sidebar_state="collapsed"  # Start with sidebar collapsed for more space
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 1rem 1rem 1rem;
    }
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3, h4 {
        font-family: 'Arial', sans-serif;
    }
    h1 {
        color: #1E3A8A;
        margin-bottom: 1.5rem;
    }
    .stButton > button {
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #2563EB;
    }
    .data-preview {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .dashboard-content {
        margin-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f3f4f6;
        border-radius: 4px 4px 0px 0px;
        padding: 8px 16px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E3A8A;
        color: white;
    }
    .success-msg {
        padding: 0.75rem;
        background-color: #ecfdf5;
        color: #065f46;
        border-radius: 0.375rem;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }
    .report-divider {
        margin: 2rem 0;
        border-top: 2px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📋 Business Analyst ICP Journal")
st.markdown("""
<p style="font-size: 1.2rem; margin-bottom: 2rem; color: #4B5563;">
    Transform your customer data into actionable business insights with AI-powered analysis and visualization
</p>
""", unsafe_allow_html=True)

# File Uploader (only CSV files are supported)
uploaded_file = st.file_uploader("Upload your customer dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    try:
        # Read CSV into DataFrame:
        df = pd.read_csv(uploaded_file)

        # Rename columns:        
        df.rename(columns={
            'Monthly Spend ($)': 'MonthlySpend',
            'Tenure (Months)': 'Tenure',
            'Churned': 'Churn'
        }, inplace=True)

        # Success message with custom styling
        st.markdown('<div class="success-msg">✅ File uploaded successfully! Your data is ready for analysis.</div>', unsafe_allow_html=True)
        
        # Create tabs for data exploration and report
        tab1, tab2 = st.tabs(["Data Exploration", "Business Report"])
        
        with tab1:
            # Two columns for layout with adjusted width ratio
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown("""
                <div class="data-preview">
                    <h3 style="margin-top: 0;">📊 Dataset Overview</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Data preview
                st.dataframe(df.head(10), use_container_width=True)
                
                # Dataset stats
                st.markdown("<h4>Dataset Statistics</h4>", unsafe_allow_html=True)
                stats_col1, stats_col2 = st.columns(2)
                with stats_col1:
                    st.metric("Rows", df.shape[0])
                with stats_col2:
                    st.metric("Columns", df.shape[1])
                
                # Data types summary
                st.markdown("<h4>Column Types</h4>", unsafe_allow_html=True)
                data_types = pd.DataFrame(df.dtypes, columns=['Data Type'])
                st.dataframe(data_types, use_container_width=True)
                
                # Generate report button
                st.markdown("<h4>Generate Full Report</h4>", unsafe_allow_html=True)
                analyze_button = st.button("🔍 Generate Business Report", type="primary")
                
            with col2:
                st.markdown("""
                <div class="dashboard-content">
                    <h3>📈 Interactive Data Visualizations</h3>
                    <p style="margin-bottom: 1rem;">Explore key metrics and patterns in your dataset with these visualizations.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Generate graphs immediately:
                with st.spinner("Generating visualizations..."):
                    graphs = generate_graphs(df)
                
                # More descriptive tab names
                viz_tabs = st.tabs(["Customer Segments", "Retention Analysis", "Financial Metrics"])
                
                with viz_tabs[0]:
                    st.markdown("""
                    <h4 style="margin-top: 0.5rem;">Customer Segmentation Analysis</h4>
                    <p>Understand how your customers are distributed across different categories.</p>
                    """, unsafe_allow_html=True)
                    
                    tab1_col1, tab1_col2 = st.columns(2)
                    with tab1_col1:
                        if 'Plan Distribution' in graphs:
                            st.pyplot(graphs['Plan Distribution'])
                            st.markdown("<p style='text-align: center; font-style: italic;'>Distribution of customers across subscription plans</p>", unsafe_allow_html=True)
                    
                    with tab1_col2:
                        if 'Top 10 Industries' in graphs:
                            st.pyplot(graphs['Top 10 Industries'])
                            st.markdown("<p style='text-align: center; font-style: italic;'>Top industries in your customer base</p>", unsafe_allow_html=True)
                
                with viz_tabs[1]:
                    st.markdown("""
                    <h4 style="margin-top: 0.5rem;">Customer Retention Insights</h4>
                    <p>Analyze churn patterns and customer loyalty metrics.</p>
                    """, unsafe_allow_html=True)
                    
                    tab2_col1, tab2_col2 = st.columns(2)
                    with tab2_col1:
                        if 'Churn Rate' in graphs:
                            st.pyplot(graphs['Churn Rate'])
                            st.markdown("<p style='text-align: center; font-style: italic;'>Customer churn distribution</p>", unsafe_allow_html=True)
                    
                    with tab2_col2:
                        if 'Tenure Distribution' in graphs:
                            st.pyplot(graphs['Tenure Distribution'])
                            st.markdown("<p style='text-align: center; font-style: italic;'>Distribution of customer tenure (months)</p>", unsafe_allow_html=True)
                    
                    # Add extra insights for this tab
                    if 'Spend vs Tenure' in graphs:
                        st.markdown("<h4>Relationship: Spend vs. Tenure</h4>", unsafe_allow_html=True)
                        st.pyplot(graphs['Spend vs Tenure'])
                        st.markdown("<p style='text-align: center; font-style: italic;'>How monthly spend correlates with customer tenure</p>", unsafe_allow_html=True)
                
                with viz_tabs[2]:
                    st.markdown("""
                    <h4 style="margin-top: 0.5rem;">Financial Performance Analysis</h4>
                    <p>Visualize spending patterns and financial metrics across your customer base.</p>
                    """, unsafe_allow_html=True)
                    
                    if 'Monthly Spend Distribution' in graphs:
                        st.pyplot(graphs['Monthly Spend Distribution'])
                        st.markdown("<p style='text-align: center; font-style: italic;'>Distribution of monthly spending across customers</p>", unsafe_allow_html=True)
                    
                    # Add some financial insights based on the data
                    if 'MonthlySpend' in df.columns:
                        finance_col1, finance_col2, finance_col3 = st.columns(3)
                        with finance_col1:
                            st.metric("Avg. Monthly Spend", f"${df['MonthlySpend'].mean():.2f}")
                        with finance_col2:
                            st.metric("Median Spend", f"${df['MonthlySpend'].median():.2f}")
                        with finance_col3:
                            st.metric("Max Spend", f"${df['MonthlySpend'].max():.2f}")
            
        with tab2:
            # Only show content on this tab if the analyze button has been clicked
            # or if the session state already has a report generated
            
            if 'report_generated' not in st.session_state:
                st.session_state.report_generated = False
                
            if analyze_button:
                st.session_state.report_generated = True
                
            if st.session_state.report_generated:
                with st.spinner("🧠 AI analyzing your data... This may take a minute or two."):
                    try:
                        # Generate the streamlit report directly
                        generate_streamlit_report(df, graphs)
                    except Exception as e:
                        st.error(f"Error generating report: {e}")
            else:
                # Show instruction to generate a report
                st.markdown("""
                <div style="text-align: center; padding: 100px 2rem; background-color: #f8fafc; border-radius: 0.5rem; margin: 2rem 0;">
                    <img src="https://img.icons8.com/fluency/96/000000/business-report.png" style="width: 96px; height: 96px;">
                    <h2 style="margin-top: 1rem;">No Business Report Generated Yet</h2>
                    <p style="margin: 1rem 0; font-size: 1.1rem;">
                        Click the "Generate Business Report" button on the Data Exploration tab to create a 
                        comprehensive ShopMax Business Analyst Journal with AI-powered insights.
                    </p>
                </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
else:
    # Show an intro message when no file is uploaded
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background-color: #f8fafc; border-radius: 0.5rem; margin: 2rem 0;">
        <img src="https://img.icons8.com/fluency/96/000000/business-report.png" style="width: 96px; height: 96px;">
        <h2 style="margin-top: 1rem;">Data-Driven Business Analysis</h2>
        <p style="margin: 1rem 0; font-size: 1.1rem;">
            Upload your customer dataset to generate a comprehensive business analysis report with 
            visualizations, AI-powered insights, and strategic recommendations.
        </p>
        <p style="font-style: italic; color: #64748b;">Get started by uploading a CSV file above.</p>
    </div>
    """, unsafe_allow_html=True)