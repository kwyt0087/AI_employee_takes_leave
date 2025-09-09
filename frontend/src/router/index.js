import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Chat from '../views/Chat.vue'
import LeaveApply from '../views/LeaveApply.vue'
import LeaveRecommend from '../views/LeaveRecommend.vue'
import LeaveList from '../views/LeaveList.vue'
import LeaveDetail from '../views/LeaveDetail.vue'
import PolicyList from '../views/PolicyList.vue'
import PolicyUpload from '../views/PolicyUpload.vue'
import Login from '../views/Login.vue'
import User from '../views/User.vue'

// 路由配置
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: false }
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chat,
    meta: { requiresAuth: true }
  },
  {
    path: '/leave-apply',
    name: 'LeaveApply',
    component: LeaveApply,
    meta: { requiresAuth: true }
  },
  {
    path: '/leave-recommend',
    name: 'LeaveRecommend',
    component: LeaveRecommend,
    meta: { requiresAuth: true }
  },
  {
    path: '/leave-list',
    name: 'LeaveList',
    component: LeaveList,
    meta: { requiresAuth: true }
  },
  {
    path: '/leave-detail/:id',
    name: 'LeaveDetail',
    component: LeaveDetail,
    meta: { requiresAuth: true }
  },
  {
    path: '/policy-list',
    name: 'PolicyList',
    component: PolicyList,
    meta: { requiresAuth: false }
  },
  {
    path: '/policy-upload',
    name: 'PolicyUpload',
    component: PolicyUpload,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/user',
    name: 'User',
    component: User,
    meta: { requiresAuth: false }
  },
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: { title: '页面不存在', keepAlive: false }
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 全局路由守卫
router.beforeEach((to, from, next) => {
  // 检查是否需要登录
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin)
  
  // 获取登录状态
  const isLoggedIn = localStorage.getItem('token') !== null
  const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
  const isAdmin = userInfo?.is_admin === true
  
  if (requiresAuth && !isLoggedIn) {
    // 需要登录但未登录，重定向到登录页面
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else if (requiresAdmin && !isAdmin) {
    // 需要管理员权限但不是管理员，重定向到首页
    next({ path: '/' })
  } else {
    // 其他情况正常放行
    next()
  }
})

export default router 