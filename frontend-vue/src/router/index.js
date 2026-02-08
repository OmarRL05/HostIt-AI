import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '@/views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/chat',
      name: 'chat',
      // component: ChatView // uncomment when file created
      component: () => import('@/views/LoginView.vue') // Temporal placeholder
    }
  ],
})

export default router
