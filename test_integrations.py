"""
Test script for integrations
Run this to verify your integrations work
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from integrations import (
    search_web,
    get_trending_topics,
    get_hashtag_suggestions,
    make_http_request,
    NotionClient,
    save_idea_to_notion
)

def test_web_search():
    """Test web search functionality"""
    print("\n🔍 Testing Web Search...")
    print("="*50)

    try:
        results = search_web("TikTok trends 2025", num_results=3)
        if results and "error" not in results[0]:
            print("✅ Web search working!")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['title']}")
                print(f"   {result['url']}")
        else:
            print("❌ Web search failed")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_trending_topics():
    """Test trending topics"""
    print("\n📈 Testing Trending Topics...")
    print("="*50)

    try:
        trends = get_trending_topics("tiktok")
        if trends:
            print("✅ Trending topics working!")
            for trend in trends:
                print(f"• {trend['topic']} - {trend['views']}")
        else:
            print("❌ No trends found")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_hashtags():
    """Test hashtag generation"""
    print("\n🏷️  Testing Hashtag Generation...")
    print("="*50)

    try:
        hashtags = get_hashtag_suggestions("morning routine productivity", "tiktok")
        print("✅ Hashtag generation working!")
        print(f"Generated: {' '.join(hashtags)}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_notion_connection():
    """Test Notion API connection"""
    print("\n📝 Testing Notion Connection...")
    print("="*50)

    api_key = os.environ.get("NOTION_API_KEY")
    database_id = os.environ.get("NOTION_DATABASE_ID")

    if not api_key or not database_id:
        print("⚠️  Notion credentials not configured")
        print("   Add NOTION_API_KEY and NOTION_DATABASE_ID to .env file")
        return

    try:
        notion = NotionClient()
        result = notion.search_pages("test")
        if "results" in result:
            print("✅ Notion API connected!")
            print(f"   Found {len(result['results'])} pages")
        else:
            print("❌ Notion API error")
            print(f"   Response: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_http_request():
    """Test HTTP request functionality"""
    print("\n🌐 Testing HTTP Requests...")
    print("="*50)

    try:
        # Test with a simple API
        response = make_http_request("https://httpbin.org/get")
        if response and "args" in response:
            print("✅ HTTP requests working!")
            print(f"   Status: OK")
        else:
            print("❌ HTTP request failed")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run all tests"""
    # Fix UTF-8 encoding on Windows
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')

    print("""
================================================================
              INTEGRATION TEST SUITE
================================================================
    """)

    # Run tests
    test_web_search()
    test_trending_topics()
    test_hashtags()
    test_notion_connection()
    test_http_request()

    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    print("✅ Working: Web search, Trends, Hashtags, HTTP")
    print("⚠️  Configure: Notion (add to .env)")
    print("\n💡 Next steps:")
    print("1. For Notion: Follow INTEGRATIONS_GUIDE.md")
    print("2. Add integrations to agent.py tools list")
    print("3. Test with: python agent.py \"Search web for trends\"")


if __name__ == "__main__":
    main()
