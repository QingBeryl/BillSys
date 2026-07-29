<template>
  <div>
    <div class="page-card">
      <div class="list-header">
        <h4>全部账单</h4>
        <el-button type="primary" round @click="$router.push('/bill/add')">
          <el-icon><Plus /></el-icon> 记一笔
        </el-button>
      </div>

      <el-table :data="bills" stripe v-loading="loading" max-height="600">
        <el-table-column prop="bill_date" label="日期" width="170">
          <template #default="{ row }">{{ formatDate(row.bill_date) }}</template>
        </el-table-column>
        <el-table-column prop="type" label="类型" width="80">
          <template #default="{ row }">
            <el-tag :type="row.type === '收入' ? 'warning' : 'danger'" size="small">{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="money" label="金额" width="120">
          <template #default="{ row }">
            <span :class="row.type === '收入' ? 'money-income' : 'money-expense'">
              {{ row.type === '收入' ? '+' : '-' }}¥{{ Math.abs(row.money).toFixed(2) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="分类" width="110" />
        <el-table-column prop="sub_category" label="子分类" width="110" />
        <el-table-column prop="account" label="账户" width="110" />
        <el-table-column prop="remark" label="备注" show-overflow-tooltip />
        <el-table-column label="操作" width="140" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="$router.push(`/bill/edit/${row.id}`)">编辑</el-button>
            <el-popconfirm title="确定删除这条记录？" @confirm="handleDelete(row.id)">
              <template #reference>
                <el-button link type="danger" size="small">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getBills, deleteBill } from '../api/bills'
import { ElMessage } from 'element-plus'

const bills = ref([])
const loading = ref(false)

function formatDate(d) {
  return d ? d.substring(0, 10) : ''
}

async function loadBills() {
  loading.value = true
  try {
    const res = await getBills()
    bills.value = res.data
  } finally {
    loading.value = false
  }
}

async function handleDelete(id) {
  await deleteBill(id)
  ElMessage.success('删除成功')
  loadBills()
}

onMounted(loadBills)
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
