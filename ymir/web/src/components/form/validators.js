

import t from '@/utils/t'

export const phoneValidate = (rule, value) => {
  const reg = /^\+?\d{5,18}$/
  if (value && !reg.test(value)) {
    return Promise.reject(t("signup.phone.format.msg"))
  }
  return Promise.resolve()
}

export const trimValidator = (_, value) => {
  if (value.trim().length <= 0) {
    return Promise.reject()
  }
  return Promise.resolve()
}