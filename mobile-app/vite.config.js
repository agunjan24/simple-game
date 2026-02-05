import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { viteStaticCopy } from 'vite-plugin-static-copy'

export default defineConfig({
  plugins: [
    vue(),
    viteStaticCopy({
      targets: [
        { src: '../images', dest: '.' },
        { src: '../images_hollywood', dest: '.' },
        { src: '../images_history', dest: '.' },
      ],
    }),
  ],
  base: './',
})
