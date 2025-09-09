import { defineStore } from 'pinia'
import { leaveApi } from '../api'

// 定义请假状态
export const useLeaveStore = defineStore('leave', {
  // 状态
  state: () => ({
    // 请假类型列表
    leaveTypes: [],
    // 请假记录列表
    leaveRequests: [],
    // 请假推荐
    leaveRecommendations: null,
    // 当前请假申请
    currentLeaveRequest: null,
    // 加载状态
    loading: false,
    // 错误信息
    error: null
  }),
  
  // getters
  getters: {
    // 获取请假类型选项（用于选择器）
    leaveTypeOptions: (state) => {
      return state.leaveTypes.map(type => ({
        text: type.name,
        value: type.id
      }))
    },
    
    // 获取请假类型名称
    getLeaveTypeName: (state) => (typeId) => {
      const type = state.leaveTypes.find(t => t.id === typeId)
      return type ? type.name : '未知类型'
    },
    
    // 获取请假状态文本
    getStatusText: () => (status) => {
      const statusMap = {
        pending: '待审批',
        approved: '已批准',
        rejected: '已拒绝'
      }
      return statusMap[status] || status
    },
    
    // 获取请假状态颜色
    getStatusColor: () => (status) => {
      const colorMap = {
        pending: '#ff976a',
        approved: '#07c160',
        rejected: '#ee0a24'
      }
      return colorMap[status] || '#969799'
    }
  },
  
  // actions
  actions: {
    // 获取请假类型列表
    async fetchLeaveTypes() {
      this.loading = true
      this.error = null
      
      try {
        const types = await leaveApi.getLeaveTypes()
        this.leaveTypes = types
        return types
      } catch (error) {
        this.error = error.response?.data?.detail || '获取请假类型失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 获取请假推荐
    async getLeaveRecommendations(userId, startDate, endDate, reason) {
      this.loading = true
      this.error = null
      this.leaveRecommendations = null
      
      try {
        const data = {
          user_id: userId,
          start_date: startDate,
          end_date: endDate,
          reason
        }
        
        const recommendations = await leaveApi.getLeaveRecommendations(data)
        this.leaveRecommendations = recommendations
        return recommendations
      } catch (error) {
        this.error = error.response?.data?.detail || '获取请假推荐失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 提交请假申请
    async applyLeave(leaveData) {
      this.loading = true
      this.error = null
      
      try {
        const result = await leaveApi.applyLeave(leaveData)
        // 更新请假记录列表
        if (result.status === 'success') {
          this.fetchLeaveRequests(leaveData.user_id)
        }
        return result
      } catch (error) {
        this.error = error.response?.data?.detail || '提交请假申请失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 获取请假记录列表
    async fetchLeaveRequests(userId) {
      this.loading = true
      this.error = null
      
      try {
        const requests = await leaveApi.getLeaveRequests(userId)
        this.leaveRequests = requests
        return requests
      } catch (error) {
        this.error = error.response?.data?.detail || '获取请假记录失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 获取请假详情
    async fetchLeaveDetail(leaveId) {
      this.loading = true
      this.error = null
      
      try {
        const detail = await leaveApi.getLeaveDetail(leaveId)
        this.currentLeaveRequest = detail
        return detail
      } catch (error) {
        this.error = error.response?.data?.detail || '获取请假详情失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 清除请假推荐
    clearLeaveRecommendations() {
      this.leaveRecommendations = null
    },
    
    // 清除当前请假申请
    clearCurrentLeaveRequest() {
      this.currentLeaveRequest = null
    }
  }
}) 