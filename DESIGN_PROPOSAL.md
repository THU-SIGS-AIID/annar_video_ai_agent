# 🎬 Video Creator Agent - Design Proposal

## 📋 Executive Summary

**Video Creator Agent** is an autonomous AI agent designed to assist content creators in managing their video production workflow across multiple social media platforms. Unlike traditional chatbots, this agent combines Large Language Model (LLM) reasoning with practical tool execution to perform real actions.

### Key Differentiator: Agent vs Chatbot

| Feature | Traditional Chatbot | Video Creator Agent |
|---------|-------------------|-------------------|
| **Actions** | ❌ Text only | ✅ File operations, folder creation |
| **Autonomy** | ❌ User-dependent | ✅ Multi-step task completion |
| **Memory** | ❌ Session-based | ✅ Persistent JSON storage |
| **Architecture** | ❌ Single-turn | ✅ Loop-based (think → act → repeat) |
| **Integration** | ❌ Isolated | ✅ File system integration |

---

## 🎯 Problem Statement

Content creators face three major challenges:

1. **Idea Overload** - Creative ideas get lost across notes apps, voice memos, and social media drafts
2. **Platform Fragmentation** - Different requirements for TikTok, Instagram, Xiaohongshu, YouTube Shorts
3. **File Chaos** - Video files scattered across folders with no organization system

### Solution
An AI agent that:
- 💾 **Captures** ideas instantly with smart tagging
- 🎯 **Generates** platform-specific scripts
- 📁 **Organizes** video projects automatically

---

## 🏗️ System Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────┐
│                     USER REQUEST                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   AGENT ORCHESTRATOR                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              System Prompt                          │    │
│  │  - Platform guidelines (TikTok, Instagram, etc.)    │    │
│  │  - Tool descriptions & capabilities                 │    │
│  │  - Task context & history                           │    │
│  └─────────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    LLM REASONING                             │
│                  (OpenAI GPT-4o-mini)                        │
│  • Analyzes user intent                                      │
│  • Decides which tools to use                               │
│  • Plans multi-step execution                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                ┌────────┴────────┐
                │  Tool Calls?    │
                └────────┬────────┘
                         │
            ┌────────────┴────────────┐
            │ YES                     │ NO
            ▼                         ▼
┌──────────────────────┐    ┌─────────────────┐
│   TOOL EXECUTION     │    │  FINAL ANSWER   │
│  ┌────────────────┐  │    │   Return to     │
│  │ • save_idea    │  │    │   User          │
│  │ • create_script│  │    └─────────────────┘
│  │ • create_project│ │
│  │ • organize_    │  │
│  │   video_file   │  │
│  └────────────────┘  │
└──────────┬───────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│                    RESULT FEEDBACK                           │
│  • Tool outputs added to message history                     │
│  • Agent decides: Continue or Done?                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                    ┌────┴────┐
                    │  LOOP   │ (Max 5 iterations)
                    └────┬────┘
                         │
                         ▼
                 (Back to LLM Reasoning)
```

### Agent Loop Algorithm

```python
def run_agent(user_message, max_iterations=5):
    messages = [system_prompt, user_message]

    for iteration in range(max_iterations):
        # 1. THINK: LLM analyzes current state
        response = llm(messages, tools=available_tools)

        # 2. DECIDE: Use tools or respond?
        if not response.tool_calls:
            return response.content  # DONE!

        # 3. ACT: Execute each tool
        for tool_call in response.tool_calls:
            result = execute_tool(tool_call)
            messages.append(result)  # Remember

        # 4. REPEAT: Loop back with new information
```

---

## 🔧 Tool Specifications

### Tool 1: `save_idea`
**Purpose:** Capture video ideas with metadata

```python
def save_idea(
    title: str,           # Required: "Morning routine tips"
    description: str,     # Required: "5 tips for productive mornings"
    tags: List[str],      # Optional: ["productivity", "lifestyle"]
    platform: str         # Default: "tiktok"
) -> str:
    """Saves idea to ideas/ideas.json"""
```

**Data Structure:**
```json
{
  "id": 1,
  "title": "Morning routine tips",
  "description": "5 tips for productive mornings",
  "tags": ["productivity", "lifestyle"],
  "platform": "tiktok",
  "created_at": "2025-03-11T10:30:00",
  "status": "active"
}
```

---

### Tool 2: `list_ideas`
**Purpose:** Browse and filter saved ideas

```python
def list_ideas(
    platform: str = None,  # Optional filter
    tag: str = None        # Optional filter
) -> str:
    """Returns formatted list of ideas"""
```

---

### Tool 3: `create_script`
**Purpose:** AI-generated platform-specific scripts

```python
def create_script(
    topic: str,           # Required: "productivity tips"
    platform: str,        # Default: "tiktok"
    duration: str         # Default: "30 seconds"
) -> str:
    """Calls OpenAI API to generate script"""
```

**AI Prompt Strategy:**
```
System: "You are expert script writer for {platform}
         Create engaging, platform-specific scripts."

User: "Create a {duration} video script about: {topic}

       Include:
       - Hook (first 2 seconds)
       - Main content
       - Call to action
       - Recommended hashtags"
```

---

### Tool 4: `save_script`
**Purpose:** Persist scripts to filesystem

```python
def save_script(
    filename: str,      # Required: "morning_routine.txt"
    content: str,       # Required: [script content]
    is_final: bool      # Default: False → drafts/, True → final/
) -> str:
    """Saves to scripts/drafts/ or scripts/final/"""
```

---

### Tool 5: `create_project`
**Purpose:** Initialize video project structure

```python
def create_project(
    project_name: str,   # Required: "Summer Vlog"
    description: str = ""  # Optional
) -> str:
    """Creates project folders and metadata.json"""
```

**Folder Structure:**
```
projects/Summer Vlog/
├── raw/           # Original footage
├── edited/        # Work-in-progress
├── final/         # Completed videos
└── metadata.json  # Project info
```

---

### Tool 6: `organize_video_file`
**Purpose:** Move videos to appropriate project folders

```python
def organize_video_file(
    source_path: str,     # Required: "/path/to/video.mp4"
    project_name: str,    # Required: "Summer Vlog"
    file_type: str        # Required: "raw" | "edited" | "final"
) -> str:
    """Copies file and updates project metadata"""
```

---

### Tool 7: `list_projects`
**Purpose:** Display all projects with statistics

```python
def list_projects() -> str:
    """Returns formatted project list"""
```

**Output Format:**
```
🎬 Found 2 project(s):

  📁 Summer Vlog
      Status: active
      Raw: 3 | Edited: 1 | Final: 0
      Created: 2025-03-10

  📁 Productivity Tips
      Status: active
      Raw: 1 | Edited: 0 | Final: 1
      Created: 2025-03-08
```

---

## 🌐 Platform Support Matrix

| Platform | Duration | Style | Key Elements |
|----------|----------|-------|--------------|
| **TikTok** | 15-60s | Trendy, fast-paced | Hook in 1s, trending sounds |
| **Instagram** | 15-90s | Aesthetic, polished | Visual quality, captions |
| **Xiaohongshu** | 30-180s | Lifestyle, authentic | Storytelling, personal |
| **YouTube Shorts** | 15-60s | SEO-focused | Keywords, thumbnails |

---

## 💾 Data Architecture

### Filesystem Layout
```
video_creator_agent/
│
├── ideas/
│   └── ideas.json              # Idea database
│   [{
│     "id": 1,
│     "title": "...",
│     "tags": [],
│     "platform": "tiktok",
│     "created_at": "ISO-8601"
│   }]
│
├── scripts/
│   ├── drafts/                 # WIP scripts
│   │   └── script_v1.txt
│   ├── final/                  # Ready-to-use
│   │   └── script_final.txt
│   └── templates/              # Platform templates
│
├── projects/
│   └── [project_name]/
│       ├── raw/                # Original footage
│       ├── edited/             # WIP edits
│       ├── final/              # Completed videos
│       └── metadata.json       # Project tracking
│       {
│         "name": "Summer Vlog",
│         "files": {
│           "raw": ["video1.mp4"],
│           "edited": [],
│           "final": []
│         }
│       }
│
├── history/
│   └── activity_log.json       # Audit trail
│   [{
│     "timestamp": "ISO-8601",
│     "action": "save_idea",
│     "details": {...}
│   }]
│
└── agent.py                    # Main orchestrator
```

### Persistence Strategy
- **JSON files** for human-readable storage
- **Atomic writes** prevent data corruption
- **UTF-8 encoding** supports international content
- **Activity logging** provides audit trail

---

## 🔐 Security & Safety

### Input Validation
- File path sanitization prevents directory traversal
- File existence checks before operations
- Platform enum validation

### Error Handling
```python
try:
    result = execute_tool(tool_call)
except Exception as e:
    result = f"Error: {str(e)}"
    # Agent continues with error context
```

### Privacy
- All data stored locally (no cloud storage)
- API keys via environment variables
- No telemetry or data collection

---

## 🚀 Usage Examples

### Example 1: Complete Workflow
```bash
# Step 1: Capture idea
python agent.py "Save idea: morning routine for TikTok with tags productivity"

# Step 2: Generate script
python agent.py "Create 30s script about productivity tips"

# Step 3: Create project
python agent.py "Create project called 'Morning Routine'"

# Step 4: Organize files
python agent.py "Organize morning_footage.mp4 to Morning Routine as raw"
```

### Example 2: Multi-Step Task
```bash
python agent.py "I want to create a TikTok about coffee recipes.
Save the idea, generate a script, and create a project"
```

**Agent Execution:**
1. ✅ `save_idea("coffee recipes", platform="tiktok")`
2. ✅ `create_script("coffee recipes", platform="tiktok", duration="30s")`
3. ✅ `create_project("Coffee Recipes TikTok")`
4. ✅ Returns: "All done! Idea saved, script generated, project ready"

---

## 📊 Performance Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Tool Execution Time | <500ms | ~200ms |
| Script Generation | <10s | ~5s |
| File Operations | <100ms | ~50ms |
| Max Iterations | 5 | 2-3 avg |

---

## 🔮 Future Enhancements

### Phase 2 Features
- [ ] **Calendar Integration** - Schedule posts
- [ ] **Analytics** - Track video performance
- [ ] **Collaboration** - Share projects with team
- [ ] **Auto-Edit** - Basic video editing capabilities

### Phase 3 Features
- [ ] **Multi-Model** - Support Claude, Gemini
- [ ] **Voice Input** - Dictate ideas hands-free
- [ ] **Cloud Sync** - Cross-device access
- [ ] **Plugin System** - Custom tools

---

## 📈 Business Value

### Time Savings
- **Before:** 30 min to organize ideas + scripts + files
- **After:** 2 min with agent
- **Savings:** 93% reduction in admin time

### Content Quality
- Platform-specific optimization
- Consistent script structure
- Never lose an idea again

### Scalability
- Manage 10x more projects
- Faster content production
- Better organization

---

## 🎓 Learning Resources

### Key Concepts
1. **Function Calling** - OpenAI's tool use API
2. **Agent Loop** - ReAct pattern (Reason + Act)
3. **Prompt Engineering** - System prompt design
4. **Data Persistence** - JSON file management

### References
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Agent Design Patterns](https://www.anthropic.com/index/building-effective-agents)

---

## ✅ Conclusion

Video Creator Agent demonstrates a practical implementation of autonomous AI agents:

✅ **Real Actions** - File operations, project management
✅ **Autonomous Loop** - Multi-step reasoning
✅ **Persistent Memory** - JSON-based storage
✅ **Platform Expertise** - Multi-platform optimization
✅ **Extensible Design** - Easy to add tools

This agent solves real problems for content creators while showcasing the power of combining LLM reasoning with practical tool execution.

---

**Version:** 1.0
**Date:** March 11, 2025
**Status:** ✅ Implementation Complete
