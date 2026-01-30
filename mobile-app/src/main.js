import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router.js'
import './assets/global.css'

const pinia = createPinia()
const app = createApp(App)
app.use(pinia)
app.use(router)

// Initialize game store
import { useGameStore } from './stores/gameStore.js'
const store = useGameStore()
store.init()

app.mount('#app')
