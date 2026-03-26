# 🎬 Video Creator AI - User Guide

## 🌐 Live Demo

**Production URL:** https://web-app-ten-woad-69.vercel.app

---

## ✨ What's Working NOW

### ✅ Chat Interface
- Real-time chat interface
- Typing indicators
- Message history
- Beautiful animations

### ✅ Task Management
- **Create tasks** from Tasks tab or chat
- **Edit tasks** inline - click edit icon
- **Delete tasks** - click trash icon
- **Toggle status** - click on status icon or badge
  - Pending → In Progress → Completed → Pending

### ✅ UI Features
- Anime-inspired design with glow effects
- Responsive layout (mobile + desktop)
- Smooth animations
- Sparkle particles

---

## 🎯 How to Use

### Creating Tasks

**Method 1: From Tasks Tab**
1. Click "Tasks" in navigation
2. Click "Create Task" button
3. New task appears with "New Task" title
4. Click edit icon (pencil) to rename
5. Type new name and press Enter or click ✓

**Method 2: From Chat**
Type in chat:
- `Add task: Create content calendar`
- `Create task: Research TikTok trends`
- `add task: Plan weekly videos`

### Managing Tasks

**Edit Task:**
1. Go to Tasks tab
2. Click pencil icon (✏️) next to task
3. Edit the title
4. Press Enter or click ✓ to save
5. Click ✗ to cancel

**Delete Task:**
1. Click trash icon (🗑️) next to task
2. Task is permanently deleted

**Change Status:**
- Click on the status icon (⭕/🔄/✓)
- Or click on the status badge
- Cycles through: Pending → In Progress → Completed

### Chat Commands

Currently supported (demo mode):

**Task Creation:**
- `Add task: Your task name`
- `Create task: Your task name`

**Mock Responses:**
- `Create 5 viral titles` - Shows title ideas
- `Generate a script` - Shows sample script
- `Give me content ideas` - Shows content types
- Other messages get helpful demo response

---

## 🚧 Current Limitations

### Demo Mode (Current State)
✅ Works:
- Task management (create, edit, delete, toggle status)
- Chat interface with animations
- Mock responses for common requests
- Beautiful UI

❌ Doesn't Work Yet:
- Real AI agent responses (uses mock)
- Save ideas to database
- Generate actual scripts/titles
- Social media integrations
- Web search

### To Enable Full Features

You need to:

1. **Deploy Python Backend**
   ```bash
   # Install dependencies
   pip install fastapi uvicorn openai

   # Create api/server.py (see DEPLOYMENT.md)
   cd api
   python -m uvicorn server:app --reload
   ```

2. **Deploy Backend to Production**
   - Railway: https://railway.app
   - Render: https://render.com
   - Or any Python hosting

3. **Connect Frontend to Backend**
   - In Vercel Dashboard → Environment Variables
   - Add: `BACKEND_URL` = `https://your-backend-url.com`
   - Redeploy frontend

---

## 🎨 UI Guide

### Navigation Bar
- **About** - Project info (coming soon)
- **Skills** - View AI capabilities
- **Tasks** - Task management
- **Chat** - Chat with AI
- **Settings** - Settings (coming soon)

### Left Panel (Desktop Only)
- AI agent avatar
- Skills showcase
- Agent description

### Chat Panel
- Message history with timestamps
- Typing indicator when AI is "thinking"
- Input field with Shift+Enter for new lines
- Send button and voice input button (UI only)

### Tasks Panel
- Task list with status icons
- Create task button
- Edit/delete controls
- Status badges (clickable)

---

## 📝 Example Workflows

### Workflow 1: Content Planning

1. **Open Chat tab**
2. Type: `Add task: Plan TikTok content for next week`
3. Task created automatically
4. **Switch to Tasks tab**
5. Click on task status icon to mark as "In Progress"
6. Click edit icon to add details
7. When done, click again to mark "Completed"

### Workflow 2: Task Management

1. **Switch to Tasks tab**
2. Click "Create Task" button
3. Edit the new task: `Research viral trends`
4. Create another task: `Create 5 video scripts`
5. Click status icons to track progress
6. Delete completed tasks when done

### Workflow 3: AI Chat (Demo)

1. **Stay in Chat tab**
2. Type: `Create 5 viral titles for fitness TikTok`
3. Get mock response with title ideas
4. Type: `Add task: Use title #3 for tomorrow's video`
5. Task is created for you

---

## 🔧 Troubleshooting

### Tasks Not Saving?
- Tasks are stored in browser memory
- Refreshing the page clears all tasks
- **Solution:** This is expected in demo mode. Backend needed for persistence.

### Chat Not Responding?
- Check if you're online
- Try refreshing the page
- Check browser console for errors (F12)

### React Errors?
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+Shift+R)
- Check if using latest URL: https://web-app-ten-woad-69.vercel.app

---

## 🎯 Coming Soon

### Backend Integration
- [ ] Real AI responses from Python agent
- [ ] Save ideas to database
- [ ] Generate actual scripts/titles
- [ ] Web search integration
- [ ] Social media posting

### Enhanced Features
- [ ] Task due dates
- [ ] Task priorities
- [ ] Task categories/tags
- [ ] Task search/filter
- [ ] Export tasks to JSON

### UI Improvements
- [ ] Dark/light theme toggle
- [ ] Custom accent colors
- [ ] Animation preferences
- [ ] Compact/detailed view modes

---

## 📞 Support

**Documentation:**
- [DEPLOYMENT.md](DEPLOYMENT.md:1) - Backend setup guide
- [DEPLOYMENT_SUCCESS.md](DEPLOYMENT_SUCCESS.md:1) - Deployment info
- [README.md](README.md:1) - Project overview

**Links:**
- Live Demo: https://web-app-ten-woad-69.vercel.app
- GitHub: https://github.com/THU-SIGS-AIID/annar_video_ai_agent
- Vercel Dashboard: https://vercel.com/anna25-1076s-projects/web-app

---

**Last Updated:** 2026-03-26
**Version:** 1.0 (Demo Mode)
**Status:** ✅ Production Ready (with limitations)

---

Made with ❤️ and ✨
