# ShopMax Business Analyst Journal

A Streamlit application that analyzes customer data to generate professional business reports with visualizations and insights.

## Features

- Upload CSV data files for analysis
- Automatically generate professional visualizations
- Create a Business Analyst Journal with insights and recommendations
- Export reports as HTML files

## How to Use

1. Upload your customer dataset (CSV format)
2. Explore the data visualizations in the Data Exploration tab
3. Generate a comprehensive Business Analyst Journal with the "Generate Business Report" button
4. Export the report as HTML for sharing

## Example Dataset Format

Your CSV file should include some of these columns (not all are required):
- Plan: Subscription plan (e.g., Basic, Pro, Enterprise)
- MonthlySpend: Monthly spending amount
- Tenure: Customer tenure in months
- Churn: Boolean indicating if customer has churned
- Industry: Customer's industry

## Development

### Requirements

To run this application locally:

```bash
pip install -r requirements.txt
streamlit run app/main.py
```

### Project Structure

- `app/`: Main application code
  - `main.py`: Streamlit application entry point
  - `config.py`: Configuration settings
  - `modules/`: Application modules
    - `graph_generator.py`: Visualization generation
    - `report_generator.py`: Report generation

## Links

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Matplotlib Documentation](https://matplotlib.org/)