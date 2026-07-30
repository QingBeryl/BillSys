import http from './index'

export function getSummary() {
  return http.get('/stats/summary')
}

export function get12Month() {
  return http.get('/stats/12month')
}

export function getExpensePie() {
  return http.get('/stats/expense-pie')
}

export function getIncomePie() {
  return http.get('/stats/income-pie')
}

export function getTop5() {
  return http.get('/stats/top5')
}

export function get7Day() {
  return http.get('/stats/7day')
}

export function getBalanceTrend() {
  return http.get('/stats/balance-trend')
}

export function getRecent() {
  return http.get('/stats/recent')
}
