"""
Food Recognition Backend Package
Modern, structured backend with modular routes and utilities
"""
from flask import Flask
from flask_cors import CORS

def create_app(config_name='development'):
    """Application factory for creating Flask app instances."""
    app = Flask(__name__)
    
    # Enable CORS for frontend communication
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000", "*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Configuration
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
    
    # Register blueprints
    from .routes import predict_bp, dishes_bp, logs_bp, goals_bp
    from .routes.images import images_bp
    
    app.register_blueprint(predict_bp, url_prefix='/api')
    app.register_blueprint(dishes_bp, url_prefix='/api')
    app.register_blueprint(logs_bp, url_prefix='/api')
    app.register_blueprint(goals_bp, url_prefix='/api')
    app.register_blueprint(images_bp, url_prefix='/api')
    
    return app
