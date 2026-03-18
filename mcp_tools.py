"""
MCP Tools Integration for Video Creator Agent
Adds web search capabilities via Tavily MCP
"""

import os
import json
from typing import Optional
from mcp_client import SSEMCPClient, create_mcp_client, mcp_tools_to_openai


# Tavily MCP client (lazy initialization)
_tavily_client = None
_tavily_tools = None


def get_tavily_client():
    """Get or create Tavily MCP client"""
    global _tavily_client

    if _tavily_client is None:
        # Check if Tavily is enabled
        if not os.environ.get("TAVILY_REMOTE_SSE_URL"):
            return None

        try:
            _tavily_client = SSEMCPClient(
                os.environ["TAVILY_REMOTE_SSE_URL"]
            )
            _tavily_client.initialize()
        except Exception as e:
            print(f"⚠️  Failed to connect to Tavily MCP: {e}")
            return None

    return _tavily_client


def get_tavily_tools():
    """Get Tavily MCP tools as OpenAI function definitions"""
    global _tavily_tools

    client = get_tavily_client()
    if client is None:
        return []

    if _tavily_tools is None:
        try:
            mcp_tools = client.list_tools()
            _tavily_tools = mcp_tools_to_openai(mcp_tools)
        except Exception as e:
            print(f"⚠️  Failed to list Tavily tools: {e}")
            return []

    return _tavily_tools


def tavily_search(query: str, max_results: int = 10) -> str:
    """
    Perform web search using Tavily MCP

    Args:
        query: Search query
        max_results: Maximum number of results

    Returns:
        Search results as formatted text
    """
    client = get_tavily_client()
    if client is None:
        return "❌ Tavily MCP is not available. Please set TAVILY_REMOTE_SSE_URL environment variable."

    try:
        result = client.call_tool("tavily_search", {
            "query": query,
            "max_results": max_results
        })
        return result
    except Exception as e:
        return f"❌ Tavily search error: {str(e)}"


def tavily_extract(url: str) -> str:
    """
    Extract content from a web page using Tavily MCP

    Args:
        url: URL to extract content from

    Returns:
        Extracted content as text
    """
    client = get_tavily_client()
    if client is None:
        return "❌ Tavily MCP is not available."

    try:
        result = client.call_tool("tavily_extract", {
            "url": url
        })
        return result
    except Exception as e:
        return f"❌ Tavily extract error: {str(e)}"


# Tool definitions for agent integration
TAVILY_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information, trends, and facts using Tavily search engine. Returns relevant URLs and snippets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 10)"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_webpage",
            "description": "Extract main content from a webpage URL. Useful for getting full article text, blog posts, or documentation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the webpage to extract content from"
                    }
                },
                "required": ["url"]
            }
        }
    }
]


# Enhanced tool implementations with MCP support
def web_search(query: str, max_results: int = 10) -> str:
    """Web search tool using Tavily MCP"""
    return tavily_search(query, max_results)


def extract_webpage(url: str) -> str:
    """Extract webpage content using Tavily MCP"""
    return tavily_extract(url)


def cleanup_tavily_client():
    """Cleanup Tavily MCP client"""
    global _tavily_client, _tavily_tools

    if _tavily_client is not None:
        try:
            _tavily_client.close()
        except:
            pass

        _tavily_client = None
        _tavily_tools = None
