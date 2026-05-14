from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, Process, LLM
import os
from langchain_openai import ChatOpenAI
from crewai_tools import MCPServerAdapter
from dotenv import load_dotenv
# from langchain_groq import ChatGroq
import sys
import os
from pathlib import Path
from typing import Optional
import json
import argparse
import datetime
import time
import os
from crewai import LLM
from langchain_openai import ChatOpenAI

from crew_compliance_checker import ComplianceCheckerCrew
from crew_result_interpreter import ResultInterpreterCrew
from crew_sql_generation import SQLGenerationCrew

from langfuse import Langfuse, get_client
from openinference.instrumentation.crewai import CrewAIInstrumentor
from openinference.instrumentation.litellm import LiteLLMInstrumentor
from scoring import add_score_to_result
from test_utils import list_test_case_folders, get_test_case_by_name, run_mcp_server, update_env_db_path, load_questions_from_json, save_execution_info
from utils_db_helper import set_database_path, clean_sql_query, run_query
from crew_utils import run_sql_generation, post_sql_generation, run_compliance_checker, post_compliance_checker, run_result_interpretation, post_result_interpretation

load_dotenv()

# Set Langfuse
langfuse = Langfuse(
    secret_key=os.environ.get("LANGFUSE_SECRET_KEY"),
    public_key=os.environ.get("LANGFUSE_PUBLIC_KEY"),
    host=os.environ.get("LANGFUSE_HOST", "http://localhost:3000"),
)

CrewAIInstrumentor().instrument(skip_dep_check=True)
LiteLLMInstrumentor().instrument()

# Setup Model
model_ids = [
    "groq/compound",
    "groq/compound-mini",
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "meta-llama/llama-prompt-guard-2-22m",
    "meta-llama/llama-prompt-guard-2-86m",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "openai/gpt-oss-safeguard-20b",
    "qwen/qwen3-32b",
]

model_id = model_ids[-1]
print(f"Selected Model: {model_id}")

llm = ChatOpenAI(
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key=os.environ.get("GROQ_API_KEY"),
    temperature=0,
    model_name=f"groq/{model_id}",
    top_p=1,
    max_retries=3,
    request_timeout=60,
)
    
def run_complete_workflow(
    db_path, 
    user_input, 
    sql_generation_crew,
    compliance_checker_crew,
    result_interpreter_crew,
    result_folder=None, 
    question_metadata=None,
):
    log_messages = []
    trace_id = None
    max_crew_retries = 2
    retry_count = 0
    workflow_result = None
    max_business_retries = 2 
    
    raw_sql = ""
    reviewed_sql = ""
    compliance_report = ""
    query_result = ""
    business_interpretation = ""  

    # START-TIME
    start_time = datetime.datetime.now()

    log_messages.append(f"Using database: {db_path}")
    log_messages.append(f"User input: {user_input}")    
    try:
        with langfuse.start_as_current_span(name="sql_assistant_workflow") as span:
            trace_id = span.trace_id
            span.update(metadata={
                "user_input": user_input[:100],
                "max_crew_retries": max_crew_retries,
            })    
            while retry_count <= max_crew_retries and workflow_result is None:
                try:
                    orchestrator_suffix = f" (retry {retry_count})" if retry_count > 0 else "" 
                    with langfuse.start_as_current_span(name=f"crew_execution{orchestrator_suffix}") as execution_span:
                        print(f"[Orchestrator] Execution attempt {retry_count + 1}/{max_crew_retries + 1}")
                        execution_span.update(metadata={
                            "orchestrator_attempt": retry_count + 1,
                            "is_orchestrator_retry": retry_count > 0
                        })   
                        business_retry_count = 0
                        previous_attempts = []
                        compliance_passed = False  

                        while business_retry_count <= max_business_retries:
                            attempt_num = business_retry_count + 1
                            business_suffix = f" (business_retry {business_retry_count})" if business_retry_count > 0 else ""
                            
                            print(f"[Business Logic] Attempt {attempt_num}/{max_business_retries + 1}") 
                            # Step 1-2: Generate and Review SQL
                            with langfuse.start_as_current_span(name=f"generate_sql{business_suffix}") as sql_span:
                                try:
                                    log_messages.append(f"Step 1-2 (Attempt {attempt_num}): Generating and reviewing SQL query...")
                                    if previous_attempts:
                                        log_messages.append(f"Including context from {len(previous_attempts)} previous attempt(s)")
                                        
                                    generation_result = run_sql_generation(sql_generation_crew, user_input, previous_attempts)
                                    reviewed_sql = post_sql_generation(generation_result)
                                    
                                    log_messages.append(f"Generated & Reviewed SQL: {reviewed_sql}")
                                    sql_span.update(metadata={
                                        "sql_query": reviewed_sql[:200],
                                        "has_context": len(previous_attempts) > 0,
                                        "business_attempt": attempt_num,
                                        "completed": True
                                    })
                                except Exception as span_error:
                                    sql_span.update(metadata={
                                        "error": str(span_error),
                                        "error_type": type(span_error).__name__,
                                        "completed": False
                                    })
                                    print(f"[Langfuse] SQL generation span error: {span_error}")
                                    raise  
                                    
                            # Step 2: Compliance Check
                            with langfuse.start_as_current_span(name=f"check_compliance{business_suffix}") as compliance_span:        
                                try:
                                    log_messages.append("Step 2: Compliance check...")
                                    
                                    compliance_result = run_compliance_checker(compliance_checker_crew, reviewed_sql)
                                    compliance_report = post_compliance_checker(compliance_result)
                                    
                                    log_messages.append(f"Compliance report: {compliance_report}")
                                    compliance_passed = "verdict: pass" in compliance_report.lower()
                                    compliance_span.update(metadata={
                                        "approved": compliance_passed,
                                        "business_attempt": attempt_num,
                                        "completed": True
                                    })
                                except Exception as span_error:
                                    compliance_span.update(metadata={
                                        "error": str(span_error),
                                        "error_type": type(span_error).__name__,
                                        "completed": False
                                    })
                                    print(f"[Langfuse] Compliance check span error: {span_error}")
                                    raise  
                                                              
                            # Step 3: Execute SQL query (only if compliance passed)
                            log_messages.append("Step 3: Executing SQL query...")
                            if compliance_passed:
                                query_result = run_query(reviewed_sql, db_path)
                                log_messages.append(f"Query result:\n{query_result}")
                                
                                # Step 4: Interpret query results
                                with langfuse.start_as_current_span(name="interpret_results") as interpret_span:
                                    try:
                                        log_messages.append("Step 4: Interpreting query results...")
                                        
                                        interpretation_result = run_result_interpretation(
                                            result_interpreter_crew, 
                                            user_input, 
                                            reviewed_sql, 
                                            query_result
                                        )
                                        business_interpretation = post_result_interpretation(interpretation_result) 
                                        
                                        log_messages.append(
                                            f"Business interpretation:\n{business_interpretation}"
                                        )
                                        
                                        interpret_span.update(metadata={
                                            "interpretation_length": len(business_interpretation),
                                            "completed": True
                                        })                                        
                                    except Exception as span_error:
                                        interpret_span.update(metadata={
                                            "error": str(span_error),
                                            "error_type": type(span_error).__name__,
                                            "completed": False
                                        })
                                        print(f"[Langfuse] Result interpretation span error: {span_error}")
                                        raise                                    
                            else:
                                # Compliance failed after all retries
                                log_messages.append(
                                    f"❌ SQL query failed compliance check after {business_retry_count + 1} attempts."
                                )
                                query_result = f"Query not executed due to compliance issues after {business_retry_count + 1} attempts"
                                business_interpretation = "Interpretation not available, query was not executed"                               
                                
                                
                        execution_span.update(metadata={
                            "business_retry_count": business_retry_count,
                            "total_business_attempts": business_retry_count + 1,
                            "compliance_passed": compliance_passed,
                            "compliance_failures": len(previous_attempts)
                        })
                        
                        workflow_result = True
                        print(f"[Orchestrator] Execution attempt {retry_count + 1} completed")                        
                except Exception as crew_error:
                    retry_count += 1
                    error_msg = str(crew_error)
                    print(f"[Orchestrator] Execution attempt {retry_count} failed with exception: {error_msg}")
                    log_messages.append(f"Orchestrator attempt {retry_count} failed: {error_msg}")
                    
                    # Orchestrator-level retry
                    if retry_count <= max_crew_retries:
                        print(f"[Orchestrator] Retrying... (attempt {retry_count + 1}/{max_crew_retries + 1})")
                        # Reset all state for fresh attempt
                        raw_sql = ""
                        reviewed_sql = ""
                        compliance_report = ""
                        query_result = ""
                        business_interpretation = ""
                    else:
                        print(f"[Orchestrator] Max retries ({max_crew_retries}) reached. Giving up.")
                        raise crew_error
                span.update(metadata={
                    "completed": True,
                    "orchestrator_retry_count": retry_count,
                    "total_orchestrator_attempts": retry_count + 1,
                })                
    except Exception as span_error:
        print(f"[Langfuse] Failed to create span: {span_error}")
        raise   

    # Flush
    try:
        langfuse.flush()
        print("[Langfuse] Trace data flushed successfully")
    except Exception as flush_error:
        print(f"[Langfuse] Failed to flush trace: {flush_error}")    

    # END-TIME
    end_time = datetime.datetime.now()

    # Prepare result data
    result_data = {
        "user_input": user_input,
        "raw_sql": raw_sql,
        "reviewed_sql": reviewed_sql,
        "compliance_report": compliance_report,
        "query_result": query_result,
        "business_interpretation": business_interpretation,
        "database_path": db_path,
        "execution_time": end_time.isoformat(),
        "trace_id": trace_id if trace_id else "No trace ID available",
        "orchestrator_retry_count": retry_count,
        "total_orchestrator_attempts": retry_count + 1,
        "retry_info": "No orchestrator retries needed" if retry_count == 0 else f"Succeeded after {retry_count} orchestrator retry(s)",
    }

    # Add question metadata if provided
    if question_metadata:
        result_data["difficulty"] = question_metadata.get("difficulty", "Unknown")
        result_data["category"] = question_metadata.get("category", "Unknown")

    # Calculate and add score
    if add_score_to_result:
        try:
            result_data = add_score_to_result(result_data)
        except Exception as e:
            # If scoring fails, add error info but continue
            result_data["score"] = {
                "error": f"Scoring failed: {str(e)}",
                "total_score": 0,
                "grade": "N/A"
            }  
              
    return start_time, end_time, result_data, trace_id, retry_count


def main():
    run_mcp_server()
    cases = list_test_case_folders()
    cases = sorted(cases, key=lambda x: x["name"])
    
    # Set Crews
    sql_generation_crew = SQLGenerationCrew(llm=llm, max_crew_rpm=1)
    compliance_checker_crew = ComplianceCheckerCrew(llm=llm, max_crew_rpm=1)
    result_interpreter_crew = ResultInterpreterCrew(llm=llm, max_crew_rpm=1)
    
    for case in cases:
        test_case_name = case['name']
        test_case = get_test_case_by_name(test_case_name)
    
        db_path = test_case["database"]
        questions_file = test_case["questions"]
    
        set_database_path(db_path)
        update_env_db_path(db_path) 
    
        question_data = load_questions_from_json(questions_file, 0)
        
        user_input = question_data.get("question", str(question_data))
        question_meta = {
            "difficulty": question_data.get("difficulty", "Unknown"),
            "category": question_data.get("category", "Unknown"),
        } 
        start_time, end_time, result_data, trace_id, retry_count = run_complete_workflow(
			db_path=db_path, 
			user_input=user_input, 
    		sql_generation_crew=sql_generation_crew,
    		compliance_checker_crew=compliance_checker_crew,
    		result_interpreter_crew=result_interpreter_crew,   
			result_folder=None, 
			question_metadata=question_meta
		)
        
        # Save Execution
        folder_name = datetime.datetime.now().strftime("%d-%m-%Y %H-%M")
        result_folder = Path(folder_name)
        save_execution_info(
			result_folder, 
   			start_time, 
      		end_time, 
        	result_data, 
         	trace_id=trace_id, 
         	retry_count=retry_count
		)
        	
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

