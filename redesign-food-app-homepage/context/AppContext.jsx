"use client"

import { createContext, useContext, useState, useCallback } from "react"

const AppContext = createContext()

export const AppContextProvider = ({ children }) => {
  const [userGoals, setUserGoals] = useState({
    daily_calories: 2400,
    daily_protein: 150,
    daily_carbs: 250,
    daily_fats: 80,
  })

  const fetchUserGoals = useCallback(async () => {
    // In a real app, this would be an API call
    console.log("[v0] Fetching user goals...")
    // For demo purposes, we'll just keep the default state
  }, [])

  return <AppContext.Provider value={{ userGoals, fetchUserGoals }}>{children}</AppContext.Provider>
}

export const useAppContext = () => {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error("useAppContext must be used within an AppContextProvider")
  }
  return context
}
