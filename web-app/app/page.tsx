'use client';

import { useState, useRef, useEffect, useMemo, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Bot,
  Sparkles,
  Zap,
  Brain,
  Code,
  FileText,
  Send,
  Mic,
  Plus,
  Clock,
  CheckCircle2,
  Circle,
  Loader2,
  Edit2,
  Trash2,
  X,
  MessageSquare,
  MoreVertical,
} from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface Chat {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}

interface Task {
  id: string;
  title: string;
  status: 'pending' | 'in_progress' | 'completed';
  createdAt: Date;
  editing?: boolean;
}

const skills = [
  { name: 'Task Automation', icon: Zap, color: 'text-yellow-400' },
  { name: 'Research & Analysis', icon: Brain, color: 'text-purple-400' },
  { name: 'Content Creation', icon: FileText, color: 'text-blue-400' },
  { name: 'Coding Assistance', icon: Code, color: 'text-green-400' },
] as const;

const createSparkles = () =>
  Array.from({ length: 12 }, (_, i) => ({
    id: `sparkle-${i}`,
    style: {
      left: `${Math.random() * 100}%`,
      top: `${Math.random() * 100}%`,
      animationDelay: `${Math.random() * 3}s`,
    },
  }));

const initialSparkles = createSparkles();

// Local storage keys
const CHATS_STORAGE_KEY = 'video-creator-chats';
const TASKS_STORAGE_KEY = 'video-creator-tasks';
const CURRENT_CHAT_KEY = 'video-creator-current-chat';

export default function Home() {
  const [chats, setChats] = useState<Chat[]>([
    {
      id: 'default-chat',
      title: 'New Conversation',
      messages: [
        {
          id: '1',
          role: 'assistant',
          content:
            "Hi! 👋 I'm your AI assistant. I can help you with:\n\n• Content creation (scripts, titles, descriptions)\n• Social media automation\n• Research & trend analysis\n• Task management\n\nTry saying: 'Create 5 viral TikTok titles' or 'Add task: Plan my content'",
          timestamp: new Date(),
        },
      ],
      createdAt: new Date(),
      updatedAt: new Date(),
    },
  ]);
  const [currentChatId, setCurrentChatId] = useState<string>('default-chat');
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [activeTab, setActiveTab] = useState<'chat' | 'tasks'>('chat');
  const [tasks, setTasks] = useState<Task[]>([]);
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null);
  const [editedTaskTitle, setEditedTaskTitle] = useState('');
  const [showChatList, setShowChatList] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const sparkles = useMemo(() => initialSparkles, []);

  // Load chats from localStorage on mount
  useEffect(() => {
    const savedChats = localStorage.getItem(CHATS_STORAGE_KEY);
    const savedTasks = localStorage.getItem(TASKS_STORAGE_KEY);
    const savedCurrentChat = localStorage.getItem(CURRENT_CHAT_KEY);

    if (savedChats) {
      try {
        const parsedChats = JSON.parse(savedChats);
        // Convert date strings back to Date objects
        const chatsWithDates = parsedChats.map((chat: any) => ({
          ...chat,
          messages: chat.messages.map((msg: any) => ({
            ...msg,
            timestamp: new Date(msg.timestamp),
          })),
          createdAt: new Date(chat.createdAt),
          updatedAt: new Date(chat.updatedAt),
        }));
        setChats(chatsWithDates);
      } catch (e) {
        console.error('Failed to load chats:', e);
      }
    }

    if (savedTasks) {
      try {
        const parsedTasks = JSON.parse(savedTasks);
        const tasksWithDates = parsedTasks.map((task: any) => ({
          ...task,
          createdAt: new Date(task.createdAt),
        }));
        setTasks(tasksWithDates);
      } catch (e) {
        console.error('Failed to load tasks:', e);
      }
    }

    if (savedCurrentChat) {
      setCurrentChatId(savedCurrentChat);
    }
  }, []);

  // Save chats to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem(CHATS_STORAGE_KEY, JSON.stringify(chats));
  }, [chats]);

  // Save tasks to localStorage
  useEffect(() => {
    localStorage.setItem(TASKS_STORAGE_KEY, JSON.stringify(tasks));
  }, [tasks]);

  // Save current chat ID
  useEffect(() => {
    localStorage.setItem(CURRENT_CHAT_KEY, currentChatId);
  }, [currentChatId]);

  const getCurrentChat = useCallback(() => {
    return chats.find((chat) => chat.id === currentChatId) || chats[0];
  }, [chats, currentChatId]);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  const currentChat = getCurrentChat();

  useEffect(() => {
    scrollToBottom();
  }, [currentChat?.messages.length, scrollToBottom]);

  const handleCreateNewChat = useCallback(() => {
    const newChat: Chat = {
      id: `chat-${Date.now()}`,
      title: 'New Conversation',
      messages: [
        {
          id: `msg-${Date.now()}`,
          role: 'assistant',
          content:
            "Hi! 👋 I'm your AI assistant. How can I help you today?\n\nTry saying:\n• 'Create 5 viral TikTok titles'\n• 'Add task: Plan my content'\n• 'Generate a script for cooking video'",
          timestamp: new Date(),
        },
      ],
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    setChats((prev) => [newChat, ...prev]);
    setCurrentChatId(newChat.id);
    setActiveTab('chat');
  }, []);

  const handleDeleteChat = useCallback((chatId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (chats.length === 1) {
      // Don't delete the last chat
      return;
    }

    setChats((prev) => prev.filter((chat) => chat.id !== chatId));

    // If deleting current chat, switch to another
    if (chatId === currentChatId) {
      const remainingChats = chats.filter((chat) => chat.id !== chatId);
      setCurrentChatId(remainingChats[0].id);
    }
  }, [chats, currentChatId]);

  const handleRenameChat = useCallback((chatId: string, newTitle: string) => {
    setChats((prev) =>
      prev.map((chat) =>
        chat.id === chatId
          ? { ...chat, title: newTitle, updatedAt: new Date() }
          : chat
      )
    );
  }, []);

  const handleSendMessage = useCallback(async () => {
    if (!input.trim()) return;

    const currentChat = getCurrentChat();
    if (!currentChat) return;

    const userMessage: Message = {
      id: `msg-${Date.now()}`,
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    const updatedMessages = [...currentChat.messages, userMessage];
    const currentInput = input;
    setInput('');
    setIsTyping(true);

    // Update chat with user message
    setChats((prev) =>
      prev.map((chat) =>
        chat.id === currentChatId
          ? {
              ...chat,
              messages: updatedMessages,
              updatedAt: new Date(),
            }
          : chat
      )
    );

    // Check for task creation commands
    if (currentInput.toLowerCase().includes('add task') || currentInput.toLowerCase().includes('create task')) {
      const taskTitle = currentInput
        .replace(/add task:?\s*/i, '')
        .replace(/create task:?\s*/i, '')
        .trim();

      const newTask: Task = {
        id: `task-${Date.now()}`,
        title: taskTitle || 'New Task',
        status: 'pending',
        createdAt: new Date(),
      };

      setTasks((prev) => [...prev, newTask]);

      const taskMessage: Message = {
        id: `msg-${Date.now() + 1}`,
        role: 'assistant',
        content: `✅ Task created: "${newTask.title}"\n\nSwitch to the Tasks tab to manage it.`,
        timestamp: new Date(),
      };

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChatId
            ? {
                ...chat,
                messages: [...updatedMessages, taskMessage],
                updatedAt: new Date(),
              }
            : chat
        )
      );
      setIsTyping(false);
      return;
    }

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: currentInput }),
      });

      if (!response.ok) throw new Error('Failed to get response');

      const data = await response.json();

      const assistantMessage: Message = {
        id: `msg-${Date.now() + 1}`,
        role: 'assistant',
        content: data.message || 'I processed your request!',
        timestamp: new Date(),
      };

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChatId
            ? {
                ...chat,
                messages: [...updatedMessages, assistantMessage],
                updatedAt: new Date(),
              }
            : chat
        )
      );
    } catch (error) {
      // Mock response for demo
      const mockResponse = generateMockResponse(currentInput);
      const assistantMessage: Message = {
        id: `msg-${Date.now() + 1}`,
        role: 'assistant',
        content: mockResponse,
        timestamp: new Date(),
      };

      setChats((prev) =>
        prev.map((chat) =>
          chat.id === currentChatId
            ? {
                ...chat,
                messages: [...updatedMessages, assistantMessage],
                updatedAt: new Date(),
              }
            : chat
        )
      );
    } finally {
      setIsTyping(false);
    }
  }, [input, getCurrentChat, currentChatId]);

  const generateMockResponse = (userMessage: string): string => {
    const lower = userMessage.toLowerCase();

    if (lower.includes('script') || lower.includes('скрипт')) {
      return `📝 **Script Generation**

Here's a sample script for your video:

**Hook:** (0-3 seconds)
"Wait, you won't believe this hack!"

**Main Content:** (3-15 seconds)
Explain your topic with passion and energy. Use quick cuts and text overlays.

**CTA:** (15-18 seconds)
"Follow for more! Link in bio!"

Want me to customize this for a specific topic?`;
    }

    if (lower.includes('title') || lower.includes('заголовок')) {
      return `🎯 **Viral Title Ideas:**

1. "This One Trick Changed Everything..."
2. "Nobody Talks About This..."
3. "I Tried ____ For 30 Days..."
4. "The Secret To ____ That Nobody Knows"
5. "Why You're Failing At ____ (And How To Fix It)"

Which platform are you creating content for?`;
    }

    if (lower.includes('idea') || lower.includes('идея')) {
      return `💡 **Content Ideas:**

1. **Tutorial**: Show your expertise
2. **Behind the scenes**: Personal connection
3. **Trend response**: Join the conversation
4. **Storytime**: Engaging narrative
5. **Challenge**: Interactive content

What niche interests you?`;
    }

    return `I understand you're asking about: "${userMessage}"

Currently, I'm in demo mode. To enable full AI agent features:

1. **Deploy the Python backend** (see DEPLOYMENT.md)
2. **Set BACKEND_URL environment variable** in Vercel
3. **Redeploy** the web app

For now, I can help you create and manage tasks. Try:
- "Add task: Create content calendar"
- "Create task: Research trending topics"`;
  };

  const handleCreateTask = useCallback(() => {
    const newTask: Task = {
      id: `task-${Date.now()}`,
      title: 'New Task',
      status: 'pending',
      createdAt: new Date(),
    };
    setTasks((prev) => [...prev, newTask]);
  }, []);

  const handleEditTask = useCallback((taskId: string, newTitle: string) => {
    setTasks((prev) =>
      prev.map((task) =>
        task.id === taskId ? { ...task, title: newTitle, editing: false } : task
      )
    );
    setEditingTaskId(null);
    setEditedTaskTitle('');
  }, []);

  const handleStartEdit = useCallback((taskId: string, currentTitle: string) => {
    setEditingTaskId(taskId);
    setEditedTaskTitle(currentTitle);
  }, []);

  const handleCancelEdit = useCallback(() => {
    setEditingTaskId(null);
    setEditedTaskTitle('');
  }, []);

  const handleDeleteTask = useCallback((taskId: string) => {
    setTasks((prev) => prev.filter((task) => task.id !== taskId));
  }, []);

  const handleToggleTaskStatus = useCallback((taskId: string) => {
    setTasks((prev) =>
      prev.map((task) => {
        if (task.id === taskId) {
          const statusFlow = { pending: 'in_progress' as const, in_progress: 'completed' as const, completed: 'pending' as const };
          return { ...task, status: statusFlow[task.status] };
        }
        return task;
      })
    );
  }, []);

  const getStatusIcon = useCallback((status: Task['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle2 className="w-5 h-5 text-green-400" />;
      case 'in_progress':
        return <Loader2 className="w-5 h-5 text-yellow-400 animate-spin" />;
      default:
        return <Circle className="w-5 h-5 text-gray-400" />;
    }
  }, []);

  const currentChat = getCurrentChat();

  return (
    <div className="min-h-screen bg-anime-dark text-anime-light flex flex-col relative overflow-hidden">
      <div className="absolute inset-0 animated-bg opacity-50" />

      {sparkles.map((sparkle) => (
        <div key={sparkle.id} className="sparkle" style={sparkle.style} />
      ))}

      <header className="relative z-10 flex justify-between items-center p-4 border-b border-gray-800/50 backdrop-blur-sm bg-anime-dark/50">
        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} className="flex items-center gap-3">
          <div className="relative">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-anime-orange to-yellow-500 flex items-center justify-center shadow-glow">
              <Bot className="w-6 h-6 text-anime-dark" />
            </div>
            <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full border-2 border-anime-dark animate-pulse" />
          </div>
          <div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-anime-orange to-yellow-400 bg-clip-text text-transparent">
              Video Creator AI
            </h1>
            <p className="text-xs text-gray-400">Your intelligent assistant</p>
          </div>
        </motion.div>

        <nav className="flex gap-2">
          {['About', 'Skills', 'Tasks', 'Chat', 'Settings'].map((item, index) => (
            <motion.button
              key={item}
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              onClick={() => {
                if (item === 'Tasks') setActiveTab('tasks');
                if (item === 'Chat') setActiveTab('chat');
              }}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 ${
                (item === 'Tasks' && activeTab === 'tasks') ||
                (item === 'Chat' && activeTab === 'chat')
                  ? 'bg-anime-orange text-anime-dark shadow-glow'
                  : 'bg-anime-dark-secondary hover:bg-anime-orange/20 hover:shadow-glow-soft'
              }`}
            >
              {item}
            </motion.button>
          ))}
        </nav>
      </header>

      <div className="relative z-10 flex flex-1">
        <motion.aside
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="w-80 p-4 border-r border-gray-800/50 backdrop-blur-sm bg-anime-dark/30 flex flex-col hidden md:flex overflow-y-auto"
        >
          {/* Chat History Section */}
          <div className="mb-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wide">Chats</h3>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleCreateNewChat}
                className="p-1.5 rounded-lg bg-anime-orange/20 hover:bg-anime-orange/30 transition-colors"
                title="New chat"
              >
                <Plus className="w-4 h-4 text-anime-orange" />
              </motion.button>
            </div>

            <div className="space-y-2 max-h-64 overflow-y-auto">
              {chats.map((chat) => (
                <motion.div
                  key={chat.id}
                  whileHover={{ scale: 1.02 }}
                  onClick={() => setCurrentChatId(chat.id)}
                  className={`relative group p-3 rounded-xl cursor-pointer transition-all duration-300 ${
                    currentChatId === chat.id
                      ? 'bg-gradient-to-r from-anime-orange/20 to-yellow-500/20 border border-anime-orange/30'
                      : 'bg-anime-dark-secondary/50 hover:bg-anime-dark-secondary border border-transparent'
                  }`}
                >
                  <div className="flex items-start gap-2">
                    <MessageSquare className={`w-4 h-4 mt-0.5 flex-shrink-0 ${
                      currentChatId === chat.id ? 'text-anime-orange' : 'text-gray-400'
                    }`} />
                    <div className="flex-1 min-w-0">
                      <h4 className="text-sm font-medium truncate">{chat.title}</h4>
                      <p className="text-xs text-gray-500 truncate mt-1">
                        {chat.messages[chat.messages.length - 1]?.content.slice(0, 50)}...
                      </p>
                      <p className="text-xs text-gray-600 mt-1">
                        {chat.updatedAt.toLocaleDateString()} {chat.updatedAt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </p>
                    </div>
                    <button
                      onClick={(e) => handleDeleteChat(chat.id, e)}
                      className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-500/20 rounded transition-all"
                      title="Delete chat"
                    >
                      <Trash2 className="w-3 h-3 text-gray-500 hover:text-red-400" />
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Agent Info Section */}
          <div className="flex flex-col items-center text-center mb-6 pt-4 border-t border-gray-800/50">
            <motion.div
              className="relative"
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
            >
              <div className="w-24 h-24 rounded-full bg-gradient-to-br from-anime-orange via-yellow-400 to-pink-500 p-1 shadow-glow">
                <div className="w-full h-full rounded-full bg-anime-dark-secondary flex items-center justify-center">
                  <Bot className="w-12 h-12 text-anime-orange" />
                </div>
              </div>
              <div className="absolute -top-2 -right-2">
                <Sparkles className="w-5 h-5 text-anime-orange animate-pulse" />
              </div>
            </motion.div>

            <h2 className="text-xl font-bold mt-3 bg-gradient-to-r from-anime-orange to-yellow-400 bg-clip-text text-transparent">
              Maya AI
            </h2>
            <p className="text-xs text-gray-400 mt-1">Your creative assistant</p>
          </div>

          <div className="space-y-2">
            <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wide">Skills</h3>
            {skills.map((skill, index) => (
              <motion.div
                key={skill.name}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center gap-2 p-2.5 rounded-xl bg-anime-dark-secondary/50 glow-border transition-all duration-300 hover:scale-105 cursor-pointer"
              >
                <skill.icon className={`w-4 h-4 ${skill.color}`} />
                <span className="text-xs font-medium">{skill.name}</span>
              </motion.div>
            ))}
          </div>

          <div className="mt-auto p-3 rounded-xl bg-gradient-to-br from-anime-orange/10 to-yellow-500/10 border border-anime-orange/20">
            <p className="text-xs text-gray-300 leading-relaxed">
              I help you create content, automate tasks, conduct research, and assist with coding. Let&apos;s create something amazing together! ✨
            </p>
          </div>
        </motion.aside>

        <main className="flex-1 flex flex-col backdrop-blur-sm">
          <AnimatePresence mode="wait">
            {activeTab === 'chat' ? (
              <motion.div
                key="chat"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="flex-1 flex flex-col"
              >
                <div className="flex-1 overflow-y-auto p-6 space-y-4">
                  {currentChat?.messages.map((message) => (
                    <motion.div
                      key={message.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} message-animate`}
                    >
                      <div
                        className={`max-w-2xl px-5 py-3 rounded-2xl ${
                          message.role === 'user'
                            ? 'bg-anime-dark-secondary text-anime-light'
                            : 'bg-gradient-to-br from-anime-orange/20 to-yellow-500/20 border border-anime-orange/30 shadow-glow-soft'
                        }`}
                      >
                        <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
                        <p className="text-xs text-gray-500 mt-2">
                          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </p>
                      </div>
                    </motion.div>
                  ))}

                  {isTyping && (
                    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="flex justify-start">
                      <div className="bg-gradient-to-br from-anime-orange/20 to-yellow-500/20 border border-anime-orange/30 rounded-2xl px-5 py-3">
                        <div className="typing-indicator flex gap-1">
                          <span />
                          <span />
                          <span />
                        </div>
                      </div>
                    </motion.div>
                  )}

                  <div ref={messagesEndRef} />
                </div>

                <div className="p-4 border-t border-gray-800/50 backdrop-blur-sm bg-anime-dark/30">
                  <div className="flex gap-3 items-center">
                    <div className="flex-1 relative">
                      <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
                        placeholder="Ask me anything or give me a task... (Shift+Enter for new line)"
                        className="w-full px-5 py-3 pr-12 rounded-full bg-anime-dark-secondary border border-gray-700/50 focus:border-anime-orange/50 focus:outline-none focus:shadow-glow-soft transition-all duration-300 text-sm"
                      />
                      <button className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-full hover:bg-anime-orange/20 transition-colors">
                        <Mic className="w-4 h-4 text-gray-400" />
                      </button>
                    </div>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={handleSendMessage}
                      className="px-6 py-3 rounded-full bg-gradient-to-r from-anime-orange to-yellow-500 text-anime-dark font-semibold shadow-glow hover:shadow-glow transition-all duration-300 flex items-center gap-2"
                    >
                      <Send className="w-4 h-4" />
                      Send
                    </motion.button>
                  </div>
                  <p className="text-xs text-gray-500 mt-2 text-center">
                    Try: &quot;Create 5 viral titles&quot; or &quot;Add task: Plan content calendar&quot;
                  </p>
                </div>
              </motion.div>
            ) : (
              <motion.div
                key="tasks"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="flex-1 p-6 overflow-y-auto"
              >
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-2xl font-bold">Tasks</h2>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleCreateTask}
                    className="px-4 py-2 rounded-full bg-anime-orange text-anime-dark font-semibold shadow-glow hover:shadow-glow transition-all duration-300 flex items-center gap-2 text-sm"
                  >
                    <Plus className="w-4 h-4" />
                    Create Task
                  </motion.button>
                </div>

                <div className="space-y-3">
                  {tasks.length === 0 ? (
                    <div className="text-center py-12">
                      <Circle className="w-16 h-16 text-gray-700 mx-auto mb-4" />
                      <p className="text-gray-400">No tasks yet. Create one to get started!</p>
                      <p className="text-gray-500 text-sm mt-2">
                        You can also create tasks from chat: &quot;Add task: Your task name&quot;
                      </p>
                    </div>
                  ) : (
                    tasks.map((task) => (
                      <motion.div
                        key={task.id}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="p-4 rounded-xl bg-anime-dark-secondary/50 glow-border transition-all duration-300 hover:scale-[1.02]"
                      >
                        {editingTaskId === task.id ? (
                          <div className="flex items-center gap-3">
                            <input
                              type="text"
                              value={editedTaskTitle}
                              onChange={(e) => setEditedTaskTitle(e.target.value)}
                              onKeyPress={(e) => e.key === 'Enter' && handleEditTask(task.id, editedTaskTitle)}
                              className="flex-1 px-3 py-2 rounded-lg bg-anime-dark border border-gray-700 focus:border-anime-orange/50 focus:outline-none text-sm"
                              autoFocus
                            />
                            <motion.button
                              whileHover={{ scale: 1.1 }}
                              whileTap={{ scale: 0.9 }}
                              onClick={() => handleEditTask(task.id, editedTaskTitle)}
                              className="p-2 rounded-lg bg-green-500/20 text-green-400 hover:bg-green-500/30 transition-colors"
                            >
                              <CheckCircle2 className="w-4 h-4" />
                            </motion.button>
                            <motion.button
                              whileHover={{ scale: 1.1 }}
                              whileTap={{ scale: 0.9 }}
                              onClick={handleCancelEdit}
                              className="p-2 rounded-lg bg-red-500/20 text-red-400 hover:bg-red-500/30 transition-colors"
                            >
                              <X className="w-4 h-4" />
                            </motion.button>
                          </div>
                        ) : (
                          <div className="flex items-center justify-between">
                            <div
                              className="flex items-center gap-3 flex-1 cursor-pointer"
                              onClick={() => handleToggleTaskStatus(task.id)}
                            >
                              {getStatusIcon(task.status)}
                              <div>
                                <h3 className="font-semibold">{task.title}</h3>
                                <p className="text-xs text-gray-400 flex items-center gap-1">
                                  <Clock className="w-3 h-3" />
                                  {task.createdAt.toLocaleString()}
                                </p>
                              </div>
                            </div>
                            <div className="flex items-center gap-2">
                              <span
                                className={`px-2 py-1 rounded-full text-xs font-medium cursor-pointer hover:opacity-80 ${
                                  task.status === 'completed'
                                    ? 'bg-green-400/20 text-green-400'
                                    : task.status === 'in_progress'
                                    ? 'bg-yellow-400/20 text-yellow-400'
                                    : 'bg-gray-400/20 text-gray-400'
                                }`}
                                onClick={() => handleToggleTaskStatus(task.id)}
                              >
                                {task.status.replace('_', ' ')}
                              </span>
                              <motion.button
                                whileHover={{ scale: 1.1 }}
                                whileTap={{ scale: 0.9 }}
                                onClick={() => handleStartEdit(task.id, task.title)}
                                className="p-2 rounded-lg hover:bg-anime-orange/20 transition-colors"
                              >
                                <Edit2 className="w-4 h-4 text-gray-400" />
                              </motion.button>
                              <motion.button
                                whileHover={{ scale: 1.1 }}
                                whileTap={{ scale: 0.9 }}
                                onClick={() => handleDeleteTask(task.id)}
                                className="p-2 rounded-lg hover:bg-red-500/20 transition-colors"
                              >
                                <Trash2 className="w-4 h-4 text-gray-400" />
                              </motion.button>
                            </div>
                          </div>
                        )}
                      </motion.div>
                    ))
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </main>
      </div>
    </div>
  );
}
