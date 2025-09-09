<template>
  <div class="tab-bar">
    <van-tabbar v-model="activeTab" route>
      <van-tabbar-item icon="home-o" to="/">首页</van-tabbar-item>
      <van-tabbar-item icon="chat-o" to="/chat">AI助手</van-tabbar-item>
      <van-tabbar-item icon="calendar-o" to="/leave-apply">请假</van-tabbar-item>
      <van-tabbar-item icon="user-o" to="/user">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

// 获取当前路由
const route = useRoute()

// 激活的标签页
const activeTab = ref(0)

// 路由映射
const routeMap = {
  '/': 0,
  '/chat': 1,
  '/leave-apply': 2,
  '/user': 3
}

// 监听路由变化
watch(() => route.path, (path) => {
  // 根据路径设置激活的标签页
  if (routeMap.hasOwnProperty(path)) {
    activeTab.value = routeMap[path]
  }
}, { immediate: true })
</script>

<style scoped>
.tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
}
</style> 