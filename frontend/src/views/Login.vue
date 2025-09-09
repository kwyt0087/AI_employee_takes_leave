<template>
  <div class="login-page">
    <!-- 顶部导航栏 -->
    <van-nav-bar
      title="登录"
      fixed
      placeholder
    />
    
    <!-- 页面内容 -->
    <div class="page-container">
      <!-- 登录表单 -->
      <div class="login-form-wrapper">
        <div class="logo">
          <img src="../assets/logo.png" alt="Logo" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTI4IiBoZWlnaHQ9IjEyOCIgdmlld0JveD0iMCAwIDEyOCAxMjgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjEyOCIgaGVpZ2h0PSIxMjgiIHJ4PSI2NCIgZmlsbD0iIzE5ODlmYSIvPjxwYXRoIGQ9Ik02NCA0MEg4OFY4OEg0MFY2NEg2NFY0MFoiIGZpbGw9IndoaXRlIi8+PC9zdmc+'" />
        </div>
        <div class="app-name">AI请假系统</div>
        
        <van-form @submit="onSubmit" class="login-form">
          <van-cell-group inset>
            <!-- 用户名 -->
            <van-field
              v-model="username"
              name="username"
              label="用户名"
              placeholder="请输入用户名"
              :rules="[{ required: true, message: '请填写用户名' }]"
            />
            
            <!-- 密码 -->
            <van-field
              v-model="password"
              type="password"
              name="password"
              label="密码"
              placeholder="请输入密码"
              :rules="[{ required: true, message: '请填写密码' }]"
            />
          </van-cell-group>
          
          <!-- 登录按钮 -->
          <div style="margin: 16px;">
            <van-button 
              round 
              block 
              type="primary" 
              native-type="submit"
              :loading="loading"
            >
              登录
            </van-button>
          </div>
        </van-form>
        
        <!-- 演示账号提示 -->
        <div class="demo-tip">
          <p>演示账号：</p>
          <p>用户名：demo</p>
          <p>密码：123456</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { showToast, showSuccessToast } from 'vant'
import { useUserStore } from '../stores/user'

// 路由
const router = useRouter()
const route = useRoute()

// 状态管理
const userStore = useUserStore()

// 表单数据
const username = ref('')
const password = ref('')

// 加载状态
const loading = ref(false)

// 登录表单提交
const onSubmit = async () => {
  loading.value = true
  
  try {
    // 在实际项目中，这里应该调用登录API
    // await userStore.login(username.value, password.value)
    
    // 演示模式：模拟登录
    if (username.value === 'demo' && password.value === '123456') {
      // 模拟登录成功
      // 分离用户基本信息和年假信息
      const baseUserInfo = {
        id: 1,
        username: 'demo',
        email: 'demo@example.com',
        full_name: '演示用户',
        department: '技术部',
        position: '工程师',
        employee_id: 'EMP001',
        hire_date: '2020-01-01',
        is_active: true,
        is_admin: false
      }
      
      const annualLeaveInfo = {
        total_days: 10,
        used_days: 3,
        remaining_days: 7
      }
      
      // 设置用户信息（合并两部分数据）
      userStore.setUserInfo({
        ...baseUserInfo,
        annual_leave: annualLeaveInfo
      })
      
      // 保存token（模拟）
      localStorage.setItem('token', 'mock_token_for_demo')
      
      showSuccessToast('登录成功')
      
      // 跳转到首页或者来源页面
      const redirect = route.query.redirect || '/'
      router.replace(redirect)
    } else {
      // 登录失败
      showToast('用户名或密码错误')
    }
  } catch (error) {
    console.error('Login failed:', error)
    showToast(error.message || '登录失败')
  } finally {
    loading.value = false
  }
}

// 组件挂载时执行
onMounted(() => {
  // 如果已经登录，跳转到首页
  if (userStore.isLoggedIn) {
    router.replace('/')
  }
  
  // 设置演示账号
  username.value = 'demo'
  password.value = '123456'
})
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background-color: #f7f8fa;
}

.login-form-wrapper {
  padding: 40px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo {
  width: 80px;
  height: 80px;
  margin-bottom: 16px;
}

.logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.app-name {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 32px;
  color: #323233;
}

.login-form {
  width: 100%;
}

.demo-tip {
  margin-top: 24px;
  padding: 16px;
  background-color: #f2f3f5;
  border-radius: 8px;
  width: 100%;
  max-width: 300px;
  text-align: center;
}

.demo-tip p {
  margin: 4px 0;
  color: #646566;
}
</style> 