# MCP Integration Guide for Video Creator Agent v3.0

## Overview

Video Creator Agent v3.0 now supports **Model Context Protocol (MCP)** for enhanced interoperability with AI applications.

## What's New with MCP?

### 1. **MCP Client** - Web Search Capabilities

The agent can now use external MCP services like **Tavily** for web search:

```python
from agent import run_agent

# Agent can now search the web for current trends!
result = run_agent("Search for latest TikTok trends and generate 5 viral titles")
```

**New MCP Tools:**
- `web_search` - Search the web for current information
- `extract_webpage` - Extract content from web pages

### 2. **MCP Server** - Agent as a Service

Your Video Creator Agent can now be used by **any MCP-compatible application**:

- Claude Desktop
- Other AI agents
- Custom applications

## Installation

```bash
# Install MCP dependencies
pip install mcp

# Set Tavily environment variable (optional, for web search)
export TAVILY_REMOTE_SSE_URL="https://mcp.api-inference.modelscope.net/fc4326ad64734f/mcp"
```

## Usage Examples

### Example 1: Web Search in Agent

```bash
# The agent can now search the web!
python agent.py "Search for trending fitness topics and create a content plan"
```

### Example 2: Using Agent as MCP Server

**With Claude Desktop:**

1. Create/edit `~/.config/Claude/claude_desktop_config.json` (Linux/Mac)
   or `%APPDATA%\Claude\claude_desktop_config.json` (Windows)

2. Add the server configuration:

```json
{
  "mcpServers": {
    "video-creator-agent": {
      "command": "python",
      "args": ["C:\\Users\\User\\video_creator_agent\\mcp_server.py"],
      "env": {
        "OPENAI_API_KEY": "your-api-key",
        "OPENAI_BASE_URL": "https://api.stepfun.com/v1",
        "OPENAI_MODEL": "step-3.5-flash"
      }
    }
  }
}
```

3. Restart Claude Desktop

4. Now in Claude, you can use Video Creator Agent tools:
   - "Create a TikTok script about morning routines"
   - "Generate 5 viral titles for fitness content"
   - "Search the web for trending topics"

### Example 3: Python MCP Client

```python
from mcp_client import StdioMCPClient, mcp_tools_to_openai
from openai import OpenAI
import os

# Connect to Video Creator Agent MCP server
mcp = StdioMCPClient([
    "python",
    "C:\\Users\\User\\video_creator_agent\\mcp_server.py"
])

# Initialize connection
mcp.initialize()

# List available tools
tools = mcp.list_tools()
print(f"Available tools: {[t['name'] for t in tools]}")

# Convert to OpenAI format
openai_tools = mcp_tools_to_openai(tools)

# Use with OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

messages = [
    {"role": "system", "content": "You are a video creator assistant."},
    {"role": "user", "content": "Generate 5 viral titles for fitness TikToks"}
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=openai_tools
)

# Execute tool calls
for tool_call in response.choices[0].message.tool_calls:
    result = mcp.call_tool(
        tool_call.function.name,
        json.loads(tool_call.function.arguments)
    )
    print(f"Result: {result}")

mcp.close()
```

## Available MCP Tools

When running as an MCP server, the agent exposes these tools:

| Tool | Description |
|------|-------------|
| `save_idea` | Save video ideas with tags |
| `list_ideas` | List and filter saved ideas |
| `create_script` | Generate AI-powered scripts |
| `generate_titles` | Create viral titles |
| `generate_description` | Generate social media descriptions |
| `web_search` | Search the web (requires Tavily) |
| `get_trending_hashtags` | Get trending hashtags |
| `generate_content_plan` | Create content calendars |
| `show_stats` | Display usage statistics |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AI Application                          │
│                  (Claude, ChatGPT, etc.)                    │
└────────────────────────┬────────────────────────────────────┘
                         │ MCP Protocol
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Video Creator Agent MCP Server                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   MCP Layer                          │  │
│  │  - JSON-RPC 2.0                                      │  │
│  │  - tools/list                                        │  │
│  │  - tools/call                                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   Agent Tools                        │  │
│  │  - save_idea                                         │  │
│  │  - create_script                                     │  │
│  │  - generate_titles                                   │  │
│  │  - web_search (via Tavily MCP)                       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Benefits of MCP Integration

1. **Standardization**: Use industry-standard protocol for AI tool integration
2. **Interoperability**: Works with any MCP-compatible AI application
3. **Web Access**: Enhanced capabilities via external MCP services (Tavily)
4. **Composability**: Combine with other MCP servers for powerful workflows

## Troubleshooting

### MCP Tools Not Available

```bash
# Install MCP package
pip install mcp

# Verify installation
python -c "import mcp; print('MCP installed')"
```

### Web Search Not Working

Set the Tavily environment variable:

```bash
export TAVILY_REMOTE_SSE_URL="https://mcp.api-inference.modelscope.net/fc4326ad64734f/mcp"
```

### MCP Server Not Starting

Check Python path in config:

```json
{
  "command": "python",
  "args": ["FULL/PATH/TO/mcp_server.py"]
}
```

## Next Steps

1. **Test MCP Client**: Try web search features
2. **Deploy MCP Server**: Connect from Claude Desktop
3. **Explore Other MCP Servers**: Combine with fetch, filesystem, postgres MCP servers

## References

- [MCP Specification](https://modelcontextprotocol.io/specification)
- [nanoMCP Examples](https://github.com/sanbuphy/nanoMCP)
- [Claude Desktop Integration](https://claude.ai/mcp-integration)

---

**Version**: 3.0 with MCP support
**Date**: 2026-03-12
