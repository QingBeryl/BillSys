<template>
  <div class="page-card transfer-card">
    <h4 style="margin-bottom: 24px;">账户转账</h4>
    <el-form :model="form" label-width="100px">
      <el-form-item label="转出账户">
        <el-select v-model="form.out_account" placeholder="选择转出账户" style="width: 220px;">
          <el-option v-for="acc in accounts" :key="acc" :label="acc" :value="acc" />
        </el-select>
      </el-form-item>

      <el-form-item label="转入账户">
        <el-select v-model="form.in_account" placeholder="选择转入账户" style="width: 220px;">
          <el-option v-for="acc in accounts" :key="acc" :label="acc" :value="acc" />
        </el-select>
      </el-form-item>

      <el-form-item label="金额">
        <el-input-number v-model="form.money" :precision="2" :step="10" :min="0.01" style="width: 220px;" />
      </el-form-item>

      <el-form-item label="日期">
        <el-date-picker v-model="form.date" type="date" value-format="YYYY-MM-DD" placeholder="选择日期" style="width: 220px;" />
      </el-form-item>

      <el-form-item label="备注">
        <el-input v-model="form.remark" placeholder="可选" style="width: 300px;" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" round :loading="submitting" @click="handleTransfer">确认转账</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getMeta } from '../api/auth'
import { doTransfer } from '../api/transfer'
import { ElMessage } from 'element-plus'

const accounts = ref([])
const submitting = ref(false)

const form = reactive({
  out_account: '',
  in_account: '',
  money: 0,
  date: '',
  remark: ''
})

onMounted(async () => {
  const res = await getMeta()
  accounts.value = res.data.accounts
})

async function handleTransfer() {
  if (!form.out_account || !form.in_account || !form.money || !form.date) {
    ElMessage.warning('请填写完整信息')
    return
  }
  if (form.out_account === form.in_account) {
    ElMessage.warning('转出和转入账户不能相同')
    return
  }
  submitting.value = true
  try {
    await doTransfer({ ...form })
    ElMessage.success('转账成功')
    Object.assign(form, { out_account: '', in_account: '', money: 0, date: '', remark: '' })
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.transfer-card {
  max-width: 600px;
}
</style>
