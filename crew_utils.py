from crewai import Crew, Task
from utils_db_helper import clean_sql_query

def run_sql_generation(sql_generation_crew, user_input, previous_attempts):
    sql_input = {"user_input": user_input}
    
    if previous_attempts:
        # Add context about previous failed attempts
        context_info = "\n\nPrevious failed attempts:\n"
        for i, prev in enumerate(previous_attempts, 1):
            context_info += f"\nAttempt {i}:\n"
            context_info += f"SQL: {prev['sql'][:200]}\n"
            context_info += f"Compliance Issue: {prev['compliance_report'][:300]}\n"
        sql_input["previous_attempts_context"] = context_info   
    else:
        sql_input["previous_attempts_context"] = ""    
    generation_result = sql_generation_crew.crew().kickoff(
        inputs=sql_input
    )
    
    return generation_result

def post_sql_generation(generation_result):
    if hasattr(generation_result, 'pydantic') and generation_result.pydantic:
        return clean_sql_query(generation_result.pydantic.reviewed_sqlquery)
    else:
        return clean_sql_query(generation_result.raw if hasattr(generation_result, 'raw') else str(generation_result))

def run_compliance_checker(compliance_checker_crew, reviewed_sql):
    compliance_task = Task(
        description=f"""
        Check this SQL query for compliance and security issues: {reviewed_sql}
        Report any potential PII exposure or dangerous operations.
        """,
        agent=compliance_checker_crew.compliance_checker_agent(),
        expected_output="A compliance report with clear verdict",
    )
    compliance_crew = Crew(
        agents=[compliance_checker_crew.compliance_checker_agent()],
        tasks=[compliance_task],
    )
    compliance_result = compliance_crew.kickoff()
    return compliance_result

def post_compliance_checker(compliance_result):
    compliance_report = str(compliance_result).strip()
    return compliance_report

def run_result_interpretation(result_interpreter_crew, user_input, reviewed_sql, query_result):
    interpretation_task = Task(
        description=f"""
        Interpret these SQL query results for business users:
        
        Original Request: {user_input}
        SQL Query: {reviewed_sql}
        Query Results: {query_result}
        
        Provide a business-friendly interpretation with insights and recommendations.
        """,
        agent=result_interpreter_crew.result_interpreter_agent(),
        expected_output="A comprehensive business interpretation of the query results",
    )
    interpretation_crew = Crew(
        agents=[result_interpreter_crew.result_interpreter_agent()],
        tasks=[interpretation_task],
    )
    interpretation_result = interpretation_crew.kickoff()
    return interpretation_result

def post_result_interpretation(interpretation_result):
    business_interpretation = str(interpretation_result).strip()
    return business_interpretation