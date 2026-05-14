from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
import os

from utils_factory import create_llm, create_mcp_adapter
from shared.models import QueryInterpretation

@CrewBase
class ResultInterpreterCrew:
    """
    Result Interpreter crew for translating query results into business insights.
    
    This crew translates technical query outputs into business-friendly
    insights and recommendations, making data accessible to non-technical users.
    """

    agents_config = "configs/result_interpreter/agents.yaml"
    tasks_config = "configs/result_interpreter/tasks.yaml"

    def __init__(self, llm=None, mcp_adapter=None, max_crew_rpm=2):
        """
        Initialize the Result Interpreter Crew.

        Args:
            llm: Optional custom LLM instance.
            mcp_adapter: Optional MCP adapter for database tools.
        """
        load_dotenv(override=True)
        
        self.default_llm = create_llm(llm)
        self.mcp_adapter = create_mcp_adapter(mcp_adapter)
        self.max_crew_rpm = max_crew_rpm

    @agent
    def result_interpreter_agent(self) -> Agent:
        """
        Agent responsible for interpreting query results for business stakeholders.
        Filtered tools: row counting for context.
        """
        # Filter tools for result interpretation
        allowed_tools = [
            "run_sql_query",  # Required for executing SQL
            "count_rows",     # Optional for verification
        ]
        filtered_tools = [
            tool for tool in self.mcp_adapter.tools if tool.name in allowed_tools
        ]
        
        return Agent(
            config=self.agents_config["result_interpreter_agent"],
            tools=filtered_tools,
            verbose=True,
            memory=False,
            llm=self.default_llm,
        )

    @task
    def interpret_task(self) -> Task:
        """
        Task for interpreting query results into business insights.
        """
        return Task(
            config=self.tasks_config["interpret_task"],
            agent=self.result_interpreter_agent(),
            output_pydantic=QueryInterpretation,
        )

    @crew
    def crew(self) -> Crew:
        """
        Creates the Result Interpreter crew.

        Returns:
            Crew: Configured crew ready for result interpretation
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            max_rpm=self.max_crew_rpm,
        )
