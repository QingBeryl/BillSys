import http from './index'

export function getBudgets(month) {
  return http.get('/budget', { params: { month } })
}

export function setBudget(data) {
  return http.post('/budget', data)
}

export function deleteBudget(data) {
  return http.delete('/budget', { data })
}

export function getBudgetUsage(month) {
  return http.get('/budget/usage', { params: { month } })
}
