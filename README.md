# 🎬 Video Creator Agent

**AI Assistant for Content Creators** - Supporting TikTok, Instagram Reels, 小红书 (Xiaohongshu), and YouTube Shorts

## 🚀 Features

- 💡 **Idea Management** - Save and organize video ideas with tags
- 📝 **Script Generation** - AI-powered platform-specific scripts
- 🎬 **Project Management** - Organize video files (raw → edited → final)
- 📊 **History Tracking** - Complete activity log
- 🌐 **Multi-Platform** - Optimized for different social platforms

## 📋 Requirements

- Python 3.8+
- OpenAI API key

## 🔧 Setup

```bash
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

### Direct Command
```bash
python agent.py "Save idea: morning routine for TikTok"
```

## 💬 Example Commands

```bash
# Ideas
"Save idea: productivity tips for Instagram"
"List all my TikTok ideas"
"Show ideas with tag 'lifestyle'"

# Scripts
"Create a 30 second script about morning routine"
"Write script for Xiaohongshu about travel tips"

# Projects
"Create project called 'Summer Vlog'"
"Show all my projects"
"Organize video.mp4 to project 'Summer Vlog' as raw"
```

## 📁 Project Structure

```
video_creator_agent/
├── ideas/              # Your video ideas
├── scripts/            # Generated scripts
│   ├── drafts/        # Work in progress
│   ├── final/         # Ready to use
│   └── templates/     # Script templates
├── projects/          # Video projects
│   └── project_name/
│       ├── raw/       # Original footage
│       ├── edited/    # Work in progress
│       └── final/     # Completed videos
├── history/           # Activity log
└── agent.py           # Main agent
```

## 🛠️ Agent Tools

| Tool | Description |
|------|-------------|
| `save_idea` | Save idea with title, tags, platform |
| `list_ideas` | Browse and filter ideas |
| `create_script` | Generate AI scripts |
| `save_script` | Save script to file |
| `create_project` | Create new project |
| `organize_video_file` | Move files to project folders |
| `list_projects` | Show all projects |

## 🌟 Supported Platforms

- 🎵 **TikTok** - Short, trendy content (15-60s)
- 📸 **Instagram Reels** - Aesthetic content (15-90s)
- 📕 **小红书** - Lifestyle content (30-180s)
- 🎬 **YouTube Shorts** - SEO-focused (15-60s)

## 📊 What Makes This an AGENT (not just chatbot)?

✅ **Tools** - Can perform actions (save files, create folders)
✅ **Loop** - Multi-step reasoning (think → act → analyze → repeat)
✅ **Memory** - Remembers ideas, projects, history
✅ **Autonomy** - Can complete complex tasks independently

## 🔐 Security

- All files stored locally
- Activity logging for transparency
- Safe file operations with error handling

## 📝 License

MIT License - Feel free to use and modify!

---

**Made with ❤️ for Content Creators**
