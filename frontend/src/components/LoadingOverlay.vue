<template>
  <div class="loading-overlay" v-if="show">
    <div class="loading-content">
      <van-loading size="36px" color="#1989fa" />
      <div class="loading-text">{{ text }}</div>
    </div>
  </div>
</template>

<script setup>
// 定义属性
defineProps({
  show: {
    type: Boolean,
    default: false
  },
  text: {
    type: String,
    default: '加载中...'
  }
})
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.loading-text {
  margin-top: 12px;
  color: #646566;
}
</style> 