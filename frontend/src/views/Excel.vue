<template>
  <div>
    <div class="page-card">
      <h4 style="margin-bottom: 20px;">导出账单</h4>
      <p style="color: #8C7B6B; font-size: 13px; margin-bottom: 16px;">将当前所有账单导出为 Excel 文件</p>
      <el-button type="primary" round :loading="exporting" @click="handleExport">
        <el-icon><Download /></el-icon> 导出 Excel
      </el-button>
    </div>

    <div class="page-card">
      <h4 style="margin-bottom: 20px;">导入账单</h4>
      <p style="color: #8C7B6B; font-size: 13px; margin-bottom: 16px;">
        支持 .xlsx / .xls 格式，列名需包含：日期、收支类型、金额、类别、二级分类、账户
      </p>
      <el-upload
        ref="uploadRef"
        :auto-upload="false"
        :limit="1"
        accept=".xlsx,.xls"
        :on-change="onFileChange"
        drag
      >
        <el-icon style="font-size: 40px; color: #C4704B;"><UploadFilled /></el-icon>
        <div style="margin-top: 8px; color: #6B4E3D;">拖拽文件到此处，或点击选择</div>
      </el-upload>
      <el-button type="primary" round style="margin-top: 16px;" :loading="importing"
                 :disabled="!selectedFile" @click="handleImport">
        <el-icon><Upload /></el-icon> 开始导入
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { exportExcel, importExcel } from '../api/excel'
import { ElMessage } from 'element-plus'

const exporting = ref(false)
const importing = ref(false)
const selectedFile = ref(null)
const uploadRef = ref(null)

function onFileChange(file) {
  selectedFile.value = file.raw
}

async function handleExport() {
  exporting.value = true
  try {
    const res = await exportExcel()
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const a = document.createElement('a')
    a.href = url
    a.download = '账单.xlsx'
    a.click()
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (e) {
    ElMessage.error('导出失败')
  } finally {
    exporting.value = false
  }
}

async function handleImport() {
  if (!selectedFile.value) return
  importing.value = true
  try {
    const res = await importExcel(selectedFile.value)
    ElMessage.success(res.data.message)
    selectedFile.value = null
    uploadRef.value?.clearFiles()
  } catch (e) {
    // 错误已在拦截器处理
  } finally {
    importing.value = false
  }
}
</script>
