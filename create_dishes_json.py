"""
Generate initial dishes.json with placeholders for all 121 classes.
Run once to create the file, then manually edit to add real data.
"""

import json
import os

# Food-101 classes (101 total)
FOOD_101_CLASSES = [
    'apple_pie', 'baby_back_ribs', 'baklava', 'beef_carpaccio', 'beef_tartare',
    'beet_salad', 'beignets', 'bibimbap', 'bread_pudding', 'breakfast_burrito',
    'bruschetta', 'caesar_salad', 'cannoli', 'caprese_salad', 'carrot_cake',
    'ceviche', 'cheese_plate', 'cheesecake', 'chicken_curry', 'chicken_parmesan',
    'chicken_quesadilla', 'chicken_wings', 'chocolate_cake', 'chocolate_mousse',
    'churros', 'clam_chowder', 'club_sandwich', 'crab_cakes', 'creme_brulee',
    'croque_madame', 'croque_monsieur', 'cruciferous_vegetables', 'cup_cakes',
    'cured_ham', 'curry_soup', 'custard_tart', 'daikon_radish', 'danish',
    'deviled_eggs', 'dosas', 'double_stuf_oreo', 'doughnut', 'duck_confit',
    'dumplings', 'edamame', 'eggs_benedict', 'eggs_royale', 'elephant_ear',
    'escargots', 'espresso', 'farinata', 'fassolada', 'falafel',
    'fallen_chocolate_cake', 'fettuccine_alfredo', 'figs', 'fish_and_chips',
    'fish_tacos', 'fondue', 'food_truck', 'french_fries', 'french_onion_soup',
    'french_toast', 'fried_calamari', 'fried_green_tomatoes', 'fried_rice',
    'fried_shrimp', 'frittata', 'frog_legs', 'frozen_yogurt', 'fruit_salad',
    'garlic_bread', 'gazpacho', 'gelee', 'german_chocolate_cake', 'ghee',
    'ghost_pepper', 'giant_clam', 'gnocchi', 'go_for_gold_pancakes', 'goat_cheese_salad',
    'golden_retriever', 'goulash', 'grape_leaves', 'grapefruit', 'grapes',
    'grasshopper', 'gratin', 'gravy', 'greek_salad', 'green_beans',
    'green_curry', 'green_goddess_salad', 'green_tea', 'gremolata', 'grey_poupon',
    'grilled_cheese_sandwich', 'grilled_salmon', 'grits', 'ground_beef_tacos',
    'guacamole', 'gyoza', 'gyro'
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
