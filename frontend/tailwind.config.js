import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './pages/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        'soccer-green': '#1A936F',
        'soccer-gold': '#F3E34E',
        'soccer-dark': '#1E293B',
      },
    },
  },
  plugins: [],
};
export default config;