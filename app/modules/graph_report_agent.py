from langchain_openai import ChatOpenAI
from app.config import get_openai_api_key
from crewai import Agent, Task, Crew

def generate_graph_report(findings: dict) -> str:
    """
    Generate a full AI-powered Business Analyst Journal based on extracted findings.
    """

    # Initialize the LLM:
    openai_api_key = get_openai_api_key()
    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        model="gpt-4o"
    )

    # Prepare the findings text for the agent:
    findings_text = f"""
        📄 Plan Distribution:
        {findings.get("plan_distribution", {})}

        📄 Average Spend:
        ${findings.get("average_spend", "Unknown")}

        📄 Churn Rate:
        {findings.get("churn_rate", "Unknown")}

        📄 Average Tenure:
        {findings.get("average_tenure", "Unknown")} months

        📄 Top Countries:
        {', '.join(findings.get("top_countries", []))}

        📄 Top Industries:
        {', '.join(findings.get("top_industries", []))}

        📄 Signup Sources:
        {', '.join(findings.get("signup_sources", []))}
    """

    # Create the Agent:
    graph_report_agent = Agent(
        role="Business Analyst",
        goal="Analyze business data insights and generate a strategic professional report.",
        backstory=(
            "An experienced business intelligence analyst who specializes in interpreting "
            "subscription models, churn behaviors, customer demographics, and financial patterns, "
            "and translating them into actionable strategic insights."
        ),
        allow_delegation=False,
        llm=llm
    )

    # Define the Task:
    report_task = Task(
        description=f"""
            Using the following dataset insights:

            {findings_text}

            Write a professional Business Analyst Journal for ShopMax that includes:

            - Subscription Plans Insights
            - Financial Insights (Average Spend and Churn Rate)
            - Customer Tenure Insights
            - Geographic Distribution Insights
            - Signup Source Insights
            - Industry Distribution Insights
            - A Final Strategic Ideal Customer Profile (ICP) Summary:
                - Ideal country
                - Ideal plan
                - Ideal industry
                - Spending behavior
                - Strategic recommendations

            The writing should be formal, structured, and bullet-pointed when appropriate. Use a clear, professional tone.
        """,
        expected_output="A structured business analysis text covering all the requested sections, suitable for C-Level review.",
        agent=graph_report_agent
    )

    # Create a Crew to run the task (even if single-agent)
    crew = Crew(
        agents=[graph_report_agent],
        tasks=[report_task]
    )

    # 6. Run the task
    final_report = crew.kickoff()

    return final_report
