# 💼 Gestion de Factures - Django

Une application web simple de gestion de produits et de factures développée avec Django. Elle permet de :
- Ajouter, modifier et supprimer des produits (avec nom, prix, date de péremption)
- Créer des factures personnalisées avec plusieurs produits
- Gérer les quantités de chaque produit dans une facture
- Afficher le total, la quantité, le nom du client
- Exporter les factures au format **CSV**

---

## 📦 Prérequis

- Python 3.8+
- pip
- virtualenv *(optionnel mais recommandé)*

---

## 🚀 Installation

```bash
# Cloner le projet
git clone https://github.com/MenadAcheraiou/gestion_factures.git
cd gestion_factures

# Créer un environnement virtuel (recommandé)
python3 -m venv env
source env/bin/activate  # Sur Windows : env\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Créer la base de données et appliquer les migrations
python manage.py migrate

# Lancer le serveur
python manage.py runserver
