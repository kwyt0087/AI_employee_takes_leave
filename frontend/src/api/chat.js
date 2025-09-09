import request from '../utils/request'

/**
 * 发送聊天消息
 * @param {Object} data 聊天消息数据
 * @returns {Promise} 聊天响应
 */
export function sendMessage(data) {
  return request({
    url: '/api/chat/send',
    method: 'post',
    data
  })
}

/**
 * 获取聊天历史
 * @param {number|string} userId 用户ID
 * @returns {Promise} 聊天历史
 */
export function getChatHistory(userId) {
  return request({
    url: `/api/chat/history/${userId}`,
    method: 'get'
  })
}

/**
 * 清空聊天历史
 * @param {number|string} userId 用户ID
 * @returns {Promise} 清空结果
 */
export function clearChatHistory(userId) {
  return request({
    url: `/api/chat/history/${userId}/clear`,
    method: 'post'
  })
}

export default {
  sendMessage,
  getChatHistory,
  clearChatHistory
} 