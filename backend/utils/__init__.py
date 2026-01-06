"""
Utils package for backend utilities
"""
from .database import init_db, get_db_connection, close_db
from .dishes import load_dishes, get_dish, search_dishes, get_all_dishes_simplified, compute_scaled_nutrition

__all__ = [
    'init_db',
    'get_db_connection', 
    'close_db',
    'load_dishes',
    'get_dish',
    'search_dishes',
    'get_all_dishes_simplified',
    'compute_scaled_nutrition'
]
