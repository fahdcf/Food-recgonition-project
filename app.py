"""
Flask API for Food Recognition
Frontend served separately (React)
"""
from flask import Flask, request, jsonify, send_from_directory
import os
import json
import sqlite3
from datetime import datetime
import numpy as np
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import joblib
import io

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "food_app.db")

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# ==================== DATABASE SETUP ====================

def init_db():
    """Initialize SQLite database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # User goals table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_goals (
            id INTEGER PRIMARY KEY,
            user_id TEXT DEFAULT 'default_user',
            daily_calories INTEGER DEFAULT 2000,
            daily_protein_g INTEGER DEFAULT 150,
            daily_carbs_g INTEGER DEFAULT 200,
            daily_fat_g INTEGER DEFAULT 65,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Meal logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY,
            user_id TEXT DEFAULT 'default_user',
            dish_id TEXT NOT NULL,
            meal_type TEXT CHECK(meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
            grams INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )
    ''')
    
    # Initialize default user goals if not exists
    cursor.execute('SELECT * FROM user_goals WHERE user_id = ?', ('default_user',))
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO user_goals 
            (user_id, daily_calories, daily_protein_g, daily_carbs_g, daily_fat_g)
            VALUES (?, ?, ?, ?, ?)
        ''', ('default_user', 2000, 150, 200, 65))
    
    conn.commit()
    conn.close()
    print("✅ Database initialized")

# Initialize database on startup
init_db()

# Load dishes metadata
def load_dishes():
    """Load dishes.json metadata."""
    dishes_path = os.path.join(DATA_DIR, 'dishes.json')
    if os.path.exists(dishes_path):
        with open(dishes_path, 'r') as f:
            data = json.load(f)
            return {dish['id']: dish for dish in data.get('dishes', [])}
    return {}

dishes_db = load_dishes()
print(f"✅ Loaded {len(dishes_db)} dishes from metadata")

# ==================== MODEL SETUP ====================

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
            'confidence': float(probabilities[idx] * 100),
            'class_id': class_name
        })
    
    return predictions

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg']

@app.route('/')
def index():
    """Serve React frontend"""
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route('/assets/<path:path>')
def serve_static(path):
    """Serve static assets for the React frontend"""
    return send_from_directory(FRONTEND_DIR, path)

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


# ==================== USER GOALS API ====================

@app.route('/api/user/goals', methods=['GET', 'PUT'])
def user_goals():
    """Get or update user nutrition goals."""
    user_id = 'default_user'
    
    if request.method == 'GET':
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_goals WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return jsonify({
                'id': row['id'],
                'daily_calories': row['daily_calories'],
                'daily_protein_g': row['daily_protein_g'],
                'daily_carbs_g': row['daily_carbs_g'],
                'daily_fat_g': row['daily_fat_g']
            })
        else:
            return jsonify({'error': 'User goals not found'}), 404
    
    elif request.method == 'PUT':
        data = request.get_json()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE user_goals 
            SET daily_calories=?, daily_protein_g=?, daily_carbs_g=?, daily_fat_g=?, updated_at=CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (
            data.get('daily_calories', 2000),
            data.get('daily_protein_g', 150),
            data.get('daily_carbs_g', 200),
            data.get('daily_fat_g', 65),
            user_id
        ))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Goals updated'})


# ==================== DISHES API ====================

@app.route('/api/dishes/all', methods=['GET'])
def get_all_dishes():
    """Get all dishes (simplified list)."""
    dishes_list = []
    for dish_id, dish in dishes_db.items():
        dishes_list.append({
            'id': dish['id'],
            'name': dish['name'],
            'cuisine': dish.get('cuisine', 'International'),
            'calories': dish['nutrition']['calories']
        })
    return jsonify({'dishes': dishes_list})


@app.route('/api/dishes', methods=['GET'])
def search_dishes():
    """Search dishes by name."""
    query = request.args.get('search', '').lower()
    results = []
    
    for dish_id, dish in dishes_db.items():
        if query in dish['name'].lower() or query in dish['id'].lower():
            results.append({
                'id': dish['id'],
                'name': dish['name'],
                'cuisine': dish.get('cuisine', 'International'),
                'calories': dish['nutrition']['calories']
            })
    
    return jsonify({'dishes': results})


@app.route('/api/dishes/<dish_id>', methods=['GET'])
def get_dish_details(dish_id):
    """Get complete dish details (nutrition, recipe, ingredients, similar)."""
    dish = dishes_db.get(dish_id)
    
    if not dish:
        return jsonify({'error': f'Dish {dish_id} not found'}), 404
    
    return jsonify({
        'id': dish['id'],
        'name': dish['name'],
        'cuisine': dish.get('cuisine', 'International'),
        'nutrition': dish['nutrition'],
        'ingredients': dish.get('ingredients', []),
        'recipe': dish.get('recipe', {}),
        'similar_dishes': dish.get('similar_dishes', [])
    })


@app.route('/api/dishes/<dish_id>/nutrition', methods=['GET'])
def get_dish_nutrition(dish_id):
    """Get nutrition info for a dish."""
    dish = dishes_db.get(dish_id)
    
    if not dish:
        return jsonify({'error': f'Dish {dish_id} not found'}), 404
    
    return jsonify(dish['nutrition'])


@app.route('/api/dishes/<dish_id>/recipe', methods=['GET'])
def get_dish_recipe(dish_id):
    """Get recipe for a dish."""
    dish = dishes_db.get(dish_id)
    
    if not dish:
        return jsonify({'error': f'Dish {dish_id} not found'}), 404
    
    return jsonify(dish.get('recipe', {}))


@app.route('/api/dishes/<dish_id>/ingredients', methods=['GET'])
def get_dish_ingredients(dish_id):
    """Get ingredients for a dish."""
    dish = dishes_db.get(dish_id)
    
    if not dish:
        return jsonify({'error': f'Dish {dish_id} not found'}), 404
    
    return jsonify({'ingredients': dish.get('ingredients', [])})


@app.route('/api/dishes/<dish_id>/similar', methods=['GET'])
def get_similar_dishes(dish_id):
    """Get similar dishes."""
    dish = dishes_db.get(dish_id)
    
    if not dish:
        return jsonify({'error': f'Dish {dish_id} not found'}), 404
    
    similar_ids = dish.get('similar_dishes', [])
    similar = []
    for sim_id in similar_ids:
        if sim_id in dishes_db:
            sim_dish = dishes_db[sim_id]
            similar.append({
                'id': sim_dish['id'],
                'name': sim_dish['name'],
                'cuisine': sim_dish.get('cuisine', 'International')
            })
    
    return jsonify({'similar_dishes': similar})


# ==================== MEAL LOGS API ====================

def compute_scaled_nutrition(dish_id, grams):
    """Compute scaled nutrition based on portion size."""
    dish = dishes_db.get(dish_id)
    if not dish:
        return None
    
    nutrition = dish['nutrition']
    base_serving = nutrition['serving_size_g']
    
    factor = grams / base_serving
    return {
        'calories': round(nutrition['calories'] * factor, 1),
        'protein_g': round(nutrition['protein_g'] * factor, 1),
        'carbs_g': round(nutrition['carbs_g'] * factor, 1),
        'fat_g': round(nutrition['fat_g'] * factor, 1)
    }


@app.route('/api/logs', methods=['GET', 'POST'])
def manage_logs():
    """Get logs for a date or add a new log entry."""
    user_id = 'default_user'
    
    if request.method == 'GET':
        date = request.args.get('date')
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get logs for the date
        cursor.execute('''
            SELECT id, dish_id, meal_type, grams, created_at FROM logs
            WHERE user_id = ? AND DATE(created_at) = ?
            ORDER BY created_at ASC
        ''', (user_id, date))
        
        rows = cursor.fetchall()
        logs_list = []
        totals = {'calories': 0, 'protein_g': 0, 'carbs_g': 0, 'fat_g': 0}
        
        for row in rows:
            dish = dishes_db.get(row['dish_id'])
            scaled = compute_scaled_nutrition(row['dish_id'], row['grams'])
            
            if scaled:
                logs_list.append({
                    'id': row['id'],
                    'dish_id': row['dish_id'],
                    'dish_name': dish['name'] if dish else 'Unknown',
                    'meal_type': row['meal_type'],
                    'grams': row['grams'],
                    'created_at': row['created_at'],
                    'nutrition': scaled
                })
                
                totals['calories'] += scaled['calories']
                totals['protein_g'] += scaled['protein_g']
                totals['carbs_g'] += scaled['carbs_g']
                totals['fat_g'] += scaled['fat_g']
        
        # Get user goals
        cursor.execute('SELECT * FROM user_goals WHERE user_id = ?', (user_id,))
        goals = cursor.fetchone()
        conn.close()
        
        # Calculate progress
        progress = {}
        if goals:
            progress = {
                'calories': round(totals['calories'] / goals['daily_calories'] * 100, 1),
                'protein': round(totals['protein_g'] / goals['daily_protein_g'] * 100, 1),
                'carbs': round(totals['carbs_g'] / goals['daily_carbs_g'] * 100, 1),
                'fat': round(totals['fat_g'] / goals['daily_fat_g'] * 100, 1)
            }
        
        return jsonify({
            'date': date,
            'logs': logs_list,
            'totals': totals,
            'progress': progress
        })
    
    elif request.method == 'POST':
        data = request.get_json()
        dish_id = data.get('dish_id')
        meal_type = data.get('meal_type', 'lunch')
        grams = data.get('grams', 100)
        
        if not dish_id:
            return jsonify({'error': 'dish_id is required'}), 400
        
        if dish_id not in dishes_db:
            return jsonify({'error': f'Dish {dish_id} not found'}), 404
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO logs (user_id, dish_id, meal_type, grams)
            VALUES (?, ?, ?, ?)
        ''', (user_id, dish_id, meal_type, grams))
        conn.commit()
        
        log_id = cursor.lastrowid
        conn.close()
        
        scaled = compute_scaled_nutrition(dish_id, grams)
        
        return jsonify({
            'success': True,
            'id': log_id,
            'nutrition': scaled
        }), 201


@app.route('/api/logs/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    """Delete a log entry."""
    user_id = 'default_user'
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM logs WHERE id = ? AND user_id = ?', (log_id, user_id))
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Log entry not found'}), 404
    
    conn.close()
    return jsonify({'success': True, 'message': 'Log deleted'})


@app.route('/api/logs/summary', methods=['GET'])
def logs_summary():
    """Get summary of logs for a date."""
    user_id = 'default_user'
    date = request.args.get('date')
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM logs
        WHERE user_id = ? AND DATE(created_at) = ?
    ''', (user_id, date))
    
    rows = cursor.fetchall()
    totals = {'calories': 0, 'protein_g': 0, 'carbs_g': 0, 'fat_g': 0}
    
    for row in rows:
        scaled = compute_scaled_nutrition(row['dish_id'], row['grams'])
        if scaled:
            for key in totals:
                totals[key] += scaled[key]
    
    # Get goals
    cursor.execute('SELECT * FROM user_goals WHERE user_id = ?', (user_id,))
    goals = cursor.fetchone()
    conn.close()
    
    progress = {}
    if goals:
        progress = {
            'calories': round(totals['calories'] / goals['daily_calories'] * 100, 1),
            'protein': round(totals['protein_g'] / goals['daily_protein_g'] * 100, 1),
            'carbs': round(totals['carbs_g'] / goals['daily_carbs_g'] * 100, 1),
            'fat': round(totals['fat_g'] / goals['daily_fat_g'] * 100, 1)
        }
    
    return jsonify({
        'date': date,
        'totals': totals,
        'goals': {
            'daily_calories': goals['daily_calories'],
            'daily_protein_g': goals['daily_protein_g'],
            'daily_carbs_g': goals['daily_carbs_g'],
            'daily_fat_g': goals['daily_fat_g']
        } if goals else {},
        'progress': progress
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
