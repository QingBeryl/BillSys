<template>
  <div class="layout">
    <!-- 顶部导航栏 -->
    <header class="top-nav">
      <div class="nav-left">
        <div class="logo">BillSys</div>
        <el-menu :default-active="activeMenu" router mode="horizontal" class="nav-menu"
                 background-color="transparent" text-color="#D4C4B0" active-text-color="#E8A987">
          <el-menu-item index="/dashboard">
            <el-icon><DataAnalysis /></el-icon>
            <span>仪表盘</span>
          </el-menu-item>
          <el-menu-item index="/bills">
            <el-icon><List /></el-icon>
            <span>收支记录</span>
          </el-menu-item>
          <el-menu-item index="/bill/add">
            <el-icon><EditPen /></el-icon>
            <span>记一笔</span>
          </el-menu-item>
          <el-menu-item index="/budget">
            <el-icon><Wallet /></el-icon>
            <span>预算</span>
          </el-menu-item>
          <el-menu-item index="/excel">
            <el-icon><Document /></el-icon>
            <span>数据导出</span>
          </el-menu-item>
          <el-menu-item v-if="userStore.isAdmin" index="/users">
            <el-icon><UserFilled /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
        </el-menu>
      </div>
      <div class="nav-right">
        <span class="username">{{ userStore.username }}</span>
        <el-button text type="danger" @click="userStore.logout()">
          <el-icon><SwitchButton /></el-icon> 退出
        </el-button>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'

const route = useRoute()
const userStore = useUserStore()

const activeMenu = computed(() => {
  if (route.path.startsWith('/bill/edit')) return '/bill/add'
  return route.path
})
</script>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.top-nav {
  height: 60px;
  background: linear-gradient(90deg, #43301F 0%, #2E1F14 100%);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 12px rgba(30, 15, 5, 0.2);
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.logo {
  font-size: 20px;
  font-weight: 700;
  color: #E8A987;
  letter-spacing: 2px;
  white-space: nowrap;
}

.nav-menu {
  border-bottom: none !important;
}

.nav-menu .el-menu-item {
  height: 60px;
  line-height: 60px;
  font-size: 14px;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.username {
  color: #D4C4B0;
  font-size: 14px;
}

.content {
  flex: 1;
  padding: 28px 32px;
}
</style>
