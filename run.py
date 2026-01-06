"""
Entry point for the Food Recognition Flask application
Run with: python run.py
"""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend import create_app
from backend.utils import init_db, load_dishes
from backend.models import load_model, get_device

def main():
    """Initialize and run the Flask application."""
    
    print("\n" + "="*70)
    print("🚀 Food Recognition App Starting...")
    print("="*70)
    
    # Initialize database
    print("\n📊 Initializing database...")
    init_db()
    
    # Load dishes
    print("📚 Loading dishes metadata...")
    dishes = load_dishes()
    print(f"✅ Loaded {len(dishes)} dishes")
    
    # Load model
    print("\n🧠 Loading AI model...")
    model, scaler, class_names = load_model()
    device = get_device()
    print(f"✅ Model ready with {len(class_names)} classes on {device}")
    
    # Create Flask app
    print("\n🔧 Initializing Flask app...")
    app = create_app('development')
    
    print("\n" + "="*70)
    print("✨ Application Ready!")
    print("="*70)
    print(f"\n🌐 Open your browser: http://localhost:5000")
    print(f"📍 API Docs: http://localhost:5000/api/health")
    print(f"🎨 Frontend: http://localhost:5173 (if running npm run dev)")
    print("\n⚙️  Press CTRL+C to stop the server\n")
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False,
        use_debugger=False
    )

if __name__ == '__main__':
    main()
