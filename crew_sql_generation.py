from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
import os

from utils_factory import create_llm, create_mcp_adapter
from shared.models import ReviewedSQLQuery, SQLQuery

@CrewBase
class SQLGenerationCrew:
    """
    SQL Generation crew for creating and validating SQL queries.
    
    This crew combines SQL generation and review in a single workflow,
    with two specialized agents working sequentially to produce validated SQL.
    """

    agents_config = "configs/sql_generation/agents.yaml"
    tasks_config = "configs/sql_generation/tasks.yaml"

    def __init__(self, llm=None, mcp_adapter=None, max_crew_rpm=2):
        """
        Initialize the SQL Generation Crew.

        Args:
            llm: Optional custom LLM instance.
            mcp_adapter: Optional MCP adapter for database tools.
        """
        load_dotenv(override=True)
        self.default_llm = create_llm(llm)
        self.mcp_adapter = create_mcp_adapter(mcp_adapter)
        self.max_crew_rpm = max_crew_rpm

    @agent
    def sql_generator_agent(self) -> Agent:
        """
        Agent responsible for converting natural language requests into SQL queries.
        Filtered tools: schema exploration and data sampling only.
        """
        # Filter tools for SQL Generator - needs schema exploration
        allowed_tools = [
            "get_database_schema",
            "get_table_sample",
            "get_column_stats",
            "list_tables",
        ]
        filtered_tools = [
            tool for tool in self.mcp_adapter.tools if tool.name in allowed_tools
        ]
        
        return Agent(
            config=self.agents_config["sql_generator_agent"],
            tools=filtered_tools,
            verbose=True,
            memory=False,
            llm=self.default_llm,
        )

    @agent
    def sql_reviewer_agent(self) -> Agent:
        """
        Agent responsible for reviewing and optimizing generated SQL queries.
        Filtered tools: syntax validation and schema verification only.
        """
        # Filter tools for SQL Reviewer - needs validation and schema
        allowed_tools = [
            "validate_sql_syntax",
            "get_database_schema",
            "check_table_exists",
        ]
        filtered_tools = [
            tool for tool in self.mcp_adapter.tools if tool.name in allowed_tools
        ]
        
        return Agent(
            config=self.agents_config["sql_reviewer_agent"],
            tools=filtered_tools,
            verbose=True,
            memory=False,
            llm=self.default_llm,
        )

    @task
    def generate_sql_task(self) -> Task:
        """
        Task for generating SQL queries from natural language input.
        """
        return Task(
            config=self.tasks_config["generate_sql_task"],
            agent=self.sql_generator_agent(),
            output_pydantic=SQLQuery,
        )

    @task
    def review_sql_task(self) -> Task:
        """
        Task for reviewing and optimizing generated SQL queries.
        """
        return Task(
            config=self.tasks_config["review_sql_task"],
            agent=self.sql_reviewer_agent(),
            context=[self.generate_sql_task()],
            output_pydantic=ReviewedSQLQuery,
        )

    @crew
    def crew(self) -> Crew:
        """
        Creates the SQL Generation crew with both generator and reviewer agents.

        Returns:
            Crew: Configured crew ready for SQL generation and review
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            max_rpm=self.max_crew_rpm,
        )
