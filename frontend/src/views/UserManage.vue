<template>
  <div class="page-card">
    <div class="list-header">
      <h4>用户管理</h4>
      <el-button type="primary" round @click="openDialog()">
        <el-icon><Plus /></el-icon> 添加用户
      </el-button>
    </div>

    <el-table :data="users" stripe v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="is_admin" label="角色" width="120">
        <template #default="{ row }">
          <el-tag :type="row.is_admin ? 'danger' : 'info'" size="small">
            {{ row.is_admin ? '管理员' : '普通用户' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button link type="primary" size="small" @click="openDialog(row)">编辑</el-button>
          <el-popconfirm title="确定删除该用户？" @confirm="handleDelete(row.id)">
            <template #reference>
              <el-button link type="danger" size="small">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="editingId ? '编辑用户' : '添加用户'" width="400px">
      <el-form :model="dialogForm" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="dialogForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="dialogForm.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button round @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" round :loading="saving" @click="handleSave">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getUsers, addUser, updateUser, deleteUser } from '../api/users'
import { ElMessage } from 'element-plus'

const users = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const saving = ref(false)
const editingId = ref(null)

const dialogForm = reactive({ username: '', password: '' })

async function loadUsers() {
  loading.value = true
  try {
    const res = await getUsers()
    users.value = res.data
  } finally {
    loading.value = false
  }
}

function openDialog(row) {
  if (row) {
    editingId.value = row.id
    dialogForm.username = row.username
    dialogForm.password = ''
  } else {
    editingId.value = null
    dialogForm.username = ''
    dialogForm.password = ''
  }
  dialogVisible.value = true
}

async function handleSave() {
  if (!dialogForm.username || !dialogForm.password) {
    ElMessage.warning('请填写用户名和密码')
    return
  }
  saving.value = true
  try {
    if (editingId.value) {
      await updateUser(editingId.value, { ...dialogForm })
      ElMessage.success('更新成功')
    } else {
      await addUser({ ...dialogForm })
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    loadUsers()
  } finally {
    saving.value = false
  }
}

async function handleDelete(id) {
  await deleteUser(id)
  ElMessage.success('删除成功')
  loadUsers()
}

onMounted(loadUsers)
</script>

<style scoped>
.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.list-header h4 {
  font-size: 16px;
  color: #3D2B1F;
}
</style>
