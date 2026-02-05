import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'welcome',
    component: () => import('./views/WelcomeScreen.vue'),
  },
  {
    path: '/game',
    name: 'game',
    component: () => import('./views/GameScreen.vue'),
  },
  {
    path: '/gameover',
    name: 'gameover',
    component: () => import('./views/GameOverScreen.vue'),
  },
]

export default createRouter({
  history: createWebHashHistory(),
  routes,
})
