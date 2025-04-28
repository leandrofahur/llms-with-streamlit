from crewai import Crew, Agent, Task
from config import get_llm
from modules.agents.insights_agent import create_insights_agent
from modules.agents.quality_agent import create_quality_agent
from modules.agents.recommendations_agent import create_recommendations_agent
import pandas as pd

def generate_report(df: pd.DataFrame) -> str:
    """    
    This function orchestrates the creation of agents, tasks, and a crew to analyze a dataset and generate a report.

    Args:
        df (pd.DataFrame): The input DataFrame to analyze.

    Returns:
        str: The generated report.
    """
    
    # Check if the DataFrame is empty or too large:
    if len(df) == 0:
        return "No data to analyze."
    elif len(df) > 50:
        df_sample = df.sample(50, random_state=42)
    else:
        df_sample = df

    # Convert the DataFrame to a string:
    table_string = df_sample.to_csv(index=False)

    # Create the agents:
    insights_agent = create_insights_agent()
    quality_agent = create_quality_agent()
    recommendations_agent = create_recommendations_agent()

    # Create the tasks:
    insights_task = Task(        
        description=f"""Analyze the following customer dataset and find key patterns, trends, and interesting insights: {table_string}""",
        expected_output="A list of key patterns, trends, and interesting insights discovered in the dataset.",
        agent=insights_agent        
    )

    quality_task = Task(
        description=f"""Audit the following customer dataset and identify any data quality issues like missing values, duplicates, or inconsistencies: {table_string}""",
        expected_output="A list of detected data quality issues, missing fields, duplicates, or inconsistencies found in the dataset.",
        agent=quality_agent
    )

    recommendations_task = Task(
        description=f"""Based on the customer dataset, suggest improvements, optimizations, and next actionable steps for better business decisions: {table_string}""",
        expected_output="A list of suggested business improvements and next actionable steps based on the dataset analysis.",
        agent=recommendations_agent
    )

    # Create the crew:
    crew = Crew(
        agents=[insights_agent, quality_agent, recommendations_agent],
        tasks=[insights_task, quality_task, recommendations_task],
        llm=get_llm()
    )
    
    final_report = crew.kickoff()
    
    return final_report.raw
