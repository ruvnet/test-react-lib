import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    proxy: {
      '/proxy/api/capitolai': {
        target: 'https://animated-train-pg65x7gxvwf6r5j-5173.app.github.dev/api/v1',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/proxy\/api\/capitolai/, ''),
    },
    },
  },
  plugins: [react()],
})
