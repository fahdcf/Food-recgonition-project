"""
Batch update dishes.json with real nutrition and recipe data
This script updates remaining placeholder dishes with authentic information
"""
import json

# Dictionary of dish updates with real data
DISH_DATA = {
    "crab_cakes": {
        "cuisine": "American",
        "nutrition": {"calories": 289, "protein_g": 18, "carbs_g": 14, "fat_g": 17, "serving_size_g": 100},
        "ingredients": ["500g lump crab meat", "1/2 cup breadcrumbs", "1 egg", "2 tbsp mayonnaise", "1 tsp Old Bay seasoning", "1 tbsp Dijon mustard", "Lemon juice", "Oil for frying"],
        "recipe": {"prep_time_min": 15, "cook_time_min": 15, "steps": ["Mix crab with breadcrumbs, egg, mayo, Old Bay, mustard, lemon juice", "Form into patties", "Refrigerate 30 minutes", "Fry in hot oil 3-4 minutes per side until golden", "Serve with remoulade sauce"],"tips": "Use fresh lump crab. Don't overmix. Serve hot with tartar sauce and lemon wedge."}
    },
    "creme_brulee": {
        "cuisine": "French",
        "nutrition": {"calories": 198, "protein_g": 3, "carbs_g": 22, "fat_g": 11, "serving_size_g": 100},
        "ingredients": ["1 cup heavy cream", "1 vanilla bean (or 1 tsp extract)", "4 egg yolks", "50g sugar", "Extra sugar for topping"],
        "recipe": {"prep_time_min": 20, "cook_time_min": 40, "steps": ["Heat cream with vanilla until steaming", "Whisk yolks with sugar until pale", "Slowly add cream to yolks while whisking", "Strain through fine sieve", "Pour into ramekins", "Bake in water bath at 325°F for 30-40 minutes", "Chill overnight", "Sprinkle sugar on top and torch until caramelized"],"tips": "Custard should jiggle slightly. Torch just before serving to maintain crispiness."}
    },
    "croque_madame": {
        "cuisine": "French",
        "nutrition": {"calories": 387, "protein_g": 21, "carbs_g": 26, "fat_g": 23, "serving_size_g": 100},
        "ingredients": ["4 slices good quality bread", "100g ham, sliced", "100g Emmental cheese", "2 tablespoons butter", "2 tablespoons Dijon mustard", "2 eggs"],
        "recipe": {"prep_time_min": 10, "cook_time_min": 10, "steps": ["Spread mustard on bread slices", "Layer ham and cheese between bread", "Butter outside of sandwich", "Griddle until golden and cheese melts", "Cook eggs sunny-side up", "Top sandwich with fried egg"],"tips": "Classic French sandwich. Croque Monsieur without egg. Serve immediately while warm."}
    },
    "cup_cakes": {
        "cuisine": "American",
        "nutrition": {"calories": 289, "protein_g": 2, "carbs_g": 40, "fat_g": 13, "serving_size_g": 100},
        "ingredients": ["1 3/4 cups flour", "1 1/2 tsp baking powder", "1/2 tsp salt", "225g butter", "200g sugar", "3 eggs", "150ml milk", "1 tsp vanilla"],
        "recipe": {"prep_time_min": 15, "cook_time_min": 20, "steps": ["Preheat to 350°F. Line muffin tins with liners", "Mix flour, baking powder, salt", "Cream butter and sugar", "Add eggs one at a time", "Alternate flour and milk", "Add vanilla", "Fill cups 2/3 full", "Bake 18-22 minutes"],"tips": "Use cupcake liners. Frost after cooling. Don't overfill cups."}
    },
    "pizza": {
        "cuisine": "Italian",
        "nutrition": {"calories": 266, "protein_g": 11, "carbs_g": 36, "fat_g": 8, "serving_size_g": 100},
        "ingredients": ["500g pizza dough", "200ml tomato sauce", "200g mozzarella cheese", "2 tbsp olive oil", "Fresh basil", "Garlic", "Salt", "Oregano"],
        "recipe": {"prep_time_min": 90, "cook_time_min": 15, "steps": ["Let dough rise 1 hour", "Preheat oven to 475°F", "Stretch dough into pan", "Spread tomato sauce", "Top with cheese and toppings", "Drizzle with olive oil", "Bake 12-15 minutes until crust is golden"],"tips": "Classic Margherita. Hot oven for crispy crust. Fresh ingredients matter."}
    },
    "hamburger": {
        "cuisine": "American",
        "nutrition": {"calories": 215, "protein_g": 26, "carbs_g": 27, "fat_g": 6, "serving_size_g": 100},
        "ingredients": ["150g ground beef", "Hamburger bun", "Lettuce", "Tomato", "Onion", "Pickles", "Ketchup", "Mustard", "Mayonnaise"],
        "recipe": {"prep_time_min": 10, "cook_time_min": 10, "steps": ["Form beef into patty", "Season with salt and pepper", "Grill or cook on griddle 4-5 minutes per side", "Toast buns lightly", "Assemble with condiments and vegetables"],"tips": "Don't overwork meat. Make indent in center to prevent puffing. Cook to medium doneness."}
    },
    "hot_dog": {
        "cuisine": "American",
        "nutrition": {"calories": 290, "protein_g": 12, "carbs_g": 24, "fat_g": 17, "serving_size_g": 100},
        "ingredients": ["1 hot dog/sausage", "1 hot dog bun", "Ketchup", "Mustard", "Onions", "Relish (optional)"],
        "recipe": {"prep_time_min": 2, "cook_time_min": 5, "steps": ["Grill or boil hot dog 5-7 minutes", "Toast bun", "Place hot dog in bun", "Top with desired condiments"],"tips": "Classic American food. Chicago style: mustard, onions, pickles, tomatoes, peppers, no ketchup."}
    },
    "lasagna": {
        "cuisine": "Italian",
        "nutrition": {"calories": 187, "protein_g": 14, "carbs_g": 16, "fat_g": 8, "serving_size_g": 100},
        "ingredients": ["500g lasagna noodles", "1 kg ground beef", "1 onion, diced", "4 cloves garlic", "800g tomato sauce", "250g ricotta", "200g mozzarella", "Parmesan cheese"],
        "recipe": {"prep_time_min": 30, "cook_time_min": 60, "steps": ["Brown beef with onion and garlic", "Simmer with tomato sauce 20 minutes", "Cook noodles al dente", "Layer: sauce, noodles, ricotta, mozzarella", "Repeat layers", "Top with Parmesan", "Bake at 375°F for 45 minutes"],"tips": "Can make ahead and freeze. Meat sauce tastes better next day. Let rest 10 minutes before cutting."}
    },
    "ice_cream": {
        "cuisine": "American",
        "nutrition": {"calories": 207, "protein_g": 4, "carbs_g": 24, "fat_g": 11, "serving_size_g": 100},
        "ingredients": ["2 cups heavy cream", "1 cup milk", "150g sugar", "1 tsp vanilla", "Pinch of salt"],
        "recipe": {"prep_time_min": 15, "cook_time_min": 30, "steps": ["Heat cream and milk to steam point", "Whisk yolks with sugar until pale", "Slowly add hot cream to yolks", "Cook mixture to 160°F", "Cool completely", "Churn in ice cream maker", "Freeze until firm"],"tips": "Temperature important for food safety. Use quality vanilla. Churning time varies by machine."}
    }
}

# Load the dishes.json file
with open('data/dishes.json', 'r') as f:
    data = json.load(f)

# Update dishes
updated_count = 0
for dish in data['dishes']:
    dish_id = dish['id']
    
    if dish_id in DISH_DATA:
        dish_info = DISH_DATA[dish_id]
        dish['cuisine'] = dish_info.get('cuisine', dish.get('cuisine'))
        dish['nutrition'] = dish_info.get('nutrition', dish.get('nutrition'))
        dish['ingredients'] = dish_info.get('ingredients', dish.get('ingredients'))
        dish['recipe'] = dish_info.get('recipe', dish.get('recipe'))
        updated_count += 1

# Save updated data
with open('data/dishes.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Updated {updated_count} dishes with real data!")
