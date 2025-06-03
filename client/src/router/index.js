import { createRouter, createWebHashHistory } from 'vue-router';

// Main views
const HomeView = () => import('@/views/Home/HomeView.vue')
const LoginView = () => import('@/views/Login/LoginView.vue')
const RegisterView = () => import('@/views/Login/RegisterView.vue')
const ProfileView = () => import('@/views/Profile/ProfileView.vue')

// Messages module
const MessagesHome = () => import('@/views/Messages/MessagesHome.vue')
const ChatPage = () => import('@/views/Messages/ChatPage.vue')
const RiderProfilePage = () => import('@/views/Messages/RiderProfilePage.vue')

// Profile sub-routes
const ProfilePersonal = () => import('@/views/Profile/ProfilePersonal.vue')
const ProfileOrderHistory = () => import('@/views/Profile/ProfileOrderHistory.vue')
const ProfileSwitchAccount = () => import('@/views/Profile/ProfileSwitchAccount.vue')
const ContactServiceView = () => import('@/views/Profile/ContactServiceView.vue')
import OrderDetail from '@/views/Order/OrderDetail.vue'

const routes = [
  {
    path: '/',
    redirect: '/home' // Redirect to home instead of login (more common pattern)
  },
  {
    path: '/home',
    name: 'home',
    component: HomeView,
    meta: { 
      requiresAuth: true,
      title: '首页'
    }
  },
  {
    path: '/publish',
    name: 'publish',
    component: () => import('@/views/Home/PublishView.vue'),
    meta: {
      title: '发布委托'
    }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { 
      requiresGuest: true,
      title: '登录'
    }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: {
      requiresGuest: true,
      title: '注册'
    }
  },
  // Messages module routes
  {
    path: '/messages',
    name: 'messages',
    component: () => import('@/views/Messages/MessagesHome.vue'),
    meta: { 
      requiresAuth: true,
      title: '消息'
    }
  },
  {
    path: '/messages/chat/:chatId',
    name: 'chat',
    component: () => import('@/views/Messages/ChatPage.vue'),
    props: true,
    meta: { 
      requiresAuth: true,
      title: '聊天'
    }
  },
  {
    path: '/rider/:riderId/profile',
    name: 'rider-profile',
    component: () => import('@/views/Messages/RiderProfilePage.vue'),
    props: true,
    meta: { 
      requiresAuth: true,
      title: '送餐员资料'
    }
  },
  // Profile module routes
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/Profile/ProfileView.vue'),
    meta: { 
      requiresAuth: true,
      title: '个人资料'
    }
  },
  {
    path: '/profile/personal',
    name: 'profile-personal',
    component: () => import('@/views/Profile/ProfilePersonal.vue'),
    meta: { 
      requiresAuth: true,
      title: '个人资料'
    }
  },
  {
    path: '/profile/orders',
    name: 'profileOrders',
    component: () => import('@/views/Profile/ProfileOrderHistory.vue'),
    meta: { 
      requiresAuth: true,
      title: '历史订单'
    }
  },  {
    path: '/profile/account-management',
    name: 'profile-account-management',
    component: () => import('@/views/Profile/AccountManagement.vue'),
    meta: { 
      requiresAuth: true,
      title: '账号管理'
    }
  },
  {
    path: '/profile/contact-service',
    name: 'ContactService',
    component: ContactServiceView
  },
  // Fallback route for 404
  {
    path: '/:pathMatch(.*)*',
    redirect: '/home'
  },
  {
    path: '/orders/:id',
    name: 'OrderDetail',
    component: OrderDetail,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
  // Better scroll behavior
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Authentication guard
function checkAuthentication() {
  // 检查 localStorage 中是否有 token (与 userStore 保持一致)
  return !!localStorage.getItem('token');
  // 或者，如果你使用 Pinia/Vuex:
  // import { useUserStore } from '@/stores/userStore';
  // const userStore = useUserStore();
  // return userStore.isLoggedIn;
}

router.beforeEach((to, from, next) => {
  const isAuthenticated = checkAuthentication();
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiresGuest = to.matched.some(record => record.meta.requiresGuest);

  // 更新文档标题
  if (to.meta.title) {
    document.title = `${to.meta.title} | 学士配送`; // 确保替换 "你的应用名称"
  } else {
    document.title = '学士配送'; // 默认标题
  }

  if (requiresAuth && !isAuthenticated) {
    // 如果需要认证但用户未认证，重定向到登录页
    // 将用户尝试访问的路径作为查询参数传递，以便登录后可以重定向回去
    console.log('需要认证但未登录，跳转到登录页，目标:', to.fullPath);
    next({ name: 'login', query: { redirect: to.fullPath } });
  } else if (requiresGuest && isAuthenticated) {
    // 如果是访客页面（如登录、注册）但用户已认证，重定向到首页
    console.log('已登录，访问访客页面，跳转到首页');
    next({ name: 'home' });
  } else {
    // 其他情况（不需要认证，或者需要认证且已认证）正常导航
    console.log('正常导航至:', to.fullPath);
    next();
  }
});
export default router