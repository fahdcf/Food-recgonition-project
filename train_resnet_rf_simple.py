"""
Food Recognition - ResNet50 + Random Forest (Memory-Efficient)
Loads images on-the-fly without loading entire dataset into RAM
"""
import os
import numpy as np
import json
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, top_k_accuracy_score
import joblib
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from datasets import load_from_disk

print("="*70)
print("🚀 Food Recognition - ResNet50 + GPU + Random Forest (Memory-Efficient)")
print("="*70)

# Paths
FEATURE_CACHE_DIR = "D:/food_recognition_models/features"
MODEL_DIR = "D:/food_recognition_models"
os.makedirs(FEATURE_CACHE_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# Check GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"\n🔧 Device: {device}")
if torch.cuda.is_available():
    print(f"   GPU: {torch.cuda.get_device_name(0)}")
else:
    print("   ⚠️  No GPU - using CPU")

# Load ResNet50
print("\n🏗️  Loading ResNet50...")
resnet = models.resnet50(pretrained=True)
resnet = nn.Sequential(*list(resnet.children())[:-1])
resnet = resnet.to(device)
resnet.eval()
print("   ✅ ResNet50 loaded")

# Image preprocessing
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def extract_features_from_dataset(dataset, split_name, batch_size=16):
    """Extract features from dataset iterator (memory-efficient)"""
    print(f"\n📊 Extracting features from {split_name}...")
    
    features_list = []
    labels_list = []
    total = len(dataset)
    
    for i in range(0, total, batch_size):
        if i % (batch_size * 20) == 0 or i == 0:
            print(f"   Progress: {i}/{total} ({i*100//total}%)")
        
        batch_end = min(i + batch_size, total)
        batch_tensors = []
        batch_labels = []
        
        # Load batch of images
        for idx in range(i, batch_end):
            try:
                item = dataset[idx]
                img = item['image'].convert('RGB')
                img_tensor = preprocess(img)
                batch_tensors.append(img_tensor)
                batch_labels.append(item['label'])
            except Exception as e:
                print(f"   ⚠️  Skipping index {idx}: {e}")
                continue
        
        if not batch_tensors:
            continue
        
        # Process batch on GPU
        batch = torch.stack(batch_tensors).to(device)
        with torch.no_grad():
            batch_features = resnet(batch)
        
        batch_features = batch_features.squeeze().cpu().numpy()
        if batch_features.ndim == 1:
            batch_features = batch_features.reshape(1, -1)
        
        features_list.append(batch_features)
        labels_list.extend(batch_labels)
        
        # Clear GPU cache
        if i % (batch_size * 50) == 0 and i > 0:
            torch.cuda.empty_cache()
    
    print(f"   Progress: {total}/{total} (100%) ✓")
    
    X = np.vstack(features_list)
    y = np.array(labels_list)
    return X, y

# Check for cached features
train_feat_path = os.path.join(FEATURE_CACHE_DIR, "train_features.npy")
train_label_path = os.path.join(FEATURE_CACHE_DIR, "train_labels.npy")
val_feat_path = os.path.join(FEATURE_CACHE_DIR, "val_features.npy")
val_label_path = os.path.join(FEATURE_CACHE_DIR, "val_labels.npy")

if os.path.exists(train_feat_path) and os.path.exists(val_feat_path):
    print("\n💾 Loading cached features from D: drive...")
    X_train = np.load(train_feat_path)
    y_train = np.load(train_label_path)
    X_val = np.load(val_feat_path)
    y_val = np.load(val_label_path)
    print(f"   ✅ Train: {X_train.shape}, Val: {X_val.shape}")
else:
    # Load dataset paths
    print("\n📂 Loading dataset paths (NOT loading images yet)...")
    dataset_index_path = "food101_extended_dataset/dataset_index.json"
    with open(dataset_index_path) as f:
        index = json.load(f)
    
    num_classes = index['num_classes']
    class_names = index['class_names']
    food101_path = index['food101_path']
    
    print(f"   Classes: {num_classes}")
    print(f"   Moroccan dishes: {class_names[101:]}")
    
    # Load Food-101 dataset (this uses lazy loading - doesn't load all images)
    print(f"\n📂 Opening Food-101 dataset from {food101_path}...")
    food101 = load_from_disk(food101_path)
    
    train_dataset = food101['train']
    val_dataset = food101['validation']
    
    print(f"   Train samples: {len(train_dataset)}")
    print(f"   Val samples: {len(val_dataset)}")
    
    # Extract features (processes images in batches)
    X_train, y_train = extract_features_from_dataset(train_dataset, "TRAIN", batch_size=16)
    print(f"   ✅ Train features: {X_train.shape}")
    
    # Save immediately
    np.save(train_feat_path, X_train)
    np.save(train_label_path, y_train)
    print(f"   💾 Saved to {train_feat_path}")
    
    X_val, y_val = extract_features_from_dataset(val_dataset, "VALIDATION", batch_size=16)
    print(f"   ✅ Val features: {X_val.shape}")
    
    # Save immediately
    np.save(val_feat_path, X_val)
    np.save(val_label_path, y_val)
    print(f"   💾 Saved to {val_feat_path}")
    
    print(f"\n✅ Dataset already includes all {num_classes} classes (Food-101 + Moroccan merged)")
    print(f"   No need to load Moroccan images separately!")

# Normalize
print("\n📈 Normalizing features...")
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)
print(f"   ✅ Mean: {X_train.mean():.4f}, Std: {X_train.std():.4f}")

# Train Random Forest
print("\n" + "="*70)
print("🌲 Training Random Forest Classifier")
print("="*70)
print(f"   Training samples: {X_train.shape[0]}")
print(f"   Features per sample: {X_train.shape[1]}")
print(f"   Classes: {len(np.unique(y_train))}")

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=50,
    min_samples_split=5,
    min_samples_leaf=2,
    n_jobs=-1,
    random_state=42,
    verbose=1
)

print("\n   Training started...")
model.fit(X_train, y_train)
print("   ✅ Training complete!")

# Evaluate
print("\n" + "="*70)
print("📊 Evaluation Results")
print("="*70)

y_pred = model.predict(X_val)
acc = accuracy_score(y_val, y_pred)

# Top-5 accuracy
y_proba = model.predict_proba(X_val)
top5_acc = top_k_accuracy_score(y_val, y_proba, k=5)

print(f"   Top-1 Accuracy: {acc*100:.2f}%")
print(f"   Top-5 Accuracy: {top5_acc*100:.2f}%")

# Save models
print("\n💾 Saving models to D: drive...")
model_path = os.path.join(MODEL_DIR, "resnet_rf_model.pkl")
scaler_path = os.path.join(MODEL_DIR, "resnet_rf_scaler.pkl")

joblib.dump(model, model_path)
joblib.dump(scaler, scaler_path)

print(f"   ✅ Model saved: {model_path}")
print(f"   ✅ Scaler saved: {scaler_path}")

print("\n" + "="*70)
print("✅ TRAINING COMPLETE!")
print("="*70)
print(f"   Models saved to: {MODEL_DIR}")
print(f"   Features cached to: {FEATURE_CACHE_DIR}")
print(f"   Next run will load features instantly from disk!")
