import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../components/Dashboard.vue')
  },
  {
    path: '/movies',
    name: 'Movies',
    component: () => import('../components/MovieList.vue')
  },
  {
    path: '/prediction',
    name: 'Prediction',
    component: () => import('../components/MoviePrediction.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router    