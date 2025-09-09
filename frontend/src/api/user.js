import request from '../utils/request'

/**
 * 用户登录
 * @param {Object} data 登录参数
 * @returns {Promise} 登录结果
 */
export function login(data) {
  return request({
    url: '/api/auth/login',
    method: 'post',
    data
  })
}

/**
 * 获取用户信息
 * @param {number|string} userId 用户ID
 * @returns {Promise} 用户信息
 */
export function getUserInfo(userId) {
  return request({
    url: `/api/users/${userId}`,
    method: 'get'
  })
}

/**
 * 更新用户信息
 * @param {number|string} userId 用户ID
 * @param {Object} data 用户信息
 * @returns {Promise} 更新结果
 */
export function updateUserInfo(userId, data) {
  return request({
    url: `/api/users/${userId}`,
    method: 'put',
    data
  })
}

/**
 * 修改密码
 * @param {number|string} userId 用户ID
 * @param {Object} data 密码信息
 * @returns {Promise} 修改结果
 */
export function changePassword(userId, data) {
  return request({
    url: `/api/users/${userId}/change-password`,
    method: 'post',
    data
  })
}

/**
 * 获取用户请假统计
 * @param {number|string} userId 用户ID
 * @returns {Promise} 请假统计
 */
export function getLeaveStats(userId) {
  return request({
    url: `/api/users/${userId}/leave-stats`,
    method: 'get'
  })
}

/**
 * 获取用户年假信息
 * @param {number|string} userId 用户ID
 * @returns {Promise} 年假信息
 */
export function getAnnualLeaveInfo(userId) {
  return request({
    url: `/api/users/${userId}/annual-leave`,
    method: 'get'
  })
}

export default {
  login,
  getUserInfo,
  updateUserInfo,
  changePassword,
  getLeaveStats,
  getAnnualLeaveInfo
}
