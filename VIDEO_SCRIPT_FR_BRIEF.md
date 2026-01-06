# Script Vidéo (Version Concise) – Reconnaissance Alimentaire
Durée cible: ≤ 6 minutes
Ton: professionnel, direct, duo, mots simples

---

## 1) Objectif et architecture (≈ 40s)
Nous montrons une appli qui reconnaît un plat à partir d’une photo. Elle donne la classe, le top-5, la nutrition pour 100g, la recette et les ingrédients. Nous avons construit un backend Flask (API), un frontend React + Vite, un modèle ResNet50 + Régression Logistique, et une base SQLite.

Fichiers clés: [app.py](app.py), [frontend/src/pages/Upload.jsx](frontend/src/pages/Upload.jsx)

---

## 2) Données et classes (≈ 25s)
Nous utilisons Food-101 (101 classes) et ajoutons 20 classes marocaines. Au total, nous gérons 121 classes pour l’entraînement.

Fichier clé: [merge_and_extract_features.py](merge_and_extract_features.py)

---

## 3) Scraping des images marocaines (≈ 1 min 45s)
Pour couvrir 20 plats marocains, nous lançons des recherches en anglais, français et arabe avec Bing Image Search (icrawler). Nous téléchargeons, puis nous trions: on retire les doublons (hash MD5), on garde les images ≥ 200×200, on vérifie qu’elles sont lisibles en RGB, on regarde les cas ambigus à la main et on enlève les images hors-sujet.

Code (extraits):
```python
# scrape_moroccan_v2.py
from icrawler.builtin import BingImageCrawler
from PIL import Image
import hashlib, os

MOROCCAN_DISHES = {
    'djaj_mhamer': [
        "djaj mhamer moroccan chicken tagine",
        "djaj mhamer tajine poulet épices",
        "دجاج المحمر المغربي"
    ],
    # ... autres plats
}

def is_valid_image(path):
    try:
        with Image.open(path) as img:
            w, h = img.size
            return (w >= 200 and h >= 200 and img.mode in ("RGB", "RGBA"))
    except Exception:
        return False

def md5_of_file(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()
```

Fichier: [scrape_moroccan_v2.py](scrape_moroccan_v2.py)

Résultats: ~500 images brutes par plat → ~350–400 validées par plat; ~3 500 images marocaines conservées.

---

## 4) Extraction des caractéristiques (≈ 1 min 45s)
Nous passons chaque image dans ResNet50 (sans la dernière couche) pour obtenir un vecteur de 2048 valeurs. Avant ça, on redimensionne, on croppe en 224×224 et on normalise comme ImageNet. On traite par lots, puis on combine les vecteurs Food-101 et marocains et on normalise avec StandardScaler.

Code (extraits):
```python
# merge_and_extract_features.py
import torch, torch.nn as nn
from torchvision import models, transforms

resnet = models.resnet50(pretrained=True)
resnet = nn.Sequential(*list(resnet.children())[:-1])  # retire le classificateur
resnet.eval()

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

# img → tensor → resnet(img)[2048]
```

Fichiers: [merge_and_extract_features.py](merge_and_extract_features.py), [train_resnet_rf_simple.py](train_resnet_rf_simple.py)

---

## 5) Entraînement du modèle (≈ 1 min 45s)
Nous classons les 121 classes avec une Régression Logistique multinomiale (softmax), solver LBFGS, régularisation C=0.01. Nous entraînons sur les vecteurs normalisés, puis nous sauvegardons le modèle et le scaler avec joblib. Résultats habituels: Top-1 ≈ 85%, Top-5 ≈ 95%, inférence < 100 ms.

Code (extraits):
```python
# train_combined_models.py
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib

scaler = StandardScaler().fit(X_train)
X_train_s = scaler.transform(X_train)
X_val_s   = scaler.transform(X_val)

model = LogisticRegression(
    C=0.01,
    solver='lbfgs',
    max_iter=1000,
    multi_class='multinomial',
    n_jobs=-1,
    random_state=42,
)
model.fit(X_train_s, y_train)

proba = model.predict_proba(X_val_s)  # shape: [N, 110]

joblib.dump(model, 'D:/food_recognition_models/combined_models/Logistic_C0.01.pkl')
joblib.dump(scaler,'D:/food_recognition_models/combined_models/scaler.pkl')
```

Fichiers: [train_combined_models.py](train_combined_models.py), [app.py](app.py) pour le chargement et l’inférence.

---

## 6) Démonstration (≈ 30s)
Nous téléversons une image sur la page Upload. L'API `/api/predict` fait le prétraitement, passe par ResNet50, applique le scaler, puis la Régression Logistique pour sortir le top-5. Le frontend montre les scores et nous ouvrons les détails nutrition/recette/ingrédients. Ensuite, on peut ajouter le plat à l'apport nutritionnel quotidien: le système enregistre les calculs et on retrouve tout dans le tableau de bord.

Fichiers: [frontend/src/pages/Upload.jsx](frontend/src/pages/Upload.jsx), [app.py](app.py)

---

## 7) Conclusion (≈ 15s)
Nous avons un système bout en bout: collecte, tri, extraction, fusion, entraînement, inférence, interface. C’est simple, reproductible, et prêt pour du fine-tuning, plus d’images ou un déploiement.
