<template>
  <div>
    <!-- 报表生成 -->
    <div class="page-card">
      <h4 style="margin-bottom: 20px;">生成报表</h4>
      <p style="color: #8C7B6B; font-size: 13px; margin-bottom: 16px;">
        自动生成月度/年度报表，包含收支总览、分类占比、环比变化和账单明细
      </p>
      <div class="report-controls">
        <el-radio-group v-model="reportType" size="default">
          <el-radio-button value="month">月度报表</el-radio-button>
          <el-radio-button value="year">年度报表</el-radio-button>
        </el-radio-group>
        <el-date-picker
          v-if="reportType === 'month'"
          v-model="reportMonth"
          type="month"
          placeholder="选择月份"
          value-format="YYYY-MM"
          style="width: 160px;"
        />
        <el-date-picker
          v-else
          v-model="reportYear"
          type="year"
          placeholder="选择年份"
          value-format="YYYY"
          style="width: 160px;"
        />
        <el-button type="primary" round :loading="reporting" @click="handleReport">
          <el-icon><DataAnalysis /></el-icon> 生成报表
        </el-button>
      </div>
    </div>

    <!-- 导出账单 -->
    <div class="page-card">
      <h4 style="margin-bottom: 20px;">导出账单</h4>
      <p style="color: #8C7B6B; font-size: 13px; margin-bottom: 16px;">将当前所有账单导出为 Excel 文件</p>
      <el-button type="primary" round :loading="exporting" @click="handleExport">
        <el-icon><Download /></el-icon> 导出 Excel
      </el-button>
    </div>

    <!-- 导入账单 -->
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
import { exportExcel, importExcel, generateReport } from '../api/excel'
import { ElMessage } from 'element-plus'

const exporting = ref(false)
const importing = ref(false)
const reporting = ref(false)
const selectedFile = ref(null)
const uploadRef = ref(null)

const reportType = ref('month')
const reportMonth = ref(new Date().toISOString().slice(0, 7))
const reportYear = ref(new Date().toISOString().slice(0, 4))

function onFileChange(file) {
  selectedFile.value = file.raw
}

function downloadBlob(data, filename) {
  const url = window.URL.createObjectURL(new Blob([data]))
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  window.URL.revokeObjectURL(url)
}

async function handleReport() {
  const period = reportType.value === 'month' ? reportMonth.value : reportYear.value
  if (!period) {
    ElMessage.warning('请选择时间段')
    return
  }
  reporting.value = true
  try {
    const res = await generateReport(reportType.value, period)
    downloadBlob(res.data, `报表_${period}.xlsx`)
    ElMessage.success('报表生成成功')
  } catch (e) {
    ElMessage.error('报表生成失败')
  } finally {
    reporting.value = false
  }
}

async function handleExport() {
  exporting.value = true
  try {
    const res = await exportExcel()
    downloadBlob(res.data, '账单.xlsx')
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

<style scoped>
.report-controls {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
}
</style>
