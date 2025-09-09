import axios from 'axios'
import { showToast } from 'vant'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    // 处理错误响应
    const { response } = error
    if (response) {
      // 根据状态码处理错误
      switch (response.status) {
        case 401:
          showToast('登录已过期，请重新登录')
          // 清除token并跳转到登录页
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          setTimeout(() => {
            window.location.href = '/login'
          }, 1500)
          break
        case 403:
          showToast('没有权限访问')
          break
        case 404:
          showToast('请求的资源不存在')
          break
        case 500:
          showToast('服务器错误，请稍后再试')
          break
        default:
          showToast(response.data?.detail || '请求失败')
      }
    } else {
      // 网络错误
      showToast('网络错误，请检查网络连接')
    }
    return Promise.reject(error)
  }
)

// 用户相关API
export const userApi = {
  // 登录
  login(data) {
    return api.post('/login', data)
  },
  
  // 获取用户信息
  getUserInfo(userId) {
    return api.get(`/users/${userId}`)
  }
}

// 请假相关API
export const leaveApi = {
  // 获取请假类型
  getLeaveTypes() {
    return api.get('/leave-types')
  },
  
  // 获取请假推荐
  getLeaveRecommendations(data) {
    return api.post('/leave/recommend', data)
  },
  
  // 提交请假申请
  applyLeave(data) {
    return api.post('/leave/apply', data)
  },
  
  // 获取请假记录
  getLeaveRequests(userId) {
    return api.get(`/leave/requests/${userId}`)
  },
  
  // 获取请假详情
  getLeaveDetail(leaveId) {
    return api.get(`/leave/requests/${leaveId}`)
  }
}

// 政策相关API
export const policyApi = {
  // 获取政策列表
  getPolicies() {
    return api.get('/policies')
  },
  
  // 上传政策文件
  uploadPolicy(formData) {
    return api.post('/policies/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}

// 聊天相关API
export const chatApi = {
  // 发送消息
  sendMessage(data) {
    return api.post('/chat', data)
  }
}

export default api 