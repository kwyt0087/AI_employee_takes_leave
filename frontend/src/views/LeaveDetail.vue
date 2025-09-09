<template>
  <div class="leave-detail-page">
    <!-- 顶部导航栏 -->
    <van-nav-bar
      title="请假详情"
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
      
      <!-- 请假详情 -->
      <div class="leave-detail" v-else-if="leaveDetail">
        <!-- 状态卡片 -->
        <div class="status-card card-wrapper">
          <div class="status-icon" :class="getStatusClass(leaveDetail.status)">
            <van-icon :name="getStatusIcon(leaveDetail.status)" size="28" />
          </div>
          <div class="status-info">
            <div class="status-text">{{ getStatusText(leaveDetail.status) }}</div>
            <div class="status-desc">{{ getStatusDescription(leaveDetail.status) }}</div>
          </div>
        </div>
        
        <!-- 请假信息 -->
        <van-cell-group inset title="请假信息" class="leave-info">
          <van-cell title="请假类型" :value="leaveDetail.leave_type" />
          <van-cell title="开始日期" :value="leaveDetail.start_date" />
          <van-cell title="结束日期" :value="leaveDetail.end_date" />
          <van-cell title="请假天数" :value="`${leaveDetail.days}天`" />
          <van-cell title="请假原因" :value="leaveDetail.reason" />
          <van-cell title="申请时间" :value="formatDateTime(leaveDetail.created_at)" />
        </van-cell-group>
        
        <!-- 审批信息 -->
        <van-cell-group inset title="审批信息" class="approval-info" v-if="leaveDetail.status !== 'pending'">
          <van-cell title="审批人" :value="leaveDetail.approver || '系统自动'" />
          <van-cell title="审批时间" :value="formatDateTime(leaveDetail.approved_at)" />
          <van-cell title="审批意见" :value="leaveDetail.approval_comment || '无'" />
        </van-cell-group>
        
        <!-- AI推荐信息 -->
        <div class="ai-recommendation card-wrapper" v-if="aiRecommendation">
          <div class="section-title">AI推荐方案</div>
          <div class="recommendation-card">
            <div class="plan-header">
              <div class="plan-name">{{ aiRecommendation.plan_name }}</div>
              <van-tag 
                :type="getRecommendationLevelType(aiRecommendation.recommendation_level)"
              >
                {{ getRecommendationLevelText(aiRecommendation.recommendation_level) }}
              </van-tag>
            </div>
            
            <div class="plan-content">
              <div class="plan-item">
                <span class="label">请假类型：</span>
                <span class="value">{{ aiRecommendation.leave_type }}</span>
              </div>
              <div class="plan-item">
                <span class="label">请假天数：</span>
                <span class="value">{{ aiRecommendation.days }}天</span>
              </div>
              <div class="plan-item">
                <span class="label">是否符合政策：</span>
                <span class="value" :class="aiRecommendation.is_compliant ? 'text-success' : 'text-danger'">
                  {{ aiRecommendation.is_compliant ? '是' : '否' }}
                </span>
              </div>
              <div class="plan-item">
                <span class="label">影响：</span>
                <span class="value">{{ aiRecommendation.impact }}</span>
              </div>
            </div>
            
            <div class="plan-footer">
              <div class="pros-cons">
                <div class="pros" v-if="aiRecommendation.pros && aiRecommendation.pros.length > 0">
                  <div class="pros-title">优点：</div>
                  <ul class="pros-list">
                    <li v-for="(pro, proIndex) in aiRecommendation.pros" :key="proIndex">{{ pro }}</li>
                  </ul>
                </div>
                <div class="cons" v-if="aiRecommendation.cons && aiRecommendation.cons.length > 0">
                  <div class="cons-title">缺点：</div>
                  <ul class="cons-list">
                    <li v-for="(con, conIndex) in aiRecommendation.cons" :key="conIndex">{{ con }}</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 操作按钮 -->
        <div class="action-buttons" v-if="leaveDetail.status === 'pending'">
          <van-button 
            round 
            block 
            type="danger" 
            @click="confirmCancel"
            :loading="cancelling"
          >
            取消申请
          </van-button>
        </div>
      </div>
      
      <!-- 错误信息 -->
      <div class="error-wrapper" v-else-if="error">
        <van-empty image="error" :description="error">
          <template #bottom>
            <van-button round type="primary" @click="$router.back()">返回列表</van-button>
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
import dayjs from 'dayjs'
import { useUserStore } from '../stores/user'
import { useLeaveStore } from '../stores/leave'

// 路由
const router = useRouter()
const route = useRoute()

// 状态管理
const userStore = useUserStore()
const leaveStore = useLeaveStore()

// 请假ID
const leaveId = computed(() => parseInt(route.params.id))

// 请假详情
const leaveDetail = ref(null)

// AI推荐信息
const aiRecommendation = ref(null)

// 状态
const loading = ref(false)
const cancelling = ref(false)
const error = ref(null)

// 格式化日期时间
const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return ''
  return dayjs(dateTimeStr).format('YYYY-MM-DD HH:mm')
}

// 获取状态文本
const getStatusText = (status) => {
  return leaveStore.getStatusText(status)
}

// 获取状态图标
const getStatusIcon = (status) => {
  const iconMap = {
    'pending': 'clock-o',
    'approved': 'checked',
    'rejected': 'close',
    'cancelled': 'cross'
  }
  return iconMap[status] || 'question-o'
}

// 获取状态类名
const getStatusClass = (status) => {
  const classMap = {
    'pending': 'status-pending',
    'approved': 'status-approved',
    'rejected': 'status-rejected',
    'cancelled': 'status-cancelled'
  }
  return classMap[status] || ''
}

// 获取状态描述
const getStatusDescription = (status) => {
  const descMap = {
    'pending': '您的请假申请正在等待审批',
    'approved': '您的请假申请已被批准',
    'rejected': '您的请假申请已被拒绝',
    'cancelled': '您已取消此请假申请'
  }
  return descMap[status] || '未知状态'
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

// 确认取消请假
const confirmCancel = () => {
  showDialog({
    title: '取消请假',
    message: '确定要取消此请假申请吗？',
    showCancelButton: true
  }).then(() => {
    cancelLeave()
  }).catch(() => {
    // 取消操作
  })
}

// 取消请假
const cancelLeave = async () => {
  if (!leaveId.value) return
  
  cancelling.value = true
  
  try {
    // 在实际项目中，这里应该调用API取消请假
    // await leaveStore.cancelLeave(leaveId.value)
    
    // 模拟取消
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // 更新状态
    if (leaveDetail.value) {
      leaveDetail.value.status = 'cancelled'
    }
    
    showSuccessToast('请假申请已取消')
  } catch (error) {
    console.error('Failed to cancel leave:', error)
    showToast('取消请假失败')
  } finally {
    cancelling.value = false
  }
}

// 获取请假详情
const fetchLeaveDetail = async () => {
  if (!leaveId.value) {
    error.value = '请假ID无效'
    return
  }
  
  loading.value = true
  error.value = null
  
  try {
    // 在实际项目中，这里应该调用API获取请假详情
    // const response = await leaveStore.getLeaveDetail(leaveId.value)
    // leaveDetail.value = response
    
    // 模拟数据
    await new Promise(resolve => setTimeout(resolve, 500))
    
    leaveDetail.value = {
      id: leaveId.value,
      user_id: userStore.userId,
      leave_type: '年假',
      start_date: '2023-05-01',
      end_date: '2023-05-03',
      days: 3,
      reason: '家庭旅行',
      status: 'approved',
      created_at: '2023-04-20 10:00:00',
      approver: '张经理',
      approved_at: '2023-04-21 14:30:00',
      approval_comment: '批准',
      ai_recommendation: JSON.stringify({
        plan_name: '年假方案',
        leave_type: '年假',
        days: 3,
        recommendation_level: '高',
        is_compliant: true,
        impact: '低影响',
        pros: [
          '符合公司年假政策',
          '提前申请，便于安排工作'
        ],
        cons: [
          '五一假期前请假，可能影响工作交接'
        ]
      })
    }
    
    // 解析AI推荐
    if (leaveDetail.value.ai_recommendation) {
      try {
        aiRecommendation.value = JSON.parse(leaveDetail.value.ai_recommendation)
      } catch (e) {
        console.error('Failed to parse AI recommendation:', e)
      }
    }
  } catch (err) {
    console.error('Failed to fetch leave detail:', err)
    error.value = '获取请假详情失败'
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
  
  // 获取请假详情
  await fetchLeaveDetail()
})
</script>

<style scoped>
.status-card {
  display: flex;
  align-items: center;
  padding: 20px;
  margin-bottom: 16px;
}

.status-icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.status-pending {
  background-color: #1989fa;
  color: white;
}

.status-approved {
  background-color: #07c160;
  color: white;
}

.status-rejected {
  background-color: #ee0a24;
  color: white;
}

.status-cancelled {
  background-color: #969799;
  color: white;
}

.status-info .status-text {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 4px;
}

.status-info .status-desc {
  font-size: 14px;
  color: #646566;
}

.leave-info, .approval-info {
  margin-bottom: 16px;
}

.ai-recommendation {
  padding: 16px;
  margin-bottom: 16px;
}

.recommendation-card {
  margin-top: 12px;
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

.action-buttons {
  margin: 24px 16px;
}

.loading-wrapper, .error-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}
</style>