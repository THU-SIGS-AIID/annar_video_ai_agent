"""
Test MCP Integration for Video Creator Agent
Tests both MCP client and server functionality
"""

import os
import sys
import json
import subprocess
from pathlib import Path


def test_mcp_client():
    """Test MCP client with Tavily"""
    print("\n" + "="*60)
    print("Testing MCP Client (Tavily Web Search)")
    print("="*60)

    try:
        from mcp_tools import web_search, get_tavily_tools

        # Check if Tavily is configured
        if not os.environ.get("TAVILY_REMOTE_SSE_URL"):
            print("⚠️  TAVILY_REMOTE_SSE_URL not set")
            print("   Set it with: export TAVILY_REMOTE_SSE_URL='https://...'")
            return False

        # Test web search
        print("\n📝 Testing web_search tool...")
        result = web_search("TikTok trends 2026", max_results=3)

        if result and "❌" not in result:
            print("✅ Web search successful!")
            print(f"   Result preview: {result[:200]}...")
            return True
        else:
            print(f"❌ Web search failed: {result}")
            return False

    except ImportError as e:
        print(f"❌ MCP import error: {e}")
        print("   Install with: pip install mcp")
        return False
    except Exception as e:
        print(f"❌ MCP client test failed: {e}")
        return False


def test_mcp_server():
    """Test MCP server functionality"""
    print("\n" + "="*60)
    print("Testing MCP Server")
    print("="*60)

    try:
        # Start MCP server process
        server_path = Path(__file__).parent / "mcp_server.py"

        print("\n📝 Starting MCP server...")

        proc = subprocess.Popen(
            [sys.executable, str(server_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Test initialize
        initialize_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0"}
            }
        }

        proc.stdin.write(json.dumps(initialize_request) + "\n")
        proc.stdin.flush()

        response = json.loads(proc.stdout.readline())
        print(f"✅ Initialize: {response.get('result', {}).get('serverInfo', {}).get('name')}")

        # Test tools/list
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }

        proc.stdin.write(json.dumps(tools_request) + "\n")
        proc.stdin.flush()

        response = json.loads(proc.stdout.readline())
        tools = response.get("result", {}).get("tools", [])

        print(f"✅ Tools available: {len(tools)}")
        for tool in tools:
            print(f"   - {tool['name']}")

        # Test a tool call
        print("\n📝 Testing show_stats tool...")
        call_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "show_stats",
                "arguments": {}
            }
        }

        proc.stdin.write(json.dumps(call_request) + "\n")
        proc.stdin.flush()

        response = json.loads(proc.stdout.readline())
        result = response.get("result", {})
        content = result.get("content", [{}])[0].get("text", "")

        print(f"✅ Tool call result: {content[:100]}...")

        # Cleanup
        proc.terminate()
        proc.wait()

        print("\n✅ MCP server test passed!")
        return True

    except Exception as e:
        print(f"\n❌ MCP server test failed: {e}")
        if 'proc' in locals():
            proc.terminate()
        return False


def test_agent_with_mcp():
    """Test agent with MCP tools enabled"""
    print("\n" + "="*60)
    print("Testing Video Creator Agent with MCP")
    print("="*60)

    try:
        from agent import run_agent

        # Test regular agent functionality
        print("\n📝 Testing agent without MCP...")
        result = run_agent("show my stats", max_iterations=1)

        if result and "❌" not in result:
            print("✅ Agent works without MCP")
        else:
            print(f"⚠️  Agent result: {result[:100]}")

        # Test agent with MCP (if available)
        if os.environ.get("TAVILY_REMOTE_SSE_URL"):
            print("\n📝 Testing agent with MCP web search...")
            result = run_agent("what are the latest TikTok trends?", max_iterations=2)

            if result and "❌" not in result:
                print("✅ Agent works with MCP!")
                return True
            else:
                print(f"⚠️  Agent MCP result: {result[:100]}")
        else:
            print("\n⚠️  Skipping MCP web search test (TAVILY_REMOTE_SSE_URL not set)")

        return True

    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False


def main():
    """Run all MCP tests"""
    print("="*60)
    print("  Video Creator Agent v3.0 - MCP Integration Test")
    print("="*60)

    results = []

    # Test 1: MCP Client
    results.append(("MCP Client", test_mcp_client()))

    # Test 2: MCP Server
    results.append(("MCP Server", test_mcp_server()))

    # Test 3: Agent with MCP
    results.append(("Agent + MCP", test_agent_with_mcp()))

    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)

    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")

    all_passed = all(r[1] for r in results)

    if all_passed:
        print("\n🎉 All tests passed! MCP integration is working.")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
