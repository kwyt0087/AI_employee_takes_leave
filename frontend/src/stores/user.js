import { defineStore } from 'pinia'
import { userApi } from '../api'

// 定义用户状态
export const useUserStore = defineStore('user', {
  // 状态
  state: () => ({
    // 用户信息
    userInfo: null,
    // 登录状态
    isLoggedIn: false,
    // 加载状态
    loading: false,
    // 错误信息
    error: null
  }),
  
  // getters
  getters: {
    // 获取用户ID
    userId: (state) => state.userInfo?.id,
    // 获取用户名
    username: (state) => state.userInfo?.username,
    // 获取用户全名
    fullName: (state) => state.userInfo?.full_name,
    // 是否是管理员
    isAdmin: (state) => state.userInfo?.is_admin || false
  },
  
  // actions
  actions: {
    // 设置用户信息
    setUserInfo(userInfo) {
      this.userInfo = userInfo
      this.isLoggedIn = true
      // 保存到localStorage
      localStorage.setItem('user', JSON.stringify(userInfo))
    },
    
    // 清除用户信息
    clearUserInfo() {
      this.userInfo = null
      this.isLoggedIn = false
      // 清除localStorage
      localStorage.removeItem('user')
      localStorage.removeItem('token')
    },
    
    // 初始化用户信息（从localStorage）
    initUserInfo() {
      const userStr = localStorage.getItem('user')
      if (userStr) {
        try {
          this.userInfo = JSON.parse(userStr)
          this.isLoggedIn = true
        } catch (error) {
          console.error('Failed to parse user info:', error)
          this.clearUserInfo()
        }
      }
    },
    
    // 登录
    async login(username, password) {
      this.loading = true
      this.error = null
      
      try {
        const response = await userApi.login({ username, password })
        debugger
        // 保存token
        localStorage.setItem('token', response.access_token)
        
        // 获取用户信息
        await this.fetchUserInfo(response.user_id)
        
        return response
      } catch (error) {
        this.error = error.response?.data?.detail || '登录失败'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 登出
    logout() {
      this.clearUserInfo()
      // 可以添加其他登出逻辑，如调用登出API
    },
    
    // 获取用户信息
    async fetchUserInfo(userId) {
      this.loading = true
      this.error = null
      
      try {
        // 如果没有传入userId，则使用store中的userId
        const id = userId || this.userId
        if (!id) {
          throw new Error('用户ID不存在')
        }
        
        // 获取基础用户信息
        const userInfo = await userApi.getUserInfo(id)
        
        // 获取年假信息
        const annualLeaveInfo = await userApi.getAnnualLeaveInfo(id)
        
        // 合并数据
        const fullUserInfo = {
          ...userInfo,
          annual_leave: annualLeaveInfo
        }
        
        this.setUserInfo(fullUserInfo)
        return fullUserInfo
      } catch (error) {
        this.error = error.response?.data?.detail || '获取用户信息失败'
        throw error
      } finally {
        this.loading = false
      }
    }
  }
}) 