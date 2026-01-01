
# Food Recognition Project - Updated Overview

## 📋 Contents
1) Overview
2) Environment
3) Datasets
4) Feature pipeline
5) Models & results (Food-101 baseline and combined set)
6) Scrapers
7) Web app
8) Files & paths
9) Next steps

---

## 1) Overview
- Food recognition using ResNet50 features + classic ML classifiers.
- Baseline: Food-101 (101 classes).
- Current combined set: Food-101 + Moroccan v1 (9 dishes) → 110 classes, trained Logistic C=0.01.
- In progress: Moroccan v2 scraper (5 specialty dishes) to refresh/replace the Moroccan set (target 105 total classes after swap).

---

## 2) Environment
- OS: Windows
- Python: 3.12 (`conda env: food_gpu`)
- GPU: NVIDIA with CUDA 12.4

Key deps:
```
pytorch >=2.0, torchvision, pytorch-cuda=12.4
scikit-learn, joblib, numpy, pillow
icrawler (for scraping)
flask, torch, torchvision
```

Install (core):
```powershell
conda create -n food_gpu python=3.12
conda activate food_gpu
conda install pytorch torchvision pytorch-cuda=12.4 -c pytorch -c nvidia
pip install scikit-learn joblib pillow icrawler flask
```

---

## 3) Datasets

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

## 4) Feature Pipeline
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

## 5) Models & Results

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

## 6) Scrapers

### `scrape_incremental.py` (legacy, v1)
- Continues existing Moroccan v1 set; per-query temp folders; duplicate hashing; targets 750 train / 250 val per class.

### `scrape_moroccan_v2.py` (current)
- 8 dishes, ~108 queries each (EN/FR/AR).
- Validation: min 150px size, aspect ratio ≤4:1, image integrity, MD5 dedupe.
- Downloads per-query to `D:/moroccan_food_images_v2/temp_<dish>/query_<n>/`, then splits 75/25 into `train/` and `validation/`.
- Resume-safe: if interrupted, keeps temp folders and resumes from the next query.

---

## 7) Web App
- File: `app.py`
- Framework: Flask; drag-and-drop upload UI (`templates/`).
- Pipeline: load ResNet50 on GPU/CPU → extract 2048-dim features → scale → Logistic C=0.01 prediction → top-5.
- Expects assets:
   - Model: `D:/food_recognition_models/combined_models/Logistic_C0.01.pkl`
   - Scaler: `D:/food_recognition_models/combined_models/scaler.pkl`
   - Class names: `D:/food_recognition_models/features/final_class_names.npy`
- Run: `conda activate food_gpu; python app.py` (defaults to port 5000).

---

## 8) Files & Paths (current repo)
- `app.py` — Flask inference app.
- `train_resnet_rf_simple.py` — Food-101 feature extraction baseline.
- `merge_and_extract_features.py` — Extract Moroccan features.
- `merge_existing_features.py` — Merge Food-101 + Moroccan features.
- `train_combined_models.py` — Train Logistic / KNN on combined features.
- `scrape_incremental.py` — Legacy Moroccan v1 incremental scraper.
- `scrape_moroccan_v2.py` — New validated scraper with resume.
- `templates/` — Web UI templates.
- `requirements_training.txt` — Dependency list.

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

## 9) Next Steps (Dec 2025)
1) Finish Moroccan v2 scraping (5 dishes: djaj_mhamer, chebakia, fekkas, harsha, sefanj) to ~1000 images/class.
2) Extract features for Moroccan v2 (`merge_and_extract_features.py`).
3) Re-merge with Food-101 (`merge_existing_features.py`) → updated combined features and class names.
4) Retrain combined models (`train_combined_models.py`) with Logistic C=0.01 and KNN k=30.
5) Update `app.py` assets to the new model/scaler/class names if paths change (e.g., new combined_models_v2/ folder).

Last updated: December 11, 2025
