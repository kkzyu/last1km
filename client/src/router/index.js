import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import MessagesHome from '@/views/Messages/MessagesHome.vue';
import ChatPage from '@/views/Messages/ChatPage.vue';
import RiderProfilePage from '@/views/Messages/RiderProfilePage.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/messages',
    name: 'MessagesHome',
    component: MessagesHome,
    meta: { title: '消息' }
  },
  {
    // 使用 :chatId 作为动态参数，代表某个具体的聊天
    path: '/messages/chat/:chatId',
    name: 'ChatPage',
    component: ChatPage,
    props: true, // 允许将路由参数作为 props 传递给组件
    meta: { title: '聊天详情' }
  },
  {
    // 使用 :riderId 作为动态参数，代表某个骑手
    path: '/rider/:riderId/profile',
    name: 'RiderProfilePage',
    component: RiderProfilePage,
    props: true,
    meta: { title: '送餐员主页' }
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/ProfileView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
