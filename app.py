"""
Flask Web App for Food Recognition
Upload an image and get predictions from the trained model
"""
from flask import Flask, render_template, request, jsonify
import os
import numpy as np
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import joblib
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Paths
MODEL_DIR = "D:/food_recognition_models/combined_models"
FEATURE_DIR = "D:/food_recognition_models/features"

# Load model and scaler
print("Loading model...")
model = joblib.load(os.path.join(MODEL_DIR, 'Logistic_C0.01.pkl'))
scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
class_names = np.load(os.path.join(FEATURE_DIR, 'final_class_names.npy'), allow_pickle=True)
print(f"✅ Model loaded! {len(class_names)} classes")

# Load ResNet50 for feature extraction
print("Loading ResNet50...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
resnet = models.resnet50(pretrained=True)
resnet = nn.Sequential(*list(resnet.children())[:-1])
resnet = resnet.to(device)
resnet.eval()
print(f"✅ ResNet50 loaded on {device}")

# Image preprocessing
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def extract_features(image):
    """Extract ResNet50 features from a PIL Image"""
    img_tensor = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        features = resnet(img_tensor)
    features = features.squeeze().cpu().numpy()
    return features.reshape(1, -1)

def predict_image(image):
    """Predict food class from image"""
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
            'confidence': float(probabilities[idx] * 100)
        })
    
    return predictions

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg']

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@app.route('/api/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload a JPG or PNG image'}), 400
    
    try:
        # Read image
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        # Get predictions
        predictions = predict_image(image)
        
        return jsonify({
            'success': True,
            'predictions': predictions
        })
    
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model': 'Logistic Regression C=0.01',
        'classes': len(class_names),
        'device': str(device)
    })

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 Food Recognition App Starting...")
    print("="*70)
    print(f"📊 Model: Logistic Regression (C=0.01)")
    print(f"🏷️  Classes: {len(class_names)} (101 Food-101 + 9 Moroccan)")
    print(f"🔧 Device: {device}")
    print("="*70)
    print("\n🌐 Open your browser and go to: http://localhost:5000")
    print("\n")
    
    app.run(host='0.0.0.0', port=5000, use_reloader=False)
