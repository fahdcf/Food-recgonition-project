"""
Extract 3 sample images from each Food-101 class from parquet files
CORRECTED VERSION - Uses official Food-101 classes
"""
import pandas as pd
from pathlib import Path
from PIL import Image
import io
from collections import defaultdict

# Paths
PARQUET_DIR = Path("d:/food 101 dataset")
OUTPUT_DIR = Path("d:/food_101_thumbnails")

# Official Food-101 classes (alphabetically sorted)
# Source: https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/
FOOD_101_OFFICIAL = [
    'apple_pie', 'baby_back_ribs', 'baklava', 'beef_carpaccio', 'beef_tartare',
    'beet_salad', 'beignets', 'bibimbap', 'bread_pudding', 'breakfast_burrito',
    'bruschetta', 'caesar_salad', 'cannoli', 'caprese_salad', 'carrot_cake',
    'ceviche', 'cheesecake', 'cheese_plate', 'chicken_curry', 'chicken_quesadilla',
    'chicken_wings', 'chocolate_cake', 'chocolate_mousse', 'churros', 'clam_chowder',
    'club_sandwich', 'crab_cakes', 'creme_brulee', 'croque_madame', 'cup_cakes',
    'deviled_eggs', 'donuts', 'dumplings', 'edamame', 'eggs_benedict',
    'escargots', 'falafel', 'filet_mignon', 'fish_and_chips', 'foie_gras',
    'french_fries', 'french_onion_soup', 'french_toast', 'fried_calamari', 'fried_rice',
    'frozen_yogurt', 'garlic_bread', 'gnocchi', 'greek_salad', 'grilled_cheese_sandwich',
    'grilled_salmon', 'guacamole', 'gyoza', 'hamburger', 'hot_and_sour_soup',
    'hot_dog', 'huevos_rancheros', 'hummus', 'ice_cream', 'lasagna',
    'lobster_bisque', 'lobster_roll_sandwich', 'macaroni_and_cheese', 'macarons', 'miso_soup',
    'mussels', 'nachos', 'omelette', 'onion_rings', 'oysters',
    'pad_thai', 'paella', 'pancakes', 'panna_cotta', 'peking_duck',
    'pho', 'pizza', 'pork_chop', 'poutine', 'prime_rib',
    'pulled_pork_sandwich', 'ramen', 'ravioli', 'red_velvet_cake', 'risotto',
    'samosa', 'sashimi', 'scallops', 'seaweed_salad', 'shrimp_and_grits',
    'spaghetti_bolognese', 'spaghetti_carbonara', 'spring_rolls', 'steak', 'strawberry_shortcake',
    'sushi', 'tacos', 'takoyaki', 'tiramisu', 'tuna_tartare',
    'waffles'
]

def load_class_mapping():
    """Create mapping from label index to class name"""
    # Create mapping: label_index -> class_name
    label_to_class = {i: class_name for i, class_name in enumerate(FOOD_101_OFFICIAL)}
    return label_to_class

def extract_thumbnails():
    """Extract 3 images per class from parquet files."""
    
    # Load class name mapping
    label_to_class = load_class_mapping()
    print(f"Loaded {len(label_to_class)} Food-101 classes")
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Track images per class
    class_images = defaultdict(int)
    images_per_class = 3
    
    # Process train parquet files
    parquet_files = sorted(PARQUET_DIR.glob("train-*.parquet"))
    
    print(f"Found {len(parquet_files)} parquet files")
    print(f"Extracting {images_per_class} images per class...")
    
    for parquet_file in parquet_files:
        print(f"\nProcessing: {parquet_file.name}")
        
        # Read parquet file
        df = pd.read_parquet(parquet_file)
        
        for idx, row in df.iterrows():
            label_idx = row['label']
            
            # Get class name from label index
            class_name = label_to_class.get(label_idx)
            if not class_name:
                continue
            
            # Skip if we already have enough images for this class
            if class_images[class_name] >= images_per_class:
                continue
            
            # Create class directory
            class_dir = OUTPUT_DIR / class_name
            class_dir.mkdir(exist_ok=True)
            
            # Get image data
            image_data = row['image']
            
            # Handle different image formats in parquet
            if isinstance(image_data, dict):
                # Image is stored as dict with 'bytes' key
                img_bytes = image_data.get('bytes')
                if img_bytes:
                    img = Image.open(io.BytesIO(img_bytes))
                else:
                    continue
            elif isinstance(image_data, bytes):
                # Image is stored directly as bytes
                img = Image.open(io.BytesIO(image_data))
            else:
                # Try to convert to image directly
                try:
                    img = Image.fromarray(image_data)
                except:
                    continue
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save image
            img_count = class_images[class_name]
            img_path = class_dir / f"{class_name}_{img_count + 1}.jpg"
            img.save(img_path, 'JPEG', quality=85)
            
            class_images[class_name] += 1
            
            # Print progress
            if class_images[class_name] == images_per_class:
                print(f"  ✓ {class_name}: {images_per_class} images extracted")
        
        # Check if we're done
        total_classes = len(label_to_class)
        completed_classes = sum(1 for count in class_images.values() if count >= images_per_class)
        print(f"Progress: {completed_classes}/{total_classes} classes complete")
        
        if completed_classes >= total_classes:
            print("\n✓ All classes extracted!")
            break
    
    print(f"\n{'='*50}")
    print(f"Extraction complete!")
    print(f"Total classes: {len(class_images)}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"{'='*50}")

if __name__ == "__main__":
    extract_thumbnails()
