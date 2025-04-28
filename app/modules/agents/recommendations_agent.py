from crewai import Agent
from config import get_llm

def create_recommendations_agent() -> Agent:
    """
    Create a recommendations agent.
    """
    return Agent(
        role="Data Strategist",
        goal="Propose actionable improvements and next steps based on the data insights.",
        backstory="A strategist who translates data into meaningful business actions and improvements.",
        allow_delegation=False,
        llm=get_llm()
    )