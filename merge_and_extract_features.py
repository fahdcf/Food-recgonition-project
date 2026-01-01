"""
Merge Food-101 and Moroccan datasets, then extract ResNet50 features
Using the same batch processing method as the original Food-101 extraction
"""
import os
import numpy as np
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

print("="*70)
print("🚀 Combined Dataset Feature Extraction - ResNet50")
print("="*70)

# Paths
food101_root = "D:/food_dataset/images"
moroccan_root = "D:/moroccan_food_images"
output_dir = "D:/food_recognition_models/features"
cache_dir = "D:/food_recognition_models/cache"  # For incremental saves
os.makedirs(output_dir, exist_ok=True)
os.makedirs(cache_dir, exist_ok=True)

# Check GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"\n🔧 Device: {device}")
if torch.cuda.is_available():
    print(f"   GPU: {torch.cuda.get_device_name(0)}")

# Load ResNet50
print("\n🏗️  Loading ResNet50...")
resnet = models.resnet50(pretrained=True)
resnet = nn.Sequential(*list(resnet.children())[:-1])
resnet = resnet.to(device)
resnet.eval()
print("   ✅ ResNet50 loaded")

# Image preprocessing (same as original)
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def load_existing_features(cache_dir, split):
    """Load existing cached features if available"""
    cache_file = os.path.join(cache_dir, f'{split}_cache.npz')
    if os.path.exists(cache_file):
        print(f"\n💾 Found existing cache: {cache_file}")
        data = np.load(cache_file, allow_pickle=True)
        # Convert back from single array to list format
        features = data['features'].tolist() if len(data['features']) > 0 else []
        return {
            'features': features,
            'labels': data['labels'].tolist(),
            'processed_classes': set(data['processed_classes'])
        }
    return {'features': [], 'labels': [], 'processed_classes': set()}

def save_incremental_cache(cache_dir, split, features, labels, processed_classes):
    """Save features incrementally to prevent data loss"""
    cache_file = os.path.join(cache_dir, f'{split}_cache.npz')
    # Combine features into single array for saving
    if len(features) > 0:
        combined_features = np.vstack(features)
    else:
        combined_features = np.array([])
    
    np.savez_compressed(cache_file, 
                       features=combined_features, 
                       labels=np.array(labels), 
                       processed_classes=np.array(list(processed_classes)))
    print(f"   💾 Saved checkpoint to cache")

def collect_and_extract_features_incremental(food101_root, moroccan_root, split, cache_dir):
    """Collect paths and extract features class by class with incremental saving"""
    
    # Load existing cache
    cache_data = load_existing_features(cache_dir, split)
    
    # If we have cached features, convert them properly
    if len(cache_data['features']) > 0:
        # Features come back as a single array, we need to keep them as list
        all_features = [cache_data['features']]
    else:
        all_features = []
    
    all_labels = list(cache_data['labels']) if len(cache_data['labels']) > 0 else []
    processed_classes = cache_data['processed_classes']
    
    class_names = []
    
    # Food-101 split mapping
    food101_split = 'train' if split == 'train' else 'test'
    food101_path = os.path.join(food101_root, food101_split)
    
    # Process Food-101 classes FIRST (larger dataset)
    if os.path.exists(food101_path):
        food101_classes = sorted(os.listdir(food101_path))
        print(f"\n📂 Processing Food-101 {split} set...")
        print(f"   Total Food-101 classes: {len(food101_classes)}")
        
        for class_name in food101_classes:
            class_path = os.path.join(food101_path, class_name)
            if not os.path.isdir(class_path):
                continue
            
            class_names.append(class_name)
            class_idx = len(class_names) - 1
            
            # Skip if already processed
            if class_name in processed_classes:
                print(f"   ✓ Skipping {class_name} (already processed)")
                continue
            
            # Collect images for this class
            images = []
            for img_name in os.listdir(class_path):
                img_path = os.path.join(class_path, img_name)
                if img_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                    images.append(img_path)
            
            if len(images) == 0:
                continue
            
            # Extract features for this class
            print(f"   Processing {class_name}: {len(images)} images...")
            class_features, class_labels = extract_features_batch(images, [class_idx]*len(images), class_name, batch_size=16)
            
            # Append to results
            all_features.append(class_features)
            all_labels.extend(class_labels)
            processed_classes.add(class_name)
            
            # Save checkpoint after each class
            save_incremental_cache(cache_dir, split, all_features, all_labels, processed_classes)
    
    # Moroccan split mapping
    moroccan_split = 'train' if split == 'train' else 'validation'
    moroccan_path = os.path.join(moroccan_root, moroccan_split)
    
    # Process Moroccan classes AFTER Food-101
    if os.path.exists(moroccan_path):
        moroccan_classes = sorted(os.listdir(moroccan_path))
        print(f"\n📂 Processing Moroccan {split} set...")
        print(f"   Total Moroccan classes: {len(moroccan_classes)}")
        
        for class_name in moroccan_classes:
            class_path = os.path.join(moroccan_path, class_name)
            if not os.path.isdir(class_path):
                continue
            
            full_class_name = f"moroccan_{class_name}"
            class_names.append(full_class_name)
            class_idx = len(class_names) - 1
            
            # Skip if already processed
            if full_class_name in processed_classes:
                print(f"   ✓ Skipping {full_class_name} (already processed)")
                continue
            
            # Collect images for this class
            images = []
            for img_name in os.listdir(class_path):
                img_path = os.path.join(class_path, img_name)
                if img_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                    images.append(img_path)
            
            if len(images) == 0:
                continue
            
            # Extract features for this class
            print(f"   Processing {full_class_name}: {len(images)} images...")
            class_features, class_labels = extract_features_batch(images, [class_idx]*len(images), full_class_name, batch_size=16)
            
            # Append to results
            all_features.append(class_features)
            all_labels.extend(class_labels)
            processed_classes.add(full_class_name)
            
            # Save checkpoint after each class
            save_incremental_cache(cache_dir, split, all_features, all_labels, processed_classes)
    
    # Combine all features
    if isinstance(all_features[0], list):
        all_features = [f for f in all_features if len(f) > 0]
    X = np.vstack(all_features)
    y = np.array(all_labels)
    
    return X, y, class_names

def extract_features_batch(image_paths, labels, split_name, batch_size=16):
    """Extract features using batch processing (same as original method)"""
    print(f"\n📊 Extracting features from {split_name}...")
    
    features_list = []
    labels_list = []
    total = len(image_paths)
    
    for i in range(0, total, batch_size):
        if i % (batch_size * 20) == 0 or i == 0:
            print(f"   Progress: {i}/{total} ({i*100//total}%)")
        
        batch_end = min(i + batch_size, total)
        batch_tensors = []
        batch_labels = []
        
        # Load batch of images
        for idx in range(i, batch_end):
            try:
                img = Image.open(image_paths[idx]).convert('RGB')
                img_tensor = preprocess(img)
                batch_tensors.append(img_tensor)
                batch_labels.append(labels[idx])
            except Exception as e:
                print(f"   ⚠️  Skipping {image_paths[idx]}: {e}")
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

# Process training set
print("\n" + "="*70)
print("PROCESSING TRAINING SET")
print("="*70)
X_train, y_train, class_names = collect_and_extract_features_incremental(food101_root, moroccan_root, 'train', cache_dir)

# Save final training features
train_feat_path = os.path.join(output_dir, 'combined_train_features.npy')
train_label_path = os.path.join(output_dir, 'combined_train_labels.npy')
np.save(train_feat_path, X_train)
np.save(train_label_path, y_train)
print(f"\n💾 Saved training features: {X_train.shape}")
print(f"   {train_feat_path}")

# Process validation set
print("\n" + "="*70)
print("PROCESSING VALIDATION SET")
print("="*70)
X_val, y_val, _ = collect_and_extract_features_incremental(food101_root, moroccan_root, 'test', cache_dir)

# Save final validation features
val_feat_path = os.path.join(output_dir, 'combined_val_features.npy')
val_label_path = os.path.join(output_dir, 'combined_val_labels.npy')
np.save(val_feat_path, X_val)
np.save(val_label_path, y_val)
print(f"\n💾 Saved validation features: {X_val.shape}")
print(f"   {val_feat_path}")

# Save class names
class_names_path = os.path.join(output_dir, 'combined_class_names.npy')
np.save(class_names_path, class_names)
print(f"\n📋 Class summary:")
print(f"   Total classes: {len(class_names)}")
print(f"   Food-101: {sum(1 for c in class_names if not c.startswith('moroccan_'))}")
print(f"   Moroccan: {sum(1 for c in class_names if c.startswith('moroccan_'))}")
print("\n   Moroccan classes:")
for c in class_names:
    if c.startswith('moroccan_'):
        print(f"     - {c}")

print("\n" + "="*70)
print("✅ FEATURE EXTRACTION COMPLETE!")
print("="*70)
