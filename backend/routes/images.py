"""
Image serving routes for food dishes
"""
from flask import Blueprint, send_file, jsonify
import os
import random
from pathlib import Path

images_bp = Blueprint('images', __name__)

# Dataset paths
FOOD101_PATH = "d:/food_101_thumbnails"
MOROCCAN_PATH_V1 = "d:/moroccan_food_images/train"
MOROCCAN_PATH_V2 = "d:/moroccan_food_images_v2/train"

def get_sample_image(dish_id):
    """Get a random sample image for a dish from the dataset."""
    
    # Check if it's a Moroccan dish
    if dish_id.startswith('moroccan_'):
        moroccan_dish = dish_id.replace('moroccan_', '')
        
        # Try both Moroccan paths
        dish_dir_v1 = Path(MOROCCAN_PATH_V1) / moroccan_dish
        dish_dir_v2 = Path(MOROCCAN_PATH_V2) / moroccan_dish
        
        if dish_dir_v1.exists():
            dish_dir = dish_dir_v1
        elif dish_dir_v2.exists():
            dish_dir = dish_dir_v2
        else:
            # Try without the moroccan_ prefix in the folder name
            dish_dir_v1_alt = Path(MOROCCAN_PATH_V1) / dish_id
            dish_dir_v2_alt = Path(MOROCCAN_PATH_V2) / dish_id
            
            if dish_dir_v1_alt.exists():
                dish_dir = dish_dir_v1_alt
            elif dish_dir_v2_alt.exists():
                dish_dir = dish_dir_v2_alt
            else:
                return None
    else:
        # Food-101 dish
        dish_dir = Path(FOOD101_PATH) / dish_id
    
    if not dish_dir.exists():
        return None
    
    # Get all image files
    image_extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')
    images = [f for f in dish_dir.iterdir() if f.suffix in image_extensions]
    
    if not images:
        return None
    
    # Return the first image (sorted)
    return sorted(images)[0]

def get_multiple_images(dish_id, count=3):
    """Get multiple sample images for a dish from the dataset."""
    
    # Check if it's a Moroccan dish
    if dish_id.startswith('moroccan_'):
        moroccan_dish = dish_id.replace('moroccan_', '')
        
        # Try both Moroccan paths
        dish_dir_v1 = Path(MOROCCAN_PATH_V1) / moroccan_dish
        dish_dir_v2 = Path(MOROCCAN_PATH_V2) / moroccan_dish
        
        if dish_dir_v1.exists():
            dish_dir = dish_dir_v1
        elif dish_dir_v2.exists():
            dish_dir = dish_dir_v2
        else:
            dish_dir_v1_alt = Path(MOROCCAN_PATH_V1) / dish_id
            dish_dir_v2_alt = Path(MOROCCAN_PATH_V2) / dish_id
            
            if dish_dir_v1_alt.exists():
                dish_dir = dish_dir_v1_alt
            elif dish_dir_v2_alt.exists():
                dish_dir = dish_dir_v2_alt
            else:
                return []
    else:
        # Food-101 dish
        dish_dir = Path(FOOD101_PATH) / dish_id
    
    if not dish_dir.exists():
        return []
    
    # Get all image files
    image_extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')
    images = [f for f in dish_dir.iterdir() if f.suffix in image_extensions]
    
    if not images:
        return []
    
    # Return up to 'count' images (sorted)
    return sorted(images)[:count]

@images_bp.route('/dishes/<dish_id>/image', methods=['GET'])
def get_dish_image(dish_id):
    """Serve a sample image for a dish."""
    try:
        image_path = get_sample_image(dish_id)
        
        if image_path and image_path.exists():
            return send_file(
                str(image_path),
                mimetype='image/jpeg',
                as_attachment=False,
                download_name=f"{dish_id}.jpg"
            )
        else:
            # Return 404 if no image found
            return jsonify({'error': 'No image found for this dish'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@images_bp.route('/dishes/<dish_id>/images', methods=['GET'])
def get_dish_images(dish_id):
    """Get multiple images for a dish."""
    try:
        image_paths = get_multiple_images(dish_id, count=3)
        
        if image_paths:
            # Return URLs for the images
            image_urls = [f"/api/dishes/{dish_id}/image/{i}" for i in range(len(image_paths))]
            return jsonify({'images': image_urls})
        else:
            return jsonify({'images': []}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@images_bp.route('/dishes/<dish_id>/image/<int:index>', methods=['GET'])
def get_dish_image_by_index(dish_id, index):
    """Serve a specific image by index for a dish."""
    try:
        image_paths = get_multiple_images(dish_id, count=3)
        
        if image_paths and index < len(image_paths):
            return send_file(
                str(image_paths[index]),
                mimetype='image/jpeg',
                as_attachment=False,
                download_name=f"{dish_id}_{index}.jpg"
            )
        else:
            return jsonify({'error': 'Image not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
