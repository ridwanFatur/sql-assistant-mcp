"""
Database Helper Functions

This module contains:
1. Configuration management (database path)
2. Utility functions (SQL cleaning)
3. Legacy functions for backward compatibility
"""

import os
import sqlite3
import pandas as pd
import re

# Export all helper functions
__all__ = [
    'set_database_path',
    'get_database_path',
    'clean_sql_query',
    'run_query',
    'get_db_schema',
    'get_structured_schema',
]


# ============================================================================
# Configuration Management
# ============================================================================

# Global variable to store current database path (set by main.py)
_CURRENT_DB_PATH = None

# Environment variable name for database path (for MCP cross-process communication)
_DB_PATH_ENV_VAR = "SQL_ASSISTANT_DB_PATH"


def set_database_path(db_path: str):
    """
    Set the current database path for tools to use.
    
    This function sets both the global variable (for same-process access)
    and an environment variable (for cross-process MCP access).
    """
    global _CURRENT_DB_PATH
    _CURRENT_DB_PATH = db_path
    # Set environment variable for MCP server process to access
    os.environ[_DB_PATH_ENV_VAR] = db_path


def get_database_path() -> str:
    """
    Get the current database path.
    
    Checks multiple sources in order:
    1. Global variable (same-process access)
    2. Environment variable (cross-process MCP access)
    3. .env file (for MCP server running in separate terminal)
    4. Default relative path (fallback for development)
    
    This allows the function to work in multiple contexts.
    """
    global _CURRENT_DB_PATH
    
    # 1. Check global variable (same-process access)
    if _CURRENT_DB_PATH is not None:
        return _CURRENT_DB_PATH
    
    # 2. Check environment variable (cross-process MCP access)
    # db_path = os.environ.get(_DB_PATH_ENV_VAR)
    # if db_path is not None:
    #     print("Return From Section-2")
    #     return db_path
    
    # 3. Try to load from .env file (for MCP server in separate terminal)
    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)
        db_path = os.environ.get(_DB_PATH_ENV_VAR)
        if db_path is not None:
            return db_path
    except:
        pass
    
    # 4. If all else fails, raise error
    raise ValueError(
        "Database path not set. Please ensure:\n"
        "  1. main.py calls set_database_path() before workflow execution, OR\n"
        "  2. SQL_ASSISTANT_DB_PATH environment variable is set, OR\n"
        f"  3. {_DB_PATH_ENV_VAR} is defined in .env file"
    )


# ============================================================================
# Utility Functions
# ============================================================================

def clean_sql_query(query: str) -> str:
    """
    Clean SQL query by removing markdown code block markers, Pydantic object formatting, and extra whitespace.

    Parameters:
    - query: Raw SQL query string that may contain markdown markers or Pydantic object representation

    Returns:
    - Cleaned SQL query string ready for execution
    """
    if not query:
        return query

    # Remove Pydantic object field representation (e.g., "reviewed_sqlquery='SELECT...'")
    # Match patterns like: field_name='...' or field_name="..."
    pydantic_pattern = r"(?:reviewed_sqlquery|sqlquery)\s*=\s*['\"](.+?)['\"]"
    pydantic_match = re.search(pydantic_pattern, query, flags=re.DOTALL)
    if pydantic_match:
        query = pydantic_match.group(1)

    # Remove markdown code block markers
    query = re.sub(r"^```sql\s*", "", query, flags=re.MULTILINE)
    query = re.sub(r"^```\s*$", "", query, flags=re.MULTILINE)
    query = re.sub(r"```sql", "", query)
    query = re.sub(r"```", "", query)

    # Remove extra whitespace and normalize
    query = query.strip()

    return query


# ============================================================================
# Legacy Functions (for backward compatibility)
# ============================================================================

def run_query(query, db_path):
    """
    Execute a SQL query against the specified database.
    
    LEGACY: Use the @tool decorated run_sql_query() instead for agent usage.
    This function is kept for direct programmatic access.
    """
    try:
        # Clean the query to remove any markdown formatting
        cleaned_query = clean_sql_query(query)
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(cleaned_query, conn)
        conn.close()
        return df.head().to_string(index=False)
    except Exception as e:
        return f"Query failed: Execution failed on sql '{cleaned_query}': {e}"


def get_db_schema(db_path):
    """
    Legacy function for backward compatibility.
    Returns basic CREATE TABLE statements.
    
    LEGACY: Use the @tool decorated get_database_schema() instead for agent usage.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    schema = ""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for (table_name,) in tables:
        cursor.execute(
            f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        )
        create_stmt = cursor.fetchone()[0]
        schema += create_stmt + ";\n\n"
    conn.close()
    return schema


def get_structured_schema(db_path):
    """
    Get a user-friendly structured schema representation.
    Returns a simple list of tables and their columns.
    
    LEGACY: This provides a concise view, but consider using
    the @tool decorated get_database_schema() for richer information.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    lines = ["Available tables and columns:"]
    for (table_name,) in tables:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall()]
        lines.append(f"- {table_name}: {', '.join(columns)}")
    conn.close()
    return "\n".join(lines)


if __name__ == "__main__":
    print("Database helper module. Contains configuration and utility functions.")
