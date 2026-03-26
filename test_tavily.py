"""
Test Tavily MCP Integration
"""
import os
import sys

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_tavily_connection():
    """Test Tavily MCP connection"""
    print("=" * 60)
    print("🔍 Tavily MCP Connection Test")
    print("=" * 60)

    # Check environment variable
    tavily_url = os.environ.get("TAVILY_REMOTE_SSE_URL")
    print(f"\n📡 Tavily URL: {tavily_url}")

    if not tavily_url:
        print("❌ TAVILY_REMOTE_SSE_URL not set in .env file")
        return False

    try:
        from mcp_client import SSEMCPClient

        print("\n🔌 Connecting to Tavily MCP...")
        client = SSEMCPClient(tavily_url)
        client.initialize()
        print("✅ Connected successfully!")

        # List available tools
        print("\n🛠️  Available tools:")
        tools = client.list_tools()
        for tool in tools:
            print(f"  • {tool['name']}: {tool.get('description', 'No description')}")

        # Test web search
        print("\n🔎 Testing web search...")
        print("Query: 'TikTok trends 2026'")

        result = client.call_tool("tavily_search", {
            "query": "TikTok trends 2026",
            "max_results": 3
        })

        print("\n📊 Search results:")
        print(result[:500] if len(result) > 500 else result)  # Show first 500 chars
        print("..." if len(result) > 500 else "")

        # Test extract
        print("\n📄 Testing webpage extract...")
        print("URL: 'https://www.tiktok.com'")

        extract_result = client.call_tool("tavily_extract", {
            "url": "https://www.tiktok.com"
        })

        print("\n📝 Extracted content (first 300 chars):")
        print(extract_result[:300] if len(extract_result) > 300 else extract_result)
        print("..." if len(extract_result) > 300 else "")

        client.close()
        print("\n✅ All tests passed!")
        return True

    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("Install mcp package: pip install mcp")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_agent_with_search():
    """Test agent with web search"""
    print("\n" + "=" * 60)
    print("🤖 Testing Agent with Web Search")
    print("=" * 60)

    try:
        from agent import run_agent

        print("\n🔍 Query: 'Найди актуальные тренды TikTok и создай 3 идеи'")
        print("\n⏳ Processing...")

        result = run_agent("Найди актуальные тренды TikTok и создай 3 идеи")

        print("\n📝 Result:")
        print(result)

        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


if __name__ == "__main__":
    # Test 1: Direct MCP connection
    success1 = test_tavily_connection()

    # Test 2: Agent with web search
    if success1:
        print("\n" + "🔄" * 30)
        success2 = test_agent_with_search()

    print("\n" + "=" * 60)
    if success1:
        print("✅ Tavily MCP is ready!")
        print("\n💡 Now you can use web search in agent:")
        print("   python agent.py \"Найди тренды и создай контент\"")
    else:
        print("❌ Setup failed. Check configuration.")
    print("=" * 60)
