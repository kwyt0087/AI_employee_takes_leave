import request from '../utils/request'

/**
 * 获取政策列表
 * @returns {Promise} 政策列表
 */
export function getPolicies() {
  return request({
    url: '/api/policies',
    method: 'get'
  })
}

/**
 * 获取政策详情
 * @param {number|string} policyId 政策ID
 * @returns {Promise} 政策详情
 */
export function getPolicyDetail(policyId) {
  return request({
    url: `/api/policies/${policyId}`,
    method: 'get'
  })
}

/**
 * 上传政策文件
 * @param {FormData} formData 表单数据
 * @returns {Promise} 上传结果
 */
export function uploadPolicy(formData) {
  return request({
    url: '/api/policies/upload',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 删除政策
 * @param {number|string} policyId 政策ID
 * @returns {Promise} 删除结果
 */
export function deletePolicy(policyId) {
  return request({
    url: `/api/policies/${policyId}`,
    method: 'delete'
  })
}

/**
 * 更新政策
 * @param {number|string} policyId 政策ID
 * @param {Object} data 政策数据
 * @returns {Promise} 更新结果
 */
export function updatePolicy(policyId, data) {
  return request({
    url: `/api/policies/${policyId}`,
    method: 'put',
    data
  })
}

export default {
  getPolicies,
  getPolicyDetail,
  uploadPolicy,
  deletePolicy,
  updatePolicy
}

export default {
  getPolicies,
  getPolicyDetail,
  uploadPolicy,
  deletePolicy,
  updatePolicy
}
 