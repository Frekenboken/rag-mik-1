// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', name: 'Home', component: Home, meta: { requiresAuth: true }},
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard для приватных роутов
router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()
  if (!auth.initialized) await auth.checkAuth()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return next({ name: 'Login', query: { redirect: to.fullPath } })
  }

  if ((to.name === 'Login' || to.name === 'Register') && auth.isAuthenticated) {
    return next({ name: 'Home' })
  }

  next()
})

export default router
