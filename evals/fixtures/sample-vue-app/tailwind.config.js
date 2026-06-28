/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts}'
  ],
  theme: {
    extend: {
      colors: {
        primary: '#2563eb',
        'primary-dark': '#1e40af',
        accent: '#7c3aed',
        success: '#16a34a',
        warning: '#d97706',
        danger: '#dc2626',
        surface: '#f8fafc',
        ink: '#0f172a'
      },
      borderRadius: {
        card: '10px'
      }
    }
  },
  plugins: []
}
