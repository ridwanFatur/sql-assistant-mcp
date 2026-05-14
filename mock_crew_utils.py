from dataclasses import dataclass

@dataclass
class TokenUsage:
    total_tokens: int
    prompt_tokens: int
    cached_prompt_tokens: int
    completion_tokens: int
    successful_requests: int


class MockCrewResult:
    def __init__(self, token_usage: TokenUsage):
        self.token_usage = token_usage

    def __str__(self):
        return "Mock Crew Result"
    

def run_sql_generation(sql_generation_crew, user_input, previous_attempts):
    usage = TokenUsage(
        total_tokens=8465,
        prompt_tokens=6280,
        cached_prompt_tokens=0,
        completion_tokens=2185,
        successful_requests=4
    )
    
    result = MockCrewResult(token_usage=usage)
    return result

def post_sql_generation(generation_result):
    return "Mock post_sql_generation"

def run_compliance_checker(compliance_checker_crew, reviewed_sql):
    usage = TokenUsage(
        total_tokens=8465,
        prompt_tokens=6280,
        cached_prompt_tokens=0,
        completion_tokens=2185,
        successful_requests=4
    )
    
    result = MockCrewResult(token_usage=usage)
    return result

def post_compliance_checker(compliance_result):
    return "verdict: pass"

def run_result_interpretation(result_interpreter_crew, user_input, reviewed_sql, query_result):
    usage = TokenUsage(
        total_tokens=8465,
        prompt_tokens=6280,
        cached_prompt_tokens=0,
        completion_tokens=2185,
        successful_requests=4
    )
    
    result = MockCrewResult(token_usage=usage)
    return result

def post_result_interpretation(interpretation_result):
    return "verdict: pass"