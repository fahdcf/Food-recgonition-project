import { useEffect, useState } from 'react'
import { useAppContext } from '../context/AppContext'
import './Dashboard.css'

export const Dashboard = () => {
  const {
    userGoals,
    fetchUserGoals,
    updateUserGoals,
    todayLogs,
    dailyTotals,
    dailyProgress,
    fetchTodayLogs,
    deleteLog,
    loading,
  } = useAppContext()

  const [showGoalsModal, setShowGoalsModal] = useState(false)
  const [goalForm, setGoalForm] = useState(userGoals)

  useEffect(() => {
    fetchUserGoals()
    fetchTodayLogs()
  }, [fetchUserGoals, fetchTodayLogs])

  useEffect(() => {
    setGoalForm(userGoals)
  }, [userGoals])

  const handleSaveGoals = async () => {
    await updateUserGoals(goalForm)
    setShowGoalsModal(false)
  }

  const getMealTypeColor = (mealType) => {
    const colors = {
      breakfast: '#fbbf24',
      lunch: '#ff6b6b',
      dinner: '#4facfe',
      snack: '#a78bfa',
    }
    return colors[mealType] || '#ffffff'
  }

  const getMealTypeIcon = (mealType) => {
    const icons = {
      breakfast: '🌅',
      lunch: '☀️',
      dinner: '🌙',
      snack: '🍪',
    }
    return icons[mealType] || '🍽️'
  }

  const logsByMealType = {
    breakfast: todayLogs.filter((l) => l.meal_type === 'breakfast'),
    lunch: todayLogs.filter((l) => l.meal_type === 'lunch'),
    dinner: todayLogs.filter((l) => l.meal_type === 'dinner'),
    snack: todayLogs.filter((l) => l.meal_type === 'snack'),
  }

  const chartData = [
    { label: 'Carbs', value: dailyTotals.carbs_g, goal: userGoals.daily_carbs_g, color: '#fbbf24' },
    { label: 'Protein', value: dailyTotals.protein_g, goal: userGoals.daily_protein_g, color: '#22c55e' },
    { label: 'Fat', value: dailyTotals.fat_g, goal: userGoals.daily_fat_g, color: '#f87171' },
  ]

  return (
    <div className="dashboard">
      <div className="dashboard-container">
        <header className="dashboard-header">
          <h1>Your Nutrition Dashboard</h1>
          <button className="btn btn-secondary" onClick={() => setShowGoalsModal(true)}>
            Edit Goals
          </button>
        </header>

        {/* Daily Summary Cards */}
        <section className="summary-cards">
          <div className="summary-card primary">
            <div className="card-label">Daily Calories</div>
            <div className="card-value">{Math.round(dailyTotals.calories)}</div>
            <div className="card-goal">Goal: {userGoals.daily_calories}</div>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{
                  width: `${Math.min((dailyTotals.calories / userGoals.daily_calories) * 100, 100)}%`,
                }}
              />
            </div>
            <div className="progress-text">{Math.round(dailyProgress.calories)}%</div>
          </div>

          <div className="summary-card">
            <div className="card-label">Protein</div>
            <div className="card-value">{Math.round(dailyTotals.protein_g)}g</div>
            <div className="card-goal">Goal: {userGoals.daily_protein_g}g</div>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{
                  width: `${Math.min((dailyTotals.protein_g / userGoals.daily_protein_g) * 100, 100)}%`,
                  background: '#22c55e',
                }}
              />
            </div>
            <div className="progress-text">{Math.round(dailyProgress.protein)}%</div>
          </div>

          <div className="summary-card">
            <div className="card-label">Carbs</div>
            <div className="card-value">{Math.round(dailyTotals.carbs_g)}g</div>
            <div className="card-goal">Goal: {userGoals.daily_carbs_g}g</div>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{
                  width: `${Math.min((dailyTotals.carbs_g / userGoals.daily_carbs_g) * 100, 100)}%`,
                  background: '#fbbf24',
                }}
              />
            </div>
            <div className="progress-text">{Math.round(dailyProgress.carbs)}%</div>
          </div>

          <div className="summary-card">
            <div className="card-label">Fat</div>
            <div className="card-value">{Math.round(dailyTotals.fat_g)}g</div>
            <div className="card-goal">Goal: {userGoals.daily_fat_g}g</div>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{
                  width: `${Math.min((dailyTotals.fat_g / userGoals.daily_fat_g) * 100, 100)}%`,
                  background: '#f87171',
                }}
              />
            </div>
            <div className="progress-text">{Math.round(dailyProgress.fat)}%</div>
          </div>
        </section>

        {/* Macro Breakdown */}
        <section className="macro-breakdown">
          <h2>Macro Breakdown</h2>
          <div className="macro-bars">
            {chartData.map((macro) => (
              <div key={macro.label} className="macro-item">
                <div className="macro-info">
                  <span className="macro-label">{macro.label}</span>
                  <span className="macro-value">
                    {Math.round(macro.value)}g / {macro.goal}g
                  </span>
                </div>
                <div className="macro-bar-container">
                  <div
                    className="macro-bar-fill"
                    style={{
                      width: `${Math.min((macro.value / macro.goal) * 100, 100)}%`,
                      backgroundColor: macro.color,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Today's Meals */}
        <section className="today-meals">
          <h2>Today's Meals</h2>

          {todayLogs.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">🥗</div>
              <p>No meals logged yet. Go to Predict page to add a meal!</p>
            </div>
          ) : (
            <div className="meals-by-type">
              {Object.entries(logsByMealType).map(([mealType, logs]) => (
                logs.length > 0 && (
                  <div key={mealType} className="meal-section">
                    <h3 className="meal-title">
                      <span>{getMealTypeIcon(mealType)}</span>
                      {mealType.charAt(0).toUpperCase() + mealType.slice(1)}
                    </h3>

                    <div className="logs-list">
                      {logs.map((log) => (
                        <div key={log.id} className="log-entry">
                          <div className="log-info">
                            <div className="log-dish">
                              <h4>{log.dish_name}</h4>
                              <p className="log-portion">{log.grams}g</p>
                            </div>
                          </div>

                          <div className="log-nutrition">
                            <div className="nutrition-item">
                              <span className="nutrition-label">Cal</span>
                              <span className="nutrition-value">{Math.round(log.nutrition.calories)}</span>
                            </div>
                            <div className="nutrition-item">
                              <span className="nutrition-label">P</span>
                              <span className="nutrition-value">{Math.round(log.nutrition.protein_g)}g</span>
                            </div>
                            <div className="nutrition-item">
                              <span className="nutrition-label">C</span>
                              <span className="nutrition-value">{Math.round(log.nutrition.carbs_g)}g</span>
                            </div>
                            <div className="nutrition-item">
                              <span className="nutrition-label">F</span>
                              <span className="nutrition-value">{Math.round(log.nutrition.fat_g)}g</span>
                            </div>
                          </div>

                          <button
                            className="delete-btn"
                            onClick={() => deleteLog(log.id)}
                            title="Delete entry"
                          >
                            ✕
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )
              ))}
            </div>
          )}
        </section>
      </div>

      {/* Goals Modal */}
      {showGoalsModal && (
        <div className="modal-overlay" onClick={() => setShowGoalsModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button
              className="modal-close"
              onClick={() => setShowGoalsModal(false)}
            >
              ×
            </button>

            <h2>Edit Daily Goals</h2>

            <div className="form-group">
              <label>Daily Calories</label>
              <input
                type="number"
                value={goalForm.daily_calories}
                onChange={(e) =>
                  setGoalForm({ ...goalForm, daily_calories: parseInt(e.target.value) })
                }
              />
            </div>

            <div className="form-group">
              <label>Daily Protein (g)</label>
              <input
                type="number"
                value={goalForm.daily_protein_g}
                onChange={(e) =>
                  setGoalForm({ ...goalForm, daily_protein_g: parseInt(e.target.value) })
                }
              />
            </div>

            <div className="form-group">
              <label>Daily Carbs (g)</label>
              <input
                type="number"
                value={goalForm.daily_carbs_g}
                onChange={(e) =>
                  setGoalForm({ ...goalForm, daily_carbs_g: parseInt(e.target.value) })
                }
              />
            </div>

            <div className="form-group">
              <label>Daily Fat (g)</label>
              <input
                type="number"
                value={goalForm.daily_fat_g}
                onChange={(e) =>
                  setGoalForm({ ...goalForm, daily_fat_g: parseInt(e.target.value) })
                }
              />
            </div>

            <div className="modal-actions">
              <button className="btn btn-secondary" onClick={() => setShowGoalsModal(false)}>
                Cancel
              </button>
              <button className="btn btn-primary" onClick={handleSaveGoals} disabled={loading}>
                Save Goals
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
