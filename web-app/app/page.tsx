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
} from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface Task {
  id: string;
  title: string;
  status: 'pending' | 'in_progress' | 'completed';
  createdAt: Date;
}

const skills = [
  { name: 'Task Automation', icon: Zap, color: 'text-yellow-400' },
  { name: 'Research & Analysis', icon: Brain, color: 'text-purple-400' },
  { name: 'Content Creation', icon: FileText, color: 'text-blue-400' },
  { name: 'Coding Assistance', icon: Code, color: 'text-green-400' },
] as const;

// Move sparkles outside component to avoid re-creation
const createSparkles = () =>
  Array.from({ length: 15 }, (_, i) => ({
    id: `sparkle-${i}`,
    style: {
      left: `${Math.random() * 100}%`,
      top: `${Math.random() * 100}%`,
      animationDelay: `${Math.random() * 3}s`,
    },
  }));

const initialSparkles = createSparkles();

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: "Hi! 👋 I'm your AI assistant. I can help you with content creation, research, automation, and much more. What would you like to work on today?",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [activeTab, setActiveTab] = useState<'chat' | 'tasks'>('chat');
  const [tasks, setTasks] = useState<Task[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Memoize sparkles to prevent re-creation
  const sparkles = useMemo(() => initialSparkles, []);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const handleSendMessage = useCallback(async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });

      if (!response.ok) throw new Error('Failed to get response');

      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.message || 'I processed your request!',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  }, [input]);

  const handleCreateTask = useCallback(() => {
    const newTask: Task = {
      id: Date.now().toString(),
      title: 'New Task',
      status: 'pending',
      createdAt: new Date(),
    };
    setTasks((prev) => [...prev, newTask]);
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

  return (
    <div className="min-h-screen bg-anime-dark text-anime-light flex flex-col relative overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 animated-bg opacity-50" />

      {/* Sparkle particles */}
      {sparkles.map((sparkle) => (
        <div
          key={sparkle.id}
          className="sparkle"
          style={sparkle.style}
        />
      ))}

      {/* Header */}
      <header className="relative z-10 flex justify-between items-center p-4 border-b border-gray-800/50 backdrop-blur-sm bg-anime-dark/50">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center gap-3"
        >
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

      {/* Main Content */}
      <div className="relative z-10 flex flex-1">
        {/* Left Panel - Agent Info */}
        <motion.aside
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="w-80 p-6 border-r border-gray-800/50 backdrop-blur-sm bg-anime-dark/30 flex flex-col hidden md:flex"
        >
          <div className="flex flex-col items-center text-center mb-6">
            <motion.div
              className="relative"
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
            >
              <div className="w-32 h-32 rounded-full bg-gradient-to-br from-anime-orange via-yellow-400 to-pink-500 p-1 shadow-glow">
                <div className="w-full h-full rounded-full bg-anime-dark-secondary flex items-center justify-center">
                  <Bot className="w-16 h-16 text-anime-orange" />
                </div>
              </div>
              <div className="absolute -top-2 -right-2">
                <Sparkles className="w-6 h-6 text-anime-orange animate-pulse" />
              </div>
            </motion.div>

            <h2 className="text-2xl font-bold mt-4 bg-gradient-to-r from-anime-orange to-yellow-400 bg-clip-text text-transparent">
              Maya AI
            </h2>
            <p className="text-sm text-gray-400 mt-1">Your creative assistant</p>
          </div>

          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wide">Skills</h3>
            {skills.map((skill, index) => (
              <motion.div
                key={skill.name}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center gap-3 p-3 rounded-xl bg-anime-dark-secondary/50 glow-border transition-all duration-300 hover:scale-105 cursor-pointer"
              >
                <skill.icon className={`w-5 h-5 ${skill.color}`} />
                <span className="text-sm font-medium">{skill.name}</span>
              </motion.div>
            ))}
          </div>

          <div className="mt-auto p-4 rounded-xl bg-gradient-to-br from-anime-orange/10 to-yellow-500/10 border border-anime-orange/20">
            <p className="text-xs text-gray-300 leading-relaxed">
              I help you create content, automate tasks, conduct research, and assist with coding. Let&apos;s create something amazing together! ✨
            </p>
          </div>
        </motion.aside>

        {/* Right Panel - Main Content */}
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
                {/* Chat Messages */}
                <div className="flex-1 overflow-y-auto p-6 space-y-4">
                  {messages.map((message) => (
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
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="flex justify-start"
                    >
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

                {/* Chat Input */}
                <div className="p-4 border-t border-gray-800/50 backdrop-blur-sm bg-anime-dark/30">
                  <div className="flex gap-3 items-center">
                    <div className="flex-1 relative">
                      <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                        placeholder="Ask me anything or give me a task..."
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
                    </div>
                  ) : (
                    tasks.map((task) => (
                      <motion.div
                        key={task.id}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="p-4 rounded-xl bg-anime-dark-secondary/50 glow-border transition-all duration-300 hover:scale-[1.02] cursor-pointer"
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            {getStatusIcon(task.status)}
                            <div>
                              <h3 className="font-semibold">{task.title}</h3>
                              <p className="text-xs text-gray-400 flex items-center gap-1">
                                <Clock className="w-3 h-3" />
                                {task.createdAt.toLocaleString()}
                              </p>
                            </div>
                          </div>
                          <span
                            className={`px-2 py-1 rounded-full text-xs font-medium ${
                              task.status === 'completed'
                                ? 'bg-green-400/20 text-green-400'
                                : task.status === 'in_progress'
                                ? 'bg-yellow-400/20 text-yellow-400'
                                : 'bg-gray-400/20 text-gray-400'
                            }`}
                          >
                            {task.status.replace('_', ' ')}
                          </span>
                        </div>
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
