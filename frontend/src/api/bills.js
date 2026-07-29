import http from './index'

export function getBills() {
  return http.get('/bills')
}

export function getBill(id) {
  return http.get(`/bills/${id}`)
}

export function addBill(data) {
  return http.post('/bills', data)
}

export function updateBill(id, data) {
  return http.put(`/bills/${id}`, data)
}

export function deleteBill(id) {
  return http.delete(`/bills/${id}`)
}

export function queryBills(data) {
  return http.post('/bills/query', data)
}
