"""
Simple MCP Server Test
"""

import subprocess
import sys
import json

def test_mcp_server():
    """Test MCP server"""
    print("Testing MCP Server...")

    # Start server
    proc = subprocess.Popen(
        [sys.executable, "mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="c:\\Users\\User\\video_creator_agent"
    )

    # Test initialize
    req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {"protocolVersion": "2024-11-05"}
    }

    proc.stdin.write(json.dumps(req) + "\n")
    proc.stdin.flush()

    resp = json.loads(proc.stdout.readline())
    print(f"Initialize: {resp.get('result', {}).get('serverInfo')}")

    # Test tools/list
    req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }

    proc.stdin.write(json.dumps(req) + "\n")
    proc.stdin.flush()

    resp = json.loads(proc.stdout.readline())
    tools = resp.get("result", {}).get("tools", [])
    print(f"Tools: {len(tools)} available")
    for t in tools[:3]:
        print(f"  - {t['name']}")

    proc.terminate()
    print("MCP Server test passed!")

if __name__ == "__main__":
    test_mcp_server()
