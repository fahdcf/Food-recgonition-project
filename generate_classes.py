"""
Generate class names from Food-101 list and Moroccan dishes.
Creates initial dishes.json structure.
"""

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
    'bissara', 'couscous', 'harira', 'kefta_tagine', 'msemmen',
    'pastilla', 'rfissa', 'tagine', 'zaalouk'
]

# Moroccan v2 (11 dishes)
MOROCCAN_V2 = [
    'baghrir', 'briwat', 'chebakia', 'djaj_mhamer', 'fekkas',
    'harsha', 'khobz', 'loubia', 'makouda', 'sefanj', 'sellou'
]

ALL_CLASSES = FOOD_101_CLASSES + MOROCCAN_V1 + MOROCCAN_V2

print(f"Total classes: {len(ALL_CLASSES)}")
print(f"Food-101: {len(FOOD_101_CLASSES)}")
print(f"Moroccan v1: {len(MOROCCAN_V1)}")
print(f"Moroccan v2: {len(MOROCCAN_V2)}")
print("\nAll class names:")
for cls in ALL_CLASSES:
    print(f"  - {cls}")
