import http from './index'

export function doTransfer(data) {
  return http.post('/transfer', data)
}
