/**
 * 全局配置文件
 */

// API基础URL
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// 请求超时时间（毫秒）
export const REQUEST_TIMEOUT = 30000

// 本地存储键名
export const STORAGE_KEYS = {
  TOKEN: 'token',
  USER_INFO: 'userInfo',
  CHAT_MESSAGES: 'chatMessages'
}

// 请假状态
export const LEAVE_STATUS = {
  PENDING: 'pending',
  APPROVED: 'approved',
  REJECTED: 'rejected',
  CANCELLED: 'cancelled'
}

// 请假状态文本
export const LEAVE_STATUS_TEXT = {
  [LEAVE_STATUS.PENDING]: '待审批',
  [LEAVE_STATUS.APPROVED]: '已批准',
  [LEAVE_STATUS.REJECTED]: '已拒绝',
  [LEAVE_STATUS.CANCELLED]: '已取消'
}

// 请假状态颜色
export const LEAVE_STATUS_COLOR = {
  [LEAVE_STATUS.PENDING]: '#1989fa',
  [LEAVE_STATUS.APPROVED]: '#07c160',
  [LEAVE_STATUS.REJECTED]: '#ee0a24',
  [LEAVE_STATUS.CANCELLED]: '#969799'
}

// 政策分类
export const POLICY_CATEGORIES = [
  { text: '请假制度', value: 'leave' },
  { text: '考勤制度', value: 'attendance' },
  { text: '加班调休', value: 'overtime' },
  { text: '薪资福利', value: 'salary' },
  { text: '其他', value: 'other' }
]

// 默认配置
export default {
  API_BASE_URL,
  REQUEST_TIMEOUT,
  STORAGE_KEYS,
  LEAVE_STATUS,
  LEAVE_STATUS_TEXT,
  LEAVE_STATUS_COLOR,
  POLICY_CATEGORIES
} 