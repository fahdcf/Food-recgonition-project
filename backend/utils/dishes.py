"""
Dishes data loader and utilities
"""
import json
import os

def get_dishes_json_path():
    """Get the dishes.json path."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, 'data', 'dishes.json')

DISHES_JSON_PATH = get_dishes_json_path()
_dishes_cache = None

def load_dishes():
    """Load dishes.json metadata into memory."""
    global _dishes_cache
    
    if _dishes_cache is not None:
        return _dishes_cache
    
    if os.path.exists(DISHES_JSON_PATH):
        with open(DISHES_JSON_PATH, 'r') as f:
            data = json.load(f)
            _dishes_cache = {dish['id']: dish for dish in data.get('dishes', [])}
            return _dishes_cache
    
    return {}

def get_dish(dish_id):
    """Get a single dish by ID."""
    dishes = load_dishes()
    return dishes.get(dish_id)

def search_dishes(query):
    """Search dishes by name or ID."""
    dishes = load_dishes()
    results = []
    
    query_lower = query.lower()
    for dish_id, dish in dishes.items():
        if query_lower in dish['name'].lower() or query_lower in dish['id'].lower():
            results.append(dish)
    
    return results

def get_all_dishes_simplified():
    """Get simplified list of all dishes (for grid view)."""
    dishes = load_dishes()
    simplified = []
    
    for dish_id, dish in dishes.items():
        simplified.append({
            'id': dish['id'],
            'name': dish['name'],
            'cuisine': dish.get('cuisine', 'International'),
            'calories': dish['nutrition']['calories']
        })
    
    return simplified

def compute_scaled_nutrition(dish_id, grams):
    """Compute scaled nutrition based on portion size."""
    dish = get_dish(dish_id)
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
