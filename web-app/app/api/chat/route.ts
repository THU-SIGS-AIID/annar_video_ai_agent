import { NextRequest, NextResponse } from 'next/server';

// This route forwards messages to the Python agent backend
// In production, you'd want to add authentication, rate limiting, etc.

export async function POST(request: NextRequest) {
  try {
    const { message } = await request.json();

    if (!message || typeof message !== 'string') {
      return NextResponse.json(
        { error: 'Invalid message' },
        { status: 400 }
      );
    }

    // For now, return a mock response
    // TODO: Integrate with actual Python agent backend
    const mockResponse = await simulateAgentResponse(message);

    return NextResponse.json({
      message: mockResponse,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Chat API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

async function simulateAgentResponse(userMessage: string): Promise<string> {
  // Simulate processing delay
  await new Promise(resolve => setTimeout(resolve, 1000));

  const lowerMessage = userMessage.toLowerCase();

  // Simple pattern matching for demo purposes
  if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
    return "Hello! How can I help you today? I can assist with content creation, research, automation tasks, and much more! 🚀";
  }

  if (lowerMessage.includes('create') || lowerMessage.includes('generate')) {
    return "I'd be happy to help you create content! I can generate ideas, scripts, titles, and descriptions for your videos. What type of content are you working on? 🎬";
  }

  if (lowerMessage.includes('tiktok') || lowerMessage.includes('instagram') || lowerMessage.includes('youtube')) {
    return "Great choice! I can help you optimize content for " + (
      lowerMessage.includes('tiktok') ? 'TikTok' :
      lowerMessage.includes('instagram') ? 'Instagram' :
      'YouTube'
    ) + ". Would you like me to generate viral titles, trending hashtags, or a content strategy? 📱";
  }

  if (lowerMessage.includes('help')) {
    return `Here's what I can help you with:

✨ **Content Creation**
- Generate viral video titles
- Create engaging scripts
- Write descriptions with hashtags
- Generate thumbnail ideas

📊 **Planning & Organization**
- Create content calendars
- Save and organize video ideas
- Project management

🔍 **Research & Trends**
- Discover trending hashtags
- Analyze best posting times
- Market research

🤖 **Automation**
- Social media account management
- Cross-platform posting
- Analytics tracking

What would you like to work on?`;
  }

  // Default response
  return `I understand you're asking about: "${userMessage}"

I'm your AI assistant specialized in content creation and automation. I can help you with:

1. **Video Content**: Generate ideas, scripts, titles, descriptions
2. **Social Media**: Optimize for TikTok, Instagram, YouTube
3. **Trends**: Find viral topics and hashtags
4. **Automation**: Manage accounts and schedule posts

Could you provide more details about what you'd like to accomplish?`;
}
