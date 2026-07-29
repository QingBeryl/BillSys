<template>
  <div class="page-card form-card">
    <h4 style="margin-bottom: 24px;">{{ isEdit ? '编辑账单' : '记一笔' }}</h4>
    <el-form :model="form" label-width="90px" label-position="right" v-loading="pageLoading">
      <el-form-item label="类型">
        <el-radio-group v-model="form.type" size="large">
          <el-radio-button value="支出">支出</el-radio-button>
          <el-radio-button value="收入">收入</el-radio-button>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="分类">
        <el-select v-model="form.category" placeholder="选择分类" @change="onCategoryChange" style="width: 220px;">
          <el-option v-for="cat in categoryKeys" :key="cat" :label="cat" :value="cat" />
        </el-select>
      </el-form-item>

      <el-form-item label="子分类">
        <el-select v-model="form.sub_category" placeholder="选择子分类" style="width: 220px;">
          <el-option v-for="sub in subCategories" :key="sub" :label="sub" :value="sub" />
        </el-select>
      </el-form-item>

      <el-form-item label="金额">
        <el-input-number v-model="form.money" :precision="2" :step="1" :min="0" style="width: 220px;" />
      </el-form-item>

      <el-form-item label="日期">
        <el-date-picker v-model="form.bill_date" type="datetime" placeholder="选择日期"
                        value-format="YYYY-MM-DD HH:mm:ss" style="width: 220px;" />
      </el-form-item>

      <el-form-item label="账户">
        <el-select v-model="form.account" placeholder="选择账户" style="width: 220px;">
          <el-option v-for="acc in accounts" :key="acc" :label="acc" :value="acc" />
        </el-select>
      </el-form-item>

      <el-form-item label="账本">
        <el-input v-model="form.book_name" placeholder="日常账本" style="width: 220px;" />
      </el-form-item>

      <el-form-item label="退款">
        <el-input-number v-model="form.refund" :precision="2" :min="0" style="width: 220px;" />
      </el-form-item>

      <el-form-item label="备注">
        <el-input v-model="form.remark" type="textarea" :rows="3" placeholder="可选备注" style="width: 400px;" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" round :loading="saving" @click="handleSubmit">
          {{ isEdit ? '保存修改' : '添加' }}
        </el-button>
        <el-button round @click="$router.back()">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getMeta } from '../api/auth'
import { getBill, addBill, updateBill } from '../api/bills'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)
const pageLoading = ref(false)
const saving = ref(false)

const categories = ref({})
const accounts = ref([])

const form = reactive({
  type: '支出',
  category: '',
  sub_category: '',
  money: 0,
  bill_date: '',
  account: '',
  book_name: '日常账本',
  refund: 0,
  remark: ''
})

const categoryKeys = computed(() => Object.keys(categories.value))

const subCategories = computed(() => {
  return categories.value[form.category] || []
})

function onCategoryChange() {
  form.sub_category = ''
}

onMounted(async () => {
  pageLoading.value = true
  try {
    const metaRes = await getMeta()
    categories.value = metaRes.data.categories
    accounts.value = metaRes.data.accounts

    if (isEdit.value) {
      const billRes = await getBill(route.params.id)
      const b = billRes.data
      form.type = b.type
      form.category = b.category
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
.form-card {
  max-width: 700px;
}
</style>
