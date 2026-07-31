<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <div class="stat-cards">
      <div class="stat-group" v-for="group in statGroups" :key="group.label">
        <div class="group-label">{{ group.label }}</div>
        <div class="group-items">
          <div class="stat-item income">
            <span class="stat-label">收入</span>
            <span class="stat-value">¥{{ group.data.income.toFixed(2) }}</span>
          </div>
          <div class="stat-item expense">
            <span class="stat-label">支出</span>
            <span class="stat-value">¥{{ group.data.expense.toFixed(2) }}</span>
          </div>
          <div class="stat-item balance">
            <span class="stat-label">结余</span>
            <span class="stat-value">¥{{ group.data.balance.toFixed(2) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="charts-grid">
      <div class="chart-card">
        <h4>近12月收支趋势</h4>
        <div ref="chart12month" class="chart-box"></div>
      </div>
      <div class="chart-card">
        <h4>支出分类</h4>
        <div ref="chartExpPie" class="chart-box"></div>
      </div>
      <div class="chart-card">
        <h4>收入分类</h4>
        <div ref="chartIncPie" class="chart-box"></div>
      </div>
      <div class="chart-card">
        <h4>支出 Top5</h4>
        <div ref="chartTop5" class="chart-box"></div>
      </div>
      <div class="chart-card">
        <h4>近7天收支</h4>
        <div ref="chart7day" class="chart-box"></div>
      </div>
      <div class="chart-card">
        <h4>结余趋势</h4>
        <div ref="chartBalance" class="chart-box"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import * as echarts from 'echarts'
import { getSummary, get12Month, getExpensePie, getIncomePie, getTop5, get7Day, getBalanceTrend } from '../api/stats'

const summary = ref({ month: { income: 0, expense: 0, balance: 0 }, year: { income: 0, expense: 0, balance: 0 }, all: { income: 0, expense: 0, balance: 0 } })

const statGroups = computed(() => [
  { label: '本月', data: summary.value.month },
  { label: '本年', data: summary.value.year },
  { label: '总计', data: summary.value.all }
])

// 图表DOM引用
const chart12month = ref(null)
const chartExpPie = ref(null)
const chartIncPie = ref(null)
const chartTop5 = ref(null)
const chart7day = ref(null)
const chartBalance = ref(null)

let charts = []

function initChart(dom, option) {
  const chart = echarts.init(dom)
  chart.setOption(option)
  charts.push(chart)
  return chart
}

// 空数据提示组件
const noDataGraphic = {
  type: 'group',
  left: 'center',
  top: 'middle',
  children: [
    { type: 'text', style: { text: '暂无数据', fontSize: 14, fill: '#B8A99A', textAlign: 'center' } }
  ]
}

async function loadCharts() {
  const [res12, resExp, resInc, resTop, res7, resBal] = await Promise.all([
    get12Month(), getExpensePie(), getIncomePie(), getTop5(), get7Day(), getBalanceTrend()
  ])

  // 12月趋势（始终有12个月的数据，无需判空）
  const d12 = res12.data
  initChart(chart12month.value, {
    tooltip: { trigger: 'axis' },
    legend: { data: ['收入', '支出'] },
    xAxis: { type: 'category', data: d12.map(i => i.month) },
    yAxis: { type: 'value' },
    series: [
      { name: '收入', type: 'line', data: d12.map(i => i.income), smooth: true, itemStyle: { color: '#E6A23C' } },
      { name: '支出', type: 'line', data: d12.map(i => i.expense), smooth: true, itemStyle: { color: '#C4704B' } }
    ]
  })

  // 支出饼图
  const expData = resExp.data
  initChart(chartExpPie.value, {
    tooltip: { trigger: 'item', formatter: '{b}: ¥{c} ({d}%)' },
    graphic: expData.length ? [] : [noDataGraphic],
    series: [{ type: 'pie', radius: ['40%', '70%'], data: expData, emphasis: { itemStyle: { shadowBlur: 10 } } }]
  })

  // 收入饼图
  const incData = resInc.data
  initChart(chartIncPie.value, {
    tooltip: { trigger: 'item', formatter: '{b}: ¥{c} ({d}%)' },
    graphic: incData.length ? [] : [noDataGraphic],
    series: [{ type: 'pie', radius: ['40%', '70%'], data: incData, emphasis: { itemStyle: { shadowBlur: 10 } } }]
  })

  // Top5 横向柱状
  const top5Data = resTop.data
  initChart(chartTop5.value, {
    tooltip: { trigger: 'axis' },
    graphic: top5Data.length ? [] : [noDataGraphic],
    xAxis: { type: 'value' },
    yAxis: { type: 'category', data: top5Data.map(i => i.name).reverse() },
    series: [{ type: 'bar', data: top5Data.map(i => i.value).reverse(), itemStyle: { color: '#C4704B', borderRadius: [0, 6, 6, 0] } }]
  })

  // 7天收支（始终有7天数据，无需判空）
  const d7 = res7.data
  initChart(chart7day.value, {
    tooltip: { trigger: 'axis' },
    legend: { data: ['收入', '支出'] },
    xAxis: { type: 'category', data: d7.map(i => i.day) },
    yAxis: { type: 'value' },
    series: [
      { name: '收入', type: 'line', data: d7.map(i => i.income), smooth: true, itemStyle: { color: '#E6A23C' } },
      { name: '支出', type: 'line', data: d7.map(i => i.expense), smooth: true, itemStyle: { color: '#C4704B' } }
    ]
  })

  // 结余趋势
  const bal = resBal.data
  initChart(chartBalance.value, {
    tooltip: { trigger: 'axis' },
    graphic: bal.length ? [] : [noDataGraphic],
    xAxis: { type: 'category', data: bal.map(i => i.day) },
    yAxis: { type: 'value' },
    series: [{
      type: 'line', data: bal.map(i => i.balance), smooth: true,
      areaStyle: { color: 'rgba(196,112,75,0.15)' },
      itemStyle: { color: '#C4704B' }
    }]
  })
}

function handleResize() {
  charts.forEach(c => c.resize())
}

onMounted(async () => {
  try {
    const sumRes = await getSummary()
    summary.value = sumRes.data
    await loadCharts()
    window.addEventListener('resize', handleResize)
  } catch (e) {
    console.error('加载仪表盘数据失败', e)
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  charts.forEach(c => c.dispose())
  charts = []
})
</script>

<style scoped>
.stat-cards {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
}

.stat-group {
  flex: 1;
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(140, 90, 50, 0.08);
}

.group-label {
  font-size: 13px;
  color: #8C7B6B;
  margin-bottom: 12px;
  font-weight: 600;
}

.group-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-label {
  font-size: 13px;
  color: #6B4E3D;
}

.stat-value {
  font-size: 15px;
  font-weight: 700;
}

.stat-item.income .stat-value { color: #E6A23C; }
.stat-item.expense .stat-value { color: #C4704B; }
.stat-item.balance .stat-value { color: #67C23A; }

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.chart-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(140, 90, 50, 0.08);
}

.chart-card h4 {
  margin-bottom: 12px;
  color: #3D2B1F;
  font-size: 15px;
}

.chart-box {
  height: 280px;
}
</style>
