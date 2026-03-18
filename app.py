"""
Video Creator Agent - Web Interface v3.0
Beautiful Gradio UI for AI-powered content creation
"""

import gradio as gr
from agent import run_agent, AgentError
import os
import re

# Custom CSS for beautiful design
custom_css = """
/* Main Container */
.gradio-container {
    max-width: 1200px !important;
    margin: auto !important;
}

/* Header Styling */
.main-header {
    text-align: center;
    padding: 2rem 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.main-header h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: 700;
}

.main-header p {
    margin: 0.5rem 0 0;
    opacity: 0.95;
    font-size: 1.1rem;
}

/* Chat Box */
.chatbot-container {
    border-radius: 15px !important;
    overflow: hidden;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

/* Platform Cards */
.platform-card {
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem;
    transition: transform 0.2s;
    cursor: pointer;
}

.platform-card:hover {
    transform: translateY(-2px);
}

/* Feature Tags */
.feature-tag {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 20px;
    font-size: 0.85rem;
    margin: 0.25rem;
}

/* Action Buttons */
.action-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.3s;
}

.action-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

/* Stats Card */
.stats-card {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
}

/* Quick Commands */
.quick-command {
    background: white;
    border: 2px solid #e0e0e0;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    margin: 0.25rem;
    cursor: pointer;
    transition: all 0.2s;
}

.quick-command:hover {
    border-color: #667eea;
    background: #f8f9ff;
}
"""

# Quick command templates
QUICK_COMMANDS = [
    "💡 Show all my ideas",
    "📝 Generate script about productivity",
    "🎯 Create 5 viral titles for fitness",
    "📊 Show my statistics",
    "📅 Create 7-day content plan",
    "🔍 Search history for scripts",
    "📤 Export all my ideas",
    "#️⃣ Get trending hashtags"
]

def process_command(message, history):
    """Process user command and return response"""
    try:
        # Run agent with optimized settings for web interface
        # Reduce iterations for faster responses
        result = run_agent(message, max_iterations=2)

        # Remove ANSI color codes for Gradio compatibility
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_result = ansi_escape.sub('', result)

        return clean_result

    except AgentError as e:
        return f"❌ Error: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

def get_agent_stats():
    """Get agent statistics"""
    try:
        from agent import show_stats
        return show_stats()
    except:
        return "No statistics available yet. Run some commands first!"

def show_platform_info(platform):
    """Show platform-specific information"""
    configs = {
        "tiktok": "🎵 **TikTok**\n\nDuration: 15-60s\nStyle: Trendy, fast-paced\nBest: Hook in 1s, trending sounds",
        "instagram": "📸 **Instagram Reels**\n\nDuration: 15-90s\nStyle: Aesthetic, polished\nBest: High quality, captions",
        "xiaohongshu": "🌸 **Xiaohongshu**\n\nDuration: 30-180s\nStyle: Lifestyle, authentic\nBest: Storytelling, personal",
        "youtube_shorts": "🎬 **YouTube Shorts**\n\nDuration: 15-60s\nStyle: SEO-focused\nBest: Keywords, thumbnails"
    }
    return configs.get(platform.lower(), "Select a platform above")

# Create Gradio interface
with gr.Blocks() as demo:

    # Header
    gr.HTML("""
    <div class="main-header">
        <h1>🎬 Video Creator Agent</h1>
        <p>AI-Powered Assistant for TikTok, Instagram, Xiaohongshu & YouTube Shorts</p>
    </div>
    """)

    # Main layout
    with gr.Row():
        # Left column - Chat interface
        with gr.Column(scale=2):
            gr.Markdown("## 💬 Chat with Agent")

            chatbot = gr.Chatbot(
                label="Agent Conversation",
                height=400,
                show_label=False
            )

            with gr.Row():
                msg = gr.Textbox(
                    label="Your Command",
                    placeholder="Ask me anything: 'Generate viral titles', 'Save idea', 'Show stats'...",
                    scale=4,
                    lines=2
                )
                submit = gr.Button("Send", scale=1, variant="primary")

            # Quick commands
            gr.Markdown("### ⚡ Quick Commands")
            with gr.Row():
                quick_cmd1 = gr.Button(QUICK_COMMANDS[0], size="sm")
                quick_cmd2 = gr.Button(QUICK_COMMANDS[1], size="sm")
            with gr.Row():
                quick_cmd3 = gr.Button(QUICK_COMMANDS[2], size="sm")
                quick_cmd4 = gr.Button(QUICK_COMMANDS[3], size="sm")
            with gr.Row():
                quick_cmd5 = gr.Button(QUICK_COMMANDS[4], size="sm")
                quick_cmd6 = gr.Button(QUICK_COMMANDS[5], size="sm")
            with gr.Row():
                quick_cmd7 = gr.Button(QUICK_COMMANDS[6], size="sm")
                quick_cmd8 = gr.Button(QUICK_COMMANDS[7], size="sm")

            gr.Markdown("""
            ### 💡 Example Commands

            **Ideas:**
            - `Save idea: morning routine TikTok with tags lifestyle`
            - `List all my ideas for Instagram`
            - `Show ideas with tag 'fitness'`

            **Scripts:**
            - `Create 30s script about productivity tips`
            - `Write script for Instagram about travel`

            **AI Generation:**
            - `Generate 5 viral titles for cooking`
            - `Create description with hashtags`
            - `Get 3 thumbnail ideas for gaming`

            **Projects:**
            - `Create project called 'Summer Vlog'`
            - `Show all my projects`
            - `Organize video file`

            **Analytics:**
            - `Show my stats`
            - `Search history for 'script'`
            """)

        # Right column - Stats & Info
        with gr.Column(scale=1):
            gr.Markdown("## 📊 Your Stats")

            stats_output = gr.Markdown(
                value=get_agent_stats(),
                label="Statistics"
            )

            refresh_stats = gr.Button("🔄 Refresh Stats", size="sm")

            gr.Markdown("---")

            gr.Markdown("## 🌐 Platform Info")

            platform_dropdown = gr.Dropdown(
                choices=["TikTok", "Instagram", "Xiaohongshu", "YouTube Shorts"],
                value="TikTok",
                label="Select Platform"
            )

            platform_info = gr.Markdown(
                value=show_platform_info("TikTok"),
                label="Platform Details"
            )

            gr.Markdown("---")

            gr.Markdown("""
            ### 🎯 Features

            <span class="feature-tag">18 AI Tools</span>
            <span class="feature-tag">Multi-Platform</span>
            <span class="feature-tag">Smart Organization</span>

            ### 📱 Supported

            🎵 TikTok
            📸 Instagram Reels
            🌸 Xiaohongshu
            🎬 YouTube Shorts
            """, sanitize_html=False)

    # Footer
    gr.HTML("""
    <div style="text-align: center; padding: 2rem; color: #666;">
        <p>Made with ❤️ for Content Creators</p>
        <p>Powered by OpenAI GPT-4o-mini</p>
    </div>
    """)

    # Event handlers
    def user_message(user_message, history):
        """Add user message to history"""
        # Gradio 6.0+ format: list of dicts with 'role' and 'content'
        return "", history + [{"role": "user", "content": user_message}]

    def bot_response(history):
        """Generate bot response"""
        user_message = history[-1]["content"] if history else ""
        bot_message = process_command(user_message, history)
        # Append bot response to history
        return history + [{"role": "assistant", "content": bot_message}]

    # Chat interactions
    submit.click(
        user_message,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot]
    ).then(
        bot_response,
        inputs=chatbot,
        outputs=chatbot
    )

    msg.submit(
        user_message,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot]
    ).then(
        bot_response,
        inputs=chatbot,
        outputs=chatbot
    )

    # Quick command buttons
    quick_cmd_btns = [quick_cmd1, quick_cmd2, quick_cmd3, quick_cmd4,
                      quick_cmd5, quick_cmd6, quick_cmd7, quick_cmd8]

    for btn, cmd in zip(quick_cmd_btns, QUICK_COMMANDS):
        btn.click(
            lambda c=cmd: (c, [{"role": "user", "content": c}]),
            outputs=[msg, chatbot]
        ).then(
            bot_response,
            inputs=chatbot,
            outputs=chatbot
        )

    # Refresh stats
    refresh_stats.click(
        get_agent_stats,
        outputs=stats_output
    )

    # Platform info
    platform_dropdown.change(
        show_platform_info,
        inputs=platform_dropdown,
        outputs=platform_info
    )

# Launch
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
        share=False,
        show_error=True
    )
