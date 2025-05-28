import { defineStore } from 'pinia'
import { getUserProfile } from '@/api/auth.js'

export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: {
      id: null,
      username: '',
      nickname: '',
      avatar: '',
      gender: '',
      phone: '',
      email: '',
      default_pickup_address: '',
      default_delivery_address: '',
      status: '',
      created_at: null,
      last_login: null
    },
    isLoggedIn: false
  }),

  getters: {
    displayName: (state) => state.userInfo.nickname || state.userInfo.username || '未知用户',
    avatarUrl: (state) => state.userInfo.avatar || './images/ProfilePortrait.jpg',
    hasCompleteProfile: (state) => {
      return !!(state.userInfo.nickname && (state.userInfo.phone || state.userInfo.email))
    }
  },

  actions: {
    setUserInfo(userInfo) {
      this.userInfo = { ...this.userInfo, ...userInfo }
      this.isLoggedIn = true
      // 同步到localStorage
      localStorage.setItem('userInfo', JSON.stringify(this.userInfo))
    },

    async fetchUserInfo() {
      try {
        const response = await getUserProfile()
        if (response.code === 200) {
          this.setUserInfo(response.data.user)
          return response.data.user
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
        throw error
      }
    },

    updateUserInfo(updates) {
      this.userInfo = { ...this.userInfo, ...updates }
      localStorage.setItem('userInfo', JSON.stringify(this.userInfo))
    },

    logout() {
      this.userInfo = {
        id: null,
        username: '',
        nickname: '',
        avatar: '',
        gender: '',
        phone: '',
        email: '',
        default_pickup_address: '',
        default_delivery_address: '',
        status: '',
        created_at: null,
        last_login: null
      }
      this.isLoggedIn = false
      localStorage.removeItem('userInfo')
      localStorage.removeItem('authToken')
    },

    initFromStorage() {
      const token = localStorage.getItem('authToken')
      const userInfo = localStorage.getItem('userInfo')
      
      if (token && userInfo) {
        try {
          this.userInfo = JSON.parse(userInfo)
          this.isLoggedIn = true
        } catch (error) {
          console.error('解析用户信息失败:', error)
          this.logout()
        }
      }
    }
  }
})