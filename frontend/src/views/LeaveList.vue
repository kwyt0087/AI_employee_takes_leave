<template>
  <div class="leave-list-page">
    <!-- 顶部导航栏 -->
    <van-nav-bar
      title="请假记录"
      left-arrow
      @click-left="$router.back()"
      fixed
      placeholder
    />
    
    <!-- 页面内容 -->
    <div class="page-container">
      <!-- 加载中 -->
      <div class="loading-wrapper" v-if="loading">
        <van-loading size="24px" vertical>加载中...</van-loading>
      </div>
      
      <!-- 请假记录列表 -->
      <div class="leave-list" v-else-if="leaveRequests.length > 0">
        <van-cell-group inset v-for="leave in leaveRequests" :key="leave.id" class="leave-item">
          <van-cell
            :title="leave.leave_type"
            :label="`${leave.start_date} 至 ${leave.end_date}（${leave.days}天）`"
            :to="`/leave-detail/${leave.id}`"
            is-link
          >
            <template #right-icon>
              <van-tag :color="getStatusColor(leave.status)">
                {{ getStatusText(leave.status) }}
              </van-tag>
            </template>
          </van-cell>
          <van-cell title="请假原因" :value="leave.reason" />
          <van-cell title="申请时间" :value="formatDateTime(leave.created_at)" />
        </van-cell-group>
      </div>
      
      <!-- 空状态 -->
      <div class="empty-wrapper" v-else>
        <van-empty description="暂无请假记录">
          <template #bottom>
            <van-button round type="primary" @click="$router.push('/leave-apply')">去请假</van-button>
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
import { showToast } from 'vant'
import dayjs from 'dayjs'
import { useUserStore } from '../stores/user'
import { useLeaveStore } from '../stores/leave'

// 路由
const router = useRouter()

// 状态管理
const userStore = useUserStore()
const leaveStore = useLeaveStore()

// 激活的标签页
const activeTab = ref(0)

// 加载状态
const loading = ref(false)

// 请假记录列表
const leaveRequests = computed(() => leaveStore.leaveRequests)

// 格式化日期时间
const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return ''
  return dayjs(dateTimeStr).format('YYYY-MM-DD HH:mm')
}

// 获取状态文本
const getStatusText = (status) => {
  return leaveStore.getStatusText(status)
}

// 获取状态颜色
const getStatusColor = (status) => {
  return leaveStore.getStatusColor(status)
}

// 获取请假记录
const fetchLeaveRequests = async () => {
  if (!userStore.userId) return
  
  loading.value = true
  
  try {
    await leaveStore.fetchLeaveRequests(userStore.userId)
  } catch (error) {
    console.error('Failed to fetch leave requests:', error)
    showToast('获取请假记录失败')
  } finally {
    loading.value = false
  }
}

// 组件挂载时执行
onMounted(async () => {
  // 初始化用户信息
  userStore.initUserInfo()
  
  // 检查是否登录
  if (!userStore.isLoggedIn) {
    showToast('请先登录')
    router.push('/login')
    return
  }
  
  // 获取请假记录
  await fetchLeaveRequests()
})
</script>

<style scoped>
.leave-list {
  padding-bottom: 16px;
}

.leave-item {
  margin-bottom: 12px;
}

.loading-wrapper, .empty-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}
</style> 