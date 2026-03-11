"""
INTEGRATIONS MODULE - Connect Agent to External Services
Supports: Notion, Web Search, HTTP Requests, Social Media APIs
"""

import os
import requests
from typing import Dict, List, Optional
import json

# ============= NOTION INTEGRATION =============

class NotionClient:
    """Simple Notion API client for agent"""

    def __init__(self):
        self.api_key = os.environ.get("NOTION_API_KEY")
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def create_page(self, database_id: str, properties: dict) -> dict:
        """Create a new page in Notion database"""
        url = f"{self.base_url}/pages"

        data = {
            "parent": {"database_id": database_id},
            "properties": properties
        }

        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def search_pages(self, query: str) -> dict:
        """Search for pages in Notion"""
        url = f"{self.base_url}/search"

        data = {
            "query": query
        }

        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def get_page_content(self, page_id: str) -> dict:
        """Get page content blocks"""
        url = f"{self.base_url}/blocks/{page_id}/children"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def append_to_page(self, page_id: str, content: str) -> dict:
        """Append content to a page"""
        url = f"{self.base_url}/blocks/{page_id}/children"

        data = {
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": content}
                            }
                        ]
                    }
                }
            ]
        }

        response = requests.patch(url, headers=self.headers, json=data)
        return response.json()


# ============= WEB SCRAPING =============

def search_web(query: str, num_results: int = 5) -> List[Dict]:
    """Search the web and return results (using DuckDuckGo HTML version)"""
    try:
        from bs4 import BeautifulSoup

        url = f"https://html.duckduckgo.com/html/?q={query}"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = []
        for result in soup.find_all('div', class_='result')[:num_results]:
            title = result.find('a', class_='result__a')
            snippet = result.find('a', class_='result__snippet')

            if title:
                results.append({
                    "title": title.get_text(),
                    "url": title.get('href'),
                    "snippet": snippet.get_text() if snippet else ""
                })

        return results

    except Exception as e:
        return [{"error": str(e)}]


def get_trending_topics(platform: str = "tiktok") -> List[Dict]:
    """Get trending topics for social platforms (simulated)"""

    # In real implementation, you'd use APIs like:
    # - TikTok: https://developers.tiktok.com/
    # - Instagram: Instagram Graph API
    # - YouTube: YouTube Data API

    trends = {
        "tiktok": [
            {"topic": "Green flag relationships", "views": "2.3M"},
            {"topic": "Silent review trend", "views": "1.8M"},
            {"topic": "POV: when your mom...", "views": "1.5M"}
        ],
        "instagram": [
            {"topic": "That girl aesthetic", "posts": "1.2M"},
            {"topic": "Day in my life", "posts": "900K"}
        ],
        "youtube": [
            {"topic": "AI tools tutorial", "videos": "500K"},
            {"topic": "Side hustle ideas", "videos": "450K"}
        ]
    }

    return trends.get(platform, [])


# ============= SOCIAL MEDIA APIS =============

class TikTokAPI:
    """Basic TikTok API integration (would need official API key)"""

    def __init__(self):
        self.api_key = os.environ.get("TIKTOK_API_KEY")
        self.base_url = "https://open.tiktokapis.com/v2"

    def get_trending_hashtags(self) -> List[Dict]:
        """Get trending hashtags"""
        # This would use the real TikTok API
        return [
            {"tag": "#fyp", "posts": "50B"},
            {"tag": "#foryou", "posts": "45B"},
            {"tag": "#viral", "posts": "30B"}
        ]


# ============= HTTP REQUESTS =============

def make_http_request(url: str, method: str = "GET", data: dict = None) -> dict:
    """Make HTTP requests to any API"""

    if method == "GET":
        response = requests.get(url, timeout=10)
    elif method == "POST":
        response = requests.post(url, json=data, timeout=10)
    else:
        return {"error": "Unsupported method"}

    try:
        return response.json()
    except:
        return {"status": response.status_code, "text": response.text}


# ============= HELPER FUNCTIONS =============

def save_idea_to_notion(title: str, description: str, tags: list, platform: str):
    """Save video idea to Notion database"""
    notion = NotionClient()
    database_id = os.environ.get("NOTION_DATABASE_ID")

    if not notion.api_key or not database_id:
        return {"error": "Notion API credentials not configured"}

    properties = {
        "Name": {
            "title": [{"text": {"content": title}}]
        },
        "Description": {
            "rich_text": [{"text": {"content": description}}]
        },
        "Tags": {
            "multi_select": [{"name": tag} for tag in tags]
        },
        "Platform": {
            "select": {"name": platform}
        }
    }

    return notion.create_page(database_id, properties)


def search_trends_for_idea(topic: str) -> str:
    """Search web for trends related to video idea"""
    results = search_web(f"{topic} trending social media 2025")

    if not results or "error" in results[0]:
        return "Could not fetch trends"

    summary = f"Trending information for '{topic}':\n\n"
    for i, result in enumerate(results[:3], 1):
        summary += f"{i}. {result['title']}\n"
        summary += f"   {result.get('snippet', '')[:100]}...\n\n"

    return summary


def get_hashtag_suggestions(topic: str, platform: str = "tiktok") -> List[str]:
    """Generate hashtag suggestions based on topic and platform"""
    base_hashtags = {
        "tiktok": ["#fyp", "#foryou", "#viral", "#tiktok"],
        "instagram": ["#explore", "#reels", "#viral", "#instagram"],
        "youtube": ["#shorts", "#trending", "#viral", "#youtube"]
    }

    topic_words = topic.lower().split()
    topic_tags = [f"#{word}" for word in topic_words[:3]]

    return base_hashtags.get(platform, []) + topic_tags


# ============= EXPORT FUNCTIONS =============

__all__ = [
    'NotionClient',
    'search_web',
    'get_trending_topics',
    'TikTokAPI',
    'make_http_request',
    'save_idea_to_notion',
    'search_trends_for_idea',
    'get_hashtag_suggestions'
]
