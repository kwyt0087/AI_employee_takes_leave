import request from '../utils/request'

/**
 * 获取请假类型列表
 * @returns {Promise} 请假类型列表
 */
export function getLeaveTypes() {
  return request({
    url: '/api/leaves/types',
    method: 'get'
  })
}

/**
 * 获取请假推荐
 * @param {Object} data 请假参数
 * @returns {Promise} 请假推荐
 */
export function getLeaveRecommendations(data) {
  return request({
    url: '/api/leaves/recommendations',
    method: 'post',
    data
  })
}

/**
 * 提交请假申请
 * @param {Object} data 请假申请数据
 * @returns {Promise} 提交结果
 */
export function applyLeave(data) {
  return request({
    url: '/api/leaves/apply',
    method: 'post',
    data
  })
}

/**
 * 获取请假记录列表
 * @param {number|string} userId 用户ID
 * @returns {Promise} 请假记录列表
 */
export function getLeaveRequests(userId) {
  return request({
    url: `/api/leaves/user/${userId}`,
    method: 'get'
  })
}

/**
 * 获取请假详情
 * @param {number|string} leaveId 请假ID
 * @returns {Promise} 请假详情
 */
export function getLeaveDetail(leaveId) {
  return request({
    url: `/api/leaves/${leaveId}`,
    method: 'get'
  })
}

/**
 * 取消请假申请
 * @param {number|string} leaveId 请假ID
 * @returns {Promise} 取消结果
 */
export function cancelLeave(leaveId) {
  return request({
    url: `/api/leaves/${leaveId}/cancel`,
    method: 'post'
  })
}

/**
 * 审批请假申请
 * @param {number|string} leaveId 请假ID
 * @param {Object} data 审批数据
 * @returns {Promise} 审批结果
 */
export function approveLeave(leaveId, data) {
  return request({
    url: `/api/leaves/${leaveId}/approve`,
    method: 'post',
    data
  })
}

export default {
  getLeaveTypes,
  getLeaveRecommendations,
  applyLeave,
  getLeaveRequests,
  getLeaveDetail,
  cancelLeave,
  approveLeave
} 