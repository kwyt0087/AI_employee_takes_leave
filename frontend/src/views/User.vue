<template>
  <div class="user-page">
    <!-- 顶部导航栏 -->
    <van-nav-bar
      title="个人中心"
      fixed
      placeholder
    />
    
    <!-- 页面内容 -->
    <div class="page-container">
      <!-- 用户信息 -->
      <div class="user-info card-wrapper" v-if="userStore.isLoggedIn">
        <div class="avatar">{{ userInitial }}</div>
        <div class="info">
          <div class="name">{{ userStore.fullName || '未登录' }}</div>
          <div class="details">
            <span class="department">{{ userStore.userInfo?.department || '未知部门' }}</span>
            <span class="position">{{ userStore.userInfo?.position || '未知职位' }}</span>
          </div>
          <div class="employee-id">工号：{{ userStore.userInfo?.employee_id || '未知' }}</div>
        </div>
      </div>
      
      <!-- 年假信息 -->
      <div class="annual-leave card-wrapper" v-if="annualLeave">
        <div class="section-title">年假信息</div>
        <div class="leave-stats">
          <div class="stat-item">
            <div class="value">{{ annualLeave.total_days || 0 }}</div>
            <div class="label">总天数</div>
          </div>
          <div class="stat-item">
            <div class="value">{{ annualLeave.used_days || 0 }}</div>
            <div class="label">已使用</div>
          </div>
          <div class="stat-item">
            <div class="value text-primary">{{ annualLeave.remaining_days || 0 }}</div>
            <div class="label">剩余天数</div>
          </div>
        </div>
      </div>
      
      <!-- 功能菜单 -->
      <van-cell-group inset title="功能菜单" class="function-menu">
        <van-cell title="我的请假记录" icon="records" is-link to="/leave-list" />
        <van-cell title="请假申请" icon="calendar-o" is-link to="/leave-apply" />
        <van-cell title="AI助手" icon="chat-o" is-link to="/chat" />
        <van-cell title="公司政策" icon="description" is-link to="/policy-list" />
      </van-cell-group>
      
      <!-- 系统设置 -->
      <van-cell-group inset title="系统设置" class="system-settings">
        <van-cell title="关于我们" icon="info-o" is-link @click="showAbout" />
        <van-cell title="退出登录" icon="sign" @click="confirmLogout" />
      </van-cell-group>
      
      <!-- 未登录状态 -->
      <div class="login-tip" v-if="!userStore.isLoggedIn">
        <van-empty description="请先登录">
          <template #bottom>
            <van-button round type="primary" @click="$router.push('/login')">去登录</van-button>
          </template>
        </van-empty>
      </div>
    </div>
    
    <!-- 底部导航栏 -->
    <van-tabbar v-model="activeTab" route>
      <van-tabbar-item icon="home-o" to="/">首页</van-tabbar-item>
      <van-tabbar-item icon="chat-o" to="/chat">AI助手</van-tabbar-item>
      <van-tabbar-item icon="calendar-o" to="/leave-apply">请假</van-tabbar-item>
      <van-tabbar-item icon="user-o" to="/user">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showDialog } from 'vant'
import { useUserStore } from '../stores/user'

// 路由
const router = useRouter()

// 状态管理
const userStore = useUserStore()

// 激活的标签页
const activeTab = ref(3)

// 用户头像首字母
const userInitial = computed(() => {
  return userStore.fullName?.charAt(0) || 'U'
})
console.log(userStore,'userStore');

// 年假信息
const annualLeave = computed(() => userStore.userInfo?.annual_leave)

// 显示关于我们
const showAbout = () => {
  showDialog({
    title: '关于我们',
    message: 'AI请假系统 v1.0.0\n基于Vue 3 + Vant UI + FastAPI + RAG技术\n提供智能请假推荐服务',
    confirmButtonText: '确定'
  })
}

// 确认退出登录
const confirmLogout = () => {
  showDialog({
    title: '退出登录',
    message: '确定要退出登录吗？',
    showCancelButton: true
  }).then(() => {
    // 执行退出登录
    userStore.logout()
    showToast('已退出登录')
    router.push('/login')
  }).catch(() => {
    // 取消退出
  })
}

// 组件挂载时执行
onMounted(() => {
  // 初始化用户信息
  userStore.initUserInfo()
})
</script>

<style scoped>
.user-info {
  display: flex;
  align-items: center;
  padding: 20px;
  margin-bottom: 16px;
}

.avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background-color: #1989fa;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  margin-right: 16px;
}

.info .name {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 4px;
}

.info .details {
  font-size: 14px;
  color: #646566;
  margin-bottom: 4px;
}

.info .details .department {
  margin-right: 8px;
}

.info .employee-id {
  font-size: 14px;
  color: #969799;
}

.annual-leave {
  padding: 16px;
  margin-bottom: 16px;
}

.leave-stats {
  display: flex;
  justify-content: space-around;
  margin-top: 12px;
}

.stat-item {
  text-align: center;
}

.stat-item .value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 4px;
}

.stat-item .label {
  font-size: 14px;
  color: #969799;
}

.function-menu, .system-settings {
  margin-bottom: 16px;
}

.login-tip {
  margin-top: 40px;
}
</style> 