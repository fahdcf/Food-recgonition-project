"""
Enhanced Moroccan Food Scraper with Image Validation
- 5 Moroccan dishes (Lham Mhamer, Chebakia, Fekkas, Harsha, Sefanj)
- Highly specific food-only queries (108 queries per dish)
- Image validation to avoid non-food images
- Hash-based duplicate detection
"""
from icrawler.builtin import BingImageCrawler
import os
import shutil
from pathlib import Path
import time
import logging
from PIL import Image
import hashlib

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# NEW Moroccan dishes with multilingual food-focused queries
MOROCCAN_DISHES = {
    'djaj_mhamer': [
        # English queries
        "djaj mhamer moroccan chicken tagine", "djaj mhamer spiced chicken recipe", "moroccan djaj mhamer served plate",
        "djaj mhamer tender chicken dish", "traditional djaj mhamer morocco", "djaj mhamer aromatic chicken meal",
        "moroccan djaj mhamer braised chicken", "djaj mhamer slow cooked chicken", "spiced djaj mhamer tagine food",
        "djaj mhamer authentic recipe", "moroccan djaj mhamer homemade", "djaj mhamer chicken cumin dish",
        "traditional djaj mhamer tagine", "djaj mhamer moroccan cuisine", "chicken djaj mhamer moroccan plate",
        "djaj mhamer spices paprika chicken", "moroccan djaj mhamer chicken bowl", "djaj mhamer rich chicken stew",
        "traditional djaj mhamer chicken", "djaj mhamer moroccan chicken", "djaj mhamer tagine bowl served",
        "moroccan djaj mhamer tender", "djaj mhamer braised chicken meal", "djaj mhamer spiced chicken dish",
        "traditional djaj mhamer plate", "djaj mhamer moroccan meal", "chicken djaj mhamer aromatic",
        "djaj mhamer slow cooked tagine", "moroccan djaj mhamer recipe", "djaj mhamer chicken food",
        "djaj mhamer cumin spices", "traditional djaj mhamer chicken", "moroccan djaj mhamer braised",
        "djaj mhamer tagine chicken served", "djaj mhamer authentic moroccan", "moroccan djaj mhamer plate",
        # French queries
        "djaj mhamer poulet marocain", "djaj mhamer tajine poulet épices", "djaj mhamer marocain servi",
        "djaj mhamer poulet tendre maroc", "djaj mhamer traditionnel marocain", "djaj mhamer poulet aromatique",
        "djaj mhamer braisé marocain", "djaj mhamer poulet mijoté", "djaj mhamer épices tajine",
        "djaj mhamer recette authentique", "djaj mhamer marocain fait maison", "djaj mhamer poulet cumin",
        "djaj mhamer traditionnel tajine", "djaj mhamer cuisine marocaine", "djaj mhamer poulet maroc",
        "djaj mhamer paprika épices", "djaj mhamer marocain bol poulet", "djaj mhamer ragoût poulet",
        "djaj mhamer traditionnel poulet", "djaj mhamer marocain poulet", "djaj mhamer tajine bol servi",
        "djaj mhamer marocain tendre", "djaj mhamer braisé poulet", "djaj mhamer épices poulet",
        "djaj mhamer traditionnel plat", "djaj mhamer marocain repas", "djaj mhamer poulet aromatique",
        "djaj mhamer mijoté tajine", "djaj mhamer marocain recette", "djaj mhamer poulet cuisine",
        "djaj mhamer cumin épices", "djaj mhamer traditionnel poulet", "djaj mhamer marocain braisé",
        "djaj mhamer tajine poulet servi", "djaj mhamer authentique marocain", "djaj mhamer marocain plat",
        # Arabic queries
        "دجاج المحمر المغربي", "دجاج محمر بالتوابل", "دجاج محمر تاجين مغربي",
        "دجاج محمر مطبوخ مغربي", "دجاج المحمر التقليدي", "دجاج محمر عطري مغربي",
        "دجاج محمر مطبوخ ببطء", "دجاج محمر تاجين لذيذ", "دجاج محمر بالتوابل المغربية",
        "دجاج المحمر الأصيل", "دجاج محمر منزلي مغربي", "دجاج محمر بالكمون",
        "دجاج محمر تاجين تقليدي", "دجاج محمر مغربي الطبخ", "دجاج محمر دجاج طري",
        "دجاج محمر بالفلفل", "دجاج محمر مغربي طبق", "دجاج محمر حساء دجاج",
        "دجاج محمر تقليدي دجاج", "دجاج محمر مغربي بالطريقة", "دجاج محمر تاجين مطبوخ",
        "دجاج محمر مغربي طري", "دجاج محمر مطبوخ بدجاج", "دجاج محمر بالتوابل الحارة",
        "دجاج محمر تقليدي طبق", "دجاج محمر مغربي وجبة", "دجاج محمر دجاج عطري",
        "دجاج محمر طهي بطء", "دجاج محمر مغربي وصفة", "دجاج محمر وجبة طعام",
        "دجاج محمر بالكمون والفلفل", "دجاج محمر تقليدي دجاج", "دجاج محمر مغربي طهي",
        "دجاج محمر تاجين مطبوخ دجاج", "دجاج محمر أصيل مغربي", "دجاج محمر مغربي طبق مغربي"
    ],
    'fekkas': [
        # English queries
        "fekkas almond biscuits moroccan", "moroccan fekkas twice baked cookies", "fekkas hard biscuits almonds food",
        "traditional fekkas morocco recipe", "fekkas dipped coffee tea plate", "moroccan fekkas crispy biscuits",
        "fekkas anise almond biscuits dish", "homemade fekkas moroccan cookies", "fekkas toasted almonds moroccan",
        "moroccan fekkas traditional baked", "fekkas biscuit served tea coffee", "authentic fekkas moroccan food",
        "fekkas almond cookies morocco", "moroccan fekkas crunchy biscuit", "fekkas baked almonds plate",
        "traditional fekkas moroccan baking", "fekkas anise flavor cookies", "moroccan fekkas homemade bake",
        "fekkas crispy almonds biscuits", "fekkas twice baked moroccan", "moroccan fekkas served plate",
        "fekkas hard almonds biscuits", "traditional fekkas recipe morocco", "fekkas almond flavor cookies",
        "moroccan fekkas baked almonds", "fekkas coffee dipping biscuit", "fekkas moroccan traditional cookie",
        "fekkas biscuits anise almonds", "moroccan fekkas crispy baked", "fekkas almonds moroccan plate",
        "traditional fekkas biscuits", "fekkas recipe moroccan cookies", "moroccan fekkas hard biscuits",
        "fekkas toasted almond bake", "moroccan fekkas dipped coffee", "fekkas authentic moroccan recipe",
        # French queries
        "fekkas biscuits amandes marocains", "fekkas marocain biscuits cuits deux fois", "fekkas biscuits durs amandes",
        "fekkas traditionnel maroc recette", "fekkas trempé café thé", "fekkas marocain biscuits croustillants",
        "fekkas anis amandes marocain", "fekkas fait maison biscuits", "fekkas amandes grillées marocain",
        "fekkas marocain traditionnel cuit", "fekkas biscuit servi café", "fekkas authentique marocain",
        "fekkas amandes biscuits maroc", "fekkas marocain biscuits croustillant", "fekkas biscuits cuits assiette",
        "fekkas traditionnel maroc biscuits", "fekkas anis saveur biscuits", "fekkas marocain fait maison",
        "fekkas biscuits amandes croustillants", "fekkas cuits deux fois maroc", "fekkas marocain servi assiette",
        "fekkas biscuits amandes durs", "fekkas recette marocaine", "fekkas amandes saveur biscuits",
        "fekkas marocain biscuits cuits", "fekkas café trempage biscuit", "fekkas marocain biscuits traditionnel",
        "fekkas biscuits anis amandes", "fekkas marocain croustillants cuits", "fekkas amandes maroc assiette",
        "fekkas traditionnel biscuits", "fekkas recette biscuits maroc", "fekkas marocain biscuits durs",
        "fekkas amandes grillées biscuit", "fekkas marocain trempage café", "fekkas authentique recette",
        # Arabic queries
        "فقاس بسكويت اللوز المغربي", "فقاس مغربي مرتين مشوي", "فقاس بسكويت صلب",
        "فقاس تقليدي مغربي", "فقاس مغمس قهوة شاي", "فقاس مغربي بسكويت مقرمش",
        "فقاس بالشمرة واللوز", "فقاس منزلي مغربي", "فقاس لوز محمص مغربي",
        "فقاس مغربي تقليدي مشوي", "فقاس بسكويت مع قهوة", "فقاس أصيل مغربي",
        "فقاس لوز بسكويت مغربي", "فقاس مغربي بسكويت مقرمش", "فقاس بسكويت مشوي طبق",
        "فقاس تقليدي مغربي بسكويت", "فقاس الشمرة نكهة بسكويت", "فقاس مغربي منزلي",
        "فقاس بسكويت لوز مقرمش", "فقاس مشوي مرتين مغربي", "فقاس مغربي طبق مشوي",
        "فقاس بسكويت لوز صلب", "فقاس وصفة مغربية", "فقاس لوز نكهة بسكويت",
        "فقاس مغربي بسكويت مشوي", "فقاس قهوة غمس بسكويت", "فقاس مغربي بسكويت تقليدي",
        "فقاس بسكويت الشمرة لوز", "فقاس مغربي مقرمش مشوي", "فقاس لوز مغربي طبق",
        "فقاس تقليدي بسكويت", "فقاس وصفة بسكويت مغربي", "فقاس مغربي بسكويت صلب",
        "فقاس لوز محمص بسكويت", "فقاس مغربي غمس قهوة", "فقاس أصيل وصفة مغربية"
    ],
    'harsha': [
        # English queries
        "harsha semolina pancake moroccan", "moroccan harsha anise bread food", "harsha pancake served plate butter",
        "traditional harsha morocco recipe", "harsha semolina flatbread anise", "moroccan harsha butter served",
        "harsha thick pancake onions dish", "homemade harsha moroccan food", "harsha semolina anise morocco",
        "moroccan harsha pancake traditional", "harsha served butter plate", "authentic harsha moroccan recipe",
        "harsha anise flavor pancake", "moroccan harsha semolina bread", "harsha pancake anise onions",
        "traditional harsha moroccan bread", "harsha butter served food", "moroccan harsha homemade pancake",
        "harsha thick flatbread anise", "moroccan harsha traditional served", "harsha semolina moroccan plate",
        "harsha pancake butter meal", "traditional harsha recipe maroc", "harsha anise semolina dish",
        "moroccan harsha pancake anise", "harsha bread butter plate served", "harsha moroccan traditional recipe",
        "harsha flatbread semolina onion", "moroccan harsha thick pancake", "harsha anise bread moroccan",
        "traditional harsha anise bread", "harsha recipe moroccan pancake", "moroccan harsha pancake butter",
        "harsha semolina anise served", "moroccan harsha butter pancake", "harsha authentic moroccan recipe",
        # French queries
        "harsha crêpe semoule marocain", "harsha marocain pain anis", "harsha crêpe servi beurre",
        "harsha traditionnel maroc recette", "harsha semoule pain plat anis", "harsha marocain beurre servi",
        "harsha crêpe épaisse oignons", "harsha fait maison marocain", "harsha semoule anis maroc",
        "harsha marocain crêpe traditionnelle", "harsha servi beurre assiette", "harsha authentique marocain",
        "harsha anis saveur crêpe", "harsha marocain semoule pain", "harsha crêpe anis oignons",
        "harsha traditionnel marocain pain", "harsha beurre servi nourriture", "harsha marocain crêpe maison",
        "harsha pain plat anis", "harsha marocain traditionnel servi", "harsha semoule marocain assiette",
        "harsha crêpe beurre repas", "harsha traditionnel recette maroc", "harsha anis semoule plat",
        "harsha marocain crêpe anis", "harsha pain beurre assiette", "harsha marocain recette traditionnelle",
        "harsha pain plat semoule", "harsha marocain crêpe épaisse", "harsha anis pain marocain",
        "harsha traditionnel anis pain", "harsha recette marocain crêpe", "harsha marocain crêpe beurre",
        "harsha semoule anis servi", "harsha marocain beurre crêpe", "harsha authentique recette marocaine",
        # Arabic queries
        "الحرشة السميد المغربية", "حرشة مغربية بالشمرة", "الحرشة خبز بالزبدة",
        "حرشة تقليدية مغربية", "الحرشة السميد خبز بالشمرة", "حرشة مغربية بالزبدة",
        "حرشة فطيرة سميد بصل", "حرشة منزلية مغربية", "الحرشة السميد والشمرة",
        "حرشة مغربية فطيرة تقليدية", "حرشة بالزبدة مع الطبق", "حرشة أصيلة مغربية",
        "حرشة نكهة الشمرة", "حرشة مغربية سميد خبز", "الحرشة فطيرة الشمرة والبصل",
        "حرشة تقليدية مغربية خبز", "حرشة بالزبدة مع الطعام", "حرشة مغربية فطيرة منزلية",
        "حرشة خبز مسطح الشمرة", "حرشة مغربية تقليدية مع", "الحرشة السميد مغربي طبق",
        "حرشة فطيرة بالزبدة وجبة", "حرشة تقليدية وصفة مغربية", "حرشة نكهة الشمرة السميد",
        "حرشة مغربية فطيرة الشمرة", "حرشة خبز مع الزبدة", "حرشة مغربية وصفة تقليدية",
        "حرشة خبز مسطح سميد", "حرشة مغربية فطيرة سميد", "حرشة الشمرة خبز مغربي",
        "حرشة تقليدية الشمرة خبز", "حرشة وصفة مغربية فطيرة", "حرشة مغربية فطيرة بالزبدة",
        "حرشة السميد والشمرة مع", "حرشة مغربية الزبدة فطيرة", "حرشة أصيلة وصفة مغربية"
    ],
    'sefanj': [
        # English queries
        "sefanj moroccan crepe thin pancake", "moroccan sefanj delicate pancake served", "sefanj crepe plate butter honey",
        "sefanj traditional morocco recipe", "moroccan sefanj thin flatbread", "sefanj pancake served butter plate",
        "traditional sefanj morocco pancake", "sefanj crepe homemade moroccan", "moroccan sefanj delicate crepe food",
        "sefanj thin pancake moroccan", "traditional sefanj recipe maroc", "sefanj butter served crepe",
        "moroccan sefanj pancake recipe", "sefanj crepe moroccan traditional", "traditional sefanj flatbread",
        "sefanj moroccan thin crepe", "moroccan sefanj served plate", "sefanj pancake butter moroccan",
        "sefanj delicate crepe morocco", "moroccan sefanj homemade pancake", "traditional sefanj crepe served",
        "sefanj thin flatbread morocco", "moroccan sefanj pancake served", "sefanj crepe butter plate food",
        "sefanj moroccan recipe pancake", "traditional sefanj morocco food", "moroccan sefanj delicate served",
        "sefanj crepe thin maroc", "moroccan sefanj pancake butter", "sefanj traditional recipe dish",
        "traditional sefanj pancake", "sefanj moroccan crepe recipe", "moroccan sefanj flatbread crepe",
        "sefanj thin pancake served", "moroccan sefanj butter pancake", "sefanj authentic moroccan recipe",
        # French queries
        "sefanj crêpe marocaine mince", "sefanj marocain crêpe fine", "sefanj crêpe servi beurre",
        "sefanj traditionnel maroc recette", "sefanj marocain pain plat mince", "sefanj pancake servi beurre",
        "sefanj traditionnel marocain crêpe", "sefanj crêpe maison marocain", "sefanj marocain crêpe fine",
        "sefanj crêpe pancake marocain", "sefanj traditionnel recette maroc", "sefanj beurre servi assiette",
        "moroccan sefanj marocain crêpe", "sefanj crêpe mince marocain", "sefanj traditionnel pain plat",
        "sefanj marocain crêpe fine servi", "moroccan sefanj pancake recette", "sefanj crêpe marocain maison",
        "sefanj crêpe mince maroc", "moroccan sefanj traditionnel crêpe", "sefanj pancake assiette beurre",
        "sefanj crêpe servi maroc", "traditionnel sefanj maroc crêpe", "sefanj marocain crêpe mince",
        "moroccan sefanj crêpe pain", "sefanj pain plat marocain", "sefanj crêpe beurre servi",
        "sefanj traditionnel crêpe pancake", "sefanj marocain recette crêpe", "moroccan sefanj mince crêpe",
        "sefanj crêpe pain plat", "sefanj marocain recette mince", "sefanj crêpe fine marocain",
        "sefanj traditionnel marocain recette", "sefanj marocain crêpe pain", "moroccan sefanj crêpe recette",
        # Arabic queries
        "سفنج مغربي رقيق", "سفنج مرقق مغربي", "سفنج مع الزبدة طبق",
        "سفنج تقليدي مغربي", "سفنج مغربي خبز رقيق", "سفنج رقيق مع الزبدة",
        "سفنج تقليدي مغربي بانكيك", "سفنج منزلي مغربي", "سفنج مغربي رقيق طعام",
        "سفنج رقيق مغربي بانكيك", "سفنج تقليدي وصفة مغربية", "سفنج بالزبدة مع الطبق",
        "سفنج مغربي وصفة بانكيك", "سفنج رقيق مغربي تقليدي", "سفنج تقليدي خبز مسطح",
        "سفنج مغربي رقيق مرقق", "سفنج مع الطبق مع", "سفنج بانكيك مع الزبدة",
        "سفنج مغربي وصفة رقيق", "سفنج تقليدي مغربي طعام", "سفنج رقيق مع الطبق",
        "سفنج خبز مسطح مغربي", "سفنج مغربي مع الطبق", "سفنج رقيق مع الزبدة طبق",
        "سفنج مغربي بانكيك رقيق", "سفنج تقليدي رقيق مرقق", "سفنج مع الزبدة الطعام",
        "سفنج تقليدي بانكيك مغربي", "سفنج مغربي خبز رقيق", "سفنج رقيق تقليدي",
        "سفنج خبز مغربي رقيق", "سفنج وصفة مغربية رقيق", "سفنج مع الطبق تقليدي",
        "سفنج رقيق مغربي وصفة", "سفنج مغربي الزبدة بانكيك", "سفنج أصيل مغربي رقيق"
    ],
    'chebakia': [
        # English queries
        "chebakia sesame honey cookies moroccan", "fried chebakia flower shape pastry", "chebakia ramadan sweet dessert plate",
        "chebakia honey syrup sesame food", "traditional chebakia morocco dessert", "moroccan chebakia fried cookies served",
        "chebakia flower pastry honey sesame", "moroccan chebakia ramadan sweet plate", "homemade chebakia cookies morocco",
        "chebakia fried dough honey syrup", "moroccan chebakia sesame cookies dessert", "chebakia flower shape ramadan food",
        "traditional chebakia morocco honey", "chebakia sweet cookies sesame served", "moroccan chebakia fried pastry plate",
        "chebakia ramadan dessert honey morocco", "moroccan chebakia flower cookies", "chebakia sesame fried sweet food",
        "traditional chebakia morocco ramadan", "chebakia honey cookies served plate", "moroccan chebakia sweet pastry",
        "chebakia flower fried morocco dessert", "moroccan chebakia traditional cookies", "chebakia honey sesame ramadan",
        "chebakia fried sweet morocco plate", "moroccan chebakia cookies honey served", "chebakia ramadan pastry sesame",
        "traditional chebakia flower morocco", "chebakia sweet fried dessert food", "moroccan chebakia homemade honey",
        "chebakia sesame ramadan cookies plate", "moroccan chebakia fried flower served", "chebakia honey pastry morocco",
        "traditional chebakia sweet cookies", "chebakia ramadan morocco honey", "moroccan chebakia sesame fried dessert",
        # French queries
        "chebakia marocain miel sésame", "chebakia frit fleur pâtisserie", "chebakia ramadan dessert marocain",
        "chebakia miel sirop sésame", "chebakia traditionnel maroc dessert", "chebakia marocain frit servi",
        "chebakia fleur pâtisserie miel", "chebakia marocain ramadan sucré", "chebakia fait maison miel maroc",
        "chebakia pâte frite sirop miel", "chebakia marocain sésame dessert", "chebakia fleur ramadan",
        "chebakia traditionnel maroc miel", "chebakia gâteaux sésame servi", "chebakia marocain frit assiette",
        "chebakia ramadan dessert miel", "chebakia marocain fleur gâteaux", "chebakia sésame frit sucré",
        "chebakia traditionnel maroc ramadan", "chebakia miel gâteaux servi", "chebakia marocain pâtisserie sucrée",
        "chebakia fleur frit maroc", "chebakia marocain traditionnel gâteaux", "chebakia miel sésame ramadan",
        "chebakia frit sucré maroc", "chebakia marocain gâteaux miel", "chebakia ramadan pâtisserie sésame",
        "chebakia traditionnel fleur maroc", "chebakia sucré frit dessert", "chebakia marocain fait maison miel",
        "chebakia sésame ramadan gâteaux", "chebakia marocain frit fleur", "chebakia miel pâtisserie maroc",
        "chebakia traditionnel gâteaux sucrés", "chebakia ramadan maroc miel", "chebakia marocain sésame frit dessert",
        # Arabic queries
        "الشباكية المغربية بالعسل", "شباكية مغربية بالسمسم", "الشباكية الرمضانية المغربية",
        "شباكية مقلية بالعسل", "الشباكية التقليدية المغربية", "شباكية مغربية حلويات",
        "الشباكية بالعسل والسمسم", "شباكية رمضان مغربية", "الشباكية المنزلية المغربية",
        "شباكية مقلية بالسمسم", "الشباكية المغربية الأصيلة", "شباكية بالعسل تقليدية",
        "الشباكية الرمضانية بالعسل", "شباكية مغربية منزلية", "الشباكية المقلية بالسمسم",
        "شباكية تقليدية مغربية", "الشباكية بالعسل الطبيعي", "شباكية رمضانية أصيلة",
        "الشباكية المغربية المقلية", "شباكية بالسمسم والعسل", "الشباكية التقليدية رمضان",
        "شباكية مغربية بالعسل", "الشباكية المنزلية بالسمسم", "شباكية مقلية تقليدية",
        "الشباكية الرمضانية الأصيلة", "شباكية مغربية حلوى", "الشباكية بالعسل المغربي",
        "شباكية تقليدية بالسمسم", "الشباكية المقلية المغربية", "شباكية منزلية بالعسل",
        "الشباكية المغربية التقليدية", "شباكية رمضان بالعسل", "الشباكية الأصيلة بالسمسم",
        "شباكية مغربية مقلية منزلية", "الشباكية بالعسل والسمسم التقليدية", "شباكية رمضانية مغربية أصيلة"
    ],
}

# Output configuration
OUTPUT_DIR = "D:/moroccan_food_images_v2"
IMAGES_PER_CLASS = 1000
TRAIN_RATIO = 0.75

def is_valid_image(img_path, min_size=150):
    """Validate image: check if it's a real image and meets minimum size"""
    try:
        with Image.open(img_path) as img:
            # Check if image can be loaded
            img.verify()
            
        # Reopen for size check (verify() closes the file)
        with Image.open(img_path) as img:
            width, height = img.size
            
            # Reject too small images (likely icons, logos, or thumbnails)
            if width < min_size or height < min_size:
                return False
            
            # Reject extremely elongated images (likely banners or decorative elements)
            aspect_ratio = max(width, height) / min(width, height)
            if aspect_ratio > 4:
                return False
            
            return True
    except Exception as e:
        logging.warning(f"Invalid image {img_path}: {e}")
        return False

def get_image_hash(img_path):
    """Calculate MD5 hash of image to detect duplicates"""
    try:
        with Image.open(img_path) as img:
            return hashlib.md5(img.tobytes()).hexdigest()
    except:
        return None

def scrape_dish(dish_name, queries, target_count):
    """Scrape images for a single dish with validation - supports resume"""
    temp_base_dir = os.path.join(OUTPUT_DIR, f"temp_{dish_name}")
    
    # Check for existing temp folders to resume
    start_query_idx = 1
    collected_hashes = set()
    valid_images = []
    
    if os.path.exists(temp_base_dir):
        # Resume from existing temp folders
        logging.info(f"Found existing temp folder for {dish_name} - resuming...")
        for query_folder in Path(temp_base_dir).glob("query_*"):
            # Load existing valid images from previous queries
            for img_file in query_folder.glob("*.*"):
                if is_valid_image(img_file):
                    img_hash = get_image_hash(img_file)
                    if img_hash and img_hash not in collected_hashes:
                        collected_hashes.add(img_hash)
                        valid_images.append(img_file)
            # Track highest query number
            try:
                query_num = int(query_folder.name.split('_')[1])
                start_query_idx = max(start_query_idx, query_num + 1)
            except:
                pass
        
        if valid_images:
            logging.info(f"Loaded {len(valid_images)} existing images, starting from query #{start_query_idx}")
    
    os.makedirs(temp_base_dir, exist_ok=True)
    
    logging.info(f"\n{'='*60}")
    logging.info(f"Scraping: {dish_name} (target: {target_count} images)")
    logging.info(f"Current: {len(valid_images)} | Need: {target_count - len(valid_images)} more")
    logging.info(f"{'='*60}")
    
    for idx, query in enumerate(queries, 1):
        # Skip already processed queries
        if idx < start_query_idx:
            continue
            
        if len(valid_images) >= target_count:
            break
        
        remaining = target_count - len(valid_images)
        logging.info(f"[{idx}/{len(queries)}] Query: '{query}' (need {remaining} more)")
        
        # Create separate temp folder for this query
        query_temp_dir = os.path.join(temp_base_dir, f"query_{idx}")
        
        # Skip if this query folder already has images
        if os.path.exists(query_temp_dir) and list(Path(query_temp_dir).glob("*.*")):
            logging.info(f"  → Query {idx} already processed, skipping...")
            continue
        
        os.makedirs(query_temp_dir, exist_ok=True)
        
        # Calculate how many more images we need
        fetch_count = min(remaining * 3, 100)  # Fetch 3x more to account for filtering
        
        try:
            crawler = BingImageCrawler(
                downloader_threads=4,
                storage={'root_dir': query_temp_dir}
            )
            
            crawler.crawl(
                keyword=query,
                max_num=fetch_count,
                min_size=(200, 200),
            )
            
            # Validate and deduplicate downloaded images from THIS query only
            new_valid = 0
            for img_file in list(Path(query_temp_dir).glob("*.*")):  # Convert to list to avoid issues
                if len(valid_images) >= target_count:
                    break
                
                # Validate image
                if not is_valid_image(img_file):
                    try:
                        img_file.unlink()
                    except:
                        pass
                    continue
                
                # Check for duplicates
                img_hash = get_image_hash(img_file)
                if img_hash and img_hash not in collected_hashes:
                    collected_hashes.add(img_hash)
                    valid_images.append(img_file)
                    new_valid += 1
                else:
                    try:
                        img_file.unlink()
                    except:
                        pass
            
            logging.info(f"  → Found {new_valid} new valid images | Total: {len(valid_images)}/{target_count}")
            time.sleep(2)
            
        except KeyboardInterrupt:
            logging.warning(f"\n⚠️  Interrupted! Progress saved. Run again to resume from query #{idx}")
            raise
        except Exception as e:
            logging.error(f"Error with query '{query}': {e}")
            continue
    
    # Split into train/val
    random.shuffle(valid_images)
    split_point = int(len(valid_images) * TRAIN_RATIO)
    train_images = valid_images[:split_point]
    val_images = valid_images[split_point:]
    
    # Create final directories
    train_dir = os.path.join(OUTPUT_DIR, "train", dish_name)
    val_dir = os.path.join(OUTPUT_DIR, "validation", dish_name)
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    
    # Move images to final locations (with error handling)
    moved_train = 0
    for i, img in enumerate(train_images):
        try:
            if img.exists():  # Check if file still exists
                ext = img.suffix
                dst = os.path.join(train_dir, f"{dish_name}_{i:04d}{ext}")
                shutil.move(str(img), dst)
                moved_train += 1
        except Exception as e:
            logging.warning(f"Failed to move train image {img.name}: {e}")
    
    moved_val = 0
    for i, img in enumerate(val_images):
        try:
            if img.exists():  # Check if file still exists
                ext = img.suffix
                dst = os.path.join(val_dir, f"{dish_name}_{i:04d}{ext}")
                shutil.move(str(img), dst)
                moved_val += 1
        except Exception as e:
            logging.warning(f"Failed to move val image {img.name}: {e}")
    
    # Cleanup temp directory
    shutil.rmtree(temp_base_dir, ignore_errors=True)
    
    logging.info(f"✓ {dish_name}: {moved_train} train, {moved_val} val")
    return moved_train + moved_val

def main():
    logging.info("="*60)
    logging.info("MOROCCAN FOOD IMAGE SCRAPER V2")
    logging.info("="*60)
    logging.info(f"Total dishes: {len(MOROCCAN_DISHES)}")
    logging.info(f"Target per dish: {IMAGES_PER_CLASS}")
    logging.info(f"Output directory: {OUTPUT_DIR}")
    logging.info(f"Image validation: ENABLED (min 150px, aspect ratio check)")
    logging.info("="*60)
    
    results = {}
    for dish_name, queries in MOROCCAN_DISHES.items():
        count = scrape_dish(dish_name, queries, IMAGES_PER_CLASS)
        results[dish_name] = count
    
    # Summary
    logging.info("\n" + "="*60)
    logging.info("SCRAPING COMPLETE!")
    logging.info("="*60)
    for dish, count in results.items():
        logging.info(f"{dish:20s}: {count:4d} images")
    logging.info(f"\nTotal images: {sum(results.values())}")
    logging.info(f"Saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    import random
    main()
