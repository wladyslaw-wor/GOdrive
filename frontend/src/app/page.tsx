'use client'

import { useEffect, useState } from 'react'
import { useTelegram } from '@/hooks/useTelegram'
import { useAuth } from '@/hooks/useAuth'
import HomePage from '@/components/HomePage'
import LoadingSpinner from '@/components/LoadingSpinner'
import ErrorMessage from '@/components/ErrorMessage'

export default function Home() {
  const { initData, isWebApp } = useTelegram()
  const { user, loading, error } = useAuth(initData)
  const [isInitialized, setIsInitialized] = useState(false)

  useEffect(() => {
    if (isWebApp && initData) {
      setIsInitialized(true)
    }
  }, [isWebApp, initData])

  if (!isWebApp) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            GOdrive - Подготовка к экзамену ПДД
          </h1>
          <p className="text-gray-600">
            Это приложение работает только в Telegram WebApp
          </p>
        </div>
      </div>
    )
  }

  if (!isInitialized) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <LoadingSpinner />
      </div>
    )
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <LoadingSpinner />
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <ErrorMessage message={error} />
      </div>
    )
  }

  return <HomePage user={user} />
}

