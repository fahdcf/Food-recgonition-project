"""
Train models on combined Food-101 + Moroccan dataset
Saves all models to D: drive with incremental checkpoints
"""
import os
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, top_k_accuracy_score
import joblib
import time

print("="*70)
print("🚀 Training Models on Combined Dataset")
print("="*70)

# Paths - ALL on D: drive
feature_dir = "D:/food_recognition_models/features"
model_dir = "D:/food_recognition_models/combined_models"
os.makedirs(model_dir, exist_ok=True)

# Load features
print("\n📂 Loading features...")
X_train = np.load(os.path.join(feature_dir, 'final_train_features.npy'))
y_train = np.load(os.path.join(feature_dir, 'final_train_labels.npy'))
X_val = np.load(os.path.join(feature_dir, 'final_val_features.npy'))
y_val = np.load(os.path.join(feature_dir, 'final_val_labels.npy'))
class_names = np.load(os.path.join(feature_dir, 'final_class_names.npy'), allow_pickle=True)

print(f"   Train features: {X_train.shape}")
print(f"   Val features: {X_val.shape}")
print(f"   Total classes: {len(class_names)}")
print(f"   Food-101 classes: {sum(1 for c in class_names if not c.startswith('moroccan_'))}")
print(f"   Moroccan classes: {sum(1 for c in class_names if c.startswith('moroccan_'))}")

# Normalize features
print("\n🔧 Normalizing features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)

# Save scaler to D: drive
scaler_path = os.path.join(model_dir, 'scaler.pkl')
joblib.dump(scaler, scaler_path)
print(f"   ✅ Saved scaler to {scaler_path}")

# Train Logistic Regression with C=0.01 (best parameter from previous experiments)
print("\n" + "="*70)
print("TRAINING LOGISTIC REGRESSION (C=0.01)")
print("="*70)

print("Training...")
start_time = time.time()
logistic_model = LogisticRegression(C=0.01, solver='lbfgs', max_iter=1000, random_state=42, n_jobs=-1)
logistic_model.fit(X_train_scaled, y_train)
train_time = time.time() - start_time

# Save model to D: drive
logistic_path = os.path.join(model_dir, 'Logistic_C0.01.pkl')
joblib.dump(logistic_model, logistic_path)
print(f"✅ Model saved to {logistic_path}")

# Evaluate
print("\nEvaluating...")
start_time = time.time()
y_pred = logistic_model.predict(X_val_scaled)
pred_time = time.time() - start_time

y_proba = logistic_model.predict_proba(X_val_scaled)

top1_acc = accuracy_score(y_val, y_pred)
top5_acc = top_k_accuracy_score(y_val, y_proba, k=5)

print(f"\n📊 Logistic Regression Results:")
print(f"   Top-1 Accuracy: {top1_acc*100:.2f}%")
print(f"   Top-5 Accuracy: {top5_acc*100:.2f}%")
print(f"   Training time: {train_time:.2f}s")
print(f"   Prediction time: {pred_time:.2f}s")

# Train KNN with k=30 distance weighting (best parameters from previous experiments)
print("\n" + "="*70)
print("TRAINING KNN (k=30, distance weighting)")
print("="*70)

print("Training...")
start_time = time.time()
knn_model = KNeighborsClassifier(n_neighbors=30, weights='distance', n_jobs=-1)
knn_model.fit(X_train_scaled, y_train)
train_time = time.time() - start_time

# Save model to D: drive
knn_path = os.path.join(model_dir, 'KNN_k30_distance.pkl')
joblib.dump(knn_model, knn_path)
print(f"✅ Model saved to {knn_path}")

# Evaluate
print("\nEvaluating...")
start_time = time.time()
y_pred_knn = knn_model.predict(X_val_scaled)
pred_time = time.time() - start_time

y_proba_knn = knn_model.predict_proba(X_val_scaled)

top1_acc_knn = accuracy_score(y_val, y_pred_knn)
top5_acc_knn = top_k_accuracy_score(y_val, y_proba_knn, k=5)

print(f"\n📊 KNN Results:")
print(f"   Top-1 Accuracy: {top1_acc_knn*100:.2f}%")
print(f"   Top-5 Accuracy: {top5_acc_knn*100:.2f}%")
print(f"   Training time: {train_time:.2f}s")
print(f"   Prediction time: {pred_time:.2f}s")

# Compare with Food-101 only results
print("\n" + "="*70)
print("COMPARISON SUMMARY")
print("="*70)
print("\nCombined Dataset (Food-101 + Moroccan):")
print(f"  Logistic C=0.01: {top1_acc*100:.2f}% top-1, {top5_acc*100:.2f}% top-5")
print(f"  KNN k=30:        {top1_acc_knn*100:.2f}% top-1, {top5_acc_knn*100:.2f}% top-5")

print("\nPrevious Food-101 Only Results (for reference):")
print(f"  Logistic C=0.01: 70.98% top-1, 91.05% top-5")
print(f"  KNN k=30:        55.92% top-1, 80.06% top-5")

print("\n📋 All files saved to D: drive:")
print(f"   Scaler: {scaler_path}")
print(f"   Logistic: {logistic_path}")
print(f"   KNN: {knn_path}")

print("\n" + "="*70)
print("✅ TRAINING COMPLETE!")
print("="*70)
