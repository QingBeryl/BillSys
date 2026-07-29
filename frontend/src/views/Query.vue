<template>
  <div>
    <div class="page-card">
      <h4 style="margin-bottom: 20px;">高级查询</h4>
      <el-form :model="query" inline label-width="80px">
        <el-form-item label="开始日期">
          <el-date-picker v-model="query.start" type="date" value-format="YYYY-MM-DD" placeholder="起始" style="width: 160px;" />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker v-model="query.end" type="date" value-format="YYYY-MM-DD" placeholder="截止" style="width: 160px;" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="query.type" clearable placeholder="全部" style="width: 100px;">
            <el-option label="收入" value="收入" />
            <el-option label="支出" value="支出" />
          </el-select>
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="query.category" clearable placeholder="全部" style="width: 130px;">
            <el-option v-for="cat in categoryKeys" :key="cat" :label="cat" :value="cat" />
          </el-select>
        </el-form-item>
        <el-form-item label="账户">
          <el-select v-model="query.account" clearable placeholder="全部" style="width: 130px;">
            <el-option v-for="acc in accounts" :key="acc" :label="acc" :value="acc" />
          </el-select>
        </el-form-item>
        <el-form-item label="最小金额">
          <el-input-number v-model="query.min" :min="0" :precision="2" controls-position="right" style="width: 130px;" />
        </el-form-item>
        <el-form-item label="最大金额">
          <el-input-number v-model="query.max" :min="0" :precision="2" controls-position="right" style="width: 130px;" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" round @click="handleQuery" :loading="loading">查询</el-button>
          <el-button round @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="page-card" v-if="results.length > 0">
      <p style="margin-bottom: 12px; color: #8C7B6B; font-size: 13px;">共 {{ results.length }} 条结果</p>
      <el-table :data="results" stripe max-height="500">
        <el-table-column prop="bill_date" label="日期" width="170">
          <template #default="{ row }">{{ row.bill_date?.substring(0, 10) }}</template>
        </el-table-column>
        <el-table-column prop="type" label="类型" width="80">
          <template #default="{ row }">
            <el-tag :type="row.type === '收入' ? 'warning' : 'danger'" size="small">{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="money" label="金额" width="120">
          <template #default="{ row }">
            <span :class="row.type === '收入' ? 'money-income' : 'money-expense'">¥{{ Math.abs(row.money).toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="分类" width="110" />
        <el-table-column prop="sub_category" label="子分类" width="110" />
        <el-table-column prop="account" label="账户" width="110" />
        <el-table-column prop="remark" label="备注" show-overflow-tooltip />
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { getMeta } from '../api/auth'
import { queryBills } from '../api/bills'

const categories = ref({})
const accounts = ref([])
const results = ref([])
const loading = ref(false)

const query = reactive({
  start: '', end: '', type: '', category: '', sub_category: '', account: '', min: undefined, max: undefined
})

const categoryKeys = computed(() => Object.keys(categories.value))

onMounted(async () => {
  const res = await getMeta()
  categories.value = res.data.categories
  accounts.value = res.data.accounts
})

async function handleQuery() {
  loading.value = true
  try {
    const params = {}
    Object.keys(query).forEach(k => {
      if (query[k] !== '' && query[k] !== undefined && query[k] !== null) params[k] = query[k]
    })
    const res = await queryBills(params)
    results.value = res.data
  } finally {
    loading.value = false
  }
}

function resetQuery() {
  Object.assign(query, { start: '', end: '', type: '', category: '', sub_category: '', account: '', min: undefined, max: undefined })
  results.value = []
}
</script>
