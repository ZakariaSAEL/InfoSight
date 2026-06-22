import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Forward /analyze requests to the FastAPI backend during local dev
      '/analyze': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
