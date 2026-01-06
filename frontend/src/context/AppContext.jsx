import React, { createContext, useState, useCallback } from 'react'

export const AppContext = createContext()

export const AppProvider = ({ children }) => {
  // User
  const [userGoals, setUserGoals] = useState({
    daily_calories: 2000,
    daily_protein_g: 150,
    daily_carbs_g: 200,
    daily_fat_g: 65,
  })

  // Dishes
  const [allDishes, setAllDishes] = useState([])
  const [currentDish, setCurrentDish] = useState(null)

  // Prediction
  const [topPrediction, setTopPrediction] = useState(null)
  const [predictions, setPredictions] = useState([])

  // Logs
  const [todayLogs, setTodayLogs] = useState([])
  const [dailyTotals, setDailyTotals] = useState({
    calories: 0,
    protein_g: 0,
    carbs_g: 0,
    fat_g: 0,
  })
  const [dailyProgress, setDailyProgress] = useState({
    calories: 0,
    protein: 0,
    carbs: 0,
    fat: 0,
  })

  // UI
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)

  // Actions
  const fetchUserGoals = useCallback(async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/user/goals')
      const data = await response.json()
      setUserGoals(data)
      setError(null)
    } catch (err) {
      setError('Failed to fetch goals')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }, [])

  const updateUserGoals = useCallback(async (goals) => {
    setLoading(true)
    try {
      const response = await fetch('/api/user/goals', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(goals),
      })
      const data = await response.json()
      if (data.success) {
        setUserGoals(goals)
        setSuccess('Goals updated!')
        setError(null)
      }
    } catch (err) {
      setError('Failed to update goals')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }, [])

  const fetchAllDishes = useCallback(async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/dishes/all')
      const data = await response.json()
      setAllDishes(data.dishes || [])
      setError(null)
    } catch (err) {
      setError('Failed to fetch dishes')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }, [])

  const fetchDishDetails = useCallback(async (dishId) => {
    setLoading(true)
    try {
      const response = await fetch(`/api/dishes/${dishId}`)
      const data = await response.json()
      setCurrentDish(data)
      setError(null)
    } catch (err) {
      setError('Failed to fetch dish details')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }, [])

  const searchDishes = useCallback(async (query) => {
    if (!query.trim()) {
      setAllDishes([])
      return
    }
    setLoading(true)
    try {
      const response = await fetch(`/api/dishes?search=${encodeURIComponent(query)}`)
      const data = await response.json()
      setAllDishes(data.dishes || [])
      setError(null)
    } catch (err) {
      setError('Failed to search dishes')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }, [])

  const fetchTodayLogs = useCallback(async (date = null) => {
    setLoading(true)
    try {
      const dateParam = date || new Date().toISOString().split('T')[0]
      const response = await fetch(`/api/logs?date=${dateParam}`)
      const data = await response.json()
      setTodayLogs(data.logs || [])
      setDailyTotals(data.totals || {})
      setDailyProgress(data.progress || {})
      setError(null)
    } catch (err) {
      setError('Failed to fetch logs')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }, [])

  const addLog = useCallback(async (dishId, mealType, grams) => {
    setLoading(true)
    try {
      const response = await fetch('/api/logs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          dish_id: dishId,
          meal_type: mealType,
          grams,
        }),
      })
      const data = await response.json()
      if (data.success) {
        setSuccess(`${grams}g added to ${mealType}!`)
        setError(null)
        // Refresh logs
        await fetchTodayLogs()
      }
    } catch (err) {
      setError('Failed to add log')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }, [fetchTodayLogs])

  const deleteLog = useCallback(async (logId) => {
    try {
      const response = await fetch(`/api/logs/${logId}`, {
        method: 'DELETE',
      })
      const data = await response.json()
      if (data.success) {
        setSuccess('Log deleted')
        setError(null)
        await fetchTodayLogs()
      }
    } catch (err) {
      setError('Failed to delete log')
      console.error(err)
    }
  }, [fetchTodayLogs])

  const clearMessages = useCallback(() => {
    setError(null)
    setSuccess(null)
  }, [])

  const value = {
    // State
    userGoals,
    allDishes,
    currentDish,
    topPrediction,
    predictions,
    todayLogs,
    dailyTotals,
    dailyProgress,
    loading,
    error,
    success,

    // Actions
    fetchUserGoals,
    updateUserGoals,
    fetchAllDishes,
    fetchDishDetails,
    searchDishes,
    setTopPrediction,
    setPredictions,
    fetchTodayLogs,
    addLog,
    deleteLog,
    clearMessages,
    setLoading,
    setError,
    setSuccess,
  }

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export const useAppContext = () => {
  const context = React.useContext(AppContext)
  if (!context) {
    throw new Error('useAppContext must be used within AppProvider')
  }
  return context
}
