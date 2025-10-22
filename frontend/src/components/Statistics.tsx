'use client'

import { useState, useEffect } from 'react'
import { api } from '@/services/api'
import LoadingSpinner from './LoadingSpinner'

interface Statistics {
  total_attempts: number
  total_questions_answered: number
  total_correct_answers: number
  average_score: number
  completed_tickets_count: number
  total_time_spent_seconds: number
  total_time_formatted: string
  last_attempt_at?: string
}

interface StatisticsProps {
  onBack: () => void
}

export default function Statistics({ onBack }: StatisticsProps) {
  const [stats, setStats] = useState<Statistics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchStatistics()
  }, [])

  const fetchStatistics = async () => {
    try {
      setLoading(true)
      const response = await api.get('/attempts/statistics/')
      setStats(response.data)
    } catch (err: any) {
      setError(err.response?.data?.message || 'Ошибка загрузки статистики')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <LoadingSpinner />
      </div>
    )
  }

  if (error) {
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
          <div className="card">
            <div className="text-center">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Ошибка</h3>
              <p className="text-gray-600 mb-4">{error}</p>
              <button onClick={fetchStatistics} className="btn-primary">
                Попробовать снова
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  const accuracy = stats ? Math.round(stats.average_score) : 0

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
        
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Статистика</h1>

        {stats ? (
          <div className="space-y-4">
            {/* Overall stats */}
            <div className="card">
              <h3 className="font-semibold text-gray-900 mb-4">Общая статистика</h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary-600">
                    {stats.total_attempts}
                  </div>
                  <div className="text-sm text-gray-600">Попыток</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-success-600">
                    {stats.completed_tickets_count}
                  </div>
                  <div className="text-sm text-gray-600">Пройдено билетов</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    {stats.total_questions_answered}
                  </div>
                  <div className="text-sm text-gray-600">Отвечено вопросов</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">
                    {accuracy}%
                  </div>
                  <div className="text-sm text-gray-600">Точность</div>
                </div>
              </div>
            </div>

            {/* Performance stats */}
            <div className="card">
              <h3 className="font-semibold text-gray-900 mb-4">Производительность</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Правильных ответов:</span>
                  <span className="font-semibold">
                    {stats.total_correct_answers} / {stats.total_questions_answered}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Средний балл:</span>
                  <span className="font-semibold">{accuracy}%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Время обучения:</span>
                  <span className="font-semibold">{stats.total_time_formatted}</span>
                </div>
              </div>
            </div>

            {/* Last activity */}
            {stats.last_attempt_at && (
              <div className="card">
                <h3 className="font-semibold text-gray-900 mb-2">Последняя активность</h3>
                <p className="text-gray-600 text-sm">
                  {new Date(stats.last_attempt_at).toLocaleDateString('ru-RU', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </p>
              </div>
            )}

            {/* Progress indicator */}
            <div className="card">
              <h3 className="font-semibold text-gray-900 mb-4">Ваш прогресс</h3>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Точность ответов</span>
                  <span>{accuracy}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${Math.min(accuracy, 100)}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="card text-center">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Статистика недоступна
            </h3>
            <p className="text-gray-600">
              Начните проходить тесты, чтобы увидеть свою статистику
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

