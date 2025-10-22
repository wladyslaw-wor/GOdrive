'use client'

import { useState, useEffect } from 'react'
import { api } from '@/services/api'
import LoadingSpinner from './LoadingSpinner'

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

interface TicketListProps {
  onTicketSelect: (ticket: Ticket) => void
  onBack: () => void
}

export default function TicketList({ onTicketSelect, onBack }: TicketListProps) {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchTickets()
  }, [])

  const fetchTickets = async () => {
    try {
      setLoading(true)
      const response = await api.get('/tickets/')
      setTickets(response.data.results || response.data)
    } catch (err: any) {
      setError(err.response?.data?.message || 'Ошибка загрузки билетов')
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
          <div className="card">
            <div className="text-center">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Ошибка</h3>
              <p className="text-gray-600 mb-4">{error}</p>
              <button onClick={fetchTickets} className="btn-primary">
                Попробовать снова
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-md mx-auto">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={onBack}
            className="flex items-center text-gray-600 hover:text-gray-900 mb-4"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Назад
          </button>
          <h1 className="text-2xl font-bold text-gray-900">Выберите билет</h1>
        </div>

        {/* Tickets list */}
        <div className="space-y-4">
          {tickets.map((ticket) => (
            <div
              key={ticket.id}
              onClick={() => onTicketSelect(ticket)}
              className="card cursor-pointer hover:shadow-lg transition-shadow"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900">
                    Билет {ticket.number}
                  </h3>
                  <p className="text-gray-600 text-sm mt-1">
                    {ticket.title}
                  </p>
                  <p className="text-gray-500 text-xs mt-2">
                    {ticket.questions_count} вопросов
                  </p>
                </div>
                <div className="flex items-center">
                  {ticket.user_progress?.is_completed ? (
                    <div className="flex items-center text-success-600">
                      <svg className="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                      <span className="text-sm font-medium">Пройден</span>
                    </div>
                  ) : (
                    <div className="text-gray-400">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                  )}
                </div>
              </div>
              
              {ticket.user_progress && (
                <div className="mt-3 pt-3 border-t border-gray-200">
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>Попыток: {ticket.user_progress.attempts_count}</span>
                    <span>Лучший результат: {ticket.user_progress.best_score}%</span>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

