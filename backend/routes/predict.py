"""
Prediction routes for food recognition
POST /api/predict - Predict food from image
"""
from flask import Blueprint, request, jsonify
import io
from PIL import Image
from ..models import predict_image, allowed_file

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction."""
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

@predict_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    from ..models import load_model, get_device
    model, _, class_names = load_model()
    device = get_device()
    
    return jsonify({
        'status': 'healthy',
        'model': 'Logistic Regression C=0.01',
        'classes': len(class_names),
        'device': str(device)
    })
