<template>
  <div>
    <div class="page-card">
      <div class="list-header">
        <h4>全部账单</h4>
        <el-button type="primary" round @click="$router.push('/bill/add')">
          <el-icon><Plus /></el-icon> 记一笔
        </el-button>
      </div>

      <!-- 筛选栏 -->
      <div class="filter-bar">
        <el-select v-model="filterType" placeholder="类型" clearable style="width: 110px;" size="default">
          <el-option label="收入" value="收入" />
          <el-option label="支出" value="支出" />
        </el-select>
        <el-select v-model="filterCategory" placeholder="分类" clearable style="width: 140px;" size="default">
          <el-option v-for="cat in categoryOptions" :key="cat" :label="cat" :value="cat" />
        </el-select>
        <el-select v-model="filterAccount" placeholder="账户" clearable style="width: 130px;" size="default">
          <el-option v-for="acc in accountOptions" :key="acc" :label="acc" :value="acc" />
        </el-select>
        <span class="filter-count">共 {{ filteredBills.length }} 条</span>
      </div>

      <el-table :data="filteredBills" stripe v-loading="loading" max-height="600">
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
import { ref, computed, onMounted } from 'vue'
import { getBills, deleteBill } from '../api/bills'
import { ElMessage } from 'element-plus'

const bills = ref([])
const loading = ref(false)

const filterType = ref('')
const filterCategory = ref('')
const filterAccount = ref('')

const categoryOptions = computed(() => {
  const set = new Set(bills.value.map(b => b.category).filter(Boolean))
  return [...set].sort()
})

const accountOptions = computed(() => {
  const set = new Set(bills.value.map(b => b.account).filter(Boolean))
  return [...set].sort()
})

const filteredBills = computed(() => {
  return bills.value.filter(b => {
    if (filterType.value && b.type !== filterType.value) return false
    if (filterCategory.value && b.category !== filterCategory.value) return false
    if (filterAccount.value && b.account !== filterAccount.value) return false
    return true
  })
})

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

.filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  padding: 12px 16px;
  background: #faf6f1;
  border-radius: 10px;
}

.filter-count {
  margin-left: auto;
  font-size: 13px;
  color: #9c8578;
}
</style>
