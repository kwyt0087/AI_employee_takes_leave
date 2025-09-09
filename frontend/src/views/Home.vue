<template>
  <div class="home-page">
    <!-- 顶部导航栏 -->
    <van-nav-bar
      title="AI请假系统"
      fixed
      placeholder
    />
    
    <!-- 页面内容 -->
    <div class="page-container">
      <!-- 用户信息卡片 -->
      <div class="user-card card-wrapper" v-if="userStore.isLoggedIn">
        <div class="user-info">
          <div class="avatar">{{ userStore.fullName?.charAt(0) || 'U' }}</div>
          <div class="info">
            <div class="name">{{ userStore.fullName || '未登录' }}</div>
            <div class="department">{{ userStore.userInfo?.department || '未知部门' }}</div>
          </div>
        </div>
        <div class="annual-leave-info" v-if="annualLeave">
          <div class="leave-item">
            <div class="label">年假总天数</div>
            <div class="value">{{ annualLeave.total_days || 0 }}天</div>
          </div>
          <div class="leave-item">
            <div class="label">已使用</div>
            <div class="value">{{ annualLeave.used_days || 0 }}天</div>
          </div>
          <div class="leave-item">
            <div class="label">剩余天数</div>
            <div class="value text-primary">{{ annualLeave.remaining_days || 0 }}天</div>
          </div>
        </div>
      </div>
      
      <!-- 功能卡片 -->
      <div class="feature-grid">
        <!-- 请假申请 -->
        <div class="feature-item" @click="navigateTo('/leave-apply')">
          <van-icon name="calendar-o" size="28" color="#1989fa" />
          <span>请假申请</span>
        </div>
        
        <!-- AI助手 -->
        <div class="feature-item" @click="navigateTo('/chat')">
          <van-icon name="chat-o" size="28" color="#07c160" />
          <span>AI助手</span>
        </div>
        
        <!-- 请假记录 -->
        <div class="feature-item" @click="navigateTo('/leave-list')">
          <van-icon name="records" size="28" color="#ff976a" />
          <span>请假记录</span>
        </div>
        
        <!-- 公司政策 -->
        <div class="feature-item" @click="navigateTo('/policy-list')">
          <van-icon name="description" size="28" color="#7232dd" />
          <span>公司政策</span>
        </div>
      </div>
      
      <!-- 最近请假记录 -->
      <div class="recent-leaves card-wrapper" v-if="recentLeaves.length > 0">
        <div class="section-title">最近请假记录</div>
        <van-cell-group inset>
          <van-cell
            v-for="leave in recentLeaves"
            :key="leave.id"
            :title="leave.leave_type"
            :label="`${leave.start_date} 至 ${leave.end_date}（${leave.days}天）`"
            :value="leaveStore.getStatusText(leave.status)"
            :to="`/leave-detail/${leave.id}`"
            is-link
          >
            <template #right-icon>
              <van-tag :color="leaveStore.getStatusColor(leave.status)">
                {{ leaveStore.getStatusText(leave.status) }}
              </van-tag>
            </template>
          </van-cell>
        </van-cell-group>
      </div>
      
      <!-- 登录提示 -->
      <div class="login-tip card-wrapper" v-if="!userStore.isLoggedIn">
        <van-empty description="请先登录">
          <van-button type="primary" @click="navigateTo('/login')">去登录</van-button>
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
import { useUserStore } from '../stores/user'
import { useLeaveStore } from '../stores/leave'

// 路由
const router = useRouter()

// 状态管理
const userStore = useUserStore()
const leaveStore = useLeaveStore()

// 激活的标签页
const activeTab = ref(0)

// 年假信息
const annualLeave = computed(() => userStore.userInfo?.annual_leave)

// 最近请假记录
const recentLeaves = computed(() => {
  return leaveStore.leaveRequests.slice(0, 3)
})

// 导航到指定路径
const navigateTo = (path) => {
  router.push(path)
}

// 组件挂载时执行
onMounted(async () => {
  // 初始化用户信息
  userStore.initUserInfo()
  
  // 如果已登录，获取请假记录
  if (userStore.isLoggedIn) {
    try {
      await leaveStore.fetchLeaveTypes()
      await leaveStore.fetchLeaveRequests(userStore.userId)
    } catch (error) {
      console.error('Failed to fetch data:', error)
    }
  }
})
</script>

<style scoped>
.user-card {
  padding: 16px;
  margin-bottom: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #1989fa;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  margin-right: 12px;
}

.info .name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 4px;
}

.info .department {
  font-size: 14px;
  color: #969799;
}

.annual-leave-info {
  display: flex;
  justify-content: space-between;
  border-top: 1px solid #ebedf0;
  padding-top: 12px;
}

.leave-item {
  text-align: center;
  flex: 1;
}

.leave-item .label {
  font-size: 12px;
  color: #969799;
  margin-bottom: 4px;
}

.leave-item .value {
  font-size: 16px;
  font-weight: bold;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.feature-item {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 12px rgba(100, 101, 102, 0.08);
  cursor: pointer;
}

.feature-item span {
  margin-top: 8px;
  font-size: 14px;
}

.recent-leaves {
  padding: 16px 0;
}

.login-tip {
  padding: 30px 0;
}
</style> 