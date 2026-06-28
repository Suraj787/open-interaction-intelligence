import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Standard Vite + Vue 3 config for a small internal dashboard.
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173
  },
  build: {
    outDir: 'dist',
    sourcemap: false
  }
})
