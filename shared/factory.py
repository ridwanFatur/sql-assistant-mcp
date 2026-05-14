"""
Factory functions for creating shared LLM and MCP adapter instances.
Centralizes configuration to avoid duplication across crews and orchestrator.
"""

import os
from langchain_openai import ChatOpenAI
from crewai_tools import MCPServerAdapter
from dotenv import load_dotenv

def create_llm(custom_llm=None):
    """
    Create a ChatOpenAI LLM instance with standard configuration.

    Args:
        custom_llm: Optional pre-configured LLM instance. If provided, returns it unchanged.

    Returns:
        ChatOpenAI instance configured from environment variables.
    """
    if custom_llm is not None:
        return custom_llm

    load_dotenv(override=True)
    
    return ChatOpenAI(
        openai_api_base=os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1"),
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        temperature=float(os.environ.get("TEMPERATURE", 0.7)),
        model_name=os.environ.get("MODEL_NAME", "gpt-4"),
        top_p=float(os.environ.get("TOP_P", 0.3)),
        max_retries=3,
        request_timeout=60,
    )


def create_mcp_adapter(custom_adapter=None):
    """
    Create an MCP adapter instance with standard configuration.

    Args:
        custom_adapter: Optional pre-configured MCP adapter. If provided, returns it unchanged.

    Returns:
        MCPServerAdapter instance configured from environment variables.
    """
    if custom_adapter is not None:
        return custom_adapter

    load_dotenv(override=True)

    mcp_server_url = os.environ.get("MCP_SERVER_URL", "http://127.0.0.1:8150/sse")
    return MCPServerAdapter({"url": mcp_server_url, "transport": "sse"})
