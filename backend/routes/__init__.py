"""
Routes package for backend API endpoints
"""
from .predict import predict_bp
from .dishes import dishes_bp
from .goals import goals_bp
from .logs import logs_bp

__all__ = ['predict_bp', 'dishes_bp', 'goals_bp', 'logs_bp']
