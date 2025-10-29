/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,svelte,ts,js}'],
  theme: {
    extend: {
      colors: {
        background: '#ffffff',
        foreground: '#000000',
        muted: '#888888',
        panel: '#f5f5f5',
        border: '#e5e5e5'
      },
      fontFamily: {
        sans: [
          'Inter',
          'ui-sans-serif', 'system-ui', 'Segoe UI', 'Roboto', 'Ubuntu', 'Cantarell', 'Noto Sans', 'Helvetica', 'Arial', 'Apple Color Emoji', 'Segoe UI Emoji'
        ]
      }
    }
  },
  plugins: [require('@tailwindcss/forms')]
};


