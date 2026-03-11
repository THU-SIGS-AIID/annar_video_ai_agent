# 🔗 INTEGRATIONS GUIDE - Connect Agent to External Services

## 🌐 AVAILABLE INTEGRATIONS

- ✅ **Notion** - Save ideas to databases
- ✅ **Web Search** - Search trends and information
- ✅ **HTTP Requests** - Connect to any API
- ✅ **Social Media** - TikTok, Instagram, YouTube (future)
- ✅ **Trending Topics** - Get platform trends

---

## 1️⃣ NOTION INTEGRATION

### Step 1: Get Notion API Key

1. Go to https://www.notion.so/my-integrations
2. Click "+ New integration"
3. Give it a name: "Video Creator Agent"
4. Select your workspace
5. Copy the **Internal Integration Token**

### Step 2: Create Database in Notion

1. Create a new page in Notion
2. Type `/database` and select "Table database"
3. Add these columns:
   - **Name** (title)
   - **Description** (text)
   - **Tags** (multi-select)
   - **Platform** (select: TikTok, Instagram, YouTube, Xiaohongshu)
   - **Status** (select: Idea, In Progress, Completed)
4. Copy the **Database ID** from the URL:
   - URL format: `https://notion.so/workspace/[DATABASE_ID]?v=...`
   - Copy the 32-character ID after `/`

### Step 3: Configure Agent

Add to `.env` file:

```bash
NOTION_API_KEY=your_internal_integration_token_here
NOTION_DATABASE_ID=your_32_character_database_id
```

### Step 4: Test It

```python
from integrations import save_idea_to_notion

# Save idea to Notion
result = save_idea_to_notion(
    title="Morning Routine Video",
    description="5 morning habits for productivity",
    tags=["productivity", "lifestyle"],
    platform="tiktok"
)
print(result)
```

---

## 2️⃣ WEB SEARCH & TRENDS

### How It Works

Uses DuckDuckGo HTML version (no API key needed!)

### Example Usage

```python
from integrations import search_web, get_trending_topics

# Search the web
results = search_web("TikTok trends 2025")
for result in results:
    print(f"{result['title']}")
    print(f"{result['url']}\n")

# Get trending topics
trends = get_trending_topics("tiktok")
for trend in trends:
    print(f"{trend['topic']} - {trend['views']}")
```

---

## 3️⃣ CONNECT TO ANY API (HTTP)

### Example: Get Weather Data

```python
from integrations import make_http_request

# GET request
weather = make_http_request(
    "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_KEY"
)
print(weather)
```

### Example: Post to Discord Webhook

```python
# POST request
webhook_url = "https://discord.com/api/webhooks/YOUR_WEBHOOK"
data = {
    "content": "New video idea created!",
    "username": "Video Creator Agent"
}

result = make_http_request(webhook_url, method="POST", data=data)
```

---

## 4️⃣ SOCIAL MEDIA APIS (Future)

### TikTok API

1. Apply for access: https://developers.tiktok.com/
2. Get API key
3. Add to `.env`:
   ```bash
   TIKTOK_API_KEY=your_key_here
   ```

### Instagram Graph API

1. Create Facebook App: https://developers.facebook.com/
2. Add Instagram Basic Display
3. Get access token

### YouTube Data API

1. Go to Google Cloud Console
2. Enable YouTube Data API v3
3. Create API key

---

## 🚀 ADDING TOOLS TO AGENT

Add these tools to `agent.py`:

```python
# Add to tools list
{
    "type": "function",
    "function": {
        "name": "search_web",
        "description": "Search the web for information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "num_results": {"type": "integer", "description": "Number of results (default 5)"}
            },
            "required": ["query"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "save_to_notion",
        "description": "Save video idea to Notion database",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Idea title"},
                "description": {"type": "string", "description": "Description"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags"},
                "platform": {"type": "string", "description": "Platform"}
            },
            "required": ["title", "description", "platform"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_trends",
        "description": "Get trending topics for a platform",
        "parameters": {
            "type": "object",
            "properties": {
                "platform": {"type": "string", "enum": ["tiktok", "instagram", "youtube"]}
            },
            "required": ["platform"]
        }
    }
}
```

Add implementations:

```python
def search_web(query, num_results=5):
    from integrations import search_web as web_search
    results = web_search(query, num_results)
    formatted = "\n".join([f"{r['title']}\n{r['url']}" for r in results])
    return formatted

def save_to_notion(title, description, tags=None, platform="tiktok"):
    from integrations import save_idea_to_notion
    result = save_idea_to_notion(title, description, tags or [], platform)
    return f"Saved to Notion: {result.get('id', 'Error')}"

def get_trends(platform):
    from integrations import get_trending_topics
    trends = get_trending_topics(platform)
    return "\n".join([f"{t['topic']} - {t['views']}" for t in trends])
```

Add to `available_functions`:

```python
available_functions = {
    # ... existing functions ...
    "search_web": search_web,
    "save_to_notion": save_to_notion,
    "get_trends": get_trends
}
```

---

## 📝 EXAMPLE COMMANDS

```bash
# Search web for trends
python agent.py "Search web for TikTok trends 2025"

# Save idea to Notion
python agent.py "Save idea to Notion: morning routine for TikTok"

# Get trending hashtags
python agent.py "Get trending hashtags for Instagram"

# Research competitors
python agent.py "Search web for top productivity channels on YouTube"
```

---

## ⚠️ SECURITY NOTES

1. **Never commit .env file** with real API keys
2. **Use environment variables** for all secrets
3. **Rotate API keys** regularly
4. **Limit API permissions** to minimum required
5. **Monitor API usage** to avoid unexpected charges

---

## 🎯 QUICK START

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure `.env`:
   ```bash
   NOTION_API_KEY=your_key
   NOTION_DATABASE_ID=your_id
   ```

3. Test integration:
   ```bash
   python agent.py "Search web for video production tips"
   ```

---

**Need help? Check the integrations.py file for more examples!**
