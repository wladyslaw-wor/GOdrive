'use client'

import { useState } from 'react'
import TicketList from './TicketList'

interface Ticket {
  id: number
  number: string
  title: string
  description: string
  status: string
  questions_count: number
  user_progress?: {
    is_completed: boolean
    completed_at?: string
    attempts_count: number
    best_score: number
  }
}

interface LearningModeProps {
  onBack: () => void
}

export default function LearningMode({ onBack }: LearningModeProps) {
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null)

  if (selectedTicket) {
    return (
      <div className="min-h-screen bg-gray-50 p-4">
        <div className="max-w-md mx-auto">
          <button
            onClick={() => setSelectedTicket(null)}
            className="flex items-center text-gray-600 hover:text-gray-900 mb-4"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Назад к списку билетов
          </button>
          <h1 className="text-2xl font-bold text-gray-900 mb-6">
            Билет {selectedTicket.number}: {selectedTicket.title}
          </h1>
          <div className="card">
            <p className="text-gray-600">
              Режим обучения позволяет изучать вопросы с подробными объяснениями.
              Вы можете переключаться между вопросами и изучать их в удобном темпе.
            </p>
            <button className="btn-primary mt-4 w-full">
              Начать изучение
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="p-4">
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
          <h1 className="text-2xl font-bold text-gray-900 mb-6">Режим обучения</h1>
          <div className="card mb-6">
            <div className="flex items-center mb-4">
              <span className="text-3xl mr-4">📚</span>
              <div>
                <h3 className="font-semibold text-gray-900">Изучение билетов</h3>
                <p className="text-sm text-gray-600">
                  Выберите билет для изучения с подробными объяснениями
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <TicketList
        onTicketSelect={setSelectedTicket}
        onBack={onBack}
      />
    </div>
  )
}

