<template>
  <div class="layout">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="logo">BillSys</div>
      <el-menu :default-active="activeMenu" router class="side-menu"
               background-color="#3D2B1F" text-color="#D4C4B0" active-text-color="#E8A987">
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
        <el-menu-item index="/query">
          <el-icon><Search /></el-icon>
          <span>查询</span>
        </el-menu-item>
        <el-menu-item index="/transfer">
          <el-icon><Switch /></el-icon>
          <span>转账</span>
        </el-menu-item>
        <el-menu-item index="/excel">
          <el-icon><Document /></el-icon>
          <span>Excel</span>
        </el-menu-item>
        <el-menu-item v-if="userStore.isAdmin" index="/users">
          <el-icon><UserFilled /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
      </el-menu>
    </aside>

    <!-- 主区域 -->
    <div class="main-area">
      <header class="top-bar">
        <span class="page-title">{{ currentTitle }}</span>
        <div class="user-info">
          <span class="username">{{ userStore.username }}</span>
          <el-button text type="danger" @click="userStore.logout()">
            <el-icon><SwitchButton /></el-icon> 退出
          </el-button>
        </div>
      </header>
      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'

const route = useRoute()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

const titleMap = {
  '/dashboard': '仪表盘',
  '/bills': '收支记录',
  '/bill/add': '记一笔',
  '/query': '高级查询',
  '/transfer': '转账',
  '/excel': 'Excel 导入导出',
  '/users': '用户管理'
}

const currentTitle = computed(() => {
  if (route.path.startsWith('/bill/edit')) return '编辑账单'
  return titleMap[route.path] || 'BillSys'
})
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 220px;
  background: linear-gradient(180deg, #43301F 0%, #2E1F14 100%);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 100;
  border-right: 1px solid rgba(232, 169, 135, 0.08);
  box-shadow: 4px 0 24px rgba(30, 15, 5, 0.15);
}

.logo {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 700;
  color: #E8A987;
  letter-spacing: 2px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.side-menu {
  border-right: none;
  flex: 1;
  background: transparent !important;
}

.main-area {
  flex: 1;
  margin-left: 220px;
  display: flex;
  flex-direction: column;
}

.top-bar {
  height: 64px;
  background: rgba(255, 252, 248, 0.72);
  backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  border-bottom: 1px solid rgba(200, 170, 130, 0.1);
  position: sticky;
  top: 0;
  z-index: 50;
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #3D2B1F;
  letter-spacing: -0.01em;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.username {
  color: #6B4E3D;
  font-size: 14px;
}

.content {
  padding: 28px 32px;
  flex: 1;
}
</style>
