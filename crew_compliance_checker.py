from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
import os

from shared.models import ComplianceReport
from utils_factory import create_llm, create_mcp_adapter


@CrewBase
class ComplianceCheckerCrew:
    """
    Compliance Checker crew for ensuring SQL queries meet security standards.
    
    This crew acts as a data governance officer, checking for potential
    security vulnerabilities, PII exposure, and policy violations.
    """

    agents_config = "configs/compliance_checker/agents.yaml"
    tasks_config = "configs/compliance_checker/tasks.yaml"

    def __init__(self, llm=None, mcp_adapter=None, max_crew_rpm=2):
        """
        Initialize the Compliance Checker Crew.

        Args:
            llm: Optional custom LLM instance.
            mcp_adapter: Optional MCP adapter for database tools.
        """
        load_dotenv(override=True)
        self.default_llm = create_llm(llm)
        self.mcp_adapter = create_mcp_adapter(mcp_adapter)
        self.max_crew_rpm = max_crew_rpm

    @agent
    def compliance_checker_agent(self) -> Agent:
        """
        Agent responsible for ensuring SQL queries meet security and compliance standards.
        Filtered tools: schema verification and table existence checking.
        """
        # Filter tools for compliance checking
        allowed_tools = [
            "get_database_schema",
            "check_table_exists",
        ]
        filtered_tools = [
            tool for tool in self.mcp_adapter.tools if tool.name in allowed_tools
        ]
        
        return Agent(
            config=self.agents_config["compliance_checker_agent"],
            tools=filtered_tools,
            verbose=True,
            memory=False,
            llm=self.default_llm,
        )

    @task
    def compliance_task(self) -> Task:
        """
        Task for checking query compliance with security and governance policies.
        """
        return Task(
            config=self.tasks_config["compliance_task"],
            agent=self.compliance_checker_agent(),
            output_pydantic=ComplianceReport,
        )

    @crew
    def crew(self) -> Crew:
        """
        Creates the Compliance Checker crew.

        Returns:
            Crew: Configured crew ready for compliance checking
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            max_rpm=self.max_crew_rpm,
        )
