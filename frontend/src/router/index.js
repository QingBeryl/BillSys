import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/',
    component: () => import('../views/Layout.vue'),
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'Dashboard', component: () => import('../views/Dashboard.vue') },
      { path: 'bills', name: 'BillList', component: () => import('../views/BillList.vue') },
      { path: 'bill/add', name: 'BillAdd', component: () => import('../views/BillForm.vue') },
      { path: 'bill/edit/:id', name: 'BillEdit', component: () => import('../views/BillForm.vue') },
      { path: 'query', name: 'Query', component: () => import('../views/Query.vue') },
      { path: 'transfer', name: 'Transfer', component: () => import('../views/Transfer.vue') },
      { path: 'excel', name: 'Excel', component: () => import('../views/Excel.vue') },
      { path: 'users', name: 'UserManage', component: () => import('../views/UserManage.vue') }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 导航守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path !== '/login' && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
