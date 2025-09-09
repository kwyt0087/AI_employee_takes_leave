<template>
  <div class="chat-page">
    <!-- 顶部导航栏 -->
    <van-nav-bar
      title="AI助手"
      left-arrow
      @click-left="$router.back()"
      fixed
      placeholder
    />
    
    <!-- 聊天内容区域 -->
    <div class="chat-container">
      <div class="chat-list" ref="chatListRef">
        <!-- 欢迎消息 -->
        <div class="chat-item system" v-if="messages.length === 0">
          <div class="chat-content">
            <p>您好，我是AI请假助手，可以帮您解答关于请假、考勤等问题，也可以为您提供请假建议。</p>
            <p>您可以这样问我：</p>
            <ul>
              <li>我想请3天假，有什么建议？</li>
              <li>年假的规定是什么？</li>
              <li>病假需要提供什么证明？</li>
              <li>婚假可以请几天？</li>
            </ul>
          </div>
        </div>
        
        <!-- 聊天消息列表 -->
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['chat-item', msg.type]"
        >
          <div class="chat-avatar" v-if="msg.type === 'ai'">AI</div>
          <div class="chat-avatar user-avatar" v-else-if="msg.type === 'user'">{{ userInitial }}</div>
          
          <div class="chat-content">
            <div v-if="msg.type === 'error'" class="error-message">
              {{ msg.content }}
            </div>
            <div v-else v-html="formatMessage(msg.content)"></div>
            
            <!-- 来源文档 -->
            <div class="source-documents" v-if="msg.sourceDocuments && msg.sourceDocuments.length > 0">
              <div class="source-title" @click="toggleSourceVisible(index)">
                <van-icon :name="sourceVisible[index] ? 'arrow-up' : 'arrow-down'" />
                查看来源
              </div>
              <div class="source-content" v-if="sourceVisible[index]">
                <div v-for="(doc, docIndex) in msg.sourceDocuments" :key="docIndex" class="source-item">
                  <div class="source-item-title">{{ doc.metadata.title || '未知来源' }}</div>
                  <div class="source-item-content">{{ doc.content }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 加载中状态 -->
        <div class="chat-item ai" v-if="chatStore.loading">
          <div class="chat-avatar">AI</div>
          <div class="chat-content">
            <div class="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 输入框区域 -->
    <div class="chat-input-wrapper">
      <div class="chat-input">
        <van-field
          v-model="inputMessage"
          placeholder="请输入问题..."
          type="textarea"
          autosize
          @keypress.enter.prevent="sendMessage"
        />
        <van-button 
          type="primary" 
          :loading="chatStore.loading"
          :disabled="!inputMessage.trim() || chatStore.loading"
          @click="sendMessage"
        >
          发送
        </van-button>
      </div>
    </div>
    
    <!-- 底部导航栏 -->
    <van-tabbar v-model="activeTab" route>
      <van-tabbar-item icon="home-o" to="/">首页</van-tabbar-item>
      <van-tabbar-item icon="chat-o" to="/chat">AI助手</van-tabbar-item>
      <van-tabbar-item icon="calendar-o" to="/leave-apply">请假</van-tabbar-item>
      <van-tabbar-item icon="user-o" to="/user">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { useChatStore } from '../stores/chat'
import { useUserStore } from '../stores/user'

// 路由
const router = useRouter()

// 状态管理
const chatStore = useChatStore()
const userStore = useUserStore()

// 输入消息
const inputMessage = ref('')

// 激活的标签页
const activeTab = ref(1)

// 聊天列表DOM引用
const chatListRef = ref(null)

// 来源文档可见状态
const sourceVisible = ref({})

// 用户头像首字母
const userInitial = computed(() => {
  return userStore.fullName?.charAt(0) || 'U'
})

// 聊天消息列表
const messages = computed(() => chatStore.messages)

// 格式化消息内容（处理换行和链接）
const formatMessage = (content) => {
  if (!content) return ''
  
  // 替换换行符为<br>
  let formatted = content.replace(/\n/g, '<br>')
  
  // 将URL转换为可点击的链接
  formatted = formatted.replace(
    /(https?:\/\/[^\s]+)/g,
    '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
  )
  
  return formatted
}

// 切换来源文档的可见性
const toggleSourceVisible = (index) => {
  sourceVisible.value[index] = !sourceVisible.value[index]
}

// 发送消息
const sendMessage = async () => {
  // 检查是否登录
  if (!userStore.isLoggedIn) {
    showToast('请先登录')
    router.push('/login')
    return
  }
  
  // 检查消息是否为空
  const message = inputMessage.value.trim()
  if (!message || chatStore.loading) return
  
  // 清空输入框
  inputMessage.value = ''
  
  try {
    // 发送消息
    await chatStore.sendMessage(userStore.userId, message)
    
    // 保存聊天记录
    chatStore.saveMessages()
    
    // 滚动到底部
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Failed to send message:', error)
  }
}

// 滚动到底部
const scrollToBottom = () => {
  if (chatListRef.value) {
    chatListRef.value.scrollTop = chatListRef.value.scrollHeight
  }
}

// 监听消息列表变化，自动滚动到底部
watch(() => messages.value.length, async () => {
  await nextTick()
  scrollToBottom()
})

// 组件挂载时执行
onMounted(() => {
  // 初始化用户信息
  userStore.initUserInfo()
  
  // 加载聊天记录
  chatStore.loadMessages()
  
  // 滚动到底部
  nextTick(() => {
    scrollToBottom()
  })
})
</script>

<style scoped>
.chat-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.chat-container {
  flex: 1;
  overflow: hidden;
  padding-bottom: 60px;
  padding-top: 46px;
}

.chat-list {
  height: 100%;
  overflow-y: auto;
  padding: 16px;
}

.chat-item {
  display: flex;
  margin-bottom: 16px;
}

.chat-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #1989fa;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  margin-right: 12px;
  flex-shrink: 0;
}

.user-avatar {
  background-color: #07c160;
}

.chat-content {
  max-width: 70%;
  padding: 12px;
  border-radius: 8px;
  background-color: #f5f5f5;
  word-break: break-word;
}

.chat-item.user {
  flex-direction: row-reverse;
}

.chat-item.user .chat-avatar {
  margin-right: 0;
  margin-left: 12px;
}

.chat-item.user .chat-content {
  background-color: #e1f3ff;
}

.chat-item.system .chat-content {
  max-width: 100%;
  background-color: #f0f9eb;
  border-left: 4px solid #07c160;
}

.chat-input-wrapper {
  position: fixed;
  bottom: 50px;
  left: 0;
  right: 0;
  padding: 8px 16px;
  background-color: #fff;
  border-top: 1px solid #ebedf0;
  z-index: 10;
}

.chat-input {
  display: flex;
  align-items: flex-end;
}

.chat-input :deep(.van-field) {
  flex: 1;
  margin-right: 8px;
}

.error-message {
  color: #ee0a24;
}

.source-documents {
  margin-top: 8px;
  font-size: 12px;
}

.source-title {
  color: #1989fa;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.source-title .van-icon {
  margin-right: 4px;
}

.source-content {
  margin-top: 8px;
  padding: 8px;
  background-color: rgba(0, 0, 0, 0.03);
  border-radius: 4px;
}

.source-item {
  margin-bottom: 8px;
}

.source-item-title {
  font-weight: bold;
  margin-bottom: 4px;
}

.source-item-content {
  color: #666;
  font-size: 12px;
}

.loading-dots {
  display: flex;
  align-items: center;
}

.loading-dots span {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #1989fa;
  margin-right: 4px;
  animation: loading 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.loading-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes loading {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}
</style> 