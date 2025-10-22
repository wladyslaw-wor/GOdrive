import { useState, useEffect } from 'react'
import { api } from '@/services/api'

interface User {
  id: number
  telegram_id: number
  telegram_username: string
  telegram_first_name: string
  telegram_last_name: string
  full_name: string
  display_name: string
  language: string
  exclude_passed_tickets: boolean
  avatar?: string
  phone?: string
  is_verified: boolean
  is_active: boolean
  created_at: string
  last_activity?: string
}

export const useAuth = (initData: string) => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!initData) {
      setLoading(false)
      return
    }

    const authenticate = async () => {
      try {
        setLoading(true)
        setError(null)

        // Set authorization header
        api.defaults.headers['X-Telegram-Init-Data'] = initData

        // Get user profile
        const response = await api.get('/auth/profile/')
        setUser(response.data)
      } catch (err: any) {
        console.error('Authentication error:', err)
        setError(err.response?.data?.message || 'Ошибка аутентификации')
      } finally {
        setLoading(false)
      }
    }

    authenticate()
  }, [initData])

  const updateProfile = async (data: Partial<User>) => {
    try {
      const response = await api.patch('/auth/profile/', data)
      setUser(response.data)
      return response.data
    } catch (err: any) {
      console.error('Profile update error:', err)
      throw err
    }
  }

  const updateActivity = async () => {
    try {
      await api.post('/auth/activity/')
    } catch (err) {
      console.error('Activity update error:', err)
    }
  }

  return {
    user,
    loading,
    error,
    updateProfile,
    updateActivity,
  }
}

