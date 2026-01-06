import { useState, useRef, useEffect } from 'react'
import { useAppContext } from '../context/AppContext'
import './Upload.css'

export const Upload = () => {
  const fileInputRef = useRef(null)
  const [file, setFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [selectedMealType, setSelectedMealType] = useState('lunch')
  const [quantity, setQuantity] = useState('100')
  const [quantityUnit, setQuantityUnit] = useState('grams')
  const [isDragging, setIsDragging] = useState(false)
  const [showAddModal, setShowAddModal] = useState(false)

  const { topPrediction, setTopPrediction, setPredictions, predictions, loading, setLoading, addLog } = useAppContext()

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl)
    }
  }, [previewUrl])

  const handleFile = (incomingFile) => {
    if (!incomingFile?.type.startsWith('image/')) {
      alert('Please upload an image file (JPG, PNG)')
      return
    }

    setFile(incomingFile)
    setPredictions([])

    const nextUrl = URL.createObjectURL(incomingFile)
    setPreviewUrl((prev) => {
      if (prev) URL.revokeObjectURL(prev)
      return nextUrl
    })
  }

  const handleAnalyze = async () => {
    if (!file) return

    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        body: formData,
      })
      const data = await response.json()

      if (data.success && data.predictions?.[0]) {
        setPredictions(data.predictions)
        // Save top prediction globally
        setTopPrediction(data.predictions[0])
        setShowAddModal(true)
      } else {
        alert('Failed to predict dish')
      }
    } catch (err) {
      console.error(err)
      alert('Network error')
    } finally {
      setLoading(false)
    }
  }

  const handleAddToLog = async () => {
    if (!topPrediction) return

    const grams = quantityUnit === 'grams' ? parseInt(quantity) : parseInt(quantity) * 100

    await addLog(topPrediction.class_id, selectedMealType, grams)
    resetForm()
  }

  const resetForm = () => {
    setFile(null)
    setPreviewUrl(null)
    setPredictions([])
    setShowAddModal(false)
    setQuantity('100')
    setQuantityUnit('grams')
    setSelectedMealType('lunch')
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  const onDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    handleFile(e.dataTransfer.files?.[0])
  }

  return (
    <div className="upload-page">
      <div className="upload-container">
        <header className="upload-header">
          <h1>Upload & Analyze</h1>
          <p>Upload your food image to get instant nutrition information</p>
        </header>

        <div className="upload-content">
          {!previewUrl ? (
            <div
              className={`upload-area ${isDragging ? 'dragover' : ''}`}
              onClick={() => fileInputRef.current?.click()}
              onDragOver={(e) => {
                e.preventDefault()
                setIsDragging(true)
              }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={onDrop}
            >
              <div className="upload-icon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                  <polyline points="17 8 12 3 7 8" />
                  <line x1="12" y1="3" x2="12" y2="15" />
                </svg>
              </div>
              <h3>Drop your food image here</h3>
              <p>or click to browse • Ctrl+V to paste</p>
              <span className="upload-hint">Supports JPG, PNG up to 16MB</span>

              <input
                ref={fileInputRef}
                type="file"
                accept="image/jpeg,image/jpg,image/png"
                hidden
                onChange={(e) => handleFile(e.target.files?.[0])}
              />
            </div>
          ) : (
            <div className="preview-section">
              <img src={previewUrl} alt="Preview" className="preview-image" />
              <div className="preview-actions">
                <button className="btn btn-secondary" onClick={resetForm}>
                  Change Image
                </button>
                <button className="btn btn-primary" onClick={handleAnalyze} disabled={loading}>
                  {loading ? 'Analyzing...' : 'Analyze Image'}
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Prediction Results Modal */}
      {showAddModal && topPrediction && (
        <div className="modal-overlay" onClick={() => setShowAddModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setShowAddModal(false)}>×</button>

            <div className="prediction-result">
              <h2>{topPrediction.class}</h2>
              <div className="confidence-badge">
                {topPrediction.confidence.toFixed(1)}% confidence
              </div>

              <div className="meal-selector">
                <label>Meal Type</label>
                <div className="meal-options">
                  {['breakfast', 'lunch', 'dinner', 'snack'].map((type) => (
                    <button
                      key={type}
                      className={`meal-btn ${selectedMealType === type ? 'active' : ''}`}
                      onClick={() => setSelectedMealType(type)}
                    >
                      {type.charAt(0).toUpperCase() + type.slice(1)}
                    </button>
                  ))}
                </div>
              </div>

              <div className="quantity-section">
                <label>Quantity</label>
                <div className="quantity-presets">
                  <button
                    className={`preset ${quantity === '100' && quantityUnit === 'grams' ? 'active' : ''}`}
                    onClick={() => {
                      setQuantity('100')
                      setQuantityUnit('grams')
                    }}
                  >
                    100g
                  </button>
                  <button
                    className={`preset ${quantity === '200' && quantityUnit === 'grams' ? 'active' : ''}`}
                    onClick={() => {
                      setQuantity('200')
                      setQuantityUnit('grams')
                    }}
                  >
                    200g
                  </button>
                  <button
                    className={`preset ${quantity === '1' && quantityUnit === 'plate' ? 'active' : ''}`}
                    onClick={() => {
                      setQuantity('1')
                      setQuantityUnit('plate')
                    }}
                  >
                    Full Plate
                  </button>
                </div>

                <div className="custom-quantity">
                  <input
                    type="number"
                    value={quantity}
                    onChange={(e) => setQuantity(e.target.value)}
                    min="1"
                  />
                  <select value={quantityUnit} onChange={(e) => setQuantityUnit(e.target.value)}>
                    <option value="grams">grams</option>
                    <option value="plate">plate (100g)</option>
                  </select>
                </div>
              </div>

              <button className="btn btn-primary btn-full" onClick={handleAddToLog}>
                Add to {selectedMealType.charAt(0).toUpperCase() + selectedMealType.slice(1)}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
