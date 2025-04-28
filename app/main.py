import streamlit as st
import pandas as pd
from config import get_openai_api_key
from modules.graph_generator import generate_graphs
from modules.report_generator import generate_markdown_report
import os

# Create static directory for images if it doesn't exist
os.makedirs('app/static/images', exist_ok=True)

# Load OpenAI API key:
openai_api_key = get_openai_api_key()

st.set_page_config(
    page_title="📋 Business Analyst ICP Journal",
    page_icon="🧠",
    layout="wide",  # Changed to wide layout for better graph display
)

st.title("📋 Business Analyst ICP Journal")
st.write("Upload a CSV file and generate a report with visualizations using AI agents!")

# File Uploader (only CSV files are supported)
uploaded_file = st.file_uploader("Upload your CSV file here", type=["csv"])

if uploaded_file is not None:
    try:
        # Read CSV into DataFrame:
        df = pd.read_csv(uploaded_file)

        # TODO: In the future, we should use create a normalized schema for the data.
        #  Manually rename columns:        
        df.rename(columns={
            'Monthly Spend ($)': 'MonthlySpend',
            'Tenure (Months)': 'Tenure',
            'Churned': 'Churn'
        }, inplace=True)

        st.success("✅ File uploaded successfully!")
        
        # Two columns for layout
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("### 📊 Dataset Preview")
            st.dataframe(df.head(10))
            
            # Display dataset statistics
            st.markdown("### 📈 Dataset Stats")
            st.write(f"Rows: {df.shape[0]}")
            st.write(f"Columns: {df.shape[1]}")
            
            # Button to trigger analysis
            analyze_button = st.button("🔍 Analyze Data", type="primary")
        
        with col2:
            # Generate graphs immediately:
            with st.spinner("Generating visualizations..."):
                graphs = generate_graphs(df)
                
            tabs = st.tabs(["Distribution", "Customer Behavior", "Financial"])
            
            with tabs[0]:
                if 'Plan Distribution' in graphs:
                    st.pyplot(graphs['Plan Distribution'])
                if 'Top 10 Industries' in graphs:
                    st.pyplot(graphs['Top 10 Industries'])
            
            with tabs[1]:
                if 'Churn Rate' in graphs:
                    st.pyplot(graphs['Churn Rate'])
                if 'Spend vs Tenure' in graphs:
                    st.pyplot(graphs['Spend vs Tenure'])
            
            with tabs[2]:
                if 'Monthly Spend Distribution' in graphs:
                    st.pyplot(graphs['Monthly Spend Distribution'])
                if 'Tenure Distribution' in graphs:
                    st.pyplot(graphs['Tenure Distribution'])
        
        # If analyze button is clicked, generate the full report
        if analyze_button:
            with st.spinner("AI agents are working... please wait 🚀"):
                try:
                    # Generate markdown report with embedded graphs
                    markdown_report = generate_markdown_report(df, graphs)

                    # Display result using markdown with HTML enabled
                    st.markdown("---")
                    st.markdown("## 📋 Enhanced Business Analysis Report")
                    st.markdown(markdown_report, unsafe_allow_html=True)
                    
                    # Add download button for the report
                    st.download_button(
                        label="📥 Download Report",
                        data=markdown_report,
                        file_name="business_analysis_report.html",
                        mime="text/html"
                    )
                except Exception as e:
                    st.error(f"Error generating report: {e}")

    except Exception as e:
        st.error(f"Error reading CSV file: {e}")