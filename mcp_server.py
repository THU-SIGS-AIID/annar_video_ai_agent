"""
Video Creator Agent - MCP Server
Exposes agent tools via Model Context Protocol (stdio transport)

Usage:
    python mcp_server.py

Then connect with any MCP client:
    - Claude Desktop (add to claude_desktop_config.json)
    - Any MCP-compatible application
"""

import sys
import json
from typing import Dict, Any, List
from agent import (
    save_idea, list_ideas, create_script, save_script,
    create_project, organize_video_file, list_projects, show_stats,
    generate_titles, generate_description, generate_thumbnails_ideas,
    optimize_seo, generate_content_plan, export_ideas, import_ideas,
    create_script_template, search_history, get_trending_hashtags,
    analyze_best_post_time, web_search, extract_webpage
)


# Tool mappings
AGENT_FUNCTIONS = {
    "save_idea": save_idea,
    "list_ideas": list_ideas,
    "create_script": create_script,
    "save_script": save_script,
    "create_project": create_project,
    "organize_video_file": organize_video_file,
    "list_projects": list_projects,
    "show_stats": show_stats,
    "generate_titles": generate_titles,
    "generate_description": generate_description,
    "generate_thumbnails_ideas": generate_thumbnails_ideas,
    "optimize_seo": optimize_seo,
    "generate_content_plan": generate_content_plan,
    "export_ideas": export_ideas,
    "import_ideas": import_ideas,
    "create_script_template": create_script_template,
    "search_history": search_history,
    "get_trending_hashtags": get_trending_hashtags,
    "analyze_best_post_time": analyze_best_post_time,
    "web_search": web_search,
    "extract_webpage": extract_webpage,
}


# MCP Tool definitions
MCP_TOOLS = [
    {
        "name": "save_idea",
        "description": "Save a video idea with title, description, tags and platform",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Idea title (min 3 chars)"},
                "description": {"type": "string", "description": "Detailed description"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags for categorization"},
                "platform": {"type": "string", "enum": ["tiktok", "instagram", "xiaohongshu", "youtube_shorts"], "description": "Target platform"}
            },
            "required": ["title", "description"]
        }
    },
    {
        "name": "list_ideas",
        "description": "List all saved ideas with filtering options",
        "inputSchema": {
            "type": "object",
            "properties": {
                "platform": {"type": "string", "description": "Filter by platform"},
                "tag": {"type": "string", "description": "Filter by tag"},
                "limit": {"type": "integer", "description": "Limit results"}
            }
        }
    },
    {
        "name": "create_script",
        "description": "Generate an AI-powered video script with platform-specific optimization",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "Topic for the script"},
                "platform": {"type": "string", "description": "Target platform"},
                "duration": {"type": "string", "description": "Target duration (e.g., '30 seconds')"},
                "tone": {"type": "string", "description": "Tone of the script"}
            },
            "required": ["topic"]
        }
    },
    {
        "name": "generate_titles",
        "description": "Generate viral, clickbait video titles using AI",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "Video topic"},
                "platform": {"type": "string", "description": "Target platform"},
                "count": {"type": "integer", "description": "Number of titles (default: 5)"}
            },
            "required": ["topic"]
        }
    },
    {
        "name": "generate_description",
        "description": "Generate social media post descriptions with hashtags",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "Video topic"},
                "platform": {"type": "string", "description": "Target platform"},
                "tone": {"type": "string", "description": "Tone of description"}
            },
            "required": ["topic"]
        }
    },
    {
        "name": "web_search",
        "description": "Search the web for current information, trends, and facts",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "max_results": {"type": "integer", "description": "Max results (default: 10)"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_trending_hashtags",
        "description": "Get trending and relevant hashtags for platform and niche",
        "inputSchema": {
            "type": "object",
            "properties": {
                "platform": {"type": "string", "description": "Target platform"},
                "niche": {"type": "string", "description": "Content niche"},
                "count": {"type": "integer", "description": "Number of hashtags (default: 10)"}
            }
        }
    },
    {
        "name": "generate_content_plan",
        "description": "Generate a content calendar with daily video ideas",
        "inputSchema": {
            "type": "object",
            "properties": {
                "niche": {"type": "string", "description": "Content niche"},
                "platform": {"type": "string", "description": "Target platform"},
                "days": {"type": "integer", "description": "Number of days (default: 7)"}
            },
            "required": ["niche"]
        }
    },
    {
        "name": "show_stats",
        "description": "Display usage statistics and analytics",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


class MCPServer:
    """MCP Server for Video Creator Agent"""

    def __init__(self):
        self.initialized = False

    def send_response(self, response: Dict[str, Any]):
        """Send JSON-RPC response to stdout"""
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()

    def send_error(self, code: int, message: str):
        """Send JSON-RPC error response"""
        self.send_response({
            "jsonrpc": "2.0",
            "error": {
                "code": code,
                "message": message
            },
            "id": None
        })

    def send_result(self, result: Any, request_id: Any = None):
        """Send JSON-RPC result response"""
        response = {
            "jsonrpc": "2.0",
            "result": result
        }
        if request_id is not None:
            response["id"] = request_id
        self.send_response(response)

    def handle_initialize(self, params: Dict, request_id: Any):
        """Handle initialize request"""
        self.initialized = True
        self.send_result({
            "protocolVersion": "2024-11-05",
            "serverInfo": {
                "name": "video-creator-agent",
                "version": "3.0"
            },
            "capabilities": {
                "tools": {}
            }
        }, request_id)

    def handle_tools_list(self, params: Dict, request_id: Any):
        """Handle tools/list request"""
        self.send_result({
            "tools": MCP_TOOLS
        }, request_id)

    def handle_tools_call(self, params: Dict, request_id: Any):
        """Handle tools/call request"""
        try:
            name = params.get("name")
            arguments = params.get("arguments", {})

            if name not in AGENT_FUNCTIONS:
                raise ValueError(f"Unknown tool: {name}")

            # Execute the tool function
            func = AGENT_FUNCTIONS[name]
            result = func(**arguments)

            # Return result in MCP format
            self.send_result({
                "content": [
                    {
                        "type": "text",
                        "text": str(result)
                    }
                ]
            }, request_id)

        except Exception as e:
            self.send_error(-32603, f"Tool execution error: {str(e)}")

    def handle_request(self, request: Dict):
        """Handle incoming JSON-RPC request"""
        try:
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")

            if method == "initialize":
                self.handle_initialize(params, request_id)

            elif method == "tools/list":
                if not self.initialized:
                    self.send_error(-32600, "Not initialized")
                else:
                    self.handle_tools_list(params, request_id)

            elif method == "tools/call":
                if not self.initialized:
                    self.send_error(-32600, "Not initialized")
                else:
                    self.handle_tools_call(params, request_id)

            else:
                self.send_error(-32601, f"Method not found: {method}")

        except Exception as e:
            self.send_error(-32603, f"Request handling error: {str(e)}")


def main():
    """Main MCP server loop"""
    server = MCPServer()

    # Send ready notification
    sys.stderr.write("Video Creator Agent MCP Server started\n")
    sys.stderr.flush()

    # Read requests from stdin
    for line in sys.stdin:
        if not line.strip():
            continue

        try:
            request = json.loads(line.strip())
            server.handle_request(request)
        except json.JSONDecodeError:
            server.send_error(-32700, "Parse error")


if __name__ == "__main__":
    main()
