# 🎬 Video Creator Agent v3.0

**AI-Powered Assistant for Content Creators** - Supporting TikTok, Instagram Reels, Xiaohongshu, and YouTube Shorts

[![Live Demo](https://img.shields.io/badge/🌐-View_Live_Demo-990C31?style=for-the-badge&logo=vercel&logoColor=white)](https://video-creator-agent.vercel.app)
[![GitHub](https://img.shields.io/badge/📦-Repository-49020A?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AMatved/annar_video_ai_agent)

> **🚀 Live Demo:** [video-creator-agent.vercel.app](https://video-creator-agent.vercel.app) - Explore the interactive website with MCP integration showcase!

## 🚀 Features

### Core Capabilities
- 💡 **Idea Management** - Save and organize video ideas with smart tags
- 📝 **Script Generation** - AI-powered platform-specific scripts
- 🎬 **Project Management** - Organize video files (raw → edited → final)
- 📊 **Analytics** - Usage statistics and activity tracking
- 🌐 **Multi-Platform** - Optimized for 4 major social platforms

### 🆕 New in v3.0

#### AI Generation Tools
- 🎯 **Viral Titles** - Generate clickbait titles optimized for engagement
- 📄 **Social Descriptions** - Create post descriptions with hashtags
- 🎨 **Thumbnail Ideas** - Visual concepts for video thumbnails
- 🔍 **SEO Optimization** - Optimize content for discoverability
- 📅 **Content Planning** - Generate 7-day content calendars

#### Content Management
- 📤 **Export Ideas** - Backup all ideas to JSON
- 📥 **Import Ideas** - Import from JSON files
- 📋 **Script Templates** - Save reusable script templates
- 🔍 **History Search** - Search through all past actions

#### External Data
- #️⃣ **Trending Hashtags** - Get popular hashtags for your niche
- ⏰ **Best Post Times** - Analyze optimal posting schedules

## 📋 Requirements

- Python 3.8+
- OpenAI API key

## 🔧 Setup

```bash
# Clone the repository
git clone https://github.com/THU-SIGS-AIID/annar_video_ai_agent.git
cd annar_video_ai_agent

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-key-here"
export OPENAI_BASE_URL="your-base-url"  # optional
export OPENAI_MODEL="gpt-4o-mini"  # optional
```

## 🎯 Usage

### Interactive Mode
```bash
python agent.py
```

### Command Line
```bash
python agent.py "Save idea: morning routine for TikTok"
```

## 💬 Example Commands

### Core Functions
```bash
# Ideas
python agent.py "Save idea: productivity tips for Instagram with tags lifestyle"
python agent.py "List all my TikTok ideas"
python agent.py "Show ideas with tag 'fitness'"

# Scripts
python agent.py "Create a 30s script about productivity tips"
python agent.py "Write script for Instagram about travel tips"

# Projects
python agent.py "Create project called 'Summer Vlog'"
python agent.py "Show all my projects"
```

### AI Generation (New!)
```bash
# Generate viral titles
python agent.py "Generate 5 viral titles for cooking TikToks"

# Create social descriptions
python agent.py "Generate description for fitness video with hashtags"

# Get thumbnail ideas
python agent.py "Create 3 thumbnail concepts for gaming content"

# SEO optimization
python agent.py "Optimize my video content for SEO with keywords: ai, future"
```

### Content Management (New!)
```bash
# Content planning
python agent.py "Create 7-day content plan for tech niche on YouTube Shorts"

# Export/Import
python agent.py "Export all my ideas to backup"
python agent.py "Import ideas from backup.json"

# Search history
python agent.py "Search history for 'script' actions"
```

### External Data (New!)
```bash
# Trending hashtags
python agent.py "Get trending hashtags for gaming niche on TikTok"

# Best posting times
python agent.py "Analyze best posting times for young adults on Instagram"
```

## 📁 Project Structure

```
video_creator_agent/
├── agent.py              # Main agent with 18 tools
├── config.json           # Configuration
├── requirements.txt      # Dependencies
├── README.md            # Documentation
├── website/             # Presentation website
│   └── index.html       # Landing page
├── DESIGN_PROPOSAL.md   # Architecture documentation
├── ideas/               # Your video ideas
│   └── ideas.json      # Ideas database
├── scripts/            # Generated scripts
│   ├── drafts/        # Work-in-progress
│   ├── final/         # Ready scripts
│   └── templates/     # Script templates
├── projects/          # Video projects
│   └── [project]/
│       ├── raw/       # Original footage
│       ├── edited/    # Work-in-progress
│       └── final/     # Completed videos
└── history/           # Activity tracking
    └── activity_log.json # Agent log
```

## 🛠️ Available Tools (18 Total)

| Tool | Category | Description |
|------|----------|-------------|
| `save_idea` | Core | Save video ideas with tags and platform |
| `list_ideas` | Core | Browse and filter saved ideas |
| `create_script` | Core | Generate AI-powered scripts |
| `save_script` | Core | Save scripts to drafts/final folders |
| `create_project` | Core | Create video project structure |
| `organize_video_file` | Core | Move files to project folders |
| `list_projects` | Core | Show all projects with stats |
| `show_stats` | Core | Display usage statistics |
| `generate_titles` | AI | Create viral video titles |
| `generate_description` | AI | Generate social media descriptions |
| `generate_thumbnails_ideas` | AI | Design thumbnail concepts |
| `optimize_seo` | AI | Optimize content for SEO |
| `generate_content_plan` | Management | Create content calendars |
| `export_ideas` | Management | Backup ideas to JSON |
| `import_ideas` | Management | Import ideas from JSON |
| `create_script_template` | Management | Save script templates |
| `search_history` | Management | Search past actions |
| `get_trending_hashtags` | Data | Get trending hashtags |
| `analyze_best_post_time` | Data | Best posting times analysis |

## 🌟 Supported Platforms

| Platform | Duration | Style | Key Features |
|----------|----------|-------|--------------|
| **TikTok** | 15-60s | Trendy, fast-paced | Hook in 1s, trending sounds |
| **Instagram** | 15-90s | Aesthetic, polished | High quality, captions |
| **Xiaohongshu** | 30-180s | Lifestyle, authentic | Storytelling, personal |
| **YouTube Shorts** | 15-60s | SEO-focused | Keywords, thumbnails |

## 📊 What Makes This an AGENT (Not Chatbot)

| Feature | Chatbot | This Agent |
|---------|---------|------------|
| **Actions** | ❌ Text only | ✅ 18 executable tools |
| **Autonomy** | ❌ User-dependent | ✅ Multi-step reasoning |
| **Memory** | ❌ Session-only | ✅ Persistent storage |
| **Architecture** | ❌ Single-turn | ✅ ReAct loop (think → act → repeat) |
| **Integration** | ❌ Isolated | ✅ File system + AI APIs |

## 🔐 Security & Privacy

- All data stored locally
- No telemetry or data collection
- API keys via environment variables only
- Safe file operations with validation

## 📖 Documentation

- [Design Proposal](DESIGN_PROPOSAL.md) - Architecture and technical details
- [Website](website/index.html) - Interactive demo and features overview

## 🧪 Testing

Run the test suite to verify functionality:
```bash
python test_agent.py
```

## 🤝 Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

## 📝 License

MIT License - See LICENSE file for details

## 🎓 Academic Use

This project was developed as part of the AI Agent Design course at Tsinghua University.

---

**Made with ❤️ for Content Creators**

Powered by OpenAI GPT-4o-mini
