<template>
  <div class="login-wrapper">
    <div class="login-card">
      <h2 class="login-title">BillSys</h2>
      <p class="login-subtitle">创建新账号</p>
      <el-form :model="form" @submit.prevent="handleRegister" label-position="top">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="2-20个字符" prefix-icon="User" size="large" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="至少6位"
                    prefix-icon="Lock" size="large" show-password />
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input v-model="form.confirm" type="password" placeholder="再次输入密码"
                    prefix-icon="Lock" size="large" show-password @keyup.enter="handleRegister" />
        </el-form-item>
        <el-button type="primary" size="large" :loading="loading"
                   class="login-btn" @click="handleRegister">
          注 册
        </el-button>
      </el-form>
      <p class="switch-link">
        已有账号？<router-link to="/login">去登录</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '../api/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const form = reactive({ username: '', password: '', confirm: '' })

async function handleRegister() {
  if (!form.username || !form.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  if (form.password.length < 6) {
    ElMessage.warning('密码长度不能少于6位')
    return
  }
  if (form.password !== form.confirm) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }
  loading.value = true
  try {
    await register({ username: form.username, password: form.password })
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch (e) {
    // 错误已在拦截器中处理
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #FFF8F0 0%, #F5E6D8 50%, #EDD9C8 100%);
}

.login-card {
  width: 400px;
  padding: 48px 40px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(140, 90, 50, 0.12);
}

.login-title {
  text-align: center;
  font-size: 32px;
  color: #C4704B;
  font-weight: 700;
  letter-spacing: 2px;
}

.login-subtitle {
  text-align: center;
  color: #8C7B6B;
  margin-bottom: 32px;
  font-size: 14px;
}

.login-btn {
  width: 100%;
  margin-top: 8px;
  border-radius: 24px;
  font-size: 16px;
  letter-spacing: 4px;
}

.switch-link {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
  color: #8C7B6B;
}

.switch-link a {
  color: #C4704B;
  text-decoration: none;
  font-weight: 500;
}

.switch-link a:hover {
  text-decoration: underline;
}
</style>
