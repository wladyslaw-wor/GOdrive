'use client'

import { useState } from 'react'
import { useTelegram } from '@/hooks/useTelegram'
import { useAuth } from '@/hooks/useAuth'
import TicketList from '@/components/TicketList'
import LearningMode from '@/components/LearningMode'
import TestingMode from '@/components/TestingMode'
import Statistics from '@/components/Statistics'
import Settings from '@/components/Settings'

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

interface HomePageProps {
  user: User
}

type View = 'home' | 'learning' | 'testing' | 'statistics' | 'settings'

export default function HomePage({ user }: HomePageProps) {
  const [currentView, setCurrentView] = useState<View>('home')
  const { MainButton, BackButton, HapticFeedback } = useTelegram()

  const handleViewChange = (view: View) => {
    HapticFeedback?.selectionChanged()
    setCurrentView(view)
  }

  const renderContent = () => {
    switch (currentView) {
      case 'learning':
        return <LearningMode onBack={() => handleViewChange('home')} />
      case 'testing':
        return <TestingMode onBack={() => handleViewChange('home')} />
      case 'statistics':
        return <Statistics onBack={() => handleViewChange('home')} />
      case 'settings':
        return <Settings onBack={() => handleViewChange('home')} />
      default:
        return (
          <div className="min-h-screen bg-gray-50 p-4">
            <div className="max-w-md mx-auto">
              {/* Header */}
              <div className="text-center mb-8">
                <h1 className="text-2xl font-bold text-gray-900 mb-2">
                  🎓 GOdrive
                </h1>
                <p className="text-gray-600">
                  Подготовка к экзамену ПДД Армении
                </p>
              </div>

              {/* User greeting */}
              <div className="card mb-6">
                <div className="flex items-center">
                  {user.avatar ? (
                    <img
                      src={user.avatar}
                      alt={user.display_name}
                      className="w-12 h-12 rounded-full mr-4"
                    />
                  ) : (
                    <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mr-4">
                      <span className="text-primary-600 font-semibold">
                        {user.display_name.charAt(0).toUpperCase()}
                      </span>
                    </div>
                  )}
                  <div>
                    <h2 className="font-semibold text-gray-900">
                      Привет, {user.display_name}!
                    </h2>
                    <p className="text-sm text-gray-600">
                      Готовы к изучению ПДД?
                    </p>
                  </div>
                </div>
              </div>

              {/* Menu buttons */}
              <div className="space-y-4">
                <button
                  onClick={() => handleViewChange('learning')}
                  className="w-full btn-primary text-left p-6"
                >
                  <div className="flex items-center">
                    <span className="text-2xl mr-4">📚</span>
                    <div>
                      <h3 className="font-semibold">Режим обучения</h3>
                      <p className="text-sm opacity-90">
                        Изучение билетов с объяснениями
                      </p>
                    </div>
                  </div>
                </button>

                <button
                  onClick={() => handleViewChange('testing')}
                  className="w-full btn-success text-left p-6"
                >
                  <div className="flex items-center">
                    <span className="text-2xl mr-4">🧪</span>
                    <div>
                      <h3 className="font-semibold">Режим тестирования</h3>
                      <p className="text-sm opacity-90">
                        Проверка знаний и получение сертификата
                      </p>
                    </div>
                  </div>
                </button>

                <button
                  onClick={() => handleViewChange('statistics')}
                  className="w-full btn-secondary text-left p-6"
                >
                  <div className="flex items-center">
                    <span className="text-2xl mr-4">📊</span>
                    <div>
                      <h3 className="font-semibold">Статистика</h3>
                      <p className="text-sm opacity-90">
                        Ваш прогресс и результаты
                      </p>
                    </div>
                  </div>
                </button>

                <button
                  onClick={() => handleViewChange('settings')}
                  className="w-full btn-secondary text-left p-6"
                >
                  <div className="flex items-center">
                    <span className="text-2xl mr-4">⚙️</span>
                    <div>
                      <h3 className="font-semibold">Настройки</h3>
                      <p className="text-sm opacity-90">
                        Персональные предпочтения
                      </p>
                    </div>
                  </div>
                </button>
              </div>
            </div>
          </div>
        )
    }
  }

  return (
    <>
      {currentView !== 'home' && (
        <div className="fixed top-0 left-0 right-0 z-10 bg-white border-b border-gray-200 p-4">
          <button
            onClick={() => handleViewChange('home')}
            className="flex items-center text-gray-600 hover:text-gray-900"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Назад
          </button>
        </div>
      )}
      <div className={currentView !== 'home' ? 'pt-16' : ''}>
        {renderContent()}
      </div>
    </>
  )
}

