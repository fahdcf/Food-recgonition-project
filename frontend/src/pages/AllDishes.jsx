import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAppContext } from '../context/AppContext'
import './Dishes.css'

export const AllDishes = () => {
  const { allDishes, fetchAllDishes, searchDishes, loading } = useAppContext()
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    if (!searchTerm.trim()) {
      fetchAllDishes()
    }
  }, [fetchAllDishes])

  const handleSearch = (e) => {
    const term = e.target.value
    setSearchTerm(term)

    if (term.trim()) {
      searchDishes(term)
    } else {
      fetchAllDishes()
    }
  }

  return (
    <div className="dishes-page">
      <div className="dishes-container">
        <header className="dishes-header">
          <h1>Explore Dishes</h1>
          <p>Browse our collection of 120+ dishes with full nutrition information</p>

          <div className="search-box">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8" />
              <path d="m21 21-4.35-4.35" />
            </svg>
            <input
              type="text"
              placeholder="Search dishes..."
              value={searchTerm}
              onChange={handleSearch}
              className="search-input"
            />
          </div>
        </header>

        {loading ? (
          <div className="loading-state">
            <div className="spinner" />
            <p>Loading dishes...</p>
          </div>
        ) : allDishes.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🔍</div>
            <p>No dishes found. Try another search term!</p>
          </div>
        ) : (
          <div className="dishes-grid">
            {allDishes.map((dish) => (
              <Link key={dish.id} to={`/dishes/${dish.id}`} className="dish-card">
                <div className="dish-card-header">
                  <div className="dish-icon">🍽️</div>
                  <div className="dish-cuisine-badge">{dish.cuisine}</div>
                </div>

                <h3 className="dish-name">{dish.name}</h3>

                <div className="dish-stats">
                  <div className="stat">
                    <span className="stat-label">Calories</span>
                    <span className="stat-value">{dish.calories}</span>
                  </div>
                </div>

                <div className="card-footer">
                  <span className="view-link">View Details →</span>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
