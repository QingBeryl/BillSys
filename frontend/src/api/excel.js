import http from './index'

export function exportExcel() {
  return http.get('/excel/export', { responseType: 'blob' })
}

export function importExcel(file) {
  const formData = new FormData()
  formData.append('file', file)
  return http.post('/excel/import', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}
