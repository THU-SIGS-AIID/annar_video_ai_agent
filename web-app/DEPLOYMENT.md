# 🚀 Deployment Guide - Video Creator AI Web App

Complete guide to deploy the Video Creator AI web interface to production.

## 📋 Prerequisites

Before deploying, make sure you have:

- ✅ Node.js 18+ installed
- ✅ Git installed
- ✅ Vercel account (free tier works)
- ✅ GitHub account (for Vercel integration)

## 🌐 Deployment Options

### Option 1: Vercel (Recommended) ⭐

Vercel is the easiest and fastest way to deploy Next.js apps.

#### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

#### Step 2: Login to Vercel

```bash
vercel login
```

#### Step 3: Deploy from web-app directory

```bash
cd web-app
vercel
```

Follow the prompts:
- **Set up and deploy?** → `Y`
- **Which scope?** → Select your account
- **Link to existing project?** → `N`
- **Project name** → `video-creator-ai-web`
- **In which directory is your code?** → `./`
- **Want to override settings?** → `N`

Vercel will:
1. Build your app
2. Deploy it to a URL like: `https://video-creator-ai-web.vercel.app`
3. Provide you with the production URL

#### Step 4: Set up custom domain (optional)

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to Settings → Domains
4. Add your custom domain
5. Configure DNS records as instructed

#### Step 5: Environment Variables

1. Go to Project Settings → Environment Variables
2. Add the following:

```env
NEXT_PUBLIC_API_URL=https://your-backend-api.com/api
NEXT_PUBLIC_APP_URL=https://your-domain.com
```

### Option 2: Northflank

Northflank is great for more complex deployments with custom backends.

#### Step 1: Create Northflank Account

Go to [northflank.com](https://northflank.com) and sign up.

#### Step 2: Create a New Project

1. Click "Create Project"
2. Name: `video-creator-ai`
3. Region: Choose closest to your audience

#### Step 3: Add a Combined Service

1. Click "Add Service" → "Combined Service"
2. Configure:

**Basic Settings:**
- Name: `web-app`
- Image: `node:18-alpine`
- Port: `3000`

**Build & Run:**
```bash
# Build command
cd web-app && npm install && npm run build

# Start command
cd web-app && npm start
```

**Environment Variables:**
```env
NEXT_PUBLIC_API_URL=https://your-backend-api.com/api
NEXT_PUBLIC_APP_URL=https://your-app.northflank.com
NODE_ENV=production
```

**Resources:**
- CPU: 0.1 (free tier)
- RAM: 128 MB (free tier)
- Replicas: 1

#### Step 4: Deploy

Click "Create" and Northflank will:
1. Build your application
2. Deploy it to their infrastructure
3. Provide a URL like: `https://your-app.northflank.com`

### Option 3: Self-Hosted (Docker)

For complete control, you can self-host using Docker.

#### Step 1: Create Dockerfile

Create `web-app/Dockerfile`:

```dockerfile
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
```

#### Step 2: Update next.config.js

```javascript
module.exports = {
  output: 'standalone',
  // ... other config
};
```

#### Step 3: Build and Run

```bash
cd web-app
docker build -t video-creator-ai-web .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=https://your-api.com video-creator-ai-web
```

## 🔌 Backend Integration

### Setting Up the Python Backend API

The web app needs to connect to your Python agent backend.

#### Step 1: Create FastAPI Backend

Create `api/server.py`:

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
sys.path.insert(0, '..')

from agent import run_agent

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = run_agent(request.message)
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### Step 2: Update Web App API Route

Update `web-app/app/api/chat/route.ts`:

```typescript
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

export async function POST(request: NextRequest) {
  try {
    const { message } = await request.json();

    const response = await fetch(`${BACKEND_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to connect to agent backend' },
      { status: 500 }
    );
  }
}
```

#### Step 3: Deploy Backend

Deploy the Python backend to:
- **Vercel Serverless Functions**
- **Railway** (recommended for Python)
- **Render**
- **AWS Lambda**
- **Google Cloud Run**

## 🌍 Production Checklist

Before going live:

- [ ] Set up custom domain
- [ ] Configure SSL/HTTPS
- [ ] Set up environment variables
- [ ] Enable error tracking (Sentry)
- [ ] Set up analytics (Vercel Analytics, Plausible)
- [ ] Configure rate limiting
- [ ] Add authentication (if needed)
- [ ] Set up monitoring
- [ ] Test all features
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline

## 🔒 Security Best Practices

1. **Environment Variables**: Never commit `.env` files
2. **API Keys**: Use server-side storage, never expose to client
3. **CORS**: Configure specific origins in production
4. **Rate Limiting**: Implement to prevent abuse
5. **Authentication**: Add user authentication if needed
6. **HTTPS**: Always use HTTPS in production

## 📊 Monitoring & Analytics

### Vercel Analytics

```bash
npm install @vercel/analytics
```

Add to `app/layout.tsx`:

```typescript
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

### Error Tracking

```bash
npm install @sentry/nextjs
```

## 🔄 CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Vercel

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: cd web-app && npm install

      - name: Build
        run: cd web-app && npm run build

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          vercel-args: '--prod'
          working-directory: ./web-app
```

## 🐛 Troubleshooting

### Build Fails on Vercel

```bash
# Clear cache and redeploy
vercel --force
```

### Environment Variables Not Working

1. Check variable names (must start with `NEXT_PUBLIC_` for client access)
2. Redeploy after changing variables
3. Check Vercel dashboard for correct values

### Styles Not Loading

1. Check `tailwind.config.ts` content paths
2. Ensure `globals.css` is imported
3. Clear Next.js cache: `rm -rf .next`

## 📞 Support

- **Vercel Docs**: https://vercel.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **Northflank Docs**: https://docs.northflank.com

---

**Happy Deploying!** 🚀🎉
