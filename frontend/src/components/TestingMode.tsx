'use client'

import { useState, useEffect } from 'react'
import { api } from '@/services/api'
import { useTelegram } from '@/hooks/useTelegram'
import LoadingSpinner from './LoadingSpinner'

interface TestingModeProps {
  onBack: () => void
}

export default function TestingMode({ onBack }: TestingModeProps) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { HapticFeedback } = useTelegram()

  const startRandomTest = async () => {
    try {
      setLoading(true)
      setError(null)
      HapticFeedback?.impactOccurred('medium')

      const response = await api.get('/tickets/random/')
      // Navigate to test with random ticket
      console.log('Random ticket:', response.data)
    } catch (err: any) {
      setError(err.response?.data?.message || 'Ошибка загрузки билета')
      HapticFeedback?.notificationOccurred('error')
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
        
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Режим тестирования</h1>
        
        <div className="card mb-6">
          <div className="flex items-center mb-4">
            <span className="text-3xl mr-4">🧪</span>
            <div>
              <h3 className="font-semibold text-gray-900">Тестирование знаний</h3>
              <p className="text-sm text-gray-600">
                Проверьте свои знания по ПДД Армении
              </p>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <button
            onClick={startRandomTest}
            disabled={loading}
            className="w-full btn-success p-6 text-left disabled:opacity-50"
          >
            <div className="flex items-center">
              <span className="text-2xl mr-4">🎲</span>
              <div>
                <h3 className="font-semibold">Случайный билет</h3>
                <p className="text-sm opacity-90">
                  {loading ? 'Загрузка...' : 'Начать тест со случайным билетом'}
                </p>
              </div>
            </div>
          </button>

          {loading && (
            <div className="flex justify-center">
              <LoadingSpinner />
            </div>
          )}

          {error && (
            <div className="card bg-error-50 border border-error-200">
              <div className="flex items-center">
                <svg className="w-5 h-5 text-error-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
                <p className="text-error-700">{error}</p>
              </div>
            </div>
          )}

          <div className="card bg-blue-50 border border-blue-200">
            <h4 className="font-semibold text-blue-900 mb-2">Как работает тестирование:</h4>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Вам будет предложен случайный билет</li>
              <li>• Ответьте на все вопросы билета</li>
              <li>• В конце увидите результат и объяснения</li>
              <li>• При 100% правильных ответов билет считается пройденным</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

