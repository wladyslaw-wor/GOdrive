'use client'

import { useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { useTelegram } from '@/hooks/useTelegram'

interface SettingsProps {
  onBack: () => void
}

export default function Settings({ onBack }: SettingsProps) {
  const { user, updateProfile } = useAuth('')
  const { HapticFeedback } = useTelegram()
  const [loading, setLoading] = useState(false)

  const handleLanguageChange = async (language: string) => {
    if (!user) return
    
    try {
      setLoading(true)
      HapticFeedback?.selectionChanged()
      await updateProfile({ language })
    } catch (error) {
      console.error('Error updating language:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleExcludePassedToggle = async () => {
    if (!user) return
    
    try {
      setLoading(true)
      HapticFeedback?.selectionChanged()
      await updateProfile({ 
        exclude_passed_tickets: !user.exclude_passed_tickets 
      })
    } catch (error) {
      console.error('Error updating setting:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-md mx-auto">
        <button
          onClick={onBack}
          className="flex items-center text-gray-600 hover:text-gray-900 mb-4"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Назад
        </button>
        
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Настройки</h1>

        <div className="space-y-4">
          {/* Language settings */}
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">Язык интерфейса</h3>
            <div className="space-y-2">
              {[
                { value: 'hy', label: 'Հայերեն' },
                { value: 'ru', label: 'Русский' },
                { value: 'en', label: 'English' },
              ].map((lang) => (
                <button
                  key={lang.value}
                  onClick={() => handleLanguageChange(lang.value)}
                  disabled={loading}
                  className={`w-full p-3 rounded-lg border text-left transition-colors ${
                    user?.language === lang.value
                      ? 'border-primary-500 bg-primary-50 text-primary-900'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  {lang.label}
                </button>
              ))}
            </div>
          </div>

          {/* Test settings */}
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">Настройки тестирования</h3>
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium text-gray-900">
                  Исключать пройденные билеты
                </h4>
                <p className="text-sm text-gray-600">
                  При выборе случайного билета исключать уже пройденные без ошибок
                </p>
              </div>
              <button
                onClick={handleExcludePassedToggle}
                disabled={loading}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  user?.exclude_passed_tickets ? 'bg-primary-600' : 'bg-gray-200'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    user?.exclude_passed_tickets ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
          </div>

          {/* Profile info */}
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">Профиль</h3>
            <div className="space-y-3">
              <div>
                <label className="text-sm font-medium text-gray-700">Имя</label>
                <p className="text-gray-900">{user?.display_name}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700">Telegram ID</label>
                <p className="text-gray-900">{user?.telegram_id}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700">Дата регистрации</label>
                <p className="text-gray-900">
                  {user?.created_at ? new Date(user.created_at).toLocaleDateString('ru-RU') : 'Неизвестно'}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

