# 🎬 Script Vidéo Explicative - Projet de Reconnaissance Alimentaire
## Version Française - 6 minutes maximum

---

## 📋 STRUCTURE GÉNÉRALE
- **Durée totale**: ~6 minutes (~1400 mots parlés)
- **Sections**: 5 parties principales
- **Rythme**: Clair et pédagogique pour un professeur

---

## PARTIE 1: INTRODUCTION & IDÉE GÉNÉRALE (1 min)

### 📝 Script à dire:
"Bonjour professeur, je vais vous présenter mon projet de reconnaissance alimentaire. L'idée est simple mais puissante : créer une application intelligente qui reconnaît automatiquement n'importe quel plat à partir d'une photo, puis fournit des informations nutritionnelles détaillées.

Imaginez : vous prenez une photo de votre déjeuner, l'application vous dit 'c'est une pizza margherita', vous donne les calories, les protéines, les glucides, et même la recette pour la cuisiner à la maison. C'est une application complète de nutrition et de bien-être."

### 🔧 Contexte Technique:
- **Objectif**: Classification d'images de 110 classes alimentaires différentes
- **Résultat**: Prédictions avec probabilités et informations nutritionnelles
- **Public**: Personnes voulant suivre leur nutrition simplement

---

## PARTIE 2: TECH STACK & DONNÉES (1 min 20 sec)

### 📝 Script à dire:
"Passons à la technologie utilisée. Pour l'intelligence artificielle, j'ai choisi ResNet50, qui est un réseau de neurones profond très populaire pour la reconnaissance d'images. C'est comme avoir un expert en images qui a été entraîné sur des millions de photos.

Pour la classification, j'utilise une Régression Logistique. Contrairement à ce qu'on pourrait penser, ce n'est pas seulement pour oui ou non. Avec la bonne configuration, elle peut prédire 110 classes différentes simultanément, avec des probabilités pour chacune.

Pour les données, j'ai utilisé deux sources :
1. Le dataset Food-101 : 101 classes alimentaires internationales, 750 images par classe
2. Mes propres images Marocaines : 9 plats marocains authentiques que j'ai scraped moi-même

Total : 110 classes alimentaires, environ 80 000 images au départ."

### 🔧 Détails Techniques:
- **Backend**: Flask (Python) - API REST
- **Frontend**: React 19 + Vite - Interface moderne
- **Base de données**: SQLite - Logs et objectifs nutritionnels
- **Modèle ML**: ResNet50 (extraction) + Régression Logistique (classification)
- **GPU**: CUDA pour accélération (sinon CPU)

### 📁 Fichiers Référencés:
- `app.py` - Serveur Flask principal
- `requirements_training.txt` - Dépendances ML
- `requirements_backend.txt` - Dépendances serveur

---

## PARTIE 3: SCRAPING & VALIDATION DES IMAGES MAROCAINES (1 min 10 sec)

### 📝 Script à dire:
"Puisque les plats marocains ne sont pas dans Food-101, j'ai dû les télécharger moi-même depuis Internet. J'ai écrit un script qui utilise Bing Image Search pour télécharger automatiquement des images.

Voici le processus : pour chaque plat, par exemple le 'Djaj Mhamer' - un poulet épicé marocain - j'ai créé 108 requêtes de recherche différentes. Pourquoi 108 ? Parce que je voulais être très spécifique : 'djaj mhamer moroccan chicken', 'traditional djaj mhamer recipe', 'spiced moroccan djaj mhamer'... en anglais, français, et même en arabe.

Mais attention ! Internet, c'est du n'importe quoi. On télécharge plein d'images qui ne sont pas du tout des plats - des logos, des textes, des gens cuisinant... C'est là que la validation entre en jeu."

### 🔍 Étapes de Validation:
1. **Détection des doublons** : Avec des hash MD5, on enlève les 100 copies de la même image
2. **Filtrage de taille** : Minimum 200x200 pixels (sinon c'est trop petit)
3. **Validation RGB** : S'assurer que c'est une vraie image couleur
4. **Inspection visuelle** : J'ai manuellement vérifié les images bizarres
5. **Suppression de bruit** : Enlever les images non-alimentaires

### 📊 Résultats du Scraping:
- Téléchargé: ~500 images par plat (5500 au total)
- Après validation: ~350-400 images par plat
- Images valides conservées: ~3500 pour Marocain

### 📁 Fichiers Référencés:
- `scrape_moroccan_v2.py` (lignes 1-443) - Script principal de scraping
  - Utilise `icrawler` pour Bing Image Search
  - Validation avec `PIL (Python Image Library)`
  - Hash-based duplicate detection
  - Queries multilingues (108 par dish)

---

## PARTIE 4: EXTRACTION DE FEATURES & FUSION (1 min 15 sec)

### 📝 Script à dire:
"Maintenant on a nos images, mais l'ordinateur ne sait pas les utiliser directement. On doit convertir chaque image en nombres - des 'features' ou 'caractéristiques'.

Voici comment ça marche : ResNet50 est déjà entraîné sur des millions d'images. Je le 'décapite' - je retire la dernière couche qui donne les prédictions - et j'utilise le reste comme un détecteur de caractéristiques. C'est comme un traducteur d'images.

Chaque image de 224x224 pixels devient un vecteur de 2048 nombres. Ces nombres représentent les 'textures, formes, couleurs' que ResNet50 a appris.

Pour Food-101, c'était simple : j'ai téléchargé les features déjà extraites. Pour les images marocaines, j'ai fait la même chose : ResNet50 + batchs de 16 images pour économiser la mémoire."

### 🔧 Processus Technique:

#### Extraction Food-101:
- Features déjà calculées
- Normalisées avec StandardScaler
- Format: (nombre_images, 2048)

#### Extraction Marocain:
```python
# Exemple du code
resnet = models.resnet50(pretrained=True)
resnet = nn.Sequential(*list(resnet.children())[:-1])  # Remove classifier
# Input: 224x224 RGB image
# Output: 2048-dimensional feature vector
```

#### Fusion:
- Concaténation Food-101 + Marocain
- StandardScaler appliqué à l'ensemble
- Labels: 0-100 (Food-101), 101-109 (Marocain)
- Train/Val/Test split: 70/15/15

### 📁 Fichiers Référencés:
- `merge_and_extract_features.py` (lignes 1-288) - Fusion des datasets
  - Charge food101_root: `D:/food_dataset/images`
  - Charge moroccan_root: `D:/moroccan_food_images`
  - Output: `D:/food_recognition_models/features/`
  - Batch processing pour économie mémoire
  - Incremental saving en cache NPZ

### 📊 Output:
- `train_features.npy` : (56000, 2048)
- `train_labels.npy` : (56000,)
- `val_features.npy` : (12000, 2048)
- `val_labels.npy` : (12000,)
- `test_features.npy` : (12000, 2048)
- `test_labels.npy` : (12000,)

---

## PARTIE 5: ENTRAÎNEMENT DU MODÈLE & PARAMÈTRES (1 min 20 sec)

### 📝 Script à dire:
"Maintenant qu'on a nos features, on entraîne le modèle de classification. La Régression Logistique, c'est un algorithme classique, mais très efficace pour la classification multi-classes.

Pourquoi la Régression Logistique et pas un réseau de neurones complexe ? Parce que :
1. On a déjà les features intelligentes de ResNet50
2. La Régression Logistique fait déjà du multi-classe
3. C'est rapide à entraîner et très interprétable

Parlons des paramètres clés : Le paramètre C = 0.01. C'est quoi ? C'est l'inverse de la force de régularisation. 

Imaginez un artiste qui dessine. S'il a trop de liberté (C trop grand), il dessine n'importe comment. S'il a trop de contraintes (C trop petit), il ne peut rien faire. C = 0.01 signifie : 'sois assez strict pour ne pas overfitter'.

Le modèle fait exactement ça : il crée une frontière de décision dans l'espace de 2048 dimensions pour séparer nos 110 classes. Et il le fait de manière à généraliser, pas juste mémoriser.

Comment prédire 110 classes ? La Régression Logistique utilise 'softmax' en interne. Pour chaque prédiction, elle donne 110 probabilités qui additionnent à 100%. On prend la classe avec la plus haute probabilité - c'est la top-1 prédiction. On peut aussi donner top-5 : les 5 meilleures hypothèses."

### 🔧 Paramètres du Modèle:
```python
# Configuration d'entraînement
LogisticRegression(
    C=0.01,              # Régularisation: évite l'overfitting
    solver='lbfgs',      # Optimiseur
    max_iter=1000,       # Itérations maximales
    multi_class='multinomial',  # Support multi-classe
    n_jobs=-1,           # Parallélisation
    random_state=42
)
```

### 📊 Résultats d'Entraînement:
- **Accuracy Top-1** : ~85%
- **Accuracy Top-5** : ~95%
- **Temps d'entraînement** : ~2-3 minutes (GPU)
- **Temps de prédiction** : <100ms par image

### 🔄 Comment Marche le Multi-classe:

```
Input: vecteur 2048-dim
    ↓
Régression Logistique transforme en probabilités
    ↓
Output: 110 probabilités (une par classe)
    ↓
Softmax: normalise à 100%
    ↓
argmax: prend la classe avec prob la plus haute
    ↓
Résultat: 'Pizza Margherita' avec 94.3% de confiance
```

### 💾 Sauvegarde du Modèle:
```python
# app.py - Chargement
import joblib

model = joblib.load('D:/food_recognition_models/combined_models/Logistic_C0.01.pkl')
scaler = joblib.load('D:/food_recognition_models/combined_models/scaler.pkl')

# Prédiction
features = extract_features(image)  # ResNet50
features_scaled = scaler.transform(features)  # Normalise
predictions = model.predict_proba(features_scaled)  # 110 probabilités
top_class = np.argmax(predictions)
confidence = predictions[0, top_class]
```

### 📁 Fichiers Référencés:
- `train_combined_models.py` ou `train_resnet_rf_simple.py` (lignes 1-224)
  - Charge features depuis cache
  - Entraîne LogisticRegression avec C=0.01
  - Teste sur set de validation
  - Sauvegarde en `.pkl` (joblib format)
  - Génère rapport de précision (top-1, top-5)

### 📁 Modèles Sauvegardés:
- `D:/food_recognition_models/combined_models/Logistic_C0.01.pkl` - Le modèle entraîné
- `D:/food_recognition_models/combined_models/scaler.pkl` - Normalisation des données
- `class_names.json` - Mapping classe -> nom plat

---

## PARTIE 6: FRONTEND - UTILISATION (1 min 15 sec)

### 📝 Script à dire:
"Maintenant que le modèle est entraîné et sauvegardé, passons à l'interface utilisateur - ce que voit le client.

L'application a plusieurs pages principales :

**Page 1 - Upload & Prédiction :**
L'utilisateur peut télécharger une image de plat. Le front-end l'envoie au serveur Flask en REST API. Le serveur :
1. Reçoit l'image
2. La redimensionne à 224x224
3. Applique les mêmes normalisations que l'entraînement
4. Extrait les features avec ResNet50
5. Normalise les features
6. Prédit avec Régression Logistique
7. Retourne top-5 classes avec probabilités

Tout ça en moins de 100 millisecondes.

**Page 2 - Détails du Plat :**
Une fois identifié, l'utilisateur voit :
- Image du plat
- Nom et cuisine d'origine
- 3 onglets : Nutrition, Recette, Ingrédients

**Page 3 - Nutrition Détaillée :**
Les données nutritionnelles sont dans `dishes.json` - 121 plats au total. Chaque plat a :
- Calories par 100g
- Protéines, glucides, lipides
- Liste complète des ingrédients
- Étapes de recette

L'utilisateur peut changer la portion (ex: 150g) et les calories s'ajustent automatiquement.

**Page 4 - Historique & Objectifs :**
L'utilisateur peut logger ses repas, voir les totaux du jour, comparer avec ses objectifs de nutrition.

Tout est stocké en SQLite local."

### 🔧 Architecture Frontend:

```
frontend/
├── src/
│   ├── pages/
│   │   ├── Landing.jsx (accueil avec démo)
│   │   ├── Upload.jsx (prédiction)
│   │   ├── DishDetail.jsx (détails plat)
│   │   ├── AllDishes.jsx (galerie)
│   │   └── Dashboard.jsx (historique)
│   ├── components/
│   │   ├── Navbar.jsx
│   │   └── Toast.jsx (notifications)
│   ├── context/
│   │   └── AppContext.jsx (état global)
│   └── styles/ (CSS glassmorphism)
├── public/
│   └── couscous_15.jpg (démo image)
└── index.html (Font Awesome CDN)
```

### 📡 Endpoints API (Flask):

```
POST /api/predict
- Input: image file
- Output: top-5 classes avec probabilités

GET /api/dishes
- Output: liste de tous les plats

GET /api/dishes/{id}
- Output: détails complets d'un plat (nutrition, recette, ingrédients)

POST /api/logs
- Input: meal log (dish_id, grams, meal_type)
- Output: confirmation + nutrition

GET /api/logs/daily
- Output: résumé nutrition du jour
```

### 🎨 Design:
- **Style**: Glassmorphism (verre teinté moderne)
- **Animations**: Font Awesome Icons + transitions smooth
- **Responsive**: Mobile-first, fonctionne sur tous les appareils
- **Dark Mode**: Thème sombre par défaut

### 📁 Fichiers Référencés:
- `frontend/src/pages/Upload.jsx` - Prédiction (chargement image, envoi API, affichage résultats)
- `frontend/src/pages/DishDetail.jsx` - Détails plat (3 onglets: Nutrition, Recette, Ingrédients)
- `frontend/src/context/AppContext.jsx` - État global (dishes, logs, predictions)
- `app.py` (lignes 100-571) - Routes Flask
  - `/api/predict` - Extraction + prédiction
  - `/api/dishes` - Liste complète
  - `/api/logs` - Logging nutrition

---

## 📊 RÉSUMÉ COMPLET DU FLUX

```
USER EXPERIENCE:
1. Visite site → voir démo
2. Clique "Start Recognition"
3. Upload image du plat
   ↓
BACKEND PROCESSING:
4. Image reçue par Flask
5. Resize 224x224 + normalize
6. ResNet50 extrait features (2048-dim)
7. StandardScaler normalise
8. LogisticRegression(C=0.01) prédit
9. Top-5 probabilités calculées
   ↓
FRONTEND DISPLAY:
10. Top prédiction + probabilité
11. Clic → détails du plat
12. Voir nutrition, recette, ingrédients
13. Changer portion → calcul auto
14. "Add to log" → sauvegarde en DB
15. Vue historique nutrition du jour
```

---

## 🔑 POINTS CLÉS À RETENIR

| Aspect | Détail |
|--------|--------|
| **Modèle** | ResNet50 + Régression Logistique |
| **Classes** | 110 (101 Food-101 + 9 Marocains) |
| **Précision** | 85% top-1, 95% top-5 |
| **Temps Prédiction** | <100ms |
| **Frontend** | React 19 + Vite |
| **Backend** | Flask REST API |
| **Database** | SQLite (logs + nutrition) |
| **Données Nutritionnelles** | 121 plats détaillés |
| **Validation Scraping** | Hash-based + taille + format RGB |
| **Paramètre Clé** | C=0.01 (régularisation) |

---

## 📁 ARBORESCENCE DES FICHIERS CLÉS

```
Food Recognition Project/
├── Backend ML:
│   ├── scrape_moroccan_v2.py (Bing Image scraping + validation)
│   ├── merge_and_extract_features.py (ResNet50 features)
│   ├── train_combined_models.py (LogisticRegression C=0.01)
│   └── app.py (Flask API server)
│
├── Frontend:
│   ├── frontend/src/pages/
│   │   ├── Landing.jsx (démo + call-to-action)
│   │   ├── Upload.jsx (prédiction)
│   │   ├── DishDetail.jsx (détails complets)
│   │   ├── AllDishes.jsx (galerie)
│   │   └── Dashboard.jsx (historique)
│   ├── frontend/index.html (Font Awesome CDN)
│   └── frontend/src/context/AppContext.jsx (état global)
│
├── Data:
│   ├── data/dishes.json (121 plats + nutrition + recettes)
│   ├── data/food_app.db (SQLite - logs + goals)
│   └── frontend/public/couscous_15.jpg (démo image)
│
└── Models:
    ├── D:/food_recognition_models/combined_models/
    │   ├── Logistic_C0.01.pkl (modèle entraîné)
    │   ├── scaler.pkl (normalisation)
    │   └── class_names.json (mapping)
    └── D:/food_recognition_models/features/
        ├── train_features.npy (56000, 2048)
        ├── train_labels.npy
        ├── val_features.npy
        └── test_features.npy
```

---

## 💡 POINTS DE DISCUSSION POSSIBLE POUR LE PROFESSEUR

1. **Sur le Scraping**: "Pourquoi validation si minutieuse ? Parce que des mauvaises données = mauvais modèle"
2. **Sur la Régularisation**: "C=0.01 c'est un sweet spot entre sous-fit et sur-fit"
3. **Sur le Multi-classe**: "Softmax généralise naturellement pour N classes"
4. **Sur Accuracy 85%**: "C'est bon pour production car Food-101 est un dataset difficile (101 classes, plats similaires)"
5. **Sur Performance**: "<100ms car ResNet feature + linear prediction est très rapide"

---

## 🎬 TIMING ESTIMÉ

| Section | Durée |
|---------|-------|
| Intro | 60s |
| Tech Stack | 80s |
| Scraping & Validation | 70s |
| Features & Fusion | 75s |
| Entraînement Modèle | 80s |
| Frontend & Usage | 75s |
| **TOTAL** | **~6 min** |

---

**Créé le**: 6 Janvier 2026  
**Projet**: Food Recognition - Full Stack Application  
**Auteur**: [Votre Nom]  
**Version**: 1.0 - Script Complet Français
