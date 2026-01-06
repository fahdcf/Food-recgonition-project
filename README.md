
# 🍕 Food Recognition Project - Full-Stack App

## 📋 Contents
1) Overview
2) Features
3) Environment
4) Architecture
5) Datasets
6) Feature pipeline
7) Models & results
8) Web application
9) Files & paths
10) Next steps

---

## 1) Overview
- **Full-stack food recognition application** with AI-powered image classification and comprehensive nutrition tracking
- **Backend**: Flask REST API with modular architecture (routes, models, utils)
- **Frontend**: React 19 + Vite with dark glassmorphic UI
- **AI Model**: ResNet50 feature extraction + Logistic Regression (C=0.01)
- **Dataset**: 110 classes (101 Food-101 + 9 Moroccan dishes)
- **Database**: SQLite with meal logging and goal tracking

---

## 2) Features

### 🔍 AI-Powered Recognition
- Upload food images for instant classification
- ResNet50 deep learning feature extraction
- Top-5 predictions with confidence scores
- Supports 110 international dishes

### 📊 Comprehensive Nutrition
- Detailed macronutrient breakdown (calories, protein, carbs, fat)
- Adjustable portion sizes (grams)
- Per-100g standardized nutrition data
- 174 dishes in nutrition database

### 👨‍🍳 Recipe Information
- Step-by-step cooking instructions
- Prep and cook time estimates
- Chef's tips and tricks
- Ingredient lists with quantities

### 📝 Meal Logging & Goals
- Track daily meals (breakfast, lunch, dinner, snack)
- Set custom nutrition goals
- Real-time progress tracking
- Daily summaries with goal achievement
- Persistent storage (SQLite)

### 🔎 Smart Discovery
- Browse all 174 dishes
- Search by dish name
- View similar dish recommendations
- Detailed dish pages with tabs (Nutrition, Recipe, Ingredients)

---

## 3) Environment
- OS: Windows
- Python: 3.12 (`conda env: food_gpu`)
- GPU: NVIDIA with CUDA 12.4

Key deps:
```
# Backend
flask, flask-cors
pytorch >=2.0, torchvision, pytorch-cuda=12.4
scikit-learn, joblib, numpy, pillow

# Frontend
react 19, vite, react-router-dom

# Data scraping
icrawler
```

Install backend:
```powershell
conda create -n food_gpu python=3.12
conda activate food_gpu
conda install pytorch torchvision pytorch-cuda=12.4 -c pytorch -c nvidia
pip install -r requirements_backend.txt
```

Install frontend:
```powershell
cd frontend
npm install
```

---

## 4) Architecture

### Backend (Modular Flask)
```
backend/
├── __init__.py          # Flask app factory
├── config.py            # Configuration settings
├── routes/
│   ├── predict.py       # Image prediction endpoints
│   ├── dishes.py        # Dish browsing & search (7 endpoints)
│   ├── goals.py         # User nutrition goals
│   └── logs.py          # Meal logging & summaries
├── models/
│   └── __init__.py      # ML model loading & inference
└── utils/
    ├── database.py      # SQLite utilities
    └── dishes.py        # Dish data management
```

### Frontend (React + Vite)
```
frontend/src/
├── pages/
│   ├── Landing.jsx      # Hero page
│   ├── Upload.jsx       # Image upload & prediction
│   ├── Dashboard.jsx    # Meal tracking & goals
│   ├── AllDishes.jsx    # Browse all dishes
│   └── DishDetail.jsx   # Single dish view
├── context/
│   └── AppContext.jsx   # Global state management
└── App.jsx              # Router setup
```

### API Endpoints

**Prediction**
- `POST /api/predict` - Upload image for classification
- `GET /api/health` - Health check

**Dishes** (7 endpoints)
- `GET /api/dishes/all` - Get all dishes
- `GET /api/dishes?search=<query>` - Search dishes
- `GET /api/dishes/<id>` - Get dish details
- `GET /api/dishes/<id>/nutrition` - Get nutrition info
- `GET /api/dishes/<id>/recipe` - Get recipe
- `GET /api/dishes/<id>/ingredients` - Get ingredients
- `GET /api/dishes/<id>/similar` - Get similar dishes

**Goals**
- `GET /api/user/goals` - Get user nutrition goals
- `PUT /api/user/goals` - Update nutrition goals

**Logs**
- `GET /api/logs?date=<YYYY-MM-DD>` - Get logs for date
- `POST /api/logs` - Add meal log
- `DELETE /api/logs/<id>` - Delete log
- `GET /api/logs/summary` - Get daily summary

---

## 5) Datasets

### Food-101 (baseline)
- Path: `D:/food_dataset/Food-101/`
- Train 75,750 / Val 25,250 (101 classes)

### Moroccan v1 (current combined training set)
- Path: `D:/moroccan_food_images/train|validation/<dish>`
- Classes (9): couscous, tagine, pastilla, harira, rfissa, bissara, msemmen, kefta_tagine, zaalouk
- Used in current combined training (110 classes total with Food-101).

### Moroccan v2 (in progress, higher quality)
- Script: `scrape_moroccan_v2.py`
- Output: `D:/moroccan_food_images_v2/train|validation/<dish>`
- Dishes (5): djaj_mhamer, chebakia, fekkas, harsha, sefanj
  - **Djaj Mhamer**: Spiced chicken tagine (slow-cooked)
  - **Chebakia**: Sesame honey cookies (Ramadan sweet)
  - **Fekkas**: Almond twice-baked biscuits (dipped in coffee/tea)
  - **Harsha**: Semolina flatbread pancake with anise (breakfast)
  - **Sefanj**: Thin delicate Moroccan crepe (lighter pancake)
- Validation rules: min 150px, aspect ratio ≤4:1, hash-based dedupe, multilingual queries (EN/FR/AR), per-query temp folders; supports resume.
- Target: ~1000 images per dish, 750 train / 250 validation split.

---

## 6) Feature Pipeline
- Extractor: ResNet50 (ImageNet), avg-pool 2048-dim features.
- Preprocess: 256 resize → 224 center crop → ImageNet norm.
- Scripts:
   - `train_resnet_rf_simple.py` (Food-101 feature extraction baseline)
   - `merge_and_extract_features.py` (Moroccan images → features)
   - `merge_existing_features.py` (combine Food-101 + Moroccan features)
- Combined feature outputs (current):
   - `D:/food_recognition_models/features/final_train_features.npy`
   - `D:/food_recognition_models/features/final_val_features.npy`
   - `D:/food_recognition_models/features/final_class_names.npy`
- Scaler: `D:/food_recognition_models/combined_models/scaler.pkl`

---

## 7) Models & Results

### Food-101 baseline (101 classes)
- Model: Logistic Regression C=0.01 (lbfgs)
- Accuracy: ~70.98% top-1, ~91.05% top-5 (features only; baseline reference)

### Combined (Food-101 + Moroccan v1 → 110 classes)
- Training script: `train_combined_models.py`
- Best: Logistic Regression C=0.01
- Accuracy: ~67% top-1, ~88% top-5
- Model path: `D:/food_recognition_models/combined_models/Logistic_C0.01.pkl`
- Scaler path: `D:/food_recognition_models/combined_models/scaler.pkl`
- KNN (comparison): `D:/food_recognition_models/combined_models/KNN_k30_distance.pkl` (much slower, lower accuracy)

Planned (after Moroccan v2 refresh → 109 classes):
- Re-extract Moroccan v2 features, re-merge, re-train Logistic C=0.01 and KNN k=30.

---

## 8) Web Application

### Running the App

**Start Backend:**
```powershell
conda activate food_gpu
python run.py
```
Backend runs on `http://localhost:5000`

**Start Frontend:**
```powershell
cd frontend
npm run dev
```
Frontend runs on `http://localhost:5173`

### Application Flow

1. **Landing Page** - Hero section with feature highlights
2. **Upload Image** - Drag & drop or click to upload food photo
3. **View Prediction** - See top-5 predictions with confidence scores
4. **Add to Meal** - Select meal type (breakfast/lunch/dinner/snack) and portion size
5. **Dashboard** - Track daily nutrition, view logs, set goals
6. **Browse Dishes** - Explore all 174 dishes with search
7. **Dish Details** - View nutrition, recipes, and ingredients

### Database Schema

**user_goals** table:
- `id`, `user_id`, `daily_calories`, `daily_protein_g`, `daily_carbs_g`, `daily_fat_g`, `updated_at`

**logs** table:
- `id`, `user_id`, `dish_id`, `meal_type`, `grams`, `created_at`, `notes`

### Data Files

- `data/dishes.json` - 174 dishes with nutrition, recipes, ingredients
- `data/food_app.db` - SQLite database (auto-created)

---

## 9) Scrapers

### `scrape_incremental.py` (legacy, v1)
- Continues existing Moroccan v1 set; per-query temp folders; duplicate hashing; targets 750 train / 250 val per class.

### `scrape_moroccan_v2.py` (current)
- 8 dishes, ~108 queries each (EN/FR/AR).
- Validation: min 150px size, aspect ratio ≤4:1, image integrity, MD5 dedupe.
- Downloads per-query to `D:/moroccan_food_images_v2/temp_<dish>/query_<n>/`, then splits 75/25 into `train/` and `validation/`.
- Resume-safe: if interrupted, keeps temp folders and resumes from the next query.

---


## 10) Files & Paths

### Project Structure
```
Food Recognition Project/
├── backend/              # Modular Flask backend
│   ├── routes/          # API endpoints
│   ├── models/          # ML model loading
│   └── utils/           # Database & utilities
├── frontend/            # React frontend
│   ├── src/
│   │   ├── pages/      # Page components
│   │   └── context/    # State management
│   └── package.json
├── data/
│   ├── dishes.json     # 174 dishes database
│   └── food_app.db     # SQLite database
├── run.py              # Backend entry point
├── create_dishes_json.py
├── requirements_backend.txt
└── README.md
```

### Training Scripts
- `train_resnet_rf_simple.py` — Food-101 feature extraction baseline
- `merge_and_extract_features.py` — Extract Moroccan features
- `merge_existing_features.py` — Merge Food-101 + Moroccan features
- `train_combined_models.py` — Train Logistic / KNN on combined features
- `scrape_incremental.py` — Legacy Moroccan v1 scraper
- `scrape_moroccan_v2.py` — Moroccan v2 validated scraper

Model/feature storage (D: drive):
```
D:/food_recognition_models/
   ├── features/
   │   ├── final_train_features.npy
   │   ├── final_val_features.npy
   │   └── final_class_names.npy
   └── combined_models/
         ├── Logistic_C0.01.pkl
         ├── KNN_k30_distance.pkl
         └── scaler.pkl
```

---

## 11) Next Steps
1) Finish Moroccan v2 scraping (5 dishes: djaj_mhamer, chebakia, fekkas, harsha, sefanj) to ~1000 images/class
2) Extract features for Moroccan v2 (`merge_and_extract_features.py`)
3) Re-merge with Food-101 (`merge_existing_features.py`) → updated combined features and class names
4) Retrain combined models (`train_combined_models.py`) with Logistic C=0.01 and KNN k=30
5) Expand dishes.json with more detailed recipes and ingredient lists
6) Add user authentication for multi-user support
7) Implement meal plan suggestions based on nutrition goals

---

**Last updated:** January 1, 2026  
**Status:** Full-stack app with 5 advanced features operational  
**Model:** 110 classes (101 Food-101 + 9 Moroccan) - 67% top-1, 88% top-5 accuracy
