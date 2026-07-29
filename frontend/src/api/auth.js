import http from './index'

export function login(data) {
  return http.post('/auth/login', data)
}

export function getMe() {
  return http.get('/auth/me')
}

export function getMeta() {
  return http.get('/meta')
}
