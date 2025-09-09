import axios from 'axios'
import { showToast } from 'vant'
import { API_BASE_URL, REQUEST_TIMEOUT, STORAGE_KEYS } from '../config'

// 创建axios实例
const service = axios.create({
  baseURL: API_BASE_URL,
  timeout: REQUEST_TIMEOUT
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 从localStorage中获取token
    const token = localStorage.getItem(STORAGE_KEYS.TOKEN)
    
    // 如果有token，则添加到请求头中
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    
    // 如果响应成功，直接返回数据
    return res
  },
  error => {
    console.error('Response error:', error)
    
    // 处理错误响应
    const { response } = error
    
    if (response) {
      // 根据状态码处理不同的错误
      switch (response.status) {
        case 400:
          showToast(response.data.detail || '请求参数错误')
          break
        case 401:
          showToast('登录已过期，请重新登录')
          // 清除token和用户信息
          localStorage.removeItem(STORAGE_KEYS.TOKEN)
          localStorage.removeItem(STORAGE_KEYS.USER_INFO)
          // 跳转到登录页面
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
          showToast(response.data.detail || '请求失败')
      }
    } else {
      // 网络错误或请求被取消
      showToast('网络错误，请检查网络连接')
    }
    
    return Promise.reject(error)
  }
)

// 导出请求方法
export default service 