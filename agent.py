"""
Video Creator Agent v3.0 - AI Assistant for Content Creators
Supports: TikTok, Instagram Reels, Xiaohongshu, YouTube Shorts

Core Features:
- Idea management with tags and filtering
- AI-powered script generation
- Project organization and file management
- Usage statistics and analytics

NEW in v3.0:
- AI Generation: Viral titles, descriptions, thumbnails, SEO optimization
- Content Management: Export/import, templates, content planning, history search
- External Data: Trending hashtags, best posting times
- Enhanced error handling with retry mechanism
- Beautiful CLI output with colors and progress
"""

import os
import sys
import json
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict

# Fix UTF-8 encoding on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# ============= LOAD .ENV FILE =============
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

# ============= MCP INTEGRATION =============
try:
    from mcp_tools import TAVILY_TOOLS, web_search, extract_webpage, get_tavily_tools, cleanup_tavily_client
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("⚠️  MCP tools not available. Install mcp package for web search features.")

# ============= CONFIGURATION =============
BASE_DIR = Path(__file__).parent
IDEAS_FILE = BASE_DIR / "ideas" / "ideas.json"
HISTORY_FILE = BASE_DIR / "history" / "activity_log.json"
STATS_FILE = BASE_DIR / "history" / "statistics.json"
PROJECTS_DIR = BASE_DIR / "projects"
SCRIPTS_DIR = BASE_DIR / "scripts"

# Platform-specific configurations
PLATFORM_CONFIGS = {
    "tiktok": {
        "name": "TikTok",
        "duration": "15-60s",
        "style": "Trendy, fast-paced, energetic",
        "hook": "Must grab attention in 1 second",
        "tips": "Use trending sounds, quick cuts, text overlays",
        "hashtags": "#fyp #foryou #viral",
        "emoji": "🎵"
    },
    "instagram": {
        "name": "Instagram Reels",
        "duration": "15-90s",
        "style": "Aesthetic, polished, visual",
        "hook": "Visual appeal + clear value proposition",
        "tips": "High quality visuals, captions, consistent aesthetic",
        "hashtags": "#reels #explore #viral",
        "emoji": "📸"
    },
    "xiaohongshu": {
        "name": "小红书 (Xiaohongshu)",
        "duration": "30-180s",
        "style": "Lifestyle, authentic, storytelling",
        "hook": "Personal story + relatable moment",
        "tips": "Be authentic, show daily life, share tips",
        "hashtags": "#小红书 #分享 #生活",
        "emoji": "📕"
    },
    "youtube_shorts": {
        "name": "YouTube Shorts",
        "duration": "15-60s",
        "style": "SEO-focused, informative, engaging",
        "hook": "Clear value proposition + keyword optimization",
        "tips": "Optimize title, use keywords, strong CTA",
        "hashtags": "#shorts #youtubeshorts #trending",
        "emoji": "🎬"
    }
}

# ANSI Color codes for beautiful output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ============= STATISTICS TRACKING =============
@dataclass
class Statistics:
    total_runs: int = 0
    successful_runs: int = 0
    failed_runs: int = 0
    tool_calls: Dict[str, int] = None
    total_duration: float = 0.0
    last_run: str = None

    def __post_init__(self):
        if self.tool_calls is None:
            self.tool_calls = {}

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

def load_statistics() -> Statistics:
    """Load usage statistics from file"""
    try:
        if STATS_FILE.exists():
            with open(STATS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return Statistics.from_dict(data)
    except Exception:
        pass
    return Statistics()

def save_statistics(stats: Statistics):
    """Save usage statistics to file"""
    STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats.to_dict(), f, indent=2, ensure_ascii=False)

# ============= ERROR HANDLING & RETRY =============
class AgentError(Exception):
    """Base exception for agent errors"""
    pass

def retry_with_backoff(
    func,
    max_retries: int = 3,
    base_delay: float = 1.0,
    backoff_factor: float = 2.0
):
    """Retry function with exponential backoff"""
    last_error = None

    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                delay = base_delay * (backoff_factor ** attempt)
                print(f"{Colors.YELLOW}⚠️  Retry {attempt + 1}/{max_retries} after {delay:.1f}s{Colors.END}")
                time.sleep(delay)
            else:
                print(f"{Colors.RED}❌ Max retries reached{Colors.END}")

    raise last_error

def validate_input(data: dict, required_fields: list) -> bool:
    """Validate required input fields"""
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValueError(f"Missing required field: {field}")
    return True

def safe_execute(func, *args, **kwargs):
    """Safely execute function with error handling"""
    try:
        return func(*args, **kwargs), None
    except Exception as e:
        return None, str(e)

# ============= OPENAI CLIENT =============
client = None

def get_client():
    """Get or create OpenAI client"""
    global client
    if client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise AgentError("OPENAI_API_KEY not found in environment variables")

        client = OpenAI(
            api_key=api_key,
            base_url=os.environ.get("OPENAI_BASE_URL")
        )
    return client

# ============= ENHANCED LOGGING =============
def log_action(action: str, details: dict, success: bool = True):
    """Enhanced logging with success/failure tracking"""
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = []

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
            "success": success
        }

        history.append(log_entry)

        # Keep only last 1000 entries
        history = history[-1000:]

        # Create directory if not exists
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"{Colors.YELLOW}⚠️  Logging error: {e}{Colors.END}")

def update_tool_stats(tool_name: str, success: bool = True):
    """Update tool usage statistics"""
    stats = load_statistics()
    if tool_name not in stats.tool_calls:
        stats.tool_calls[tool_name] = 0
    if success:
        stats.tool_calls[tool_name] += 1
    save_statistics(stats)

# ============= PRETTY PRINTING =============
def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def print_tool_call(tool_name: str, args: dict):
    """Print tool call with formatting"""
    args_str = json.dumps(args, ensure_ascii=False)
    print(f"{Colors.CYAN}   → {tool_name}({args_str}){Colors.END}")

def print_tool_result(result: str, success: bool = True):
    """Print tool result with formatting"""
    if success:
        preview = result[:100] + '...' if len(result) > 100 else result
        print(f"{Colors.GREEN}   ← {preview}{Colors.END}\n")
    else:
        print(f"{Colors.RED}   ← {result}{Colors.END}\n")

def print_platform_banner(platform: str):
    """Print platform-specific banner"""
    config = PLATFORM_CONFIGS.get(platform, PLATFORM_CONFIGS["tiktok"])
    print(f"\n{Colors.BOLD}{config['emoji']} {config['name']}{Colors.END}")
    print(f"{Colors.CYAN}Duration: {config['duration']}{Colors.END}")
    print(f"{Colors.CYAN}Style: {config['style']}{Colors.END}")

def show_statistics(stats: Statistics):
    """Display usage statistics"""
    print(f"\n{Colors.BOLD}📊 Usage Statistics{Colors.END}")
    print(f"{Colors.CYAN}{'─'*40}{Colors.END}")

    if stats.total_runs > 0:
        success_rate = (stats.successful_runs / stats.total_runs) * 100
        avg_duration = stats.total_duration / stats.total_runs
        print(f"Total runs: {stats.total_runs}")
        print(f"Success rate: {success_rate:.1f}%")
        print(f"Avg duration: {avg_duration:.2f}s")
    else:
        print("No statistics yet")

    if stats.tool_calls:
        print(f"\n{Colors.BOLD}Tool Usage:{Colors.END}")
        for tool, count in sorted(stats.tool_calls.items(), key=lambda x: x[1], reverse=True):
            print(f"  {tool}: {count} calls")

    print(f"{Colors.CYAN}{'─'*40}{Colors.END}\n")

# ============= ENHANCED TOOLS DEFINITION =============
tools = [
    {
        "type": "function",
        "function": {
            "name": "save_idea",
            "description": "Save a video idea with title, description, tags and platform. Validates input and prevents duplicates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Catchy idea title (min 3 chars)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of the idea"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Tags for categorization (e.g., ['lifestyle', 'productivity'])"
                    },
                    "platform": {
                        "type": "string",
                        "enum": ["tiktok", "instagram", "xiaohongshu", "youtube_shorts"],
                        "description": "Target platform"
                    }
                },
                "required": ["title", "description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_ideas",
            "description": "List all saved ideas with filtering options. Shows platform, tags, and creation date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "platform": {"type": "string", "description": "Filter by platform"},
                    "tag": {"type": "string", "description": "Filter by tag"},
                    "limit": {"type": "integer", "description": "Limit results (default: all)"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_script",
            "description": "Generate an engaging, platform-specific video script using AI. Includes hook, main content, CTA, and hashtags.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Topic or idea for the script"},
                    "platform": {
                        "type": "string",
                        "description": "Target platform (affects style and format)"
                    },
                    "duration": {
                        "type": "string",
                        "description": "Target duration (e.g., '15 seconds', '30 seconds', '60 seconds')"
                    },
                    "tone": {
                        "type": "string",
                        "description": "Tone of the script (e.g., 'energetic', 'calm', 'funny')"
                    }
                },
                "required": ["topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_script",
            "description": "Save generated script to file system with auto-naming if needed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Script filename (auto-generated if not provided)"},
                    "content": {"type": "string", "description": "Script content to save"},
                    "is_final": {"type": "boolean", "description": "Save to final/ (true) or drafts/ (false)"}
                },
                "required": ["content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_project",
            "description": "Create a new video project with organized folder structure (raw, edited, final) and metadata.",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_name": {"type": "string", "description": "Name of the project (will be sanitized)"},
                    "description": {"type": "string", "description": "Project description or concept"}
                },
                "required": ["project_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "organize_video_file",
            "description": "Copy and organize video file to appropriate project folder. Updates project metadata.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_path": {"type": "string", "description": "Path to source video file"},
                    "project_name": {"type": "string", "description": "Target project name"},
                    "file_type": {
                        "type": "string",
                        "enum": ["raw", "edited", "final"],
                        "description": "Type of video file"
                    }
                },
                "required": ["source_path", "project_name", "file_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_projects",
            "description": "List all projects with detailed statistics including file counts and status.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "show_stats",
            "description": "Display usage statistics and analytics including tool usage and success rates.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_titles",
            "description": "Generate viral, clickbait video titles using AI. Creates multiple title options optimized for clicks and engagement.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Video topic or subject"},
                    "platform": {"type": "string", "description": "Target platform for title optimization"},
                    "count": {"type": "integer", "description": "Number of titles to generate (default: 5)"}
                },
                "required": ["topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_description",
            "description": "Generate engaging social media post descriptions with hashtags and call-to-action.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Video topic or subject"},
                    "platform": {"type": "string", "description": "Target platform"},
                    "tone": {"type": "string", "description": "Tone of description (engaging, professional, funny, etc.)"}
                },
                "required": ["topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_thumbnails_ideas",
            "description": "Generate creative thumbnail concepts with visual descriptions, colors, and design elements.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Video topic for thumbnail"},
                    "platform": {"type": "string", "description": "Target platform"},
                    "count": {"type": "integer", "description": "Number of thumbnail concepts (default: 3)"}
                },
                "required": ["topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "optimize_seo",
            "description": "Optimize content for SEO with keywords, tags, and trending topics for better discoverability.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Content to optimize"},
                    "platform": {"type": "string", "description": "Target platform"},
                    "keywords": {"type": "array", "items": {"type": "string"}, "description": "Keywords to focus on"}
                },
                "required": ["content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_content_plan",
            "description": "Generate a content calendar with daily video ideas, posting times, and engagement strategies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "niche": {"type": "string", "description": "Content niche or category"},
                    "platform": {"type": "string", "description": "Target platform"},
                    "days": {"type": "integer", "description": "Number of days to plan (default: 7)"}
                },
                "required": ["niche"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "export_ideas",
            "description": "Export all saved ideas to a JSON file for backup or sharing.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Export filename (auto-generated if not provided)"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "import_ideas",
            "description": "Import ideas from a JSON file. Can merge with existing ideas or replace them.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_path": {"type": "string", "description": "Path to JSON file to import"},
                    "merge": {"type": "boolean", "description": "Merge with existing ideas (true) or replace (false)"}
                },
                "required": ["source_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_script_template",
            "description": "Save a script as a reusable template for future use.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Template name"},
                    "content": {"type": "string", "description": "Script content to save as template"},
                    "platform": {"type": "string", "description": "Platform this template is for"}
                },
                "required": ["name", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_history",
            "description": "Search through agent activity history to find past actions and results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "integer", "description": "Maximum results to return (default: 10)"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_trending_hashtags",
            "description": "Get trending and relevant hashtags for a platform and niche.",
            "parameters": {
                "type": "object",
                "properties": {
                    "platform": {"type": "string", "description": "Target platform"},
                    "niche": {"type": "string", "description": "Content niche or category"},
                    "count": {"type": "integer", "description": "Number of hashtags (default: 10)"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_best_post_time",
            "description": "Analyze and recommend the best posting times based on platform and audience demographics.",
            "parameters": {
                "type": "object",
                "properties": {
                    "platform": {"type": "string", "description": "Target platform"},
                    "audience": {"type": "string", "description": "Target audience description (e.g., 'young adults', 'professionals')"}
                }
            }
        }
    }
]

# Add MCP tools if available
if MCP_AVAILABLE:
    tools.extend(TAVILY_TOOLS)

# ============= ENHANCED TOOL IMPLEMENTATIONS =============

def save_idea(title: str, description: str, tags: Optional[List[str]] = None, platform: str = "tiktok") -> str:
    """Save a video idea with validation and duplicate check"""
    try:
        # Validate input
        validate_input({"title": title, "description": description}, ["title", "description"])

        if len(title) < 3:
            raise ValueError("Title must be at least 3 characters long")

        # Load existing ideas
        try:
            with open(IDEAS_FILE, 'r', encoding='utf-8') as f:
                ideas = json.load(f)
        except:
            ideas = []

        # Check for duplicates
        for idea in ideas:
            if idea["title"].lower() == title.lower() and idea["platform"] == platform:
                return f"⚠️  Idea '{title}' already exists for {platform}!"

        # Create new idea
        idea = {
            "id": len(ideas) + 1,
            "title": title.strip(),
            "description": description.strip(),
            "tags": [tag.strip() for tag in (tags or [])],
            "platform": platform,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }

        ideas.append(idea)

        # Save to file
        IDEAS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(IDEAS_FILE, 'w', encoding='utf-8') as f:
            json.dump(ideas, f, indent=2, ensure_ascii=False)

        log_action("save_idea", {"title": title, "platform": platform, "tags": len(tags or [])}, success=True)
        update_tool_stats("save_idea", success=True)

        return f"✅ Idea saved: '{title}' for {platform} with {len(tags or [])} tags"

    except Exception as e:
        log_action("save_idea", {"title": title, "error": str(e)}, success=False)
        update_tool_stats("save_idea", success=False)
        return f"❌ Error saving idea: {str(e)}"

def list_ideas(platform: Optional[str] = None, tag: Optional[str] = None, limit: Optional[int] = None) -> str:
    """List and filter ideas with pagination support"""
    try:
        with open(IDEAS_FILE, 'r', encoding='utf-8') as f:
            ideas = json.load(f)
    except:
        return "No ideas found. Create your first idea!"

    # Apply filters
    if platform:
        ideas = [i for i in ideas if i.get("platform") == platform]
    if tag:
        ideas = [i for i in ideas if tag.lower() in [t.lower() for t in i.get("tags", [])]]

    if not ideas:
        return f"No ideas found matching criteria (platform: {platform}, tag: {tag})"

    # Apply limit
    if limit and limit < len(ideas):
        ideas = ideas[:limit]

    result = f"\n📝 Found {len(ideas)} idea(s):\n\n"
    for idea in ideas:
        config = PLATFORM_CONFIGS.get(idea['platform'], PLATFORM_CONFIGS["tiktok"])
        result += f"  [{idea['id']}] {idea['title']}\n"
        result += f"      {config['emoji']} Platform: {idea['platform']} | Tags: {', '.join(idea['tags'])}\n"
        result += f"      Created: {idea['created_at'][:10]}\n\n"

    log_action("list_ideas", {"count": len(ideas)}, success=True)
    return result

def create_script(topic: str, platform: str = "tiktok", duration: str = "30 seconds", tone: str = "energetic") -> str:
    """Generate an AI-powered script with platform-specific optimization"""
    try:
        config = PLATFORM_CONFIGS.get(platform, PLATFORM_CONFIGS["tiktok"])

        # Enhanced system prompt
        system_prompt = f"""You are an expert script writer for {config['name']} videos.

Platform Characteristics:
- Duration: {config['duration']}
- Style: {config['style']}
- Hook Strategy: {config['hook']}
- Best Practices: {config['tips']}

Your scripts must be:
1. Attention-grabbing from the first second
2. Optimized for the platform's unique style
3. Include clear call-to-action
4. Use platform-appropriate language and format

Script Structure:
🎯 HOOK (first 1-2 seconds): Grab attention immediately
📬 MAIN CONTENT: Deliver value concisely and engagingly
📢 CALL-TO-ACTION: Clear, specific next step
# HASHTAGS: 5-8 relevant hashtags including {config['hashtags']}"""

        # Enhanced user prompt
        user_prompt = f"""Create a {duration} {tone} video script about: {topic}

Requirements:
- Platform: {config['name']}
- Tone: {tone}
- Target duration: {duration}

Include:
1. Visual/scene descriptions in [brackets]
2. Spoken dialogue or voiceover
3. Text overlays timing
4. Music/sound suggestions
5. Recommended hashtags

Make it engaging, shareable, and optimized for {config['name']}'s algorithm!"""

        # Call OpenAI with retry
        def generate_script():
            api_client = get_client()
            response = api_client.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=1500
            )
            return response.choices[0].message.content

        script = retry_with_backoff(generate_script, max_retries=3)

        log_action("create_script", {
            "topic": topic,
            "platform": platform,
            "duration": duration
        }, success=True)

        update_tool_stats("create_script", success=True)

        # Add platform banner to output
        result = f"\n{config['emoji']} Script generated for {config['name']}\n"
        result += f"{'─'*50}\n"
        result += script
        result += f"\n{'─'*50}\n"
        return result

    except Exception as e:
        log_action("create_script", {"topic": topic, "error": str(e)}, success=False)
        update_tool_stats("create_script", success=False)
        return f"❌ Error generating script: {str(e)}"

def save_script(content: str, filename: Optional[str] = None, is_final: bool = False) -> str:
    """Save script with auto-generated filename if needed"""
    try:
        folder = "final" if is_final else "drafts"
        script_dir = SCRIPTS_DIR / folder
        script_dir.mkdir(parents=True, exist_ok=True)

        # Auto-generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"script_{timestamp}.txt"

        # Ensure .txt extension
        if not filename.endswith('.txt'):
            filename += '.txt'

        script_path = script_dir / filename

        # Save content
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)

        log_action("save_script", {"filename": filename, "folder": folder}, success=True)
        update_tool_stats("save_script", success=True)

        return f"✅ Script saved to: {script_path}"

    except Exception as e:
        log_action("save_script", {"error": str(e)}, success=False)
        update_tool_stats("save_script", success=False)
        return f"❌ Error saving script: {str(e)}"

def create_project(project_name: str, description: str = "") -> str:
    """Create a new video project with organized folders"""
    try:
        # Sanitize project name
        safe_name = "".join(c for c in project_name if c.isalnum() or c in (' ', '-', '_')).strip()
        if not safe_name:
            raise ValueError("Project name cannot be empty or only special characters")

        project_path = PROJECTS_DIR / safe_name

        if project_path.exists():
            return f"⚠️  Project '{safe_name}' already exists!"

        # Create folder structure
        folders = ["raw", "edited", "final"]
        for folder in folders:
            (project_path / folder).mkdir(parents=True, exist_ok=True)

        # Create metadata
        metadata = {
            "name": safe_name,
            "description": description.strip(),
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "files": {
                "raw": [],
                "edited": [],
                "final": []
            },
            "statistics": {
                "total_files": 0,
                "last_updated": datetime.now().isoformat()
            }
        }

        with open(project_path / "metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        log_action("create_project", {"project_name": safe_name}, success=True)
        update_tool_stats("create_project", success=True)

        return f"✅ Project created: '{safe_name}'\n   Folders: {', '.join(folders)}\n   Path: {project_path}"

    except Exception as e:
        log_action("create_project", {"error": str(e)}, success=False)
        update_tool_stats("create_project", success=False)
        return f"❌ Error creating project: {str(e)}"

def organize_video_file(source_path: str, project_name: str, file_type: str) -> str:
    """Organize video file with validation and metadata update"""
    try:
        source = Path(source_path).resolve()
        project_path = PROJECTS_DIR / project_name

        # Validate inputs
        if not source.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")

        if not project_path.exists():
            raise FileNotFoundError(f"Project not found: {project_name}")

        if file_type not in ["raw", "edited", "final"]:
            raise ValueError(f"Invalid file_type: {file_type}")

        dest_folder = project_path / file_type
        dest_path = dest_folder / source.name

        # Check if file already exists
        if dest_path.exists():
            return f"⚠️  File '{source.name}' already exists in {project_name}/{file_type}/"

        # Copy file
        shutil.copy2(source, dest_path)

        # Update metadata
        metadata_path = project_path / "metadata.json"
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        metadata["files"][file_type].append({
            "filename": source.name,
            "added_at": datetime.now().isoformat(),
            "size": source.stat().st_size
        })

        metadata["statistics"]["total_files"] += 1
        metadata["statistics"]["last_updated"] = datetime.now().isoformat()

        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        log_action("organize_video_file", {
            "project": project_name,
            "file_type": file_type,
            "filename": source.name
        }, success=True)

        update_tool_stats("organize_video_file", success=True)

        return f"✅ File organized: '{source.name}' → {project_name}/{file_type}/"

    except Exception as e:
        log_action("organize_video_file", {"error": str(e)}, success=False)
        update_tool_stats("organize_video_file", success=False)
        return f"❌ Error organizing file: {str(e)}"

def list_projects() -> str:
    """List all projects with detailed statistics"""
    try:
        if not PROJECTS_DIR.exists():
            return "No projects yet. Create your first project!"

        projects = [d for d in PROJECTS_DIR.iterdir() if d.is_dir()]

        if not projects:
            return "No projects yet."

        result = f"\n🎬 Found {len(projects)} project(s):\n\n"

        for project in sorted(projects):
            metadata_path = project / "metadata.json"
            if metadata_path.exists():
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)

                raw_count = len(metadata['files']['raw'])
                edited_count = len(metadata['files']['edited'])
                final_count = len(metadata['files']['final'])

                result += f"  📁 {metadata['name']}\n"
                result += f"      Status: {metadata['status']}\n"
                result += f"      Files: {Colors.GREEN}Raw: {raw_count}{Colors.END} | {Colors.YELLOW}Edited: {edited_count}{Colors.END} | {Colors.BLUE}Final: {final_count}{Colors.END}\n"
                if metadata.get('description'):
                    result += f"      Description: {metadata['description']}\n"
                result += f"      Created: {metadata['created_at'][:10]}\n\n"

        log_action("list_projects", {"count": len(projects)}, success=True)
        return result

    except Exception as e:
        log_action("list_projects", {"error": str(e)}, success=False)
        return f"❌ Error listing projects: {str(e)}"

def show_stats() -> str:
    """Display usage statistics"""
    try:
        stats = load_statistics()
        show_statistics(stats)
        log_action("show_stats", {}, success=True)
        return "✅ Statistics displayed above"
    except Exception as e:
        return f"❌ Error showing statistics: {str(e)}"

# ============= NEW AI GENERATION TOOLS =============

def generate_titles(topic: str, platform: str = "tiktok", count: int = 5) -> str:
    """Generate viral, clickbait video titles using AI"""
    try:
        config = PLATFORM_CONFIGS.get(platform, PLATFORM_CONFIGS["tiktok"])

        system_prompt = f"""You are a viral content title expert for {config['name']}.

Platform: {config['name']}
Style: {config['style']}
Target: Create titles that grab attention and drive engagement

Title Strategies:
1. Use numbers and specific results
2. Create curiosity gaps
3. Use emotional triggers
4. Include platform-specific keywords
5. Keep it short and punchy
6. Use power words (amazing, incredible, secret, etc.)"""

        user_prompt = f"""Generate {count} viral video titles for: {topic}

Requirements:
- Platform: {config['name']}
- Each title should be under 60 characters
- Include a mix of: how-to, listicle, shocking, curiosity, and emotional titles
- Make them shareable and clickable
- Avoid clickbait that doesn't deliver

Format as a numbered list with brief explanation for each title."""

        def generate():
            api_client = get_client()
            response = api_client.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.9,
                max_tokens=800
            )
            return response.choices[0].message.content

        titles = retry_with_backoff(generate, max_retries=2)

        log_action("generate_titles", {"topic": topic, "platform": platform, "count": count}, success=True)
        update_tool_stats("generate_titles", success=True)

        result = f"\n{config['emoji']} {count} Viral Titles for {config['name']}\n"
        result += f"{'='*60}\n"
        result += titles
        result += f"\n{'='*60}\n"
        return result

    except Exception as e:
        log_action("generate_titles", {"error": str(e)}, success=False)
        update_tool_stats("generate_titles", success=False)
        return f"❌ Error generating titles: {str(e)}"

def generate_description(topic: str, platform: str = "tiktok", tone: str = "engaging") -> str:
    """Generate social media post descriptions with hashtags"""
    try:
        config = PLATFORM_CONFIGS.get(platform, PLATFORM_CONFIGS["tiktok"])

        system_prompt = f"""You are a social media copywriting expert for {config['name']}.

Platform: {config['name']}
Best practices: {config['tips']}

Create descriptions that:
1. Hook readers in the first line
2. Provide value or entertainment
3. Include relevant hashtags
4. Have clear call-to-action
5. Match the platform's tone and style"""

        user_prompt = f"""Write a {tone} social media description for a video about: {topic}

Requirements:
- Platform: {config['name']}
- Tone: {tone}
- Length: 150-300 characters
- Include 5-10 relevant hashtags including {config['hashtags']}
- Add engaging call-to-action
- Use emojis appropriately
- Make it shareable"""

        def generate():
            api_client = get_client()
            response = api_client.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=500
            )
            return response.choices[0].message.content

        description = retry_with_backoff(generate, max_retries=2)

        log_action("generate_description", {"topic": topic, "platform": platform}, success=True)
        update_tool_stats("generate_description", success=True)

        result = f"\n{config['emoji']} Description for {config['name']}\n"
        result += f"{'='*60}\n"
        result += description
        result += f"\n{'='*60}\n"
        return result

    except Exception as e:
        log_action("generate_description", {"error": str(e)}, success=False)
        update_tool_stats("generate_description", success=False)
        return f"❌ Error generating description: {str(e)}"

def generate_thumbnails_ideas(topic: str, platform: str = "tiktok", count: int = 3) -> str:
    """Generate creative thumbnail ideas with visual descriptions"""
    try:
        config = PLATFORM_CONFIGS.get(platform, PLATFORM_CONFIGS["tiktok"])

        system_prompt = f"""You are a visual design expert for {config['name']} thumbnails.

Platform: {config['name']}
Style: {config['style']}

Create thumbnail concepts that:
1. Grab attention immediately
2. Clearly communicate the video topic
3. Use colors, faces, and text effectively
4. Follow platform best practices
5. Drive clicks and engagement"""

        user_prompt = f"""Design {count} thumbnail concepts for: {topic}

For each thumbnail, describe:
- Main visual/imagery
- Color scheme
- Text overlay (if any)
- Facial expression or focal point
- Composition/layout
- Why this design works

Make them visually striking and platform-appropriate."""

        def generate():
            api_client = get_client()
            response = api_client.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.85,
                max_tokens=1000
            )
            return response.choices[0].message.content

        thumbnails = retry_with_backoff(generate, max_retries=2)

        log_action("generate_thumbnails_ideas", {"topic": topic, "platform": platform}, success=True)
        update_tool_stats("generate_thumbnails_ideas", success=True)

        result = f"\n🎨 {count} Thumbnail Concepts for {config['name']}\n"
        result += f"{'='*60}\n"
        result += thumbnails
        result += f"\n{'='*60}\n"
        return result

    except Exception as e:
        log_action("generate_thumbnails_ideas", {"error": str(e)}, success=False)
        update_tool_stats("generate_thumbnails_ideas", success=False)
        return f"❌ Error generating thumbnail ideas: {str(e)}"

def optimize_seo(content: str, platform: str = "youtube_shorts", keywords: Optional[List[str]] = None) -> str:
    """Optimize content for SEO with keywords and trending topics"""
    try:
        config = PLATFORM_CONFIGS.get(platform, PLATFORM_CONFIGS["youtube_shorts"])

        system_prompt = f"""You are an SEO expert for {config['name']}.

Platform: {config['name']}
Focus: {config['tips']}

SEO optimization includes:
1. Keyword placement and density
2. Trending topic integration
3. Search volume optimization
4. Engagement optimization
5. Platform algorithm optimization"""

        keyword_str = ", ".join(keywords) if keywords else "auto-detect"

        user_prompt = f"""Optimize this content for SEO on {config['name']}

Content: {content}
Keywords: {keyword_str}

Provide:
1. Optimized title
2. Keyword-enhanced description
3. Recommended tags (10-15)
4. SEO score and suggestions
5. Trending topic opportunities"""

        def generate():
            api_client = get_client()
            response = api_client.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content

        seo_optimized = retry_with_backoff(generate, max_retries=2)

        log_action("optimize_seo", {"platform": platform, "keywords": keyword_str}, success=True)
        update_tool_stats("optimize_seo", success=True)

        result = f"\n🔍 SEO Optimization for {config['name']}\n"
        result += f"{'='*60}\n"
        result += seo_optimized
        result += f"\n{'='*60}\n"
        return result

    except Exception as e:
        log_action("optimize_seo", {"error": str(e)}, success=False)
        update_tool_stats("optimize_seo", success=False)
        return f"❌ Error optimizing SEO: {str(e)}"

# ============= CONTENT MANAGEMENT TOOLS =============

def generate_content_plan(niche: str, platform: str = "tiktok", days: int = 7) -> str:
    """Generate a content calendar with daily video ideas"""
    try:
        config = PLATFORM_CONFIGS.get(platform, PLATFORM_CONFIGS["tiktok"])

        system_prompt = f"""You are a content strategist for {config['name']} creators.

Platform: {config['name']}
Best posting times and content types for maximum engagement.

Create content plans that:
1. Mix different content formats
2. Maintain consistency
3. Build audience loyalty
4. Follow platform trends
5. Include variety to avoid fatigue"""

        user_prompt = f"""Create a {days}-day content plan for: {niche}

Platform: {config['name']}

For each day, provide:
- Content type (tutorial, trend, story, etc.)
- Video topic/idea
- Best posting time
- Hashtag suggestions
- Engagement strategy

Make it practical, varied, and achievable."""

        def generate():
            api_client = get_client()
            response = api_client.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=2000
            )
            return response.choices[0].message.content

        content_plan = retry_with_backoff(generate, max_retries=2)

        log_action("generate_content_plan", {"niche": niche, "platform": platform, "days": days}, success=True)
        update_tool_stats("generate_content_plan", success=True)

        result = f"\n📅 {days}-Day Content Plan for {niche} on {config['name']}\n"
        result += f"{'='*60}\n"
        result += content_plan
        result += f"\n{'='*60}\n"
        return result

    except Exception as e:
        log_action("generate_content_plan", {"error": str(e)}, success=False)
        update_tool_stats("generate_content_plan", success=False)
        return f"❌ Error generating content plan: {str(e)}"

def export_ideas(filename: Optional[str] = None) -> str:
    """Export all ideas to JSON file"""
    try:
        # Load ideas
        try:
            with open(IDEAS_FILE, 'r', encoding='utf-8') as f:
                ideas = json.load(f)
        except:
            return "❌ No ideas to export"

        if not ideas:
            return "❌ No ideas to export"

        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ideas_export_{timestamp}.json"

        export_path = BASE_DIR / "exports" / filename
        export_path.parent.mkdir(parents=True, exist_ok=True)

        # Export with metadata
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "total_ideas": len(ideas),
            "ideas": ideas
        }

        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        log_action("export_ideas", {"count": len(ideas), "filename": filename}, success=True)
        update_tool_stats("export_ideas", success=True)

        return f"✅ Exported {len(ideas)} ideas to: {export_path}"

    except Exception as e:
        log_action("export_ideas", {"error": str(e)}, success=False)
        update_tool_stats("export_ideas", success=False)
        return f"❌ Error exporting ideas: {str(e)}"

def import_ideas(source_path: str, merge: bool = True) -> str:
    """Import ideas from JSON file"""
    try:
        source = Path(source_path).resolve()

        if not source.exists():
            return f"❌ File not found: {source_path}"

        # Load import file
        with open(source, 'r', encoding='utf-8') as f:
            import_data = json.load(f)

        if "ideas" in import_data:
            imported_ideas = import_data["ideas"]
        else:
            imported_ideas = import_data if isinstance(import_data, list) else [import_data]

        # Load existing ideas
        try:
            with open(IDEAS_FILE, 'r', encoding='utf-8') as f:
                existing_ideas = json.load(f)
        except:
            existing_ideas = []

        if not merge:
            existing_ideas = []

        # Merge or replace
        added_count = 0
        for idea in imported_ideas:
            # Check for duplicates
            is_duplicate = any(
                i["title"].lower() == idea.get("title", "").lower()
                for i in existing_ideas
            )

            if not is_duplicate:
                idea["id"] = len(existing_ideas) + 1
                idea["imported_at"] = datetime.now().isoformat()
                existing_ideas.append(idea)
                added_count += 1

        # Save
        IDEAS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(IDEAS_FILE, 'w', encoding='utf-8') as f:
            json.dump(existing_ideas, f, indent=2, ensure_ascii=False)

        log_action("import_ideas", {"imported": added_count, "source": source.name}, success=True)
        update_tool_stats("import_ideas", success=True)

        action = "merged" if merge else "imported"
        return f"✅ {action} {added_count} ideas from {source.name} (total: {len(existing_ideas)})"

    except Exception as e:
        log_action("import_ideas", {"error": str(e)}, success=False)
        update_tool_stats("import_ideas", success=False)
        return f"❌ Error importing ideas: {str(e)}"

def create_script_template(name: str, content: str, platform: str = "tiktok") -> str:
    """Save a script as a reusable template"""
    try:
        templates_dir = SCRIPTS_DIR / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)

        # Sanitize template name
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
        template_path = templates_dir / f"{safe_name}.json"

        # Create template structure
        template = {
            "name": safe_name,
            "platform": platform,
            "created_at": datetime.now().isoformat(),
            "content": content,
            "variables": []  # Could extract placeholders
        }

        # Save template
        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)

        log_action("create_script_template", {"name": safe_name, "platform": platform}, success=True)
        update_tool_stats("create_script_template", success=True)

        return f"✅ Template '{safe_name}' saved for {platform}"

    except Exception as e:
        log_action("create_script_template", {"error": str(e)}, success=False)
        update_tool_stats("create_script_template", success=False)
        return f"❌ Error creating template: {str(e)}"

def search_history(query: str, limit: int = 10) -> str:
    """Search through agent activity history"""
    try:
        if not HISTORY_FILE.exists():
            return "No history found"

        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)

        # Search through history
        query_lower = query.lower()
        results = []

        for entry in history:
            # Search in action name
            if query_lower in entry.get("action", "").lower():
                results.append(entry)
                continue

            # Search in details
            details = entry.get("details", {})
            details_str = json.dumps(details, ensure_ascii=False).lower()
            if query_lower in details_str:
                results.append(entry)

        if not results:
            return f"No results found for '{query}'"

        # Sort by timestamp (newest first)
        results.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        # Apply limit
        results = results[:limit]

        # Format results
        output = f"\n🔍 Found {len(results)} result(s) for '{query}':\n\n"
        for i, entry in enumerate(results, 1):
            status = "✅" if entry.get("success", True) else "❌"
            timestamp = entry.get("timestamp", "")[:19].replace("T", " ")
            action = entry.get("action", "unknown")
            details = entry.get("details", {})

            output += f"{status} [{i}] {timestamp}\n"
            output += f"    Action: {action}\n"
            output += f"    Details: {json.dumps(details, ensure_ascii=False)[:100]}...\n\n"

        log_action("search_history", {"query": query, "results": len(results)}, success=True)
        update_tool_stats("search_history", success=True)

        return output

    except Exception as e:
        log_action("search_history", {"error": str(e)}, success=False)
        update_tool_stats("search_history", success=False)
        return f"❌ Error searching history: {str(e)}"

# ============= EXTERNAL DATA TOOLS =============

def get_trending_hashtags(platform: str = "tiktok", niche: Optional[str] = None, count: int = 10) -> str:
    """Get trending hashtags for platform and niche"""
    try:
        config = PLATFORM_CONFIGS.get(platform, PLATFORM_CONFIGS["tiktok"])

        system_prompt = f"""You are a social media trends expert for {config['name']}.

Provide trending, relevant hashtags that:
1. Are currently popular or evergreen
2. Match the content niche
3. Have good engagement potential
4. Are platform-appropriate
5. Mix of broad and specific tags"""

        niche_str = niche if niche else "general content"
        user_prompt = f"""Generate {count} trending hashtags for {config['name']}

Niche: {niche_str}

Include:
- Platform-specific trending tags
- Niche-specific evergreen tags
- Broad discovery tags
- Engagement-focused tags

Format as a comma-separated list with brief explanation of why each tag works."""

        def generate():
            api_client = get_client()
            response = api_client.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            return response.choices[0].message.content

        hashtags = retry_with_backoff(generate, max_retries=2)

        log_action("get_trending_hashtags", {"platform": platform, "niche": niche_str}, success=True)
        update_tool_stats("get_trending_hashtags", success=True)

        result = f"\n#️⃣ {count} Trending Hashtags for {config['name']} ({niche_str})\n"
        result += f"{'='*60}\n"
        result += hashtags
        result += f"\n{'='*60}\n"
        return result

    except Exception as e:
        log_action("get_trending_hashtags", {"error": str(e)}, success=False)
        update_tool_stats("get_trending_hashtags", success=False)
        return f"❌ Error getting trending hashtags: {str(e)}"

def analyze_best_post_time(platform: str = "tiktok", audience: str = "general") -> str:
    """Analyze best posting times based on platform and audience"""
    try:
        config = PLATFORM_CONFIGS.get(platform, PLATFORM_CONFIGS["tiktok"])

        system_prompt = f"""You are a social media analytics expert for {config['name']}.

Provide data-driven posting time recommendations based on:
- Platform peak usage times
- Audience demographics
- Engagement patterns
- Algorithm favorability
- Day-of-week variations"""

        user_prompt = f"""Analyze the best posting times for {config['name']}

Target audience: {audience}

Provide:
- Best days of the week to post
- Optimal time ranges (in multiple timezones)
- Why these times work best
- Special considerations for this audience
- Testing strategies for optimization"""

        def generate():
            api_client = get_client()
            response = api_client.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content

        analysis = retry_with_backoff(generate, max_retries=2)

        log_action("analyze_best_post_time", {"platform": platform, "audience": audience}, success=True)
        update_tool_stats("analyze_best_post_time", success=True)

        result = f"\n⏰ Best Posting Times for {config['name']} (Audience: {audience})\n"
        result += f"{'='*60}\n"
        result += analysis
        result += f"\n{'='*60}\n"
        return result

    except Exception as e:
        log_action("analyze_best_post_time", {"error": str(e)}, success=False)
        update_tool_stats("analyze_best_post_time", success=False)
        return f"❌ Error analyzing best post times: {str(e)}"

# ============= AGENT LOOP =============

available_functions = {
    "save_idea": save_idea,
    "list_ideas": list_ideas,
    "create_script": create_script,
    "save_script": save_script,
    "create_project": create_project,
    "organize_video_file": organize_video_file,
    "list_projects": list_projects,
    "show_stats": show_stats,
    "generate_titles": generate_titles,
    "generate_description": generate_description,
    "generate_thumbnails_ideas": generate_thumbnails_ideas,
    "optimize_seo": optimize_seo,
    "generate_content_plan": generate_content_plan,
    "export_ideas": export_ideas,
    "import_ideas": import_ideas,
    "create_script_template": create_script_template,
    "search_history": search_history,
    "get_trending_hashtags": get_trending_hashtags,
    "analyze_best_post_time": analyze_best_post_time,
    # MCP tools (if available)
    "web_search": web_search if MCP_AVAILABLE else lambda **kwargs: "❌ MCP not available",
    "extract_webpage": extract_webpage if MCP_AVAILABLE else lambda **kwargs: "❌ MCP not available"
}

def run_agent(user_message: str, max_iterations: int = 5) -> str:
    """Enhanced main agent loop with statistics and error handling"""

    start_time = time.time()
    stats = load_statistics()

    try:
        # Enhanced system prompt
        mcp_features = "\nWEB SEARCH (via MCP):\n🌐 web_search - Search the web for current trends and information\n📄 extract_webpage - Extract content from web pages" if MCP_AVAILABLE else ""

        system_prompt = f"""You are a Video Creator Agent v3.0 - an advanced AI assistant for content creators.

SUPPORTED PLATFORMS:
🎵 TikTok - Short, trendy, 15-60s
📸 Instagram Reels - Aesthetic, 15-90s
📕 小红书 (Xiaohongshu) - Lifestyle, 30-180s
🎬 YouTube Shorts - SEO-focused, 15-60s

CORE CAPABILITIES:
💡 Save and organize video ideas with smart tags
📝 Generate platform-specific, engaging scripts
🎬 Create and manage video project structures
📁 Organize video files (raw → edited → final)
📊 Track and display usage statistics

AI GENERATION TOOLS:
🎯 generate_titles - Viral, clickbait titles for any topic
📄 generate_description - Social media descriptions with hashtags
🎨 generate_thumbnails_ideas - Creative thumbnail concepts
🔍 optimize_seo - SEO optimization with keywords and tags
📅 generate_content_plan - Content calendar with daily ideas

CONTENT MANAGEMENT:
📤 export_ideas - Backup all ideas to JSON
📥 import_ideas - Import ideas from JSON file
📋 create_script_template - Save scripts as reusable templates
🔎 search_history - Search past actions and results

EXTERNAL DATA:
#️⃣ get_trending_hashtags - Trending hashtags for platform/niche
⏰ analyze_best_post_time - Best posting times analysis
{mcp_features}

YOUR APPROACH:
- Be concise, helpful, and action-oriented
- Use emojis to make responses engaging
- Validate inputs before processing
- Suggest related actions when appropriate
- Always explain what you're doing and why

WORKFLOWS TO SUGGEST:
When users ask for content creation, suggest: titles → script → description → hashtags
When users ask for planning, suggest: content plan → save ideas → create projects
When users ask for optimization, suggest: SEO → trending hashtags → best post times
When users ask for current trends: suggest: web_search → generate titles based on trends

Remember: You're not just a chatbot - you're an AGENT that takes action!"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]

        print_header("🎬 VIDEO CREATOR AGENT v3.0")
        print(f"{Colors.BOLD}📝 Task:{Colors.END} {user_message}")
        print(f"{Colors.CYAN}{'─'*70}{Colors.END}\n")

        # Agent loop with enhanced output
        for iteration in range(max_iterations):
            print(f"{Colors.YELLOW}🔄 Iteration {iteration + 1}/{max_iterations}{Colors.END}")

            # Call LLM
            def get_llm_response():
                api_client = get_client()
                return api_client.chat.completions.create(
                    model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                    messages=messages,
                    tools=tools
                )

            response = retry_with_backoff(get_llm_response, max_retries=2)
            message = response.choices[0].message
            messages.append(message)

            # Check if agent wants to use tools
            if not message.tool_calls:
                print(f"\n{Colors.GREEN}✅ Task completed!{Colors.END}\n")
                print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
                result = message.content

                # Update statistics
                stats.successful_runs += 1
                stats.total_runs += 1
                stats.last_run = datetime.now().isoformat()
                save_statistics(stats)

                return result

            # Execute tool calls
            print(f"{Colors.BLUE}🔧 Executing {len(message.tool_calls)} tool call(s){Colors.END}\n")

            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print_tool_call(function_name, function_args)

                # Execute function with error handling
                try:
                    function_response = available_functions[function_name](**function_args)
                    print_tool_result(function_response, success=True)
                except Exception as e:
                    function_response = f"Error executing {function_name}: {str(e)}"
                    print_tool_result(function_response, success=False)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": function_response
                })

        # Max iterations reached
        stats.total_runs += 1
        stats.failed_runs += 1
        save_statistics(stats)

        return "⚠️  Max iterations reached. Task may be incomplete."

    except Exception as e:
        stats.total_runs += 1
        stats.failed_runs += 1
        save_statistics(stats)
        return f"❌ Agent error: {str(e)}"

    finally:
        # Update total duration
        duration = time.time() - start_time
        stats = load_statistics()
        stats.total_duration += duration
        save_statistics(stats)

        print(f"\n{Colors.CYAN}⏱️  Completed in {duration:.2f} seconds{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# ============= CLI =============

if __name__ == "__main__":
    print(f"""
{Colors.BOLD}{Colors.CYAN}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║           🎬 VIDEO CREATOR AGENT v3.0 🎬                         ║
║       AI Assistant for Content Creators                         ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.END}
{Colors.GREEN}Supported platforms:{Colors.END} TikTok, Instagram Reels, Xiaohongshu, YouTube Shorts

{Colors.YELLOW}✨ NEW FEATURES:{Colors.END}
  AI Generation: generate_titles, generate_description, optimize_seo
  Content Management: export/import ideas, search_history, content plans
  External Data: trending hashtags, best posting times analysis

{Colors.YELLOW}Examples:{Colors.END}
  * "Generate 5 viral titles for morning routine TikTok"
  * "Create 7-day content plan for fitness niche on Instagram"
  * "Generate description for cooking video with hashtags"
  * "Get trending hashtags for tech niche on YouTube Shorts"
  * "Optimize my video content for SEO with keywords: ai, future"
  * "Export all my ideas to backup"
  * "Search history for 'script' actions"
  * "Analyze best posting times for young adults on TikTok"
    """)

    # Interactive or command-line mode
    if len(sys.argv) < 2:
        print(f"{Colors.CYAN}💡 Interactive mode{Colors.END}")
        task = input(f"\n{Colors.BOLD}🎬 Your task:{Colors.END} ").strip()
    else:
        task = " ".join(sys.argv[1:])

    if task:
        try:
            result = run_agent(task)
            if result:
                print(f"\n{Colors.BOLD}{Colors.GREEN}📋 Result:{Colors.END}")
                print(f"{Colors.CYAN}{'─'*70}{Colors.END}")
                print(result)
                print(f"{Colors.CYAN}{'─'*70}{Colors.END}\n")
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}⚠️  Interrupted by user{Colors.END}\n")
        except Exception as e:
            print(f"\n{Colors.RED}❌ Fatal error: {e}{Colors.END}\n")
    else:
        print(f"{Colors.RED}❌ No task provided. Exiting.{Colors.END}\n")
