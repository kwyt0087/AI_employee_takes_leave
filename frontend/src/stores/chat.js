import { defineStore } from 'pinia'
import { chatApi } from '../api'

// 定义聊天状态
export const useChatStore = defineStore('chat', {
  // 状态
  state: () => ({
    // 聊天消息列表
    messages: [],
    // 是否正在加载
    loading: false,
    // 错误信息
    error: null
  }),
  
  // getters
  getters: {
    // 获取聊天历史
    chatHistory: (state) => state.messages
  },
  
  // actions
  actions: {
    // 发送消息
    async sendMessage(userId, content) {
      // 添加用户消息到列表
      const userMessage = {
        id: Date.now(),
        type: 'user',
        content,
        timestamp: new Date().toISOString()
      }
      this.messages.push(userMessage)
      
      // 设置加载状态
      this.loading = true
      this.error = null
      
      try {
        // 发送消息到服务器
        const data = {
          user_id: userId,
          message: content
        }
        
        // 调用API
        const response = await chatApi.sendMessage(data)
        
        // 添加AI回复到列表
        const aiMessage = {
          id: Date.now() + 1,
          type: 'ai',
          content: response.response,
          timestamp: new Date().toISOString(),
          sourceDocuments: response.source_documents || []
        }
        this.messages.push(aiMessage)
        
        return aiMessage
      } catch (error) {
        // 处理错误
        this.error = error.response?.data?.detail || '发送消息失败'
        
        // 添加错误消息
        const errorMessage = {
          id: Date.now() + 1,
          type: 'error',
          content: this.error,
          timestamp: new Date().toISOString()
        }
        this.messages.push(errorMessage)
        
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 清空聊天记录
    clearMessages() {
      this.messages = []
    },
    
    // 从本地存储加载聊天记录
    loadMessages() {
      const savedMessages = localStorage.getItem('chatMessages')
      if (savedMessages) {
        try {
          this.messages = JSON.parse(savedMessages)
        } catch (error) {
          console.error('Failed to parse chat messages:', error)
          this.messages = []
        }
      }
    },
    
    // 保存聊天记录到本地存储
    saveMessages() {
      localStorage.setItem('chatMessages', JSON.stringify(this.messages))
    }
  }
}) 