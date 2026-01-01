"""
Merge existing Food-101 features with newly extracted Moroccan features
"""
import os
import numpy as np

print("="*70)
print("🔗 Merging Food-101 and Moroccan Features")
print("="*70)

feature_dir = "D:/food_recognition_models/features"

# Load Food-101 features
print("\n📂 Loading Food-101 features...")
food101_train_features = np.load(os.path.join(feature_dir, 'train_features.npy'))
food101_train_labels = np.load(os.path.join(feature_dir, 'train_labels.npy'))
food101_val_features = np.load(os.path.join(feature_dir, 'val_features.npy'))
food101_val_labels = np.load(os.path.join(feature_dir, 'val_labels.npy'))

print(f"   Train: {food101_train_features.shape}")
print(f"   Val: {food101_val_features.shape}")

# Load Moroccan features (just extracted)
print("\n📂 Loading Moroccan features...")
moroccan_train_features = np.load(os.path.join(feature_dir, 'combined_train_features.npy'))
moroccan_train_labels = np.load(os.path.join(feature_dir, 'combined_train_labels.npy'))
moroccan_val_features = np.load(os.path.join(feature_dir, 'combined_val_features.npy'))
moroccan_val_labels = np.load(os.path.join(feature_dir, 'combined_val_labels.npy'))

print(f"   Train: {moroccan_train_features.shape}")
print(f"   Val: {moroccan_val_features.shape}")

# Food-101 has 101 classes (labels 0-100)
# Moroccan classes should start from 101
num_food101_classes = 101
moroccan_train_labels_adjusted = moroccan_train_labels + num_food101_classes
moroccan_val_labels_adjusted = moroccan_val_labels + num_food101_classes

# Merge training features
print("\n🔗 Merging training sets...")
merged_train_features = np.vstack([food101_train_features, moroccan_train_features])
merged_train_labels = np.concatenate([food101_train_labels, moroccan_train_labels_adjusted])

print(f"   Merged train features: {merged_train_features.shape}")
print(f"   Merged train labels: {merged_train_labels.shape}")

# Merge validation features
print("\n🔗 Merging validation sets...")
merged_val_features = np.vstack([food101_val_features, moroccan_val_features])
merged_val_labels = np.concatenate([food101_val_labels, moroccan_val_labels_adjusted])

print(f"   Merged val features: {merged_val_features.shape}")
print(f"   Merged val labels: {merged_val_labels.shape}")

# Create class names list
print("\n📋 Creating class names...")
# We need to get Food-101 class names - they should be in order 0-100
# For now, create generic names
food101_class_names = [f"food101_class_{i}" for i in range(101)]
moroccan_class_names = [
    "moroccan_bissara",
    "moroccan_couscous", 
    "moroccan_harira",
    "moroccan_kefta_tagine",
    "moroccan_msemmen",
    "moroccan_pastilla",
    "moroccan_rfissa",
    "moroccan_tagine",
    "moroccan_zaalouk"
]

all_class_names = food101_class_names + moroccan_class_names

print(f"   Total classes: {len(all_class_names)}")
print(f"   Food-101: {len(food101_class_names)}")
print(f"   Moroccan: {len(moroccan_class_names)}")

# Save merged features
print("\n💾 Saving merged features...")
train_path = os.path.join(feature_dir, 'final_train_features.npy')
train_label_path = os.path.join(feature_dir, 'final_train_labels.npy')
val_path = os.path.join(feature_dir, 'final_val_features.npy')
val_label_path = os.path.join(feature_dir, 'final_val_labels.npy')
class_names_path = os.path.join(feature_dir, 'final_class_names.npy')

np.save(train_path, merged_train_features)
np.save(train_label_path, merged_train_labels)
np.save(val_path, merged_val_features)
np.save(val_label_path, merged_val_labels)
np.save(class_names_path, all_class_names)

print(f"   ✅ {train_path}")
print(f"   ✅ {train_label_path}")
print(f"   ✅ {val_path}")
print(f"   ✅ {val_label_path}")
print(f"   ✅ {class_names_path}")

print("\n" + "="*70)
print("✅ MERGE COMPLETE!")
print("="*70)
print(f"\nFinal dataset: {len(all_class_names)} classes")
print(f"   Training samples: {len(merged_train_labels)}")
print(f"   Validation samples: {len(merged_val_labels)}")
