<template>
  <div class="policy-upload-page">
    <!-- 顶部导航栏 -->
    <van-nav-bar
      title="上传政策"
      left-arrow
      @click-left="$router.back()"
      fixed
      placeholder
    />
    
    <!-- 页面内容 -->
    <div class="page-container">
      <!-- 上传表单 -->
      <van-form @submit="onSubmit" class="upload-form">
        <van-cell-group inset title="政策信息">
          <!-- 政策标题 -->
          <van-field
            v-model="title"
            name="title"
            label="政策标题"
            placeholder="请输入政策标题"
            :rules="[{ required: true, message: '请填写政策标题' }]"
          />
          
          <!-- 政策描述 -->
          <van-field
            v-model="description"
            rows="3"
            autosize
            type="textarea"
            name="description"
            label="政策描述"
            placeholder="请输入政策描述"
            :rules="[{ required: true, message: '请填写政策描述' }]"
          />
          
          <!-- 政策分类 -->
          <van-field
            v-model="category"
            is-link
            readonly
            name="category"
            label="政策分类"
            placeholder="请选择政策分类"
            :rules="[{ required: true, message: '请选择政策分类' }]"
            @click="showCategoryPicker = true"
          />
          
          <!-- 文件上传 -->
          <div class="file-upload-field">
            <div class="field-label">政策文件</div>
            <van-uploader
              v-model="fileList"
              :max-count="1"
              :max-size="10 * 1024 * 1024"
              :before-read="beforeFileUpload"
              @oversize="onFileOversize"
            />
            <div class="field-tip">支持txt、pdf、docx、csv、json格式，大小不超过10MB</div>
          </div>
        </van-cell-group>
        
        <!-- 提交按钮 -->
        <div style="margin: 16px;">
          <van-button 
            round 
            block 
            type="primary" 
            native-type="submit"
            :loading="uploading"
          >
            上传政策
          </van-button>
        </div>
      </van-form>
      
      <!-- 分类选择器 -->
      <van-popup v-model:show="showCategoryPicker" position="bottom">
        <van-picker
          :columns="categoryOptions"
          @confirm="onCategoryConfirm"
          @cancel="showCategoryPicker = false"
        />
      </van-popup>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showSuccessToast } from 'vant'
import { useUserStore } from '../stores/user'

// 路由
const router = useRouter()

// 状态管理
const userStore = useUserStore()

// 表单数据
const title = ref('')
const description = ref('')
const category = ref('')
const fileList = ref([])

// 控制弹出层显示
const showCategoryPicker = ref(false)

// 上传状态
const uploading = ref(false)

// 政策分类选项
const categoryOptions = [
  { text: '请假制度', value: 'leave' },
  { text: '考勤制度', value: 'attendance' },
  { text: '加班调休', value: 'overtime' },
  { text: '薪资福利', value: 'salary' },
  { text: '其他', value: 'other' }
]

// 分类确认
const onCategoryConfirm = (value) => {
  category.value = value.text
  showCategoryPicker.value = false
}

// 文件上传前验证
const beforeFileUpload = (file) => {
  // 检查文件类型
  const allowedTypes = ['text/plain', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/csv', 'application/json']
  const fileExtension = file.name.split('.').pop().toLowerCase()
  const allowedExtensions = ['txt', 'pdf', 'docx', 'csv', 'json']
  
  if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
    showToast('不支持的文件类型')
    return false
  }
  
  return true
}

// 文件大小超出限制
const onFileOversize = () => {
  showToast('文件大小不能超过10MB')
}

// 表单提交
const onSubmit = async () => {
  // 检查是否登录
  if (!userStore.isLoggedIn) {
    showToast('请先登录')
    router.push('/login')
    return
  }
  
  // 检查是否有管理员权限
  if (!userStore.isAdmin) {
    showToast('您没有上传权限')
    return
  }
  
  // 检查是否选择了文件
  if (fileList.value.length === 0) {
    showToast('请选择要上传的文件')
    return
  }
  
  uploading.value = true
  
  try {
    // 在实际项目中，这里应该调用API上传政策文件
    // const formData = new FormData()
    // formData.append('title', title.value)
    // formData.append('description', description.value)
    // formData.append('category', category.value)
    // formData.append('file', fileList.value[0].file)
    // await policyApi.uploadPolicy(formData)
    
    // 模拟上传
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    showSuccessToast('政策上传成功')
    
    // 跳转到政策列表页面
    router.replace('/policy-list')
  } catch (error) {
    console.error('Failed to upload policy:', error)
    showToast(error.response?.data?.detail || '上传失败')
  } finally {
    uploading.value = false
  }
}

// 组件挂载时执行
onMounted(() => {
  // 初始化用户信息
  userStore.initUserInfo()
  
  // 检查是否登录
  if (!userStore.isLoggedIn) {
    showToast('请先登录')
    router.push('/login')
    return
  }
  
  // 检查是否有管理员权限
  if (!userStore.isAdmin) {
    showToast('您没有上传权限')
    router.back()
    return
  }
})
</script>

<style scoped>
.upload-form {
  margin-top: 16px;
}

.file-upload-field {
  padding: 16px;
  position: relative;
}

.field-label {
  margin-bottom: 8px;
  color: #646566;
  font-size: 14px;
}

.field-tip {
  margin-top: 8px;
  color: #969799;
  font-size: 12px;
}
</style> 