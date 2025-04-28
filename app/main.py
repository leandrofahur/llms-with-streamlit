import streamlit as st
import pandas as pd
from config import get_openai_api_key
from modules.crew_agents import generate_report
from modules.graph_generator import generate_graphs

# Load OpenAI API key:
openai_api_key = get_openai_api_key()

st.set_page_config(
    page_title="📋 Business Analyst ICP Journal",
    page_icon="🧠",
    layout="centered",
)

st.title("📋 Business Analyst ICP Journal")
st.write("Upload a CSV file and generate a report using AI agents!")

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
        st.dataframe(df)

        # Generate graphs:
        graphs = generate_graphs(df)
        # st.success("✅ Graphs generated successfully!")
        
        for title, fig in graphs.items():
            st.markdown(f"### 📊 {title}")
            st.pyplot(fig)

        # Button to trigger AI report
        if st.button("🔍 Analyze"):
            with st.spinner("AI agents are working... please wait 🚀"):
                try:
                    # Generate AI report:
                    final_report = generate_report(df)

                    # Display result:
                    st.success("✅ Report generated successfully!")
                    st.markdown("---")
                    st.markdown("### 📋 Final AI-Generated Report")
                    st.write(final_report)
                except Exception as e:
                    st.error(f"Error generating report: {e}")

    except Exception as e:
        st.error(f"Error reading CSV file: {e}")