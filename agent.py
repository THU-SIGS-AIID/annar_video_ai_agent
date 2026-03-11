"""
Video Creator Agent - AI Assistant for Content Creators
Supports: TikTok, Instagram Reels, Xiaohongshu, YouTube Shorts
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# Fix UTF-8 encoding on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# ============= LOAD .ENV FILE =============
from dotenv import load_dotenv
load_dotenv()

# ============= CONFIGURATION =============
BASE_DIR = Path(__file__).parent
IDEAS_FILE = BASE_DIR / "ideas" / "ideas.json"
HISTORY_FILE = BASE_DIR / "history" / "activity_log.json"
PROJECTS_DIR = BASE_DIR / "projects"
SCRIPTS_DIR = BASE_DIR / "scripts"

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_BASE_URL")
)

# ============= TOOLS DEFINITION =============
tools = [
    {
        "type": "function",
        "function": {
            "name": "save_idea",
            "description": "Save a video idea with title, description, tags and platform",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Idea title"},
                    "description": {"type": "string", "description": "Detailed description"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags for categorization"},
                    "platform": {"type": "string", "enum": ["tiktok", "instagram", "xiaohongshu", "youtube_shorts"], "description": "Target platform"}
                },
                "required": ["title", "description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_ideas",
            "description": "List all saved ideas, optionally filter by platform or tags",
            "parameters": {
                "type": "object",
                "properties": {
                    "platform": {"type": "string", "description": "Filter by platform"},
                    "tag": {"type": "string", "description": "Filter by tag"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_script",
            "description": "Generate a video script based on an idea or topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Topic or idea for the script"},
                    "platform": {"type": "string", "description": "Target platform (tiktok, instagram, etc)"},
                    "duration": {"type": "string", "description": "Target duration (e.g., '15 seconds', '30 seconds', '60 seconds')"}
                },
                "required": ["topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_script",
            "description": "Save a script to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Script filename"},
                    "content": {"type": "string", "description": "Script content"},
                    "is_final": {"type": "boolean", "description": "Save to final/ or drafts/"}
                },
                "required": ["filename", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_project",
            "description": "Create a new video project with organized folders",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_name": {"type": "string", "description": "Name of the project"},
                    "description": {"type": "string", "description": "Project description"}
                },
                "required": ["project_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "organize_video_file",
            "description": "Move a video file to appropriate project folder (raw, edited, or final)",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_path": {"type": "string", "description": "Path to source video file"},
                    "project_name": {"type": "string", "description": "Target project name"},
                    "file_type": {"type": "string", "enum": ["raw", "edited", "final"], "description": "Type of video file"}
                },
                "required": ["source_path", "project_name", "file_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_projects",
            "description": "List all projects with their status",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

# ============= TOOL IMPLEMENTATIONS =============

def log_action(action, details):
    """Log agent action to history"""
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
    except:
        history = []

    history.append({
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "details": details
    })

    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def save_idea(title, description, tags=None, platform="tiktok"):
    """Save a video idea"""
    try:
        with open(IDEAS_FILE, 'r', encoding='utf-8') as f:
            ideas = json.load(f)
    except:
        ideas = []

    idea = {
        "id": len(ideas) + 1,
        "title": title,
        "description": description,
        "tags": tags or [],
        "platform": platform,
        "created_at": datetime.now().isoformat(),
        "status": "active"
    }

    ideas.append(idea)

    with open(IDEAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(ideas, f, indent=2, ensure_ascii=False)

    log_action("save_idea", {"title": title, "platform": platform})

    return f"✅ Idea saved: '{title}' for {platform} with {len(tags or [])} tags"

def list_ideas(platform=None, tag=None):
    """List and filter ideas"""
    try:
        with open(IDEAS_FILE, 'r', encoding='utf-8') as f:
            ideas = json.load(f)
    except:
        ideas = []

    if platform:
        ideas = [i for i in ideas if i.get("platform") == platform]
    if tag:
        ideas = [i for i in ideas if tag in i.get("tags", [])]

    if not ideas:
        return "No ideas found. Create your first idea!"

    result = f"\n📝 Found {len(ideas)} idea(s):\n\n"
    for idea in ideas:
        result += f"  [{idea['id']}] {idea['title']}\n"
        result += f"      Platform: {idea['platform']} | Tags: {', '.join(idea['tags'])}\n"
        result += f"      Created: {idea['created_at'][:10]}\n\n"

    return result

def create_script(topic, platform="tiktok", duration="30 seconds"):
    """Generate a script using AI"""
    response = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": f"You are a expert script writer for {platform} videos. Create engaging, platform-specific scripts."
            },
            {
                "role": "user",
                "content": f"Create a {duration} video script about: {topic}\n\nInclude:\n- Hook (first 2 seconds)\n- Main content\n- Call to action\n- Recommended hashtags"
            }
        ]
    )

    script = response.choices[0].message.content
    log_action("create_script", {"topic": topic, "platform": platform})

    return script

def save_script(filename, content, is_final=False):
    """Save script to file"""
    folder = "final" if is_final else "drafts"
    script_path = SCRIPTS_DIR / folder / filename

    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)

    log_action("save_script", {"filename": filename, "folder": folder})

    return f"✅ Script saved to: {script_path}"

def create_project(project_name, description=""):
    """Create a new video project with organized folders"""
    project_path = PROJECTS_DIR / project_name

    folders = ["raw", "edited", "final"]
    for folder in folders:
        (project_path / folder).mkdir(parents=True, exist_ok=True)

    metadata = {
        "name": project_name,
        "description": description,
        "created_at": datetime.now().isoformat(),
        "status": "active",
        "files": {
            "raw": [],
            "edited": [],
            "final": []
        }
    }

    with open(project_path / "metadata.json", 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    log_action("create_project", {"project_name": project_name})

    return f"✅ Project created: {project_name}\n   Folders: {', '.join(folders)}"

def organize_video_file(source_path, project_name, file_type):
    """Move video file to project folder"""
    source = Path(source_path)
    project_path = PROJECTS_DIR / project_name

    if not source.exists():
        return f"❌ Error: Source file not found: {source_path}"

    if not project_path.exists():
        return f"❌ Error: Project not found: {project_name}"

    dest_folder = project_path / file_type
    dest_path = dest_folder / source.name

    shutil.copy2(source, dest_path)

    # Update metadata
    metadata_path = project_path / "metadata.json"
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    metadata["files"][file_type].append({
        "filename": source.name,
        "added_at": datetime.now().isoformat()
    })

    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    log_action("organize_video_file", {"project": project_name, "file_type": file_type})

    return f"✅ File organized: {source.name} → {project_name}/{file_type}/"

def list_projects():
    """List all projects"""
    if not PROJECTS_DIR.exists():
        return "No projects yet. Create your first project!"

    projects = [d for d in PROJECTS_DIR.iterdir() if d.is_dir()]

    if not projects:
        return "No projects yet."

    result = f"\n🎬 Found {len(projects)} project(s):\n\n"

    for project in projects:
        metadata_path = project / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            result += f"  📁 {metadata['name']}\n"
            result += f"      Status: {metadata['status']}\n"
            result += f"      Raw: {len(metadata['files']['raw'])} | "
            result += f"Edited: {len(metadata['files']['edited'])} | "
            result += f"Final: {len(metadata['files']['final'])}\n"
            result += f"      Created: {metadata['created_at'][:10]}\n\n"

    return result

# ============= AGENT LOOP =============

available_functions = {
    "save_idea": save_idea,
    "list_ideas": list_ideas,
    "create_script": create_script,
    "save_script": save_script,
    "create_project": create_project,
    "organize_video_file": organize_video_file,
    "list_projects": list_projects
}

def run_agent(user_message, max_iterations=5):
    """Main agent loop"""

    system_prompt = f"""You are a Video Creator Agent - an AI assistant for content creators.

You support these platforms:
- TikTok (short, trendy, 15-60 seconds)
- Instagram Reels (aesthetic, 15-90 seconds)
- Xiaohongshu (小红书) (lifestyle, 30-180 seconds)
- YouTube Shorts (SEO-focused, 15-60 seconds)

Your capabilities:
- Save and organize video ideas with tags
- Generate platform-specific scripts
- Create and manage video projects
- Organize video files (raw → edited → final)
- Track project history

Be concise, helpful, and action-oriented. Use emojis when appropriate."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    print(f"\n{'='*60}")
    print(f"🎬 Video Creator Agent")
    print(f"{'='*60}")
    print(f"📝 Task: {user_message}")
    print(f"{'='*60}\n")

    for iteration in range(max_iterations):
        print(f"🔄 Iteration {iteration + 1}/{max_iterations}")

        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=messages,
            tools=tools
        )

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print(f"\n✅ Final Answer:\n")
            print(f"{'='*60}")
            return message.content

        print(f"🔧 Tool calls: {len(message.tool_calls)}")

        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"   → {function_name}({json.dumps(function_args, ensure_ascii=False)})")

            try:
                function_response = available_functions[function_name](**function_args)
            except Exception as e:
                function_response = f"Error: {str(e)}"

            print(f"   ← {function_response[:100]}{'...' if len(function_response) > 100 else ''}\n")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": function_response
            })

    return "Max iterations reached"

# ============= CLI =============

if __name__ == "__main__":
    import sys

    print("""
================================================================
              VIDEO CREATOR AGENT v1.0
          AI Assistant for Content Creators
================================================================

Supported platforms: TikTok, Instagram Reels, Xiaohongshu, YouTube Shorts

Examples:
  * "Save idea: morning routine for TikTok"
  * "Create a script about productivity tips for Instagram"
  * "Create project called 'Summer Vlog'"
  * "List all my ideas"
  * "Show all projects"
    """)

    if len(sys.argv) < 2:
        print("\n💡 Usage: python agent.py \"your task here\"")
        print("   Or run interactively and type your task:")
        task = input("\n🎬 Your task: ")
    else:
        task = " ".join(sys.argv[1:])

    if task.strip():
        result = run_agent(task)
        print(f"\n{result}")
        print(f"\n{'='*60}\n")
    else:
        print("❌ No task provided. Exiting.")
