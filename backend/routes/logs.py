"""
Meal logs routes for tracking nutrition
GET /api/logs - Get logs for a date
POST /api/logs - Add new meal log
DELETE /api/logs/<id> - Delete log entry
GET /api/logs/summary - Get daily summary
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from ..utils import get_db_connection, get_dish, compute_scaled_nutrition

logs_bp = Blueprint('logs', __name__)

def get_logs_and_totals(user_id, date):
    """Helper to get logs and compute totals for a date."""
    conn = get_db_connection()
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
        dish = get_dish(row['dish_id'])
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
            'calories': round(totals['calories'] / goals['daily_calories'] * 100, 1) if goals['daily_calories'] > 0 else 0,
            'protein': round(totals['protein_g'] / goals['daily_protein_g'] * 100, 1) if goals['daily_protein_g'] > 0 else 0,
            'carbs': round(totals['carbs_g'] / goals['daily_carbs_g'] * 100, 1) if goals['daily_carbs_g'] > 0 else 0,
            'fat': round(totals['fat_g'] / goals['daily_fat_g'] * 100, 1) if goals['daily_fat_g'] > 0 else 0
        }
    
    return logs_list, totals, progress, goals

@logs_bp.route('/logs', methods=['GET', 'POST'])
def manage_logs():
    """Get logs for a date or add a new log entry."""
    user_id = 'default_user'
    
    if request.method == 'GET':
        date = request.args.get('date')
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        logs_list, totals, progress, goals = get_logs_and_totals(user_id, date)
        
        return jsonify({
            'date': date,
            'logs': logs_list,
            'totals': totals,
            'progress': progress
        })
    
    elif request.method == 'POST':
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        dish_id = data.get('dish_id')
        meal_type = data.get('meal_type', 'lunch')
        grams = data.get('grams', 100)
        
        if not dish_id:
            return jsonify({'error': 'dish_id is required'}), 400
        
        if not get_dish(dish_id):
            return jsonify({'error': f'Dish {dish_id} not found'}), 404
        
        conn = get_db_connection()
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

@logs_bp.route('/logs/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    """Delete a log entry."""
    user_id = 'default_user'
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM logs WHERE id = ? AND user_id = ?', (log_id, user_id))
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Log entry not found'}), 404
    
    conn.close()
    return jsonify({'success': True, 'message': 'Log deleted'})

@logs_bp.route('/logs/summary', methods=['GET'])
def logs_summary():
    """Get summary of logs for a date."""
    user_id = 'default_user'
    date = request.args.get('date')
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    
    logs_list, totals, progress, goals = get_logs_and_totals(user_id, date)
    
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
