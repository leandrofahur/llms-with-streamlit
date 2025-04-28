from crewai import Agent
from config import get_llm

def create_insights_agent() -> Agent:
    """
    Create an insights agent.
    """
    return Agent(
        role="Data Insights Analyst",
        goal="Discover key patterns and insights from the dataset.",
        backstory="An experienced data analyst specializing in uncovering trends and business patterns.",
        allow_delegation=False,
        llm= get_llm()
    )