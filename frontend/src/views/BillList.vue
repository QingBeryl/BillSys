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
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
          style="width: 260px;"
          size="default"
          clearable
        />
        <el-select v-model="filterType" placeholder="类型" clearable style="width: 110px;" size="default">
          <el-option label="收入" value="收入" />
          <el-option label="支出" value="支出" />
        </el-select>
        <el-select v-model="filterSubCategories" placeholder="子分类" clearable multiple collapse-tags
                   collapse-tags-tooltip style="width: 200px;" size="default">
          <el-option v-for="cat in subCategoryOptions" :key="cat" :label="cat" :value="cat" />
        </el-select>
        <el-select v-model="filterAccount" placeholder="账户" clearable style="width: 130px;" size="default">
          <el-option v-for="acc in accountOptions" :key="acc" :label="acc" :value="acc" />
        </el-select>
        <span class="filter-count">共 {{ filteredBills.length }} 条</span>
      </div>

      <!-- 总账汇总 -->
      <div class="summary-bar">
        <span class="summary-item income">收入 ¥{{ totalIncome.toFixed(2) }}</span>
        <span class="summary-item expense">支出 ¥{{ totalExpense.toFixed(2) }}</span>
        <span class="summary-item" :class="totalBalance >= 0 ? 'income' : 'expense'">
          结余 ¥{{ totalBalance.toFixed(2) }}
        </span>
        <span class="summary-note" v-if="excludedIds.size">（已排除 {{ excludedIds.size }} 笔不计入总账）</span>
      </div>

      <el-table :data="filteredBills" stripe v-loading="loading" max-height="600"
                :row-class-name="rowClassName">
        <el-table-column width="50" align="center">
          <template #header>
            <el-checkbox v-model="excludeAll" @change="toggleExcludeAll" :indeterminate="isIndeterminate" />
          </template>
          <template #default="{ row }">
            <el-checkbox :model-value="excludedIds.has(row.id)" @change="toggleExclude(row.id)" />
          </template>
        </el-table-column>
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
import { ref, computed, onMounted, watch } from 'vue'
import { getBills, deleteBill } from '../api/bills'
import { getMeta } from '../api/auth'
import { ElMessage } from 'element-plus'

const bills = ref([])
const loading = ref(false)
const metaCategories = ref({})

const filterType = ref('')
const filterSubCategories = ref([])
const filterAccount = ref('')
const dateRange = ref(null)

// 临时排除的账单ID（不计入总账，但不删除）
const excludedIds = ref(new Set())

const subCategoryOptions = computed(() => {
  if (filterType.value && metaCategories.value[filterType.value]) {
    return metaCategories.value[filterType.value]
  }
  // 未选类型时显示所有子分类
  const all = new Set()
  Object.values(metaCategories.value).forEach(list => list.forEach(s => all.add(s)))
  return [...all].sort()
})

// 切换类型时清除不属于新类型的子分类选项
watch(filterType, () => {
  const valid = subCategoryOptions.value
  filterSubCategories.value = filterSubCategories.value.filter(s => valid.includes(s))
})

const accountOptions = computed(() => {
  const set = new Set(bills.value.map(b => b.account).filter(Boolean))
  return [...set].sort()
})

const filteredBills = computed(() => {
  return bills.value.filter(b => {
    if (filterType.value && b.type !== filterType.value) return false
    if (filterSubCategories.value.length && !filterSubCategories.value.includes(b.sub_category)) return false
    if (filterAccount.value && b.account !== filterAccount.value) return false
    if (dateRange.value && dateRange.value.length === 2) {
      const day = b.bill_date ? b.bill_date.substring(0, 10) : ''
      if (day < dateRange.value[0] || day > dateRange.value[1]) return false
    }
    return true
  })
})

// 计入总账的账单（排除勾选的）
const countedBills = computed(() => {
  return filteredBills.value.filter(b => !excludedIds.value.has(b.id))
})

const totalIncome = computed(() => {
  return countedBills.value.filter(b => b.type === '收入').reduce((s, b) => s + Math.abs(b.money), 0)
})

const totalExpense = computed(() => {
  return countedBills.value.filter(b => b.type === '支出').reduce((s, b) => s + Math.abs(b.money), 0)
})

const totalBalance = computed(() => totalIncome.value - totalExpense.value)

// 全选排除
const excludeAll = ref(false)
const isIndeterminate = computed(() => {
  const ids = filteredBills.value.map(b => b.id)
  const excluded = ids.filter(id => excludedIds.value.has(id))
  return excluded.length > 0 && excluded.length < ids.length
})

function toggleExcludeAll(val) {
  if (val) {
    filteredBills.value.forEach(b => excludedIds.value.add(b.id))
  } else {
    filteredBills.value.forEach(b => excludedIds.value.delete(b.id))
  }
  excludedIds.value = new Set(excludedIds.value)
}

function toggleExclude(id) {
  if (excludedIds.value.has(id)) {
    excludedIds.value.delete(id)
  } else {
    excludedIds.value.add(id)
  }
  excludedIds.value = new Set(excludedIds.value)
  // 同步全选状态
  const ids = filteredBills.value.map(b => b.id)
  excludeAll.value = ids.length > 0 && ids.every(i => excludedIds.value.has(i))
}

function rowClassName({ row }) {
  return excludedIds.value.has(row.id) ? 'row-excluded' : ''
}

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

onMounted(async () => {
  const metaRes = await getMeta()
  metaCategories.value = metaRes.data.categories
  loadBills()
})
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
  margin-bottom: 12px;
  padding: 12px 16px;
  background: #faf6f1;
  border-radius: 10px;
}

.filter-count {
  margin-left: auto;
  font-size: 13px;
  color: #9c8578;
}

.summary-bar {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 16px;
  padding: 10px 16px;
  background: #fff;
  border: 1px solid rgba(200, 170, 130, 0.15);
  border-radius: 10px;
}

.summary-item {
  font-size: 14px;
  font-weight: 600;
}

.summary-item.income { color: #E6A23C; }
.summary-item.expense { color: #C4704B; }

.summary-note {
  font-size: 12px;
  color: #B8A99A;
}

:deep(.row-excluded) {
  opacity: 0.4;
  text-decoration: line-through;
}
</style>
