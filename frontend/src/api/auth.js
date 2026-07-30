import http from './index'

export function login(data) {
  return http.post('/auth/login', data)
}

export function register(data) {
  return http.post('/auth/register', data)
}

export function getMe() {
  return http.get('/auth/me')
}

export function getMeta() {
  return http.get('/meta')
}
