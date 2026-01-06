"""
User goals routes for nutrition targets
GET /api/user/goals - Get user goals
PUT /api/user/goals - Update user goals
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from ..utils import get_db_connection

goals_bp = Blueprint('goals', __name__)

@goals_bp.route('/user/goals', methods=['GET', 'PUT'])
def user_goals():
    """Get or update user nutrition goals."""
    user_id = 'default_user'
    
    if request.method == 'GET':
        conn = get_db_connection()
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
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        conn = get_db_connection()
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
