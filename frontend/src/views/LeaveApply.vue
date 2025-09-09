<template>
  <div class="leave-apply-page">
    <!-- 顶部导航栏 -->
    <van-nav-bar
      title="请假申请"
      left-arrow
      @click-left="$router.back()"
      fixed
      placeholder
    />
    
    <!-- 页面内容 -->
    <div class="page-container">
      <!-- 请假表单 -->
      <van-form @submit="onSubmit" class="leave-form">
        <!-- 请假类型 -->
        <van-cell-group inset title="请假信息">
          <van-field
            v-model="leaveType"
            is-link
            readonly
            name="leaveType"
            label="请假类型"
            placeholder="请选择请假类型"
            :rules="[{ required: true, message: '请选择请假类型' }]"
            @click="showLeaveTypePicker = true"
          />
          
          <!-- 开始日期 -->
          <van-field
            v-model="startDate"
            is-link
            readonly
            name="startDate"
            label="开始日期"
            placeholder="请选择开始日期"
            :rules="[{ required: true, message: '请选择开始日期' }]"
            @click="showStartDatePicker = true"
          />
          
          <!-- 结束日期 -->
          <van-field
            v-model="endDate"
            is-link
            readonly
            name="endDate"
            label="结束日期"
            placeholder="请选择结束日期"
            :rules="[{ required: true, message: '请选择结束日期' }]"
            @click="showEndDatePicker = true"
          />
          
          <!-- 请假天数 -->
          <van-field
            v-model="leaveDays"
            name="leaveDays"
            label="请假天数"
            readonly
          />
          
          <!-- 请假原因 -->
          <van-field
            v-model="reason"
            rows="3"
            autosize
            type="textarea"
            name="reason"
            label="请假原因"
            placeholder="请输入请假原因"
            :rules="[{ required: true, message: '请输入请假原因' }]"
          />
        </van-cell-group>
        
        <!-- 提交按钮 -->
        <div style="margin: 16px;">
          <van-button 
            round 
            block 
            type="primary" 
            native-type="submit"
            :loading="loading"
          >
            获取AI推荐
          </van-button>
        </div>
      </van-form>
      
      <!-- 请假类型选择器 -->
      <van-popup v-model:show="showLeaveTypePicker" position="bottom">
        <van-picker
          :columns="leaveTypeOptions"
          @confirm="onLeaveTypeConfirm"
          @cancel="showLeaveTypePicker = false"
          :default-index="selectedLeaveTypeIndex"
        />
      </van-popup>
      
      <!-- 开始日期选择器 -->
      <van-popup v-model:show="showStartDatePicker" position="bottom">
        <van-date-picker
          :min-date="minDate"
          :max-date="maxDate"
          :formatter="dateFormatter"
          @confirm="onStartDateConfirm"
          @cancel="showStartDatePicker = false"
        />
      </van-popup>
      
      <!-- 结束日期选择器 -->
      <van-popup v-model:show="showEndDatePicker" position="bottom">
        <van-date-picker
          :min-date="startDateObj || minDate"
          :max-date="maxDate"
          :formatter="dateFormatter"
          @confirm="onEndDateConfirm"
          @cancel="showEndDatePicker = false"
        />
      </van-popup>
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showDialog } from 'vant'
import dayjs from 'dayjs'
import { useUserStore } from '../stores/user'
import { useLeaveStore } from '../stores/leave'

// 路由
const router = useRouter()

// 状态管理
const userStore = useUserStore()
const leaveStore = useLeaveStore()

// 激活的标签页
const activeTab = ref(2)

// 表单数据
const leaveType = ref('')
const leaveTypeId = ref(null)
const startDate = ref('')
const endDate = ref('')
const leaveDays = ref('0')
const reason = ref('')

// 日期对象
const startDateObj = ref(null)
const endDateObj = ref(null)

// 控制弹出层显示
const showLeaveTypePicker = ref(false)
const showStartDatePicker = ref(false)
const showEndDatePicker = ref(false)

// 加载状态
const loading = ref(false)

// 日期范围
const minDate = new Date()
const maxDate = new Date(new Date().setFullYear(new Date().getFullYear() + 1))

// 计算请假类型选项
const leaveTypeOptions = computed(() => {
  return leaveStore.leaveTypes.map(type => ({
    text: type.name,
    value: type.id
  }))
})

// 计算选中的请假类型索引
const selectedLeaveTypeIndex = computed(() => {
  if (!leaveTypeId.value) return 0
  const index = leaveTypeOptions.value.findIndex(option => option.value === leaveTypeId.value)
  return index >= 0 ? index : 0
})

// 日期格式化
const dateFormatter = (type, val) => {
  if (type === 'year') {
    return `${val}年`
  }
  if (type === 'month') {
    return `${val}月`
  }
  if (type === 'day') {
    return `${val}日`
  }
  return val
}

// 计算请假天数
const calculateLeaveDays = () => {
  if (startDateObj.value && endDateObj.value) {
    // 计算日期差
    const start = dayjs(startDateObj.value)
    const end = dayjs(endDateObj.value)
    const days = end.diff(start, 'day') + 1
    
    // 计算工作日
    let workDays = 0
    for (let i = 0; i < days; i++) {
      const day = start.add(i, 'day')
      // 如果不是周末（5是周六，6是周日）
      if (day.day() !== 0 && day.day() !== 6) {
        workDays++
      }
    }
    
    leaveDays.value = workDays.toString()
  } else {
    leaveDays.value = '0'
  }
}

// 请假类型确认
const onLeaveTypeConfirm = (value) => {
  leaveType.value = value.text
  leaveTypeId.value = value.value
  showLeaveTypePicker.value = false
}

// 开始日期确认
const onStartDateConfirm = (value) => {
  startDateObj.value = value
  startDate.value = dayjs(value).format('YYYY-MM-DD')
  showStartDatePicker.value = false
  
  // 如果结束日期早于开始日期，重置结束日期
  if (endDateObj.value && dayjs(endDateObj.value).isBefore(dayjs(value))) {
    endDateObj.value = value
    endDate.value = startDate.value
  }
  
  calculateLeaveDays()
}

// 结束日期确认
const onEndDateConfirm = (value) => {
  endDateObj.value = value
  endDate.value = dayjs(value).format('YYYY-MM-DD')
  showEndDatePicker.value = false
  
  calculateLeaveDays()
}

// 监听日期变化
watch([startDateObj, endDateObj], () => {
  calculateLeaveDays()
})

// 表单提交
const onSubmit = async () => {
  // 检查是否登录
  if (!userStore.isLoggedIn) {
    showToast('请先登录')
    router.push('/login')
    return
  }
  
  // 检查表单数据
  if (!leaveTypeId.value || !startDate.value || !endDate.value || !reason.value) {
    showToast('请填写完整的请假信息')
    return
  }
  
  loading.value = true
  
  try {
    // 获取请假推荐
    const result = await leaveStore.getLeaveRecommendations(
      userStore.userId,
      startDate.value,
      endDate.value,
      reason.value
    )
    
    // 跳转到推荐页面
    router.push({
      path: '/leave-recommend',
      query: {
        leaveTypeId: leaveTypeId.value,
        leaveType: leaveType.value,
        startDate: startDate.value,
        endDate: endDate.value,
        days: leaveDays.value,
        reason: reason.value
      }
    })
  } catch (error) {
    console.error('Failed to get leave recommendations:', error)
    showDialog({
      title: '获取推荐失败',
      message: error.response?.data?.detail || '请稍后再试',
      confirmButtonText: '确定'
    })
  } finally {
    loading.value = false
  }
}

// 组件挂载时执行
onMounted(async () => {
  // 初始化用户信息
  userStore.initUserInfo()
  
  // 获取请假类型
  try {
    await leaveStore.fetchLeaveTypes()
    
    // 默认选择第一个请假类型
    if (leaveStore.leaveTypes.length > 0) {
      const firstType = leaveStore.leaveTypes[0]
      leaveType.value = firstType.name
      leaveTypeId.value = firstType.id
    }
  } catch (error) {
    console.error('Failed to fetch leave types:', error)
    showToast('获取请假类型失败')
  }
})
</script>

<style scoped>
.leave-form {
  margin-top: 16px;
}
</style> 