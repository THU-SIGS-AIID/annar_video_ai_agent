import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        'anime-orange': '#F6A560',
        'anime-dark': '#0F1112',
        'anime-dark-secondary': '#0F2124',
        'anime-light': '#F5F5F5',
        'anime-glow': 'rgba(246, 165, 96, 0.3)',
      },
      boxShadow: {
        'glow': '0 0 20px rgba(246, 165, 96, 0.4)',
        'glow-soft': '0 0 10px rgba(246, 165, 96, 0.2)',
        'inner-glow': 'inset 0 0 20px rgba(246, 165, 96, 0.1)',
      },
      animation: {
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'float': 'float 3s ease-in-out infinite',
        'sparkle': 'sparkle 1.5s ease-in-out infinite',
      },
      keyframes: {
        'pulse-glow': {
          '0%, 100%': { boxShadow: '0 0 20px rgba(246, 165, 96, 0.4)' },
          '50%': { boxShadow: '0 0 30px rgba(246, 165, 96, 0.6)' },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        'sparkle': {
          '0%, 100%': { opacity: '0.3', transform: 'scale(0.8)' },
          '50%': { opacity: '1', transform: 'scale(1.2)' },
        },
      },
    },
  },
  plugins: [],
};
export default config;
