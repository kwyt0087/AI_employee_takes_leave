<template>
  <div class="empty-state">
    <van-empty 
      :image="image" 
      :image-size="imageSize"
      :description="description"
    >
      <template #bottom v-if="$slots.bottom">
        <slot name="bottom"></slot>
      </template>
    </van-empty>
  </div>
</template>

<script setup>
// 定义属性
defineProps({
  image: {
    type: String,
    default: 'default'
  },
  imageSize: {
    type: [Number, String],
    default: 120
  },
  description: {
    type: String,
    default: '暂无数据'
  }
})
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px 16px;
}
</style> 