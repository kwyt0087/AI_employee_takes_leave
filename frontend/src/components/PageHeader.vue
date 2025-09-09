<template>
  <div class="page-header">
    <van-nav-bar
      :title="title"
      :left-text="showBack ? '返回' : ''"
      :left-arrow="showBack"
      @click-left="onClickLeft"
      :fixed="fixed"
      :placeholder="placeholder"
    >
      <template #right v-if="$slots.right">
        <slot name="right"></slot>
      </template>
    </van-nav-bar>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

// 定义属性
const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  showBack: {
    type: Boolean,
    default: true
  },
  fixed: {
    type: Boolean,
    default: true
  },
  placeholder: {
    type: Boolean,
    default: true
  },
  backPath: {
    type: String,
    default: ''
  }
})

// 定义事件
const emit = defineEmits(['click-left'])

// 获取路由
const router = useRouter()

// 点击左侧按钮
const onClickLeft = () => {
  emit('click-left')
  
  if (props.backPath) {
    router.push(props.backPath)
  } else {
    router.back()
  }
}
</script>

<style scoped>
.page-header {
  z-index: 100;
}
</style>
