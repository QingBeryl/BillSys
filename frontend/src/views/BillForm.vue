<template>
  <div class="form-page">
    <!-- 左侧：表单 -->
    <div class="form-shell">
      <div class="form-core" v-loading="pageLoading">
        <div class="form-title-area">
          <span class="form-eyebrow">{{ isEdit ? 'EDIT' : 'NEW' }}</span>
          <h3 class="form-title">{{ isEdit ? '编辑账单' : '记一笔' }}</h3>
        </div>

        <el-form :model="form" label-position="top" class="bill-form">
          <!-- 类型：独占一行 -->
          <el-form-item label="类型" class="stagger-item" style="--i:0">
            <el-radio-group v-model="form.type" size="large" @change="onTypeChange" class="type-toggle">
              <el-radio-button value="支出">支出</el-radio-button>
              <el-radio-button value="收入">收入</el-radio-button>
            </el-radio-group>
          </el-form-item>

          <!-- 双列网格区 -->
          <div class="form-grid">
            <el-form-item label="子分类" class="stagger-item" style="--i:2">
              <el-select v-model="form.sub_category" placeholder="选择子分类" style="width: 100%;">
                <el-option v-for="sub in subCategories" :key="sub" :label="sub" :value="sub" />
              </el-select>
            </el-form-item>

            <el-form-item label="金额" class="stagger-item" style="--i:3">
              <el-input-number v-model="form.money" :precision="2" :step="1" :min="0" style="width: 100%;" />
            </el-form-item>

            <el-form-item label="退款" class="stagger-item" style="--i:4">
              <el-input-number v-model="form.refund" :precision="2" :min="0" style="width: 100%;" />
            </el-form-item>

            <el-form-item label="日期" class="stagger-item" style="--i:5">
              <el-date-picker v-model="form.bill_date" type="datetime" placeholder="选择日期"
                              value-format="YYYY-MM-DD HH:mm:ss" style="width: 100%;" />
            </el-form-item>

            <el-form-item label="账户" class="stagger-item" style="--i:6">
              <el-select v-model="form.account" placeholder="选择账户" style="width: 100%;">
                <el-option v-for="acc in accounts" :key="acc" :label="acc" :value="acc" />
              </el-select>
            </el-form-item>

            <el-form-item label="账本" class="stagger-item" style="--i:7">
              <el-input v-model="form.book_name" placeholder="日常账本" style="width: 100%;" />
            </el-form-item>

            <el-form-item label="备注" class="stagger-item" style="--i:8">
              <el-input v-model="form.remark" placeholder="可选备注" style="width: 100%;" />
            </el-form-item>
          </div>

          <!-- 操作按钮 -->
          <div class="form-actions stagger-item" style="--i:9">
            <el-button type="primary" round :loading="saving" @click="handleSubmit" class="btn-submit">
              {{ isEdit ? '保存修改' : '添加' }}
            </el-button>
            <el-button round @click="$router.back()" class="btn-cancel">取消</el-button>
          </div>
        </el-form>
      </div>
    </div>

    <!-- 右侧面板 -->
    <div class="side-panel">
      <!-- 本月速览 -->
      <div class="side-card">
        <div class="side-card-title">本月速览</div>
        <div class="summary-row">
          <div class="summary-block">
            <span class="summary-value income">{{ summary.month.income.toFixed(0) }}</span>
            <span class="summary-label">收入</span>
          </div>
          <div class="summary-block">
            <span class="summary-value expense">{{ summary.month.expense.toFixed(0) }}</span>
            <span class="summary-label">支出</span>
          </div>
          <div class="summary-block">
            <span class="summary-value" :class="summary.month.balance >= 0 ? 'income' : 'expense'">
              {{ summary.month.balance.toFixed(0) }}
            </span>
            <span class="summary-label">结余</span>
          </div>
        </div>
      </div>

      <!-- 支出饼图 -->
      <div class="side-card">
        <div class="side-card-title">支出分布</div>
        <div ref="pieChartRef" class="pie-chart"></div>
      </div>

      <!-- 最近记录 -->
      <div class="side-card">
        <div class="side-card-title">最近记录</div>
        <div class="recent-list" v-if="recentBills.length">
          <div class="recent-item" v-for="(item, idx) in recentBills" :key="idx">
            <div class="recent-left">
              <span class="recent-category">{{ item.category }}</span>
              <span class="recent-sub">{{ item.sub_category }}</span>
            </div>
            <span class="recent-money" :class="item.type === '收入' ? 'income' : 'expense'">
              {{ item.type === '收入' ? '+' : '-' }}¥{{ Math.abs(item.money).toFixed(2) }}
            </span>
          </div>
        </div>
        <div class="recent-empty" v-else>暂无记录，记完第一笔就有了</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getMeta } from '../api/auth'
import { getBill, addBill, updateBill } from '../api/bills'
import { getSummary, getRecent, getExpensePie } from '../api/stats'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)
const pageLoading = ref(false)
const saving = ref(false)

const categories = ref({})
const accounts = ref([])
const recentBills = ref([])
const summary = reactive({
  month: { income: 0, expense: 0, balance: 0 }
})

const pieChartRef = ref(null)
let pieChart = null

const form = reactive({
  type: '支出',
  category: '支出',
  sub_category: '',
  money: 0,
  bill_date: '',
  account: '',
  book_name: '日常账本',
  refund: 0,
  remark: ''
})

const subCategories = computed(() => {
  return categories.value[form.type] || []
})

function onTypeChange() {
  form.category = form.type
  form.sub_category = ''
}

function renderPie(data) {
  if (!pieChartRef.value) return
  pieChart = echarts.init(pieChartRef.value)
  pieChart.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: ¥{c} ({d}%)' },
    color: ['#E8A987', '#D4874E', '#C0605A', '#A0876E', '#8FB0A0', '#B8C4D4', '#D4B896'],
    series: [{
      type: 'pie',
      radius: ['42%', '70%'],
      center: ['50%', '50%'],
      itemStyle: { borderRadius: 6, borderColor: '#fffdf9', borderWidth: 2 },
      label: { show: true, fontSize: 11, color: '#6b5344' },
      data: data
    }]
  })
}

onMounted(async () => {
  pageLoading.value = true
  try {
    const [metaRes, summaryRes, recentRes, pieRes] = await Promise.all([
      getMeta(),
      getSummary(),
      getRecent(),
      getExpensePie()
    ])
    categories.value = metaRes.data.categories
    accounts.value = metaRes.data.accounts
    summary.month = summaryRes.data.month
    recentBills.value = recentRes.data.slice(0, 5)
    renderPie(pieRes.data)

    if (isEdit.value) {
      const billRes = await getBill(route.params.id)
      const b = billRes.data
      form.type = b.type
      form.category = b.type
      form.sub_category = b.sub_category
      form.money = b.money
      form.bill_date = b.bill_date
      form.account = b.account
      form.book_name = b.book_name || '日常账本'
      form.refund = b.refund || 0
      form.remark = b.remark || ''
    }
  } finally {
    pageLoading.value = false
  }
})

onBeforeUnmount(() => {
  if (pieChart) pieChart.dispose()
})

async function handleSubmit() {
  if (!form.category || !form.sub_category || !form.money || !form.bill_date || !form.account) {
    ElMessage.warning('请填写完整信息')
    return
  }
  saving.value = true
  try {
    if (isEdit.value) {
      await updateBill(route.params.id, { ...form })
      ElMessage.success('修改成功')
    } else {
      await addBill({ ...form })
      ElMessage.success('添加成功')
    }
    router.push('/bills')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
/* ===== 页面双栏 ===== */
.form-page {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

/* ===== 左侧表单卡片 ===== */
.form-shell {
  flex: 1;
  min-width: 0;
  padding: 5px;
  background: rgba(180, 140, 100, 0.08);
  border-radius: 26px;
  border: 1px solid rgba(180, 140, 100, 0.12);
}

.form-core {
  background: #fffdf9;
  border-radius: 22px;
  padding: 36px 36px 30px;
  box-shadow:
    inset 0 1px 2px rgba(255, 255, 255, 0.9),
    0 8px 32px rgba(140, 90, 50, 0.06);
  position: relative;
  overflow: hidden;
}

.form-core::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 100px;
  background: linear-gradient(180deg, rgba(232, 190, 140, 0.06) 0%, transparent 100%);
  pointer-events: none;
}

/* ===== 标题 ===== */
.form-title-area {
  margin-bottom: 24px;
  position: relative;
}

.form-eyebrow {
  display: inline-block;
  font-size: 10px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  font-weight: 600;
  color: #c4956a;
  background: rgba(196, 149, 106, 0.1);
  padding: 3px 10px;
  border-radius: 20px;
  margin-bottom: 8px;
}

.form-title {
  font-size: 20px;
  font-weight: 700;
  color: #3D2B1F;
  margin: 0;
}

/* ===== 双列网格 ===== */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 20px;
}

/* ===== 交错入场 ===== */
.stagger-item {
  animation: fadeSlideUp 450ms cubic-bezier(0.32, 0.72, 0, 1) both;
  animation-delay: calc(var(--i) * 50ms);
}

@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ===== 输入框聚焦暖光 ===== */
.bill-form :deep(.el-input__wrapper),
.bill-form :deep(.el-select .el-input__wrapper),
.bill-form :deep(.el-textarea__inner) {
  border-radius: 12px;
  transition: box-shadow 200ms cubic-bezier(0.32, 0.72, 0, 1);
}

.bill-form :deep(.el-input__wrapper:focus-within),
.bill-form :deep(.el-select .el-input__wrapper.is-focus),
.bill-form :deep(.el-textarea__inner:focus) {
  box-shadow: 0 0 0 3px rgba(210, 150, 90, 0.12),
              0 2px 8px rgba(180, 120, 60, 0.08);
}

/* ===== 按钮 ===== */
.btn-submit {
  padding: 11px 30px;
  font-weight: 600;
  font-size: 14px;
  transition: transform 100ms ease-out, box-shadow 200ms cubic-bezier(0.32, 0.72, 0, 1);
  box-shadow: 0 4px 14px rgba(200, 120, 50, 0.2);
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(200, 120, 50, 0.28);
}

.btn-submit:active {
  transform: translateY(0) scale(0.97);
  box-shadow: 0 2px 6px rgba(200, 120, 50, 0.15);
}

.btn-cancel {
  padding: 11px 26px;
  transition: transform 100ms ease-out, background 200ms ease-out;
}

.btn-cancel:hover {
  transform: translateY(-1px);
  background: rgba(180, 140, 100, 0.06);
}

.btn-cancel:active {
  transform: translateY(0) scale(0.97);
}

.form-actions {
  display: flex;
  gap: 14px;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid rgba(200, 170, 130, 0.15);
}

/* ===== Element Plus 微调 ===== */
.bill-form :deep(.el-form-item) {
  margin-bottom: 16px;
}

.bill-form :deep(.el-form-item__label) {
  color: #6b5344;
  font-weight: 500;
  font-size: 12px;
  padding-bottom: 4px;
}

.bill-form :deep(.el-radio-button__inner) {
  border-radius: 20px !important;
  padding: 8px 24px;
  transition: all 200ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

.bill-form :deep(.el-radio-group) {
  gap: 8px;
}

.bill-form :deep(.el-input-number) {
  border-radius: 12px;
}

/* ===== 右侧面板 ===== */
.side-panel {
  width: 320px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
  animation: fadeSlideUp 550ms cubic-bezier(0.32, 0.72, 0, 1) 250ms both;
}

.side-card {
  background: #fffdf9;
  border-radius: 18px;
  padding: 20px;
  border: 1px solid rgba(200, 170, 130, 0.12);
  box-shadow: 0 4px 20px rgba(140, 90, 50, 0.05);
  transition: transform 300ms cubic-bezier(0.32, 0.72, 0, 1),
              box-shadow 300ms cubic-bezier(0.32, 0.72, 0, 1);
}

.side-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(140, 90, 50, 0.08);
}

.side-card-title {
  font-size: 12px;
  font-weight: 600;
  color: #8c6b52;
  margin-bottom: 14px;
  letter-spacing: 0.04em;
}

/* 本月速览 - 横排 */
.summary-row {
  display: flex;
  justify-content: space-between;
}

.summary-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.summary-value {
  font-size: 20px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}

.summary-value.income { color: #d4874e; }
.summary-value.expense { color: #c0605a; }

.summary-label {
  font-size: 11px;
  color: #a08872;
}

/* 饼图 */
.pie-chart {
  width: 100%;
  height: 200px;
}

/* 最近记录 */
.recent-list {
  display: flex;
  flex-direction: column;
}

.recent-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 9px 0;
  border-bottom: 1px solid rgba(200, 170, 130, 0.08);
}

.recent-item:last-child { border-bottom: none; }

.recent-left {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.recent-category {
  font-size: 13px;
  font-weight: 500;
  color: #4a3628;
}

.recent-sub {
  font-size: 11px;
  color: #b09a86;
}

.recent-money {
  font-size: 13px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

.recent-money.income { color: #d4874e; }
.recent-money.expense { color: #c0605a; }

.recent-empty {
  font-size: 12px;
  color: #c0aa96;
  text-align: center;
  padding: 16px 0;
}
</style>
