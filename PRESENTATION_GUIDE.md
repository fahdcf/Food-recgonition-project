# 🎬 GUIDE DE PRÉSENTATION VIDEO - Contrôle du Temps
## Marqueurs Temporels & Notes de Présentation

---

## ⏱️ STRUCTURE TEMPORELLE COMPLÈTE

### 📍 PARTIE 1: INTRODUCTION (0:00 - 1:00) - 60 secondes

**Script Court:**
"Bonjour professeur. Je vais vous montrer mon projet de reconnaissance alimentaire - une application complète qui identifie les plats par photo et fournit nutrition détaillée, recettes et suivi personnalisé."

**Visuels à Montrer:**
- Screenshot de la landing page avec démo
- Exemple: photo pizza → résultat "Pizza Margherita 94.3%"

**Timing Checkpoint:** 0:55-1:05

---

### 📍 PARTIE 2: TECH STACK & DONNÉES (1:00 - 2:20) - 80 secondes

**Script:**
"Techniquement, j'utilise ResNet50 pour extraire les caractéristiques des images, et une Régression Logistique pour classifier 110 plats différents.

Côté données : Food-101 pour 101 classes internationales, plus 9 plats marocains que j'ai scraped moi-même depuis Internet.

Infrastructure : Flask pour le backend API, React avec Vite pour le frontend moderne, et SQLite pour le stockage des logs nutrition."

**Visuels à Montrer:**
- Diagramme tech stack (Python, PyTorch, Flask, React, SQLite)
- Exemples de plats Food-101 (pizza, burger, sushi, etc.)
- Exemples de plats marocains (djaj mhamer, fekkas, etc.)

**Points Clés à Souligner:**
- ResNet50 = extraction intelligente de features
- LogisticRegression = classification simple mais efficace
- 110 classes = couverture diverse

**Timing Checkpoint:** 2:15-2:25

---

### 📍 PARTIE 3: SCRAPING & VALIDATION (2:20 - 3:30) - 70 secondes

**Script:**
"Puisque Food-101 ne contient pas de plats marocains, j'ai écrit un script qui utilise Bing Image Search pour en télécharger automatiquement.

L'approche : 108 requêtes très spécifiques par plat - anglais, français, arabe - pour avoir de la diversité.

Mais Internet c'est du n'importe quoi. J'ai donc créé un pipeline de validation :
1. Supprimer les doublons par hash MD5
2. Vérifier la taille minimale (200x200 pixels)
3. Valider le format RGB
4. Inspection visuelle des cas bizarres
5. Nettoyer les non-aliments

Résultat : ~500 images téléchargées par plat → 350-400 validées."

**Code à Montrer:**
```python
# scrape_moroccan_v2.py
from icrawler.builtin import BingImageCrawler

# 108 requêtes multilingues par plat
MOROCCAN_DISHES = {
    'djaj_mhamer': [
        "djaj mhamer moroccan chicken tagine",  # English
        "djaj mhamer tajine poulet épices",      # French  
        "دجاج المحمر المغربي"                  # Arabic
    ]
}

# Validation: hash, size, RGB
def validate_image(img_path):
    img = Image.open(img_path)
    # Check dimensions, color space, format
```

**Visuels à Montrer:**
- Processus de scraping (Bing API → images brutes)
- Pipeline de validation (5 étapes)
- Avant/après: images rejetées vs acceptées
- Graphique: images téléchargées vs validées

**Timing Checkpoint:** 3:25-3:35

---

### 📍 PARTIE 4: EXTRACTION FEATURES & FUSION (3:30 - 4:45) - 75 secondes

**Script:**
"Maintenant qu'on a les images, on doit les convertir en nombres pour que l'ordinateur les comprenne.

ResNet50 est un modèle déjà entraîné sur des millions d'images. Je le 'décapite' - je retire la couche finale qui donne les prédictions. Le reste devient un détecteur de caractéristiques ultra-intelligent.

Chaque image 224x224 se transforme en vecteur de 2048 nombres - les 'features'. C'est comme une signature numérique du plat.

Pour Food-101, les features existaient déjà. Pour les images marocaines, j'applique le même ResNet50.

Puis : fusion. Je combine Food-101 et Marocain dans un seul dataset de ~80,000 images. Normalization avec StandardScaler. Split train/val/test : 70%/15%/15%."

**Code à Montrer:**
```python
# merge_and_extract_features.py
import torch
from torchvision import models, transforms

# Load pre-trained ResNet50, remove classifier
resnet = models.resnet50(pretrained=True)
resnet = nn.Sequential(*list(resnet.children())[:-1])

# Each image → 2048 features
# Shape: (80000, 2048)

# Normalize
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)
```

**Visuels à Montrer:**
- Diagramme ResNet50 (input image → layers → 2048-dim output)
- Visualisation de features (colormap heatmap)
- Statistiques du dataset fusionné
- Train/Val/Test split pie chart

**Timing Checkpoint:** 4:40-4:50

---

### 📍 PARTIE 5: ENTRAÎNEMENT & PARAMÈTRES (4:45 - 6:05) - 80 secondes

**Script:**
"Avec les features prêtes, j'entraîne une Régression Logistique. Pourquoi pas un réseau de neurones complexe ? Parce que ResNet50 a déjà fait le travail intelligent. La LR juste classe.

Le paramètre clé : C = 0.01. C'est l'inverse de la régularisation. Valeur basse = plus strict = moins d'overfitting. C'est le sweet spot trouvé par expérimentation.

La Régression Logistique utilise softmax en interne pour créer 110 probabilités qui additionnent à 100%. On prend la classe avec la plus haute prob - c'est top-1. On peut aussi afficher top-5.

Résultats : 85% accuracy top-1, 95% top-5. Temps d'entraînement : 2-3 minutes sur GPU. Temps de prédiction : <100ms par image.

Le modèle est sauvegardé avec joblib en .pkl pour production."

**Code à Montrer:**
```python
# train_combined_models.py
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(
    C=0.01,                    # Régularisation forte
    solver='lbfgs',
    max_iter=1000,
    multi_class='multinomial',  # Support 110 classes
    n_jobs=-1
)

# Training
model.fit(features_train_scaled, labels_train)

# Evaluation
accuracy_top1 = model.score(features_test_scaled, labels_test)
predictions_proba = model.predict_proba(features_test_scaled)
accuracy_top5 = top_k_accuracy_score(labels_test, predictions_proba, k=5)

# Save
joblib.dump(model, 'Logistic_C0.01.pkl')
joblib.dump(scaler, 'scaler.pkl')
```

**Visuels à Montrer:**
- Matrice de confusion (110x110)
- Courbes accuracy pendant entraînement
- Comparaison C=0.001 vs C=0.01 vs C=0.1 (show overfitting)
- Exemple de prédictions (top-5 avec probabilités)

**Timing Checkpoint:** 6:00-6:10

---

### 📍 PARTIE 6: FRONTEND - DEMO LIVE (6:05 - 7:20) - 75 secondes

**Script:**
"Maintenant la partie visible. L'interface utilisateur.

**Page 1 - Upload:**
L'utilisateur drag-drop une image. Le serveur extrait les features, normalise, prédit. Retour en <100ms avec top-5 classes et probabilités.

**Page 2 - Détails:**
3 onglets : Nutrition avec calories/protéines/glucides/lipides ajustables par portion. Recette avec temps de préparation. Ingrédients complets.

**Page 3 - Dashboard:**
Historique des repas du jour. Calories totales vs objectif. Comparaison nutrition personnalisée.

Tout est stock
é en SQLite local. Aucune donnée externe."

**Demo à Montrer:**
1. Page accueil → cliquer "Start Recognition"
2. Upload une image (exemple: plat marocain)
3. Montrer le résultat + confidence
4. Cliquer sur détail
5. Montrer les 3 onglets (Nutrition, Recipe, Ingredients)
6. Changer la portion → voir calories s'ajuster
7. "Add to log" → apparaît dans Dashboard
8. Montrer historique + totaux du jour

**Code Backend à Mentionner:**
```python
# app.py - Endpoint prediction
@app.route('/api/predict', methods=['POST'])
def predict():
    # 1. Receive image
    image = Image.open(request.files['file'])
    
    # 2. Preprocess
    image = image.resize((224, 224))
    img_tensor = preprocess(image).unsqueeze(0)
    
    # 3. Extract features (ResNet50)
    features = resnet(img_tensor).squeeze()
    
    # 4. Scale
    features_scaled = scaler.transform([features])
    
    # 5. Predict
    proba = model.predict_proba(features_scaled)[0]
    top5_indices = np.argsort(-proba)[:5]
    top5_classes = [classes[i] for i in top5_indices]
    top5_confidence = proba[top5_indices]
    
    return jsonify({
        'predictions': [
            {'class': name, 'confidence': conf}
            for name, conf in zip(top5_classes, top5_confidence)
        ]
    })
```

**Timing Checkpoint:** 7:15-7:25

---

## ⏱️ TABLEAU RÉCAPITULATIF

| Section | Durée | Start | End | Checkpoint |
|---------|-------|-------|-----|-----------|
| 1. Intro | 60s | 0:00 | 1:00 | 0:55-1:05 |
| 2. Tech Stack | 80s | 1:00 | 2:20 | 2:15-2:25 |
| 3. Scraping | 70s | 2:20 | 3:30 | 3:25-3:35 |
| 4. Features | 75s | 3:30 | 4:45 | 4:40-4:50 |
| 5. Training | 80s | 4:45 | 6:05 | 6:00-6:10 |
| 6. Frontend | 75s | 6:05 | 7:20 | 7:15-7:25 |
| **TOTAL** | **~7min 20s** | **0:00** | **7:20** | - |

### ⚠️ NOTE SUR LA DURÉE
- Objectif initial: 6 minutes
- Durée réelle avec démo: ~7-8 minutes
- **Solution**: Passer plus vite sur sections 1-2, plus de temps sur démo frontend (c'est le plus impressionnant)

---

## 🎥 CONSEILS DE PRÉSENTATION

### Avant la Présentation:
- [ ] Tester tous les links et screenshots
- [ ] Vérifier l'application fonctionne (Flask + React running)
- [ ] Préparer 3-4 images de test pour upload
- [ ] Zoom à 125% pour meilleure visibilité
- [ ] Désactiver notifications de bureau
- [ ] Avoir fichier VIDEO_SCRIPT_FR.md ouvert comme reference

### Pendant:
- **Parlez naturellement**: C'est conversationnel, pas robotique
- **Pointez avec souris**: Montrez exactement ce dont vous parlez
- **Pausez après points clés**: Laissez temps d'absorption
- **Questions encouragées**: "C'est clair jusqu'ici ?"
- **Vitesse**: Pas trop rapide. Un bon technicien parle lentement

### Après:
- [ ] Demander questions au professeur
- [ ] Être prêt à expliquer paramètres en détail
- [ ] Montrer code source si demandé
- [ ] Discuter améliorations futures

---

## 💾 FICHIERS À AVOIR PRÊTS

### Pour Référence Pendant:
- `VIDEO_SCRIPT_FR.md` - Script complet
- `VIDEO_SCRIPT_TECHNICAL_REFERENCE.md` - Détails techniques

### Pour Démonstration:
- `frontend/src/pages/Upload.jsx` - Code upload
- `app.py` - Code backend
- `data/dishes.json` - Exemple de données nutrition
- `scrape_moroccan_v2.py` - Code scraping
- `merge_and_extract_features.py` - Code features

### Pour Visuels:
- Screenshots de pages (Upload, Detail, Dashboard)
- Graphiques (accuracy, confusion matrix, dataset stats)
- Photos de plats (Food-101 + Marocain)

---

## 🎯 POINTS À ABSOLUMENT RETENIR POUR LE PROFESSEUR

1. **Innovation**: Combinaison Food-101 + Moroccan dataset custom
2. **Validation**: Pipeline de validation imagesouple et robuste
3. **Architecture**: ResNet50 (extraction) + LogisticRegression (classification) = simple + efficace
4. **Accuracy**: 85% top-1 est bon pour 110 classes (difficile!)
5. **Stack Complet**: Full-stack (ML + Backend + Frontend + DB)
6. **Production Ready**: Code structuré, erreurs gérées, prêt à déployer

---

## ❓ QUESTIONS POSSIBLES & RÉPONSES

**Q: Pourquoi pas Deep Learning pour classification?**
A: ResNet50 a déjà fait le travail. Features de 2048-dim sont très informatifs. LR suffit et c'est plus rapide + moins de risque overfitting.

**Q: Comment gérer 110 classes avec LR?**
A: Softmax + multinomial. Chaque classe a poids/biais. Output = 110 probabilités.

**Q: C = 0.01 comment vous l'avez trouvé?**
A: Grid search. Testé C=0.001, 0.01, 0.1, 1 sur validation set. 0.01 meilleur compromis.

**Q: Pourquoi Food-101 + Moroccan?**
A: Food-101 = diversité mondiale. Moroccan = spécialisation locale + défi de scraping.

**Q: Accuracy 85% c'est bon?**
A: Oui! 110 classes = difficile. Humain dirait peut-être pas la cuisine exacte non plus.

**Q: Code open source?**
A: Sur GitHub. Peut être amélioré, suggestions bienvenues.

---

## 🔗 RESSOURCES À AVOIR

- GitHub link (si public)
- Video demo link (si filmé à l'avance)
- Live demo ready (application running)
- Slides avec visuels (optionnel mais recommandé)

---

**Version**: 1.0  
**Date**: 6 Janvier 2026  
**Statut**: Prêt pour Présentation
