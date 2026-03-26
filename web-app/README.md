# Video Creator AI - Web Interface

Modern anime-inspired web interface for the Video Creator AI agent.

## ✨ Features

- 🎨 Beautiful anime-inspired UI with soft glows and animations
- 💬 Real-time chat interface with AI agent
- 📋 Task management system
- 🚀 Built with Next.js 14, React, Tailwind CSS, and Framer Motion
- 📱 Fully responsive design

## 🎨 Design Features

- Soft glowing UI with pill-shaped buttons
- Anime-inspired color palette (#F6A560 orange accent)
- Smooth animations and microinteractions
- Sparkle particle effects
- Typing indicators
- Floating animations

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager

### Installation

1. Navigate to the web-app directory:
```bash
cd web-app
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## 📦 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## 🌐 Deployment

### Deploy to Vercel

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
cd web-app
vercel
```

3. Follow the prompts to complete deployment

### Environment Variables

Create a `.env.local` file in the web-app directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:3001/api
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## 🔧 Tech Stack

- **Framework**: Next.js 14 (App Router)
- **UI**: React 18
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Language**: TypeScript

## 📁 Project Structure

```
web-app/
├── app/
│   ├── api/
│   │   └── chat/
│   │       └── route.ts       # Chat API endpoint
│   ├── globals.css            # Global styles
│   ├── layout.tsx             # Root layout
│   └── page.tsx               # Main page
├── public/                    # Static assets
├── package.json               # Dependencies
├── tailwind.config.ts         # Tailwind configuration
├── tsconfig.json              # TypeScript configuration
├── next.config.js             # Next.js configuration
└── vercel.json                # Vercel deployment config
```

## 🎨 Customization

### Colors

Edit `tailwind.config.ts` to customize the color palette:

```typescript
colors: {
  'anime-orange': '#F6A560',
  'anime-dark': '#0F1112',
  'anime-dark-secondary': '#0F2124',
  'anime-light': '#F5F5F5',
}
```

### Skills

Edit `skills` array in `app/page.tsx` to customize displayed skills:

```typescript
const skills = [
  { name: 'Your Skill', icon: YourIcon, color: 'text-your-color' },
];
```

## 🔌 Backend Integration

The web app currently uses mock responses. To integrate with the Python agent backend:

1. Update `app/api/chat/route.ts` to call your Python backend
2. Configure the backend URL in environment variables
3. Implement proper error handling and authentication

Example:

```typescript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message }),
});
```

## 🐛 Troubleshooting

### Build Errors

If you encounter build errors:

1. Clear the Next.js cache:
```bash
rm -rf .next
```

2. Reinstall dependencies:
```bash
rm -rf node_modules
npm install
```

3. Rebuild:
```bash
npm run build
```

### Styling Issues

If Tailwind classes aren't working:

1. Check that `globals.css` is imported in `layout.tsx`
2. Verify `tailwind.config.ts` content paths
3. Restart the dev server

## 📝 License

This project is part of the Video Creator Agent project.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on the main repository.

---

Made with ❤️ and ✨
