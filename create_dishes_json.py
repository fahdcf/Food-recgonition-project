"""
Generate initial dishes.json with placeholders for all 121 classes.
Run once to create the file, then manually edit to add real data.
"""

import json
import os

# Food-101 classes (101 total) - Official from dataset
# Source: https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/
FOOD_101_CLASSES = [
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

# Moroccan v1 (9 dishes)
MOROCCAN_V1 = [
    'moroccan_bissara', 'moroccan_couscous', 'moroccan_harira', 'moroccan_kefta_tagine',
    'moroccan_msemmen', 'moroccan_pastilla', 'moroccan_rfissa', 'moroccan_tagine',
    'moroccan_zaalouk'
]

# Moroccan v2 (11 dishes)
MOROCCAN_V2 = [
    'moroccan_baghrir', 'moroccan_briwat', 'moroccan_chebakia', 'moroccan_djaj_mhamer',
    'moroccan_fekkas', 'moroccan_harsha', 'moroccan_khobz', 'moroccan_loubia',
    'moroccan_makouda', 'moroccan_sefanj', 'moroccan_sellou'
]

ALL_CLASSES = FOOD_101_CLASSES + MOROCCAN_V1 + MOROCCAN_V2


def format_name(class_id):
    """Convert class_id to display name."""
    return class_id.replace('_', ' ').title()


def get_cuisine(class_id):
    """Guess cuisine type from class_id."""
    if class_id.startswith('moroccan_'):
        return 'Moroccan'
    elif class_id in ['pad_thai', 'pho', 'tom_yum_goong', 'satay']:
        return 'Thai'
    elif class_id in ['sushi', 'sashimi', 'tempura', 'tonkatsu']:
        return 'Japanese'
    elif class_id in ['tacos', 'quesadilla', 'enchiladas', 'fajitas']:
        return 'Mexican'
    elif class_id in ['pizza', 'pasta', 'risotto', 'ravioli']:
        return 'Italian'
    elif class_id in ['caesar_salad', 'club_sandwich', 'cheesecake']:
        return 'American'
    else:
        return 'International'


def create_dishes_json(output_path='data/dishes.json'):
    """Generate dishes.json with all classes."""
    
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    
    dishes = {
        'dishes': [
            {
                'id': class_id,
                'name': format_name(class_id),
                'cuisine': get_cuisine(class_id),
                'nutrition': {
                    'calories': 250,  # placeholder
                    'protein_g': 10,
                    'carbs_g': 30,
                    'fat_g': 8,
                    'serving_size_g': 100
                },
                'ingredients': [
                    'Ingredient 1',
                    'Ingredient 2',
                    'Ingredient 3',
                    'Ingredient 4'
                ],
                'recipe': {
                    'prep_time_min': 20,
                    'cook_time_min': 30,
                    'steps': [
                        'Step 1: Prepare ingredients',
                        'Step 2: Cook main components',
                        'Step 3: Combine and finish',
                        'Step 4: Serve immediately'
                    ],
                    'tips': 'This is a placeholder. Update with real recipe information.'
                },
                'similar_dishes': []  # Will populate later from neighbors
            }
            for class_id in ALL_CLASSES
        ]
    }
    
    with open(output_path, 'w') as f:
        json.dump(dishes, f, indent=2)
    
    print(f"✅ Created {output_path} with {len(ALL_CLASSES)} dishes")
    print(f"   - Food-101: {len(FOOD_101_CLASSES)}")
    print(f"   - Moroccan v1: {len(MOROCCAN_V1)}")
    print(f"   - Moroccan v2: {len(MOROCCAN_V2)}")


if __name__ == '__main__':
    create_dishes_json()
