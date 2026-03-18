"""
MCP Client for Video Creator Agent
Supports: stdio, SSE, and Streamable HTTP transports
"""

import json
import os
import subprocess
import sys
import re
from typing import List, Dict, Any, Optional
from urllib import parse, request
from openai import OpenAI


class StdioMCPClient:
    """MCP client over stdin/stdout (for local MCP servers)"""

    def __init__(self, command: List[str]):
        """
        Initialize stdio MCP client

        Args:
            command: Command to spawn MCP server (e.g., ['python', 'server.py'])
        """
        self.proc = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0
        )
        self._id = 0

    def send(self, method: str, params: Dict = {}) -> Any:
        """Send JSON-RPC request and read response"""
        self._id += 1
        request_data = {
            "jsonrpc": "2.0",
            "id": self._id,
            "method": method,
            "params": params
        }

        # Send request
        self.proc.stdin.write(json.dumps(request_data) + "\n")
        self.proc.stdin.flush()

        # Read response
        response_line = self.proc.stdout.readline()
        if not response_line:
            raise RuntimeError("MCP server closed connection")

        response = json.loads(response_line.strip())
        if "error" in response:
            raise RuntimeError(f"MCP error: {response['error']}")

        return response.get("result")

    def initialize(self):
        """Initialize MCP connection"""
        return self.send("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "video-creator-agent", "version": "3.0"}
        })

    def list_tools(self) -> List[Dict]:
        """List available tools from MCP server"""
        result = self.send("tools/list")
        return result.get("tools", [])

    def call_tool(self, name: str, arguments: Dict = {}) -> str:
        """Call a tool on the MCP server"""
        result = self.send("tools/call", {
            "name": name,
            "arguments": arguments
        })

        # Extract text content from result
        if isinstance(result, dict):
            content = result.get("content", [])
            if content and len(content) > 0:
                return content[0].get("text", str(result))
        return str(result)

    def close(self):
        """Close the MCP connection"""
        if self.proc:
            self.proc.terminate()
            self.proc.wait()


class SSEMCPClient:
    """MCP client over Server-Sent Events (for remote HTTP servers)"""

    def __init__(self, sse_url: str):
        """
        Initialize SSE MCP client

        Args:
            sse_url: SSE endpoint URL
        """
        self.url = sse_url.strip().strip("`").strip()
        self._id = 0
        self._sse_resp = None
        self._message_url = None
        self._pending = {}
        self._connect_sse()

    def _connect_sse(self):
        """Connect to SSE endpoint"""
        req = request.Request(
            self.url,
            headers={"Accept": "text/event-stream"},
            method="GET"
        )
        self._sse_resp = request.urlopen(req, timeout=120)
        self._wait_for_endpoint()

    def _wait_for_endpoint(self):
        """Wait for message endpoint URL from SSE stream"""
        while not self._message_url:
            event, data = self._read_event()
            if event == "endpoint" and data:
                self._message_url = parse.urljoin(self.url, data)

    def _read_event(self):
        """Read SSE event from stream"""
        event = "message"
        data_lines = []

        while True:
            raw = self._sse_resp.readline()
            if not raw:
                raise RuntimeError("SSE stream closed")

            line = raw.decode("utf-8", errors="ignore").rstrip("\r\n")

            if line == "":
                if data_lines:
                    return event, "\n".join(data_lines)
                event = "message"
                data_lines = []
                continue

            if line.startswith(":"):
                continue  # Comment

            if line.startswith("event:"):
                event = line[6:].strip()
                continue

            if line.startswith("data:"):
                data_lines.append(line[5:].lstrip())
                continue

    def send(self, method: str, params: Dict = {}) -> Any:
        """Send JSON-RPC request via HTTP"""
        if not self._message_url:
            self._wait_for_endpoint()

        self._id += 1
        req_id = self._id

        body = json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method,
            "params": params
        }, ensure_ascii=False).encode("utf-8")

        req = request.Request(
            self._message_url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            method="POST"
        )

        with request.urlopen(req, timeout=60) as resp:
            if resp.status not in (200, 202):
                raise RuntimeError(f"HTTP {resp.status}: {resp.reason}")

        # Wait for response in SSE stream
        if req_id in self._pending:
            msg = self._pending.pop(req_id)
        else:
            while True:
                event, data = self._read_event()

                if event == "endpoint" and data:
                    self._message_url = parse.urljoin(self.url, data)
                    continue

                if not data:
                    continue

                try:
                    msg = json.loads(data)
                except json.JSONDecodeError:
                    continue

                if msg.get("id") == req_id:
                    break

                if "id" in msg:
                    self._pending[msg["id"]] = msg

        if "error" in msg:
            raise RuntimeError(msg["error"]["message"])

        return msg.get("result")

    def initialize(self):
        """Initialize MCP connection"""
        self.send("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "video-creator-agent", "version": "3.0"}
        })
        self.notify("notifications/initialized", {})

    def list_tools(self) -> List[Dict]:
        """List available tools from MCP server"""
        result = self.send("tools/list")
        return result.get("tools", [])

    def call_tool(self, name: str, arguments: Dict = {}) -> str:
        """Call a tool on the MCP server"""
        result = self.send("tools/call", {
            "name": name,
            "arguments": arguments
        })

        # Extract text content from result
        if isinstance(result, dict):
            content = result.get("content", [])
            if content and len(content) > 0:
                return content[0].get("text", str(result))
        return str(result)

    def notify(self, method: str, params: Dict = {}):
        """Send notification (no response expected)"""
        if not self._message_url:
            self._wait_for_endpoint()

        body = json.dumps({
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }, ensure_ascii=False).encode("utf-8")

        req = request.Request(
            self._message_url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            method="POST"
        )

        with request.urlopen(req, timeout=60) as resp:
            if resp.status not in (200, 202):
                raise RuntimeError(f"HTTP {resp.status} for notification")

    def close(self):
        """Close SSE connection"""
        if self._sse_resp:
            self._sse_resp.close()


def mcp_tools_to_openai(mcp_tools: List[Dict]) -> List[Dict]:
    """
    Convert MCP tool definitions to OpenAI function calling format

    Args:
        mcp_tools: List of MCP tool definitions

    Returns:
        List of OpenAI function definitions
    """
    openai_tools = []

    for tool in mcp_tools:
        openai_tool = {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool.get("description", ""),
                "parameters": tool.get("inputSchema", {})
            }
        }
        openai_tools.append(openai_tool)

    return openai_tools


# Pre-configured MCP servers
MCP_SERVERS = {
    "tavily": {
        "type": "sse",
        "url": os.environ.get("TAVILY_REMOTE_SSE_URL", "https://mcp.api-inference.modelscope.net/fc4326ad64734f/mcp"),
        "description": "Tavily web search"
    }
}


def create_mcp_client(server_name: str):
    """
    Create MCP client from pre-configured server name

    Args:
        server_name: Name of pre-configured MCP server

    Returns:
        MCP client instance (StdioMCPClient or SSEMCPClient)
    """
    if server_name not in MCP_SERVERS:
        raise ValueError(f"Unknown MCP server: {server_name}")

    config = MCP_SERVERS[server_name]

    if config["type"] == "sse":
        return SSEMCPClient(config["url"])
    elif config["type"] == "stdio":
        return StdioMCPClient(config["command"])
    else:
        raise ValueError(f"Unsupported MCP transport: {config['type']}")
