<template>
  <div class="app">
    <router-view v-slot="{ Component }">
      <keep-alive>
        <component :is="Component" />
      </keep-alive>
    </router-view>
  </div>
</template>

<script setup>
// 应用级别的逻辑可以放在这里
</script>

<style>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Segoe UI, Arial, Roboto, 'PingFang SC', 'miui', 'Hiragino Sans GB', 'Microsoft Yahei', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f7f8fa;
  color: #323233;
  font-size: 14px;
}

.app {
  min-height: 100vh;
  width: 100%;
  max-width: 750px;
  margin: 0 auto;
  position: relative;
}

/* 安全区适配 */
.safe-area-inset-bottom {
  padding-bottom: constant(safe-area-inset-bottom);
  padding-bottom: env(safe-area-inset-bottom);
}

/* 通用样式 */
.page-container {
  padding: 46px 16px 50px;
}

.page-title {
  font-size: 18px;
  font-weight: bold;
  margin: 16px 0;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  margin: 12px 0;
  color: #323233;
}

.text-primary {
  color: #1989fa;
}

.text-success {
  color: #07c160;
}

.text-danger {
  color: #ee0a24;
}

.text-warning {
  color: #ff976a;
}

.text-gray {
  color: #969799;
}

.card-wrapper {
  margin-bottom: 12px;
  border-radius: 8px;
  background-color: #fff;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(100, 101, 102, 0.08);
}
</style> 