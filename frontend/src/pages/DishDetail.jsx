import { useParams, useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { useAppContext } from '../context/AppContext'
import './DishDetail.css'

export const DishDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { currentDish, fetchDishDetails, addLog, loading, error } = useAppContext()
  const [activeTab, setActiveTab] = useState('nutrition')
  const [quantity, setQuantity] = useState(100)
  const [mealType, setMealType] = useState('lunch')

  useEffect(() => {
    fetchDishDetails(id)
  }, [id])

  if (loading) {
    return (
      <div className="dish-detail-page">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading dish details...</p>
        </div>
      </div>
    )
  }

  if (!currentDish) {
    return (
      <div className="dish-detail-page">
        <div className="error-state">
          <span className="error-icon">⚠️</span>
          <p>Dish not found</p>
          <button className="btn-back" onClick={() => navigate('/dishes')}>
            ← Back to Dishes
          </button>
        </div>
      </div>
    )
  }

  const dish = currentDish
  const scaledNutrition = {
    calories: Math.round((dish.nutrition.calories / dish.nutrition.serving_size_g) * quantity),
    protein_g: Math.round((dish.nutrition.protein_g / dish.nutrition.serving_size_g) * quantity * 10) / 10,
    carbs_g: Math.round((dish.nutrition.carbs_g / dish.nutrition.serving_size_g) * quantity * 10) / 10,
    fat_g: Math.round((dish.nutrition.fat_g / dish.nutrition.serving_size_g) * quantity * 10) / 10,
  }

  return (
    <div className="dish-detail-page">
      <div className="dish-detail-container">
        {/* Header Section */}
        <div className="detail-header">
          <button className="btn-back" onClick={() => navigate('/dishes')}>
            ← Back to Dishes
          </button>
          <div className="header-content">
            <div className="dish-icon-large">🍽️</div>
            <div className="header-text">
              <h1>{dish.name}</h1>
              <div className="cuisine-badges">
                <span className="badge">{dish.cuisine}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="detail-grid">
          {/* Left Column - Info Panels */}
          <div className="detail-left">
            {/* Tab Navigation */}
            <div className="tabs">
              <button
                className={`tab-button ${activeTab === 'nutrition' ? 'active' : ''}`}
                onClick={() => setActiveTab('nutrition')}
              >
                📊 Nutrition
              </button>
              <button
                className={`tab-button ${activeTab === 'recipe' ? 'active' : ''}`}
                onClick={() => setActiveTab('recipe')}
              >
                👨‍🍳 Recipe
              </button>
              <button
                className={`tab-button ${activeTab === 'ingredients' ? 'active' : ''}`}
                onClick={() => setActiveTab('ingredients')}
              >
                🥘 Ingredients
              </button>
            </div>

            {/* Tab Content */}
            <div className="tab-content">
              {activeTab === 'nutrition' && (
                <div className="nutrition-panel">
                  <h3>Nutritional Information</h3>
                  <p className="nutrition-disclaimer">Per {dish.nutrition.serving_size_g}g serving</p>
                  <div className="nutrition-grid">
                    <div className="nutrition-card">
                      <span className="nutrition-label">Calories</span>
                      <span className="nutrition-value">{dish.nutrition.calories}</span>
                      <span className="nutrition-unit">kcal</span>
                    </div>
                    <div className="nutrition-card">
                      <span className="nutrition-label">Protein</span>
                      <span className="nutrition-value">{dish.nutrition.protein_g}</span>
                      <span className="nutrition-unit">g</span>
                    </div>
                    <div className="nutrition-card">
                      <span className="nutrition-label">Carbs</span>
                      <span className="nutrition-value">{dish.nutrition.carbs_g}</span>
                      <span className="nutrition-unit">g</span>
                    </div>
                    <div className="nutrition-card">
                      <span className="nutrition-label">Fat</span>
                      <span className="nutrition-value">{dish.nutrition.fat_g}</span>
                      <span className="nutrition-unit">g</span>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'recipe' && (
                <div className="recipe-panel">
                  <h3>Preparation Instructions</h3>
                  {dish.recipe ? (
                    <>
                      <div className="recipe-meta">
                        <div className="meta-item">
                          <span className="icon">⏱️</span>
                          <div>
                            <p className="meta-label">Prep Time</p>
                            <p className="meta-value">{dish.recipe.prep_time || 'N/A'}</p>
                          </div>
                        </div>
                        <div className="meta-item">
                          <span className="icon">🔥</span>
                          <div>
                            <p className="meta-label">Cook Time</p>
                            <p className="meta-value">{dish.recipe.cook_time || 'N/A'}</p>
                          </div>
                        </div>
                      </div>
                      <div className="recipe-steps">
                        {dish.recipe.steps && dish.recipe.steps.length > 0 ? (
                          <>
                            <p className="section-title">Steps:</p>
                            <ol>
                              {dish.recipe.steps.map((step, idx) => (
                                <li key={idx}>{step}</li>
                              ))}
                            </ol>
                          </>
                        ) : (
                          <p className="no-data">Recipe steps coming soon</p>
                        )}
                      </div>
                      {dish.recipe.tips && (
                        <div className="recipe-tips">
                          <p className="section-title">💡 Chef's Tips:</p>
                          {Array.isArray(dish.recipe.tips) ? (
                            <ul>
                              {dish.recipe.tips.map((tip, idx) => (
                                <li key={idx}>{tip}</li>
                              ))}
                            </ul>
                          ) : (
                            <p style={{ color: 'rgba(255, 255, 255, 0.8)' }}>{dish.recipe.tips}</p>
                          )}
                        </div>
                      )}
                    </>
                  ) : (
                    <p className="no-data">Recipe information coming soon</p>
                  )}
                </div>
              )}

              {activeTab === 'ingredients' && (
                <div className="ingredients-panel">
                  <h3>Ingredients</h3>
                  {dish.ingredients && dish.ingredients.length > 0 ? (
                    <ul className="ingredients-list">
                      {dish.ingredients.map((ingredient, idx) => (
                        <li key={idx}>{ingredient}</li>
                      ))}
                    </ul>
                  ) : (
                    <p className="no-data">Ingredients list coming soon</p>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Right Column - Add to Meal Section */}
          <div className="detail-right">
            <div className="add-meal-card">
              <h3>Add to Your Meal</h3>

              {/* Quantity Selector */}
              <div className="form-group">
                <label>Quantity (grams)</label>
                <div className="quantity-input-group">
                  <button
                    className="qty-btn"
                    onClick={() => setQuantity(Math.max(10, quantity - 50))}
                  >
                    −
                  </button>
                  <input
                    type="number"
                    value={quantity}
                    onChange={(e) => setQuantity(Math.max(10, parseInt(e.target.value) || 0))}
                    className="qty-input"
                  />
                  <button
                    className="qty-btn"
                    onClick={() => setQuantity(quantity + 50)}
                  >
                    +
                  </button>
                </div>
                <div className="quick-buttons">
                  {[100, 150, 200, 250].map((val) => (
                    <button
                      key={val}
                      className={`quick-btn ${quantity === val ? 'active' : ''}`}
                      onClick={() => setQuantity(val)}
                    >
                      {val}g
                    </button>
                  ))}
                </div>
              </div>

              {/* Meal Type Selector */}
              <div className="form-group">
                <label>Meal Type</label>
                <div className="meal-buttons">
                  {['breakfast', 'lunch', 'dinner', 'snack'].map((type) => (
                    <button
                      key={type}
                      className={`meal-btn ${mealType === type ? 'active' : ''}`}
                      onClick={() => setMealType(type)}
                    >
                      {type.charAt(0).toUpperCase() + type.slice(1)}
                    </button>
                  ))}
                </div>
              </div>

              {/* Nutrition Preview */}
              <div className="nutrition-preview">
                <p className="preview-title">For {quantity}g:</p>
                <div className="preview-macros">
                  <div className="macro">
                    <span className="macro-label">Calories</span>
                    <span className="macro-value">{scaledNutrition.calories}</span>
                  </div>
                  <div className="macro">
                    <span className="macro-label">Protein</span>
                    <span className="macro-value">{scaledNutrition.protein_g}g</span>
                  </div>
                  <div className="macro">
                    <span className="macro-label">Carbs</span>
                    <span className="macro-value">{scaledNutrition.carbs_g}g</span>
                  </div>
                  <div className="macro">
                    <span className="macro-label">Fat</span>
                    <span className="macro-value">{scaledNutrition.fat_g}g</span>
                  </div>
                </div>
              </div>

              {/* Add Button */}
              <button 
                className="btn-add-meal"
                onClick={async () => {
                  await addLog(dish.id, mealType, quantity)
                  navigate('/dashboard')
                }}
              >
                Add {quantity}g to {mealType}
              </button>

              <p className="add-note">This will be added to today's meal log</p>
            </div>

            {/* Similar Dishes */}
            {dish.similar_dishes && dish.similar_dishes.length > 0 && (
              <div className="similar-dishes-card">
                <h3>Similar Dishes</h3>
                <div className="similar-list">
                  {dish.similar_dishes.map((similarId) => (
                    <button
                      key={similarId}
                      className="similar-item"
                      onClick={() => navigate(`/dishes/${similarId}`)}
                    >
                      <span className="icon">🍽️</span>
                      <span className="name">Dish #{similarId}</span>
                      <span className="arrow">→</span>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
