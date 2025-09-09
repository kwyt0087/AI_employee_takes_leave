<template>
  <div class="leave-recommend-page">
    <!-- 顶部导航栏 -->
    <van-nav-bar
      title="请假推荐"
      left-arrow
      @click-left="$router.back()"
      fixed
      placeholder
    />
    
    <!-- 页面内容 -->
    <div class="page-container">
      <!-- 请假信息 -->
      <van-cell-group inset class="leave-info">
        <van-cell title="请假类型" :value="leaveType" />
        <van-cell title="开始日期" :value="startDate" />
        <van-cell title="结束日期" :value="endDate" />
        <van-cell title="请假天数" :value="`${days}天`" />
        <van-cell title="请假原因" :value="reason" />
      </van-cell-group>
      
      <!-- 加载中 -->
      <div class="loading-wrapper" v-if="loading">
        <van-loading size="24px" vertical>加载中...</van-loading>
      </div>
      
      <!-- 推荐方案 -->
      <div class="recommendations" v-else-if="recommendations.length > 0">
        <div class="section-title">AI推荐方案</div>
        <div class="recommendation-list">
          <div 
            v-for="(plan, index) in recommendations" 
            :key="index"
            class="recommendation-card card-wrapper"
            :class="{ 'selected': selectedPlan === index }"
            @click="selectPlan(index)"
          >
            <div class="plan-header">
              <div class="plan-name">{{ plan.plan_name }}</div>
              <van-tag 
                :type="getRecommendationLevelType(plan.recommendation_level)"
              >
                {{ getRecommendationLevelText(plan.recommendation_level) }}
              </van-tag>
            </div>
            
            <div class="plan-content">
              <div class="plan-item">
                <span class="label">请假类型：</span>
                <span class="value">{{ plan.leave_type }}</span>
              </div>
              <div class="plan-item">
                <span class="label">请假天数：</span>
                <span class="value">{{ plan.days }}天</span>
              </div>
              <div class="plan-item">
                <span class="label">是否符合政策：</span>
                <span class="value" :class="plan.is_compliant ? 'text-success' : 'text-danger'">
                  {{ plan.is_compliant ? '是' : '否' }}
                </span>
              </div>
              <div class="plan-item">
                <span class="label">影响：</span>
                <span class="value">{{ plan.impact }}</span>
              </div>
            </div>
            
            <div class="plan-footer">
              <div class="pros-cons">
                <div class="pros" v-if="plan.pros && plan.pros.length > 0">
                  <div class="pros-title">优点：</div>
                  <ul class="pros-list">
                    <li v-for="(pro, proIndex) in plan.pros" :key="proIndex">{{ pro }}</li>
                  </ul>
                </div>
                <div class="cons" v-if="plan.cons && plan.cons.length > 0">
                  <div class="cons-title">缺点：</div>
                  <ul class="cons-list">
                    <li v-for="(con, conIndex) in plan.cons" :key="conIndex">{{ con }}</li>
                  </ul>
                </div>
              </div>
              
              <div class="select-indicator" v-if="selectedPlan === index">
                <van-icon name="success" color="#07c160" size="20" />
                已选择
              </div>
            </div>
          </div>
        </div>
        
        <!-- 提交按钮 -->
        <div class="submit-wrapper">
          <van-button 
            round 
            block 
            type="primary" 
            :disabled="selectedPlan === null"
            :loading="submitting"
            @click="submitLeaveRequest"
          >
            提交请假申请
          </van-button>
        </div>
      </div>
      
      <!-- 无推荐方案 -->
      <div class="empty-wrapper" v-else-if="!loading && recommendations.length === 0">
        <van-empty description="暂无推荐方案">
          <template #bottom>
            <van-button round type="primary" @click="$router.back()">返回修改</van-button>
          </template>
        </van-empty>
      </div>
      
      <!-- 错误信息 -->
      <div class="error-wrapper" v-if="error">
        <van-empty image="error" :description="error">
          <template #bottom>
            <van-button round type="primary" @click="$router.back()">返回修改</van-button>
          </template>
        </van-empty>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { showToast, showSuccessToast, showDialog } from 'vant'
import { useUserStore } from '../stores/user'
import { useLeaveStore } from '../stores/leave'

// 路由
const router = useRouter()
const route = useRoute()

// 状态管理
const userStore = useUserStore()
const leaveStore = useLeaveStore()

// 请假信息
const leaveTypeId = ref(parseInt(route.query.leaveTypeId) || null)
const leaveType = ref(route.query.leaveType || '')
const startDate = ref(route.query.startDate || '')
const endDate = ref(route.query.endDate || '')
const days = ref(route.query.days || '0')
const reason = ref(route.query.reason || '')

// 推荐方案
const recommendations = computed(() => {
  return leaveStore.leaveRecommendations?.recommendations || []
})

// 选中的方案
const selectedPlan = ref(null)

// 状态
const loading = ref(false)
const submitting = ref(false)
const error = ref(null)

// 选择方案
const selectPlan = (index) => {
  selectedPlan.value = index
}

// 获取推荐等级类型
const getRecommendationLevelType = (level) => {
  const typeMap = {
    '高': 'success',
    '中': 'warning',
    '低': 'danger'
  }
  return typeMap[level] || 'primary'
}

// 获取推荐等级文本
const getRecommendationLevelText = (level) => {
  const textMap = {
    '高': '推荐',
    '中': '一般',
    '低': '不推荐'
  }
  return textMap[level] || level
}

// 提交请假申请
const submitLeaveRequest = async () => {
  // 检查是否选择了方案
  if (selectedPlan.value === null) {
    showToast('请选择一个推荐方案')
    return
  }
  
  // 获取选中的方案
  const plan = recommendations.value[selectedPlan.value]
  
  // 确认提交
  showDialog({
    title: '确认提交',
    message: `您确定要提交这个请假申请吗？\n请假类型：${plan.leave_type}\n请假天数：${plan.days}天`,
    showCancelButton: true,
    confirmButtonText: '确认提交',
    cancelButtonText: '取消'
  }).then(async () => {
    submitting.value = true
    
    try {
      // 提交请假申请
      const result = await leaveStore.applyLeave({
        user_id: userStore.userId,
        leave_type_id: leaveTypeId.value,
        start_date: startDate.value,
        end_date: endDate.value,
        reason: reason.value,
        ai_recommendation: JSON.stringify(plan)
      })
      
      // 提交成功
      if (result.status === 'success') {
        showSuccessToast('请假申请提交成功')
        
        // 清除推荐
        leaveStore.clearLeaveRecommendations()
        
        // 跳转到请假记录页面
        router.replace('/leave-list')
      } else {
        showToast(result.message || '提交失败')
      }
    } catch (error) {
      console.error('Failed to submit leave request:', error)
      showToast(error.response?.data?.detail || '提交失败')
    } finally {
      submitting.value = false
    }
  }).catch(() => {
    // 取消提交
  })
}

// 获取请假推荐
const fetchLeaveRecommendations = async () => {
  // 检查是否有必要的参数
  if (!userStore.userId || !startDate.value || !endDate.value || !reason.value) {
    error.value = '缺少必要的请假信息'
    return
  }
  
  loading.value = true
  error.value = null
  
  try {
    // 获取请假推荐
    await leaveStore.getLeaveRecommendations(
      userStore.userId,
      startDate.value,
      endDate.value,
      reason.value
    )
    
    // 如果没有推荐
    if (!recommendations.value || recommendations.value.length === 0) {
      error.value = '没有找到合适的推荐方案'
    }
  } catch (err) {
    console.error('Failed to fetch leave recommendations:', err)
    error.value = err.response?.data?.detail || '获取推荐失败'
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
  
  // 如果已有推荐，不需要重新获取
  if (leaveStore.leaveRecommendations && leaveStore.leaveRecommendations.recommendations) {
    // 默认选择第一个推荐方案
    if (recommendations.value.length > 0) {
      selectedPlan.value = 0
    }
    return
  }
  
  // 获取请假推荐
  await fetchLeaveRecommendations()
  
  // 默认选择第一个推荐方案
  if (recommendations.value.length > 0) {
    selectedPlan.value = 0
  }
})
</script>

<style scoped>
.leave-info {
  margin-bottom: 16px;
}

.section-title {
  margin: 16px 0;
}

.recommendation-card {
  padding: 16px;
  margin-bottom: 16px;
  border: 2px solid transparent;
  transition: all 0.3s;
}

.recommendation-card.selected {
  border-color: #07c160;
}

.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.plan-name {
  font-size: 16px;
  font-weight: bold;
}

.plan-content {
  margin-bottom: 12px;
}

.plan-item {
  margin-bottom: 8px;
}

.plan-item .label {
  color: #646566;
}

.pros-cons {
  font-size: 14px;
}

.pros-title, .cons-title {
  font-weight: bold;
  margin-bottom: 4px;
}

.pros-title {
  color: #07c160;
}

.cons-title {
  color: #ee0a24;
}

.pros-list, .cons-list {
  padding-left: 20px;
  margin: 0 0 8px 0;
}

.select-indicator {
  display: flex;
  align-items: center;
  color: #07c160;
  font-weight: bold;
  margin-top: 8px;
}

.select-indicator .van-icon {
  margin-right: 4px;
}

.submit-wrapper {
  margin: 24px 16px;
}

.loading-wrapper, .empty-wrapper, .error-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  margin-top: 32px;
}
</style> 