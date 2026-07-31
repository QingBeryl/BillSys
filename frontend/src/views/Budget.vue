<template>
  <div class="budget-page">
    <!-- 月份选择 -->
    <div class="page-card">
      <div class="budget-header">
        <h4>预算与限额</h4>
        <el-date-picker
          v-model="currentMonth"
          type="month"
          placeholder="选择月份"
          value-format="YYYY-MM"
          style="width: 160px;"
          @change="loadData"
        />
      </div>

      <!-- 总预算 -->
      <div class="budget-section">
        <div class="section-title">月度总预算</div>
        <div class="total-budget-card" v-if="usage.total">
          <div class="budget-info">
            <span class="budget-amount">¥{{ usage.total.budget.toFixed(2) }}</span>
            <span class="budget-spent" :class="{ over: usage.total.remaining < 0 }">
              已花 ¥{{ usage.total.spent.toFixed(2) }}
              <template v-if="usage.total.remaining < 0"> (超支 ¥{{ Math.abs(usage.total.remaining).toFixed(2) }})</template>
              <template v-else> (剩余 ¥{{ usage.total.remaining.toFixed(2) }})</template>
            </span>
          </div>
          <el-progress
            :percentage="Math.min(usage.total.percent, 100)"
            :color="usage.total.percent > 90 ? '#F56C6C' : usage.total.percent > 70 ? '#E6A23C' : '#67C23A'"
            :stroke-width="12"
            style="margin-top: 12px;"
          />
          <div class="budget-actions">
            <el-button link type="primary" size="small" @click="openEdit('total')">修改</el-button>
            <el-button link type="danger" size="small" @click="handleDelete('total')">删除</el-button>
          </div>
        </div>
        <div class="empty-tip" v-else>
          <span>尚未设置总预算</span>
          <el-button type="primary" size="small" round @click="openEdit('total')">设置总预算</el-button>
        </div>
      </div>

      <!-- 分类预算 -->
      <div class="budget-section">
        <div class="section-title">
          分类预算
          <el-button type="primary" size="small" round @click="openEdit('')">+ 添加分类预算</el-button>
        </div>
        <div class="category-list" v-if="usage.categories && usage.categories.length">
          <div class="category-item" v-for="item in usage.categories" :key="item.category">
            <div class="cat-header">
              <span class="cat-name">{{ item.category }}</span>
              <span class="cat-numbers">
                ¥{{ item.spent.toFixed(2) }} / ¥{{ item.budget.toFixed(2) }}
                <span v-if="item.remaining < 0" class="over-text">超支</span>
              </span>
            </div>
            <el-progress
              :percentage="Math.min(item.percent, 100)"
              :color="item.percent > 90 ? '#F56C6C' : item.percent > 70 ? '#E6A23C' : '#67C23A'"
              :stroke-width="8"
              :show-text="false"
            />
            <div class="budget-actions">
              <el-button link type="primary" size="small" @click="openEdit(item.category)">修改</el-button>
              <el-button link type="danger" size="small" @click="handleDelete(item.category)">删除</el-button>
            </div>
          </div>
        </div>
        <div class="empty-tip" v-else>
          <span>暂无分类预算，点击上方按钮添加</span>
        </div>
      </div>
    </div>

    <!-- 编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="380px">
      <el-form label-position="top">
        <el-form-item label="分类" v-if="editingCategory !== 'total'">
          <el-select v-model="editForm.category" placeholder="选择分类" style="width: 100%;">
            <el-option v-for="cat in categoryOptions" :key="cat" :label="cat" :value="cat" />
          </el-select>
        </el-form-item>
        <el-form-item label="预算金额">
          <el-input-number v-model="editForm.amount" :precision="2" :step="100" :min="0" style="width: 100%;" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button round @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" round :loading="saving" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getBudgetUsage, setBudget, deleteBudget } from '../api/budget'
import { getMeta } from '../api/auth'
import { ElMessage, ElMessageBox } from 'element-plus'

const currentMonth = ref(new Date().toISOString().slice(0, 7))
const usage = ref({ total: null, categories: [] })
const categoryOptions = ref([])

const dialogVisible = ref(false)
const dialogTitle = ref('')
const editingCategory = ref('')
const saving = ref(false)
const editForm = reactive({ category: '', amount: 0 })

function openEdit(category) {
  editingCategory.value = category
  if (category === 'total') {
    dialogTitle.value = '设置月度总预算'
    editForm.category = 'total'
    editForm.amount = usage.value.total ? usage.value.total.budget : 0
  } else if (category) {
    dialogTitle.value = `修改「${category}」预算`
    editForm.category = category
    const found = usage.value.categories.find(c => c.category === category)
    editForm.amount = found ? found.budget : 0
  } else {
    dialogTitle.value = '添加分类预算'
    editForm.category = ''
    editForm.amount = 0
  }
  dialogVisible.value = true
}

async function handleSave() {
  if (editingCategory.value !== 'total' && !editForm.category) {
    ElMessage.warning('请选择分类')
    return
  }
  if (!editForm.amount || editForm.amount <= 0) {
    ElMessage.warning('请输入有效金额')
    return
  }
  saving.value = true
  try {
    await setBudget({
      month: currentMonth.value,
      category: editingCategory.value === 'total' ? 'total' : editForm.category,
      amount: editForm.amount
    })
    ElMessage.success('保存成功')
    dialogVisible.value = false
    loadData()
  } finally {
    saving.value = false
  }
}

async function handleDelete(category) {
  await ElMessageBox.confirm(`确定删除「${category === 'total' ? '总预算' : category}」的预算设置？`, '提示')
  await deleteBudget({ month: currentMonth.value, category })
  ElMessage.success('已删除')
  loadData()
}

async function loadData() {
  const res = await getBudgetUsage(currentMonth.value)
  usage.value = res.data
}

onMounted(async () => {
  const metaRes = await getMeta()
  const cats = metaRes.data.categories
  categoryOptions.value = cats['支出'] || []
  loadData()
})
</script>

<style scoped>
.budget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.budget-header h4 {
  font-size: 16px;
  color: #3D2B1F;
}

.budget-section {
  margin-bottom: 28px;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #6B4E3D;
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.total-budget-card {
  background: #faf6f1;
  border-radius: 12px;
  padding: 20px;
}

.budget-info {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.budget-amount {
  font-size: 22px;
  font-weight: 700;
  color: #3D2B1F;
}

.budget-spent {
  font-size: 13px;
  color: #67C23A;
}

.budget-spent.over {
  color: #F56C6C;
}

.budget-actions {
  margin-top: 10px;
  display: flex;
  gap: 8px;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.category-item {
  background: #faf6f1;
  border-radius: 12px;
  padding: 16px 20px;
}

.cat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.cat-name {
  font-size: 14px;
  font-weight: 600;
  color: #3D2B1F;
}

.cat-numbers {
  font-size: 13px;
  color: #8C7B6B;
}

.over-text {
  color: #F56C6C;
  font-weight: 600;
  margin-left: 6px;
}

.empty-tip {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #B8A99A;
  font-size: 13px;
  padding: 16px 0;
}
</style>
