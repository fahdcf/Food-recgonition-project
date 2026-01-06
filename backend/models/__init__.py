"""
Model loading and inference for food recognition
"""
import os
import numpy as np
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import joblib

# Model paths (adjust if needed based on your setup)
MODEL_DIR = "D:/food_recognition_models/combined_models"
FEATURE_DIR = "D:/food_recognition_models/features"

# Global model instances
_model = None
_scaler = None
_resnet = None
_class_names = None
_device = None

def get_device():
    """Get the device (CPU or GPU)."""
    global _device
    if _device is None:
        _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return _device

def load_model():
    """Load the Logistic Regression model and scaler."""
    global _model, _scaler, _class_names
    
    if _model is not None:
        return _model, _scaler, _class_names
    
    print("Loading model...")
    _model = joblib.load(os.path.join(MODEL_DIR, 'Logistic_C0.01.pkl'))
    _scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
    _class_names = np.load(os.path.join(FEATURE_DIR, 'final_class_names.npy'), allow_pickle=True)
    print(f"✅ Model loaded! {len(_class_names)} classes")
    
    return _model, _scaler, _class_names

def load_resnet():
    """Load ResNet50 for feature extraction."""
    global _resnet
    
    if _resnet is not None:
        return _resnet
    
    print("Loading ResNet50...")
    device = get_device()
    _resnet = models.resnet50(pretrained=True)
    _resnet = nn.Sequential(*list(_resnet.children())[:-1])
    _resnet = _resnet.to(device)
    _resnet.eval()
    print(f"✅ ResNet50 loaded on {device}")
    
    return _resnet

def get_preprocess_transforms():
    """Get image preprocessing transforms."""
    return transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

def extract_features(image):
    """Extract ResNet50 features from a PIL Image."""
    resnet = load_resnet()
    device = get_device()
    preprocess = get_preprocess_transforms()
    
    img_tensor = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        features = resnet(img_tensor)
    features = features.squeeze().cpu().numpy()
    return features.reshape(1, -1)

def predict_image(image):
    """Predict food class from image."""
    model, scaler, class_names = load_model()
    
    # Extract features
    features = extract_features(image)
    
    # Normalize
    features_scaled = scaler.transform(features)
    
    # Get top-5 predictions
    probabilities = model.predict_proba(features_scaled)[0]
    top5_indices = np.argsort(probabilities)[-5:][::-1]
    
    predictions = []
    for idx in top5_indices:
        class_name = class_names[idx]
        # Clean up class name for display
        if class_name.startswith('moroccan_'):
            # Moroccan dishes: "moroccan_tagine" -> "Moroccan Tagine"
            display_name = class_name.replace('moroccan_', 'Moroccan ').replace('_', ' ').title()
        else:
            # Food-101 dishes: "apple_pie" -> "Apple Pie"
            display_name = class_name.replace('_', ' ').title()
        
        predictions.append({
            'class': display_name,
            'confidence': float(probabilities[idx] * 100),
            'class_id': class_name
        })
    
    return predictions

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg']
