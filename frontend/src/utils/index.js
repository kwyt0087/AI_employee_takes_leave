import dayjs from 'dayjs'

/**
 * 格式化日期时间
 * @param {string|Date} date 日期时间
 * @param {string} format 格式化字符串
 * @returns {string} 格式化后的日期时间字符串
 */
export function formatDateTime(date, format = 'YYYY-MM-DD HH:mm:ss') {
  if (!date) return ''
  return dayjs(date).format(format)
}

/**
 * 格式化日期
 * @param {string|Date} date 日期
 * @param {string} format 格式化字符串
 * @returns {string} 格式化后的日期字符串
 */
export function formatDate(date, format = 'YYYY-MM-DD') {
  if (!date) return ''
  return dayjs(date).format(format)
}

/**
 * 计算两个日期之间的天数
 * @param {string|Date} startDate 开始日期
 * @param {string|Date} endDate 结束日期
 * @returns {number} 天数
 */
export function calculateDays(startDate, endDate) {
  if (!startDate || !endDate) return 0
  const start = dayjs(startDate)
  const end = dayjs(endDate)
  return end.diff(start, 'day') + 1
}

/**
 * 计算两个日期之间的工作日天数（不包括周末）
 * @param {string|Date} startDate 开始日期
 * @param {string|Date} endDate 结束日期
 * @returns {number} 工作日天数
 */
export function calculateWorkDays(startDate, endDate) {
  if (!startDate || !endDate) return 0
  
  const start = dayjs(startDate)
  const end = dayjs(endDate)
  const days = end.diff(start, 'day') + 1
  
  let workDays = 0
  for (let i = 0; i < days; i++) {
    const day = start.add(i, 'day')
    // 如果不是周末（0是周日，6是周六）
    if (day.day() !== 0 && day.day() !== 6) {
      workDays++
    }
  }
  
  return workDays
}

/**
 * 深拷贝对象
 * @param {Object} obj 要拷贝的对象
 * @returns {Object} 拷贝后的对象
 */
export function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') {
    return obj
  }
  
  if (obj instanceof Date) {
    return new Date(obj.getTime())
  }
  
  if (obj instanceof Array) {
    return obj.map(item => deepClone(item))
  }
  
  const cloneObj = {}
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      cloneObj[key] = deepClone(obj[key])
    }
  }
  
  return cloneObj
}

/**
 * 防抖函数
 * @param {Function} fn 要执行的函数
 * @param {number} delay 延迟时间（毫秒）
 * @returns {Function} 防抖后的函数
 */
export function debounce(fn, delay = 300) {
  let timer = null
  
  return function(...args) {
    if (timer) {
      clearTimeout(timer)
    }
    
    timer = setTimeout(() => {
      fn.apply(this, args)
      timer = null
    }, delay)
  }
}

/**
 * 节流函数
 * @param {Function} fn 要执行的函数
 * @param {number} delay 延迟时间（毫秒）
 * @returns {Function} 节流后的函数
 */
export function throttle(fn, delay = 300) {
  let timer = null
  let lastTime = 0
  
  return function(...args) {
    const now = Date.now()
    
    if (now - lastTime >= delay) {
      fn.apply(this, args)
      lastTime = now
    } else {
      if (timer) {
        clearTimeout(timer)
      }
      
      timer = setTimeout(() => {
        fn.apply(this, args)
        lastTime = Date.now()
        timer = null
      }, delay - (now - lastTime))
    }
  }
} 