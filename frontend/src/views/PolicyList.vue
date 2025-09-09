<template>
  <div class="policy-list-page">
    <!-- 顶部导航栏 -->
    <van-nav-bar
      title="公司政策"
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
      
      <!-- 政策列表 -->
      <div class="policy-list" v-else-if="policies.length > 0">
        <van-cell-group inset v-for="policy in policies" :key="policy.id" class="policy-item">
          <van-cell :title="policy.title" :label="policy.description">
            <template #right-icon>
              <van-tag :type="getTagType(policy.category)">{{ policy.category }}</van-tag>
            </template>
          </van-cell>
          <van-cell title="文件类型" :value="getFileTypeText(policy.file_type)" />
          <van-cell title="上传时间" :value="formatDateTime(policy.created_at)" />
        </van-cell-group>
      </div>
      
      <!-- 空状态 -->
      <div class="empty-wrapper" v-else>
        <van-empty description="暂无政策文件">
          <template #bottom>
            <van-button 
              round 
              type="primary" 
              @click="$router.push('/policy-upload')"
              v-if="userStore.isAdmin"
            >
              上传政策
            </van-button>
          </template>
        </van-empty>
      </div>
      
      <!-- 上传按钮 -->
      <div class="upload-button" v-if="userStore.isAdmin">
        <van-button 
          round 
          type="primary" 
          icon="plus" 
          @click="$router.push('/policy-upload')"
        >
          上传政策
        </van-button>
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import dayjs from 'dayjs'
import { useUserStore } from '../stores/user'

// 路由
const router = useRouter()

// 状态管理
const userStore = useUserStore()

// 激活的标签页
const activeTab = ref(0)

// 加载状态
const loading = ref(false)

// 政策列表
const policies = ref([
  // 示例数据
  {
    id: 1,
    title: '公司请假制度',
    description: '关于员工请假的相关规定',
    file_type: 'txt',
    category: 'leave',
    created_at: '2023-01-01 10:00:00'
  },
  {
    id: 2,
    title: '考勤制度',
    description: '关于员工考勤的相关规定',
    file_type: 'txt',
    category: 'attendance',
    created_at: '2023-01-02 10:00:00'
  },
  {
    id: 3,
    title: '加班调休规定',
    description: '关于员工加班调休的相关规定',
    file_type: 'txt',
    category: 'overtime',
    created_at: '2023-01-03 10:00:00'
  }
])

// 格式化日期时间
const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return ''
  return dayjs(dateTimeStr).format('YYYY-MM-DD HH:mm')
}

// 获取文件类型文本
const getFileTypeText = (fileType) => {
  const typeMap = {
    'txt': '文本文件',
    'pdf': 'PDF文件',
    'docx': 'Word文档',
    'csv': 'CSV表格',
    'json': 'JSON文件'
  }
  return typeMap[fileType] || fileType
}

// 获取标签类型
const getTagType = (category) => {
  const typeMap = {
    'leave': 'primary',
    'attendance': 'success',
    'overtime': 'warning',
    'salary': 'danger'
  }
  return typeMap[category] || 'default'
}

// 获取政策列表
const fetchPolicies = async () => {
  loading.value = true
  
  try {
    // 在实际项目中，这里应该调用API获取政策列表
    // const response = await policyApi.getPolicies()
    // policies.value = response
    
    // 模拟加载
    await new Promise(resolve => setTimeout(resolve, 500))
  } catch (error) {
    console.error('Failed to fetch policies:', error)
    showToast('获取政策列表失败')
  } finally {
    loading.value = false
  }
}

// 组件挂载时执行
onMounted(async () => {
  // 初始化用户信息
  userStore.initUserInfo()
  
  // 获取政策列表
  await fetchPolicies()
})
</script>

<style scoped>
.policy-list {
  padding-bottom: 16px;
}

.policy-item {
  margin-bottom: 12px;
}

.loading-wrapper, .empty-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.upload-button {
  position: fixed;
  bottom: 70px;
  right: 16px;
  z-index: 10;
}
</style> 