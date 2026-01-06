"""
Dishes routes for food browsing
GET /api/dishes/all - Get all dishes
GET /api/dishes - Search dishes
GET /api/dishes/<id> - Get dish details
GET /api/dishes/<id>/nutrition - Get nutrition
GET /api/dishes/<id>/recipe - Get recipe
GET /api/dishes/<id>/ingredients - Get ingredients
GET /api/dishes/<id>/similar - Get similar dishes
"""
from flask import Blueprint, request, jsonify
from ..utils import get_dish, search_dishes, get_all_dishes_simplified

dishes_bp = Blueprint('dishes', __name__)

@dishes_bp.route('/dishes/all', methods=['GET'])
def get_all_dishes():
    """Get all dishes (simplified list for grid view)."""
    dishes_list = get_all_dishes_simplified()
    return jsonify({'dishes': dishes_list})

@dishes_bp.route('/dishes', methods=['GET'])
def search():
    """Search dishes by name."""
    query = request.args.get('search', '').strip()
    
    if not query:
        dishes_list = get_all_dishes_simplified()
        return jsonify({'dishes': dishes_list})
    
    results = search_dishes(query)
    simplified = [{
        'id': d['id'],
        'name': d['name'],
        'cuisine': d.get('cuisine', 'International'),
        'calories': d['nutrition']['calories']
    } for d in results]
    
    return jsonify({'dishes': simplified})

@dishes_bp.route('/dishes/<dish_id>', methods=['GET'])
def get_dish_details(dish_id):
    """Get complete dish details (nutrition, recipe, ingredients, similar)."""
    dish = get_dish(dish_id)
    
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

@dishes_bp.route('/dishes/<dish_id>/nutrition', methods=['GET'])
def get_nutrition(dish_id):
    """Get nutrition info for a dish."""
    dish = get_dish(dish_id)
    
    if not dish:
        return jsonify({'error': f'Dish {dish_id} not found'}), 404
    
    return jsonify(dish['nutrition'])

@dishes_bp.route('/dishes/<dish_id>/recipe', methods=['GET'])
def get_recipe(dish_id):
    """Get recipe for a dish."""
    dish = get_dish(dish_id)
    
    if not dish:
        return jsonify({'error': f'Dish {dish_id} not found'}), 404
    
    return jsonify(dish.get('recipe', {}))

@dishes_bp.route('/dishes/<dish_id>/ingredients', methods=['GET'])
def get_ingredients(dish_id):
    """Get ingredients for a dish."""
    dish = get_dish(dish_id)
    
    if not dish:
        return jsonify({'error': f'Dish {dish_id} not found'}), 404
    
    return jsonify({'ingredients': dish.get('ingredients', [])})

@dishes_bp.route('/dishes/<dish_id>/similar', methods=['GET'])
def get_similar(dish_id):
    """Get similar dishes."""
    dish = get_dish(dish_id)
    
    if not dish:
        return jsonify({'error': f'Dish {dish_id} not found'}), 404
    
    similar_ids = dish.get('similar_dishes', [])
    similar = []
    for sim_id in similar_ids:
        sim_dish = get_dish(sim_id)
        if sim_dish:
            similar.append({
                'id': sim_dish['id'],
                'name': sim_dish['name'],
                'cuisine': sim_dish.get('cuisine', 'International')
            })
    
    return jsonify({'similar_dishes': similar})
