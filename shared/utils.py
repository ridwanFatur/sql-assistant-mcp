import os
import json
from pathlib import Path
import time
import socket

class Colors:
    """Terminal colors for better output"""

    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"
    
def print_colored(text, color):
    """Print colored text"""
    print(f"{color}{text}{Colors.END}")
    
def find_test_cases(test_cases_dir):
    """Find all valid test cases in the test_cases directory"""
    test_cases = []

    if not os.path.exists(test_cases_dir):
        print_colored(
            f"❌ Test cases directory not found: {test_cases_dir}", Colors.RED
        )
        return []

    for item in os.listdir(test_cases_dir):
        case_path = os.path.join(test_cases_dir, item)

        # Skip if not a directory
        if not os.path.isdir(case_path):
            continue

        # Check for required files
        db_path = os.path.join(case_path, "database.sqlite")
        questions_path = os.path.join(case_path, "questions.json")

        if os.path.exists(db_path) and os.path.exists(questions_path):
            # Load questions to get count
            try:
                with open(questions_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if isinstance(data, dict) and "questions" in data:
                    questions = data["questions"]
                    question_count = len(questions)
                    description = data.get("description", "")
                elif isinstance(data, list):
                    question_count = len(data)
                    description = ""
                else:
                    continue

                test_cases.append(
                    {
                        "name": item,
                        "path": case_path,
                        "database": db_path,
                        "questions_file": questions_path,
                        "question_count": question_count,
                        "description": description,
                    }
                )
            except Exception as e:
                print_colored(
                    f"⚠️  Warning: Failed to load {questions_path}: {e}", Colors.YELLOW
                )

    # Sort test cases by name (numeric order)
    test_cases.sort(key=lambda x: int(x["name"]) if x["name"].isdigit() else x["name"])

    return test_cases

def wait_for_port(host: str, port: int, timeout: float = 30.0) -> None:
    """
    Wait for TCP port to be open or timeout.

    Args:
        host: Host to connect to
        port: Port to check
        timeout: Maximum time to wait in seconds

    Raises:
        TimeoutError: If port is not available within timeout
    """
    start = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return  # Port is open
        except OSError:
            if time.time() - start > timeout:
                raise TimeoutError(f"Timeout waiting for {host}:{port}")
            time.sleep(0.2)
           

