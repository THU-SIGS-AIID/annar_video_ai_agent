# 🚀 Deployment WITHOUT Credit Card!

Don't have a credit card? No problem! Here are 100% FREE options.

---

## ⭐ Option 1: PythonAnywhere (RECOMMENDED)

**Why:** No credit card required, easy setup, FREE forever!

### Step-by-Step:

1. **Create Account:**
   - Go to: https://www.pythonanywhere.com
   - Click "Sign up"
   - No credit card needed!

2. **Create Web App:**
   - Dashboard → "Create a new web app"
   - Name: `video-creator-backend`
   - Python: 3.10
   - Click "Next"

3. **Upload Code:**
   - Choose "Upload a new project"
   - Click "Or upload your own files"
   - Upload files from `api/` folder:
     - `server.py`
     - `requirements.txt`
   - Click "Next"

4. **Configure:**
   - WSGI config file: `server.py`
   - Working directory: `/`
   - Click "Next"

5. **Environment Variables:**
   ```
   OPENAI_API_KEY=sk-your-key
   OPENAI_BASE_URL=https://api.stepfun.com/v1
   OPENAI_MODEL=step-3.5-flash
   ```
   Click "Next"

6. **Create App:**
   - Click "Create"
   - Wait 1-2 minutes

7. **Get URL:**
   - Like: `https://yourusername.pythonanywhere.com`
   - Add `/api/chat` for API calls

8. **Configure Vercel:**
   - In Vercel dashboard, add `BACKEND_URL`
   - Value: `https://yourusername.pythonanywhere.com`

✅ **Pros:** No credit card, easy, forever free
⚠️ **Cons:** Limited resources, manual upload

---

## ⭐ Option 2: Hugging Face Spaces (EASIEST!)

**Why:** Like Google Colab but always running, FREE!

### Step-by-Step:

1. **Create Account:**
   - Go to: https://huggingface.co
   - "Sign up"
   - No credit card needed!

2. **Create New Space:**
   - Click "Spaces" → "Create new Space"
   - Name: `video-creator-backend`

3. **Choose SDK:**
   - Select: "Gradio" or "Streamlit"
   - Or "Docker" for FastAPI

4. **Create Files:**
   - Create `server.py` with API code
   - Create `requirements.txt`
   - Add secrets for API keys

5. **Deploy:**
   - Click "Create Space"
   - HuggingFace deploys it

6. **Get URL:**
   - Like: `https://huggingface.co/spaces/yourname/video-creator-backend`

✅ **Pros:** Very easy, no card, CPU free
⚠️ **Cons:** Requires rewriting server.py

---

## ⭐ Option 3: Koyeb (GREAT ALTERNATIVE!)

**Why:** No credit card, generous free tier!

### Step-by-Step:

1. **Create Account:**
   - Go to: https://www.koyeb.com
   - "Sign up"
   - No credit card!

2. **Create Service:**
   - Click "Create App"
   - Choose "Git"

3. **Configure:**
   - Select: GitHub repository
   - Choose: `AMatved/annar_video_ai_agent`
   - Branch: `main`
   - Root directory: `api`

4. **Settings:**
   - Runtime: Python 3
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn server:app --host 0.0.0.0 --port 8000`

5. **Environment Variables:**
   ```
   OPENAI_API_KEY=sk-your-key
   OPENAI_BASE_URL=https://api.stepfun.com/v1
   OPENAI_MODEL=step-3.5-flash
   ```

6. **Deploy!**
   - Click "Deploy"
   - Get URL like: `https://yourname.koyeb.app`

✅ **Pros:** No card, good free tier, auto-deploys
⚠️ **Cons:** Newer platform, less docs

---

## ⭐ Option 4: Fly.io (GOOD OPTION)

**Why:** Free trial $5 free credit, no card needed initially

### Step-by-Step:

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login:**
   ```bash
   fly auth signup
   ```

3. **Launch:**
   ```bash
   fly launch --org personal
   ```

4. **Set up:**
   - Choose region
   - Set environment variables
   - Deploy

✅ **Pros:** Good free trial, modern platform
⚠️ **Cons:** CLI required, learning curve

---

## ⭐ Option 5: LOCAL + ngrok (FASTEST!)

**Why:** Test locally, no deployment needed!

### Step-by-Step:

1. **Install dependencies:**
   ```bash
   pip install -r api/requirements.txt
   ```

2. **Run server:**
   ```bash
   cd api
   python server.py
   ```

3. **Install ngrok:**
   ```bash
   # Download from https://ngrok.com
   # Or: pip install pyngrok
   ```

4. **Create tunnel:**
   ```bash
   ngrok http 8000
   ```

5. **Get URL:**
   - Like: `https://abc123.ngrok.io`

6. **Configure Vercel:**
   - Add `BACKEND_URL`: `https://abc123.ngrok.io`

✅ **Pros:** Works immediately, free, you control everything
⚠️ **Cons:** URL changes when ngrok restarts, computer must be on

---

## 🎯 My Recommendations:

### **For Production:**
1. **Koyeb** - Best alternative to Render
2. **PythonAnywhere** - Easiest, no card

### **For Testing:**
1. **Local + ngrok** - Fastest, test immediately
2. **Hugging Face** - Like Colab but permanent

### **For Learning:**
1. **Fly.io** - Modern, good docs
2. **PythonAnywhere** - Great for beginners

---

## 📋 Quick Comparison:

| Platform | No Card | Free Tier | Easy | Auto-Deploy |
|----------|----------|------------|------|-------------|
| **Koyeb** | ✅ | ✅ | ⭐⭐⭐⭐ | ✅ |
| **PythonAnywhere** | ✅ | ✅ | ⭐⭐⭐⭐⭐ | ❌ |
| **Hugging Face** | ✅ | ✅ | ⭐⭐⭐⭐⭐ | ✅ |
| **Fly.io** | ✅ | ✅ | ⭐⭐⭐ | ✅ |
| **Local+ngrok** | ✅ | ✅ | ⭐⭐⭐ | ❌ |

---

## 🚀 Quick Start:

### **Want to test NOW? (5 min)**
Use **Option 5: Local + ngrok** - see below!

### **Want production? (10 min)**
Use **Option 1: PythonAnywhere** - most reliable

---

## 💬 Need Help?

Tell me which option you prefer:
- "I want PythonAnywhere"
- "I want Koyeb"
- "I want Hugging Face"
- "I want local + ngrok"

I'll guide you step-by-step! 🚀
