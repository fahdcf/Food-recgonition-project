# 🎬 Explanatory Video Script - Food Recognition Project
## English Version - Maximum 6 minutes

---

## 📋 OVERVIEW
- **Total Duration**: ~6 minutes (~1400 spoken words)
- **Sections**: 5 main parts  
- **Audience**: University Professor
- **Language**: French (with English technical details)

---

## SCRIPT SUMMARY

The `VIDEO_SCRIPT_FR.md` file contains a complete 6-minute presentation script in French covering:

### Part 1: Introduction & Project Idea (1 min)
- What is the problem we're solving?
- Why is food recognition important?
- What is the complete solution?

### Part 2: Tech Stack & Data (1 min 20 sec)
- **AI Model**: ResNet50 + Logistic Regression
- **Backend**: Flask REST API
- **Frontend**: React 19 + Vite
- **Database**: SQLite
- **Datasets**: Food-101 (101 classes) + Moroccan (9 classes)

### Part 3: Scraping & Image Validation (1 min 10 sec)
- **Scraping Tool**: Bing Image Search via icrawler
- **Queries**: 108 multilingual queries per Moroccan dish
- **Validation**: 5-step process (hash, size, RGB, manual, clean)
- **Results**: ~3500 validated Moroccan images

### Part 4: Feature Extraction & Merging (1 min 15 sec)
- **ResNet50**: Removes classifier layer for 2048-dim features
- **Food-101**: Pre-extracted features loaded
- **Moroccan**: Features extracted similarly
- **Merge**: Combined 80K images in train/val/test split
- **Normalization**: StandardScaler applied

### Part 5: Model Training & Parameters (1 min 20 sec)
- **Algorithm**: Logistic Regression (multi-class)
- **Key Parameter**: C=0.01 (regularization strength)
- **Why LR?**: Fast, interpretable, ResNet50 already provides intelligent features
- **Multi-class**: Uses softmax to output 110 probabilities
- **Results**: 85% top-1 accuracy, 95% top-5, <100ms prediction

### Part 6: Frontend Usage (1 min 15 sec)
- **Upload Page**: Drag-drop image, instant prediction
- **Detail Page**: 3 tabs (Nutrition, Recipe, Ingredients)
- **API Flow**: Image → ResNet50 → LR prediction → UI
- **Logging**: Track meals, nutrition goals in SQLite
- **Design**: Glassmorphism, responsive, Font Awesome icons

---

## 🔧 TECHNICAL HIGHLIGHTS

### Key Files Referenced:
1. **`scrape_moroccan_v2.py`** (443 lines)
   - Bing Image crawling
   - Multi-language queries (English, French, Arabic)
   - Image validation pipeline
   - Duplicate detection via MD5 hash

2. **`merge_and_extract_features.py`** (288 lines)
   - Food-101 feature loading
   - Moroccan image processing
   - ResNet50 feature extraction
   - Batch processing for memory efficiency
   - Incremental caching

3. **`train_combined_models.py`** or **`train_resnet_rf_simple.py`** (224 lines)
   - Logistic Regression with C=0.01
   - StandardScaler normalization
   - Train/Val/Test evaluation
   - Model serialization with joblib

4. **`app.py`** (571 lines)
   - Flask API endpoints
   - Model loading and inference
   - SQLite database operations
   - CORS for React frontend

5. **Frontend Components**:
   - `Upload.jsx` - Prediction interface
   - `DishDetail.jsx` - Multi-tab details (Nutrition/Recipe/Ingredients)
   - `Landing.jsx` - Hero section with demo
   - `AppContext.jsx` - Global state management

---

## 📊 DATASET STATISTICS

| Metric | Value |
|--------|-------|
| **Food-101 Classes** | 101 |
| **Moroccan Classes** | 9 |
| **Total Classes** | 110 |
| **Total Images** | ~80,000 |
| **Train/Val/Test Split** | 70% / 15% / 15% |
| **Feature Dimension** | 2048 (ResNet50) |
| **Moroccan Images Scraped** | ~5,500 |
| **Moroccan Images Validated** | ~3,500 |
| **Nutrition Database** | 121 dishes |

---

## 🎯 MODEL PERFORMANCE

```python
# Logistic Regression Configuration
LogisticRegression(
    C=0.01,                    # Inverse regularization strength
    solver='lbfgs',            # L-BFGS optimizer
    max_iter=1000,             # Maximum iterations
    multi_class='multinomial', # Multi-class strategy
    n_jobs=-1,                 # Parallel computation
    random_state=42
)

# Results
- Top-1 Accuracy: 85%
- Top-5 Accuracy: 95%
- Training Time: 2-3 minutes (GPU)
- Prediction Time: <100ms per image
- Model Size: ~180 MB
```

---

## 🔄 COMPLETE WORKFLOW

```
┌─────────────────────────────────────────┐
│         USER UPLOADS IMAGE              │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Frontend: Validate file type/size      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Send to /api/predict endpoint          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Backend: Resize to 224x224             │
│           Apply normalization           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  ResNet50: Extract 2048-dim features    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  StandardScaler: Normalize features     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  LogisticRegression: Get 110 probs      │
│  Apply softmax → sum to 100%            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Return: Top-5 classes with confidence  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Frontend: Display results with UI      │
│  - Dish image, name, cuisine            │
│  - Confidence percentage                │
│  - Nutrition info                       │
└─────────────────────────────────────────┘
```

---

## 💾 DATA PERSISTENCE

### SQLite Database (`data/food_app.db`):
```sql
CREATE TABLE user_goals (
    id PRIMARY KEY,
    daily_calories INTEGER DEFAULT 2000,
    daily_protein_g INTEGER DEFAULT 150,
    daily_carbs_g INTEGER DEFAULT 200,
    daily_fat_g INTEGER DEFAULT 65
);

CREATE TABLE logs (
    id PRIMARY KEY,
    dish_id TEXT,
    meal_type TEXT (breakfast/lunch/dinner/snack),
    grams INTEGER,
    created_at TIMESTAMP
);
```

### JSON Metadata (`data/dishes.json`):
121 dishes with complete information:
- Nutrition per 100g (calories, protein, carbs, fat)
- Ingredients list with quantities
- Recipe steps with timing
- Chef's tips and techniques

---

## 🎨 FRONTEND ARCHITECTURE

```
React 19 + Vite Structure:

Landing Page
├── Hero section with AI demo animation
├── Feature cards (Font Awesome icons)
└── How-it-works workflow

Upload Page
├── Drag-drop file upload
├── Image preview
├── Prediction results (top-5)
└── Add to meal log modal

Dish Detail Page
├── Dish image
├── Nutrition tab
│   ├── Calories/protein/carbs/fat
│   └── Adjustable portion size
├── Recipe tab
│   ├── Prep/cook time (icons)
│   ├── Step-by-step instructions
│   └── Chef's tips (lightbulb icon)
└── Ingredients tab
    └── Complete ingredient list

Dashboard
├── Daily nutrition summary
├── Meal history (breakfast/lunch/dinner/snack)
├── Goals progress visualization
└── Edit personal nutrition goals
```

---

## 🔐 SECURITY & BEST PRACTICES

- **File Upload**: Max 16MB, type validation (image/* only)
- **API**: CORS enabled for localhost, expandable for production
- **Database**: SQLite with parameterized queries (SQL injection proof)
- **Frontend**: React context API for state management
- **Error Handling**: Try-catch blocks with user-friendly error messages

---

## 🚀 DEPLOYMENT NOTES

### To Run Locally:
```bash
# Backend
pip install -r requirements_backend.txt
python app.py  # Runs on http://localhost:5000

# Frontend
cd frontend
npm install
npm run dev    # Runs on http://localhost:5173

# Training (if needed)
pip install -r requirements_training.txt
python merge_and_extract_features.py
python train_combined_models.py
```

### Production Considerations:
- Use Gunicorn instead of Flask dev server
- Add authentication layer
- Scale to cloud (AWS/Azure/GCP)
- Implement image caching
- Add monitoring/logging

---

## 📚 REFERENCES & SOURCES

1. **ResNet50**: He et al., 2015 - "Deep Residual Learning for Image Recognition"
2. **Food-101 Dataset**: Bossard et al., 2014 - "Food-101 – Mining Discriminative Components with Random Projections"
3. **Logistic Regression**: Standard ML algorithm, softmax extension for multi-class
4. **PyTorch**: Deep learning framework for feature extraction
5. **scikit-learn**: Machine learning library for Logistic Regression

---

## ✅ CHECKLIST FOR PROFESSOR

- [x] AI-powered food recognition working
- [x] ResNet50 + LogisticRegression model trained (85% accuracy)
- [x] 110 food classes (101 Food-101 + 9 Moroccan)
- [x] Image scraping with validation pipeline
- [x] Feature extraction and merging system
- [x] Flask REST API backend
- [x] React frontend with glassmorphic UI
- [x] SQLite database for logging
- [x] 121 dishes with complete nutrition data
- [x] Responsive design + Font Awesome icons
- [x] Complete documentation

---

**Date Created**: January 6, 2026  
**Project**: Food Recognition - Full Stack Application  
**Language**: French (see `VIDEO_SCRIPT_FR.md`)  
**Duration**: ~6 minutes  
**Status**: Production Ready
