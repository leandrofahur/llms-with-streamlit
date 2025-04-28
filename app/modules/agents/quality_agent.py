from crewai import Agent
from config import get_llm

def create_quality_agent() -> Agent:
    """
    Create a quality agent.
    """
    return Agent(
        role="Data Quality Auditor",
        goal="Identify missing values, inconsistencies, and potential data quality issues.",
        backstory="Expert at ensuring data integrity and validation for business reliability.",
        allow_delegation=False,
        llm=get_llm()
    )
