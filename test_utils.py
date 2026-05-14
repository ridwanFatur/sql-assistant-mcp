import json
import os
import subprocess
from pathlib import Path
import time

from shared.utils import Colors, print_colored, wait_for_port

def run_mcp_server():
    project_root = Path(__file__).parent
    
    # Parse host from MCP_SERVER_URL or use default
    mcp_url = os.environ.get("MCP_SERVER_URL", "http://127.0.0.1:8150/sse")
    try:
        # Extract host from URL (e.g., http://127.0.0.1:8150/sse -> 127.0.0.1)
        if "://" in mcp_url:
            host_part = mcp_url.split("://")[1].split("/")[0]
            host = host_part.split(":")[0]
        else:
            host = "127.0.0.1"
    except Exception:
        host = "127.0.0.1"
    
    # Build MCP server command (let server auto-detect port)
    # Use uv run to ensure correct Python environment with all dependencies
    server_cmd = [
        "uv",
        "run",
        "python",
        "mcp_server.py",
        "--host",
        host,
    ]
    
    # If environment specifies port, use it
    if "MCP_PORT" in os.environ:
        port = int(os.environ["MCP_PORT"])
        server_cmd.extend(["--port", str(port)])
        print_colored(f"📌 Using port from environment: {port}", Colors.BLUE)
    
    # Start MCP server (inherit stdout/stderr for real-time output)
    print_colored(
        f"\n🚀 Starting MCP server: {' '.join(server_cmd)}", Colors.HEADER
    )
    print_colored("=" * 80, Colors.CYAN)
    try:
        server_proc = subprocess.Popen(
            server_cmd,
            cwd=str(project_root),
            # stdout/stderr not redirected - will print in real-time
        )
    except Exception as e:
        print_colored(f"\n❌ Failed to start MCP server: {e}", Colors.RED)
        return 1
    
    try:
        # Wait for server to start and update .env
        print_colored(f"⏳ Waiting for MCP server to start...", Colors.YELLOW)
        time.sleep(24)  # Give server time to start and write .env
    
        # Detect actual port from .env file
        actual_port = 8150  # Default port
        env_file = project_root / ".env"
    
        if env_file.exists():
            try:
                with open(env_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip().startswith("MCP_SERVER_URL="):
                            updated_url = line.strip().split("=", 1)[1].strip('"')
                            if (
                                "://" in updated_url
                                and ":" in updated_url.split("://")[1]
                            ):
                                try:
                                    url_parts = updated_url.split("://")[1].split(
                                        "/"
                                    )
                                    host_port = url_parts[0]
                                    if ":" in host_port:
                                        actual_port = int(host_port.split(":")[1])
                                        print_colored(
                                            f"📝 Detected MCP server port from .env: {actual_port}",
                                            Colors.GREEN,
                                        )
                                except (ValueError, IndexError):
                                    print_colored(
                                        f"⚠️  Could not parse port from URL: {updated_url}",
                                        Colors.YELLOW,
                                    )
                            break
            except Exception as e:
                print_colored(f"⚠️  Could not read .env file: {e}", Colors.YELLOW)
        else:
            print_colored(
                f"⚠️  .env file not found, using default port: {actual_port}",
                Colors.YELLOW,
            )
    
        # Wait for port to be ready
        print_colored("=" * 80, Colors.CYAN)
        print_colored(
            f"⏳ Waiting for MCP server to be ready at {host}:{actual_port}...",
            Colors.YELLOW,
        )
        wait_for_port(host, actual_port, timeout=30)
        print_colored(
            f"✅ MCP server is ready at http://{host}:{actual_port}", Colors.GREEN
        )
    
        # Update environment variable for consistency
        os.environ["MCP_SERVER_URL"] = f"http://{host}:{actual_port}/sse"
        print_colored(
            f"🔗 Using MCP server URL: {os.environ['MCP_SERVER_URL']}", Colors.CYAN
        )
        print_colored("=" * 80 + "\n", Colors.CYAN)
    
    except TimeoutError as e:
        print_colored(f"❌ {e}", Colors.RED)
        if server_proc and server_proc.poll() is None:
            server_proc.terminate()
        return 1
    except Exception as e:
        print_colored(f"❌ Error during MCP server startup: {e}", Colors.RED)
        if server_proc and server_proc.poll() is None:
            server_proc.terminate()
        return 1    
    
def update_env_db_path(db_path: str):
    """
    Update .env file with database path for MCP server cross-process access.

    This allows MCP server running in a separate terminal to access the
    database path set by the main application.
    """
    try:
        # Find project root
        project_root = Path(__file__).parent
        env_file = project_root / ".env"

        # Convert to absolute path
        if not os.path.isabs(db_path):
            db_path = os.path.abspath(db_path)

        env_var = "SQL_ASSISTANT_DB_PATH"

        # Read existing .env content
        env_lines = []
        db_path_found = False

        if env_file.exists():
            with open(env_file, "r") as f:
                for line in f:
                    if line.startswith(f"{env_var}="):
                        env_lines.append(f"{env_var}={db_path}\n")
                        db_path_found = True
                    else:
                        env_lines.append(line)

        # Add if not found
        if not db_path_found:
            env_lines.append(f"{env_var}={db_path}\n")

        # Write back
        with open(env_file, "w") as f:
            f.writelines(env_lines)

    except Exception as e:
        # Silent fail - not critical if .env update fails
        print(f"⚠️  Warning: Could not update .env file: {e}")

def list_test_case_folders():
    """List all available test case folders."""
    test_cases_dir = "test_cases"
    if not os.path.exists(test_cases_dir):
        return []

    folders = []
    for item in os.listdir(test_cases_dir):
        folder_path = os.path.join(test_cases_dir, item)
        if os.path.isdir(folder_path):
            db_path = os.path.join(folder_path, "database.sqlite")
            json_path = os.path.join(folder_path, "questions.json")
            if os.path.exists(db_path) and os.path.exists(json_path):
                folders.append(
                    {
                        "name": item,
                        "folder": folder_path,
                        "database": db_path,
                        "questions": json_path,
                    }
                )
    return folders

def get_test_case_by_name(case_name):
    """Get test case paths by folder name."""
    folder_path = os.path.join("test_cases", case_name)
    if not os.path.isdir(folder_path):
        return None

    db_path = os.path.join(folder_path, "database.sqlite")
    json_path = os.path.join(folder_path, "questions.json")

    if os.path.exists(db_path) and os.path.exists(json_path):
        return {
            "name": case_name,
            "folder": folder_path,
            "database": db_path,
            "questions": json_path,
        }
    return None

def load_questions_from_json(json_file_path, question_index):
    """Load a question with a specific index from a JSON file.

    Supports both formats:
    1. New format: {"test_case_name": "...", "questions": [{"id": 0, "question": "...", ...}]}
    2. Legacy format: ["question1", "question2", ...]
    """
    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # New structured format
        if isinstance(data, dict) and "questions" in data:
            questions = data["questions"]
            if 0 <= question_index < len(questions):
                question_obj = questions[question_index]
                # Add metadata to the question object
                question_obj["test_case_name"] = data.get("test_case_name", "unknown")
                question_obj["description"] = data.get("description", "")
                return question_obj
            else:
                raise IndexError(
                    f"Question index {question_index} is out of range (0-{len(questions)-1})"
                )

        # Legacy format: simple list
        elif isinstance(data, list):
            if 0 <= question_index < len(data):
                # Convert to new format for consistency
                return {
                    "id": question_index,
                    "question": data[question_index],
                    "category": "Unknown",
                    "difficulty": "Unknown",
                }
            else:
                raise IndexError(
                    f"Question index {question_index} is out of range (0-{len(data)-1})"
                )

        # Legacy format: dict with string keys
        elif isinstance(data, dict):
            if str(question_index) in data:
                return {
                    "id": question_index,
                    "question": data[str(question_index)],
                    "category": "Unknown",
                    "difficulty": "Unknown",
                }
            else:
                raise KeyError(
                    f"Question index {question_index} does not exist in the question set"
                )
        else:
            raise ValueError(
                "Incorrect JSON file format, should be a list or dictionary with 'questions' key"
            )
    except FileNotFoundError:
        raise FileNotFoundError(f"Question set file {json_file_path} not found")
    except json.JSONDecodeError:
        raise ValueError(
            f"Question set file {json_file_path} is not a valid JSON format"
        )

def save_execution_info(
    execution_folder, start_time, end_time, result, error=None, trace_id=None, retry_count=0
):
    """Save execution information including trace ID and retry count."""
    execution_info = {
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "duration_seconds": (end_time - start_time).total_seconds(),
        "success": error is None,
        "error": str(error) if error else None,
        "has_detailed_result": result is not None,
        "trace_id": trace_id if trace_id else "No trace ID available",
        "retry_count": retry_count,
        "total_attempts": retry_count + 1,
        "retry_info": "No retries needed" if retry_count == 0 else f"Succeeded after {retry_count} retry(s)",
    }

    info_file = execution_folder / "execution_info.json"
    import json

    with open(info_file, "w", encoding="utf-8") as f:
        json.dump(execution_info, f, ensure_ascii=False, indent=2)
    return info_file