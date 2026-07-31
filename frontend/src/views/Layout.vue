<template>
  <div class="layout">
    <!-- 季节氛围光斑 -->
    <div class="season-orb"></div>

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
      <router-view v-slot="{ Component }">
        <transition name="page-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'

const route = useRoute()
const userStore = useUserStore()

const activeMenu = computed(() => {
  if (route.path.startsWith('/bill/edit')) return '/bill/add'
  return route.path
})

// 季节色：根据月份设置全局氛围色
onMounted(() => {
  const month = new Date().getMonth() + 1
  let accent
  if (month >= 3 && month <= 5) accent = 'rgba(240, 180, 160, 0.14)'       // 春：蜜桃粉
  else if (month >= 6 && month <= 8) accent = 'rgba(240, 190, 100, 0.13)'   // 夏：金橘
  else if (month >= 9 && month <= 11) accent = 'rgba(200, 120, 70, 0.12)'   // 秋：陶土
  else accent = 'rgba(160, 120, 90, 0.10)'                                   // 冬：可可
  document.documentElement.style.setProperty('--season-accent', accent)
})
</script>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
}

/* 季节光斑：一个巨大的柔和渐变圆，缓慢漂移 */
.season-orb {
  position: fixed;
  width: 60vw;
  height: 60vw;
  max-width: 900px;
  max-height: 900px;
  border-radius: 50%;
  background: radial-gradient(circle, var(--season-accent, rgba(232, 169, 135, 0.12)) 0%, transparent 70%);
  top: -10%;
  right: -15%;
  z-index: 0;
  pointer-events: none;
  animation: orbDrift 60s ease-in-out infinite alternate;
  filter: blur(40px);
}

@keyframes orbDrift {
  0% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(-6vw, 8vh) scale(1.08); }
  66% { transform: translate(4vw, 12vh) scale(0.95); }
  100% { transform: translate(-3vw, 5vh) scale(1.03); }
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
  position: relative;
  z-index: 1;
}

/* 路由切换过渡 */
.page-fade-enter-active {
  transition: opacity 320ms cubic-bezier(0.32, 0.72, 0, 1),
              transform 320ms cubic-bezier(0.32, 0.72, 0, 1);
}
.page-fade-leave-active {
  transition: opacity 180ms ease-in, transform 180ms ease-in;
}
.page-fade-enter-from {
  opacity: 0;
  transform: translateY(12px);
}
.page-fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
