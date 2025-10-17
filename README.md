# Dietetic Lab - Backend

Une API REST Django pour une application de suivi nutritionnel et diététique.

## 🚀 Technologies utilisées

- Python 3.13
- Django 5.2
- Django REST Framework
- PostgreSQL
- JWT pour l'authentification


## 📋 Prérequis

- Python 3.13 ou supérieur
- pip (gestionnaire de paquets Python)
- Un environnement virtuel Python
- PostgreSQL


## 🛠️ Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/Edwige08/dietetic_lab_back.git
cd dietetic_lab_back
```

2. Créez et activez un environnement virtuel :
```bash
python -m venv .venv
source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurez les variables d'environnement dans un fichier `.env` :
```env
SECRET_KEY=votre_clé_secrète
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/dietetic_lab
```

5. Appliquez les migrations :
```bash
python manage.py migrate
```

6. Lancez le serveur de développement :
```bash
python manage.py runserver
```


## 🏗️ Structure du projet

```
dietetic_lab_back/
├── dietetic_lab_api/     # Configuration principale du projet Django
├── dietetics/            # Application principale
│   ├── models.py         # Modèles de données
│   ├── views.py          # Vues et logique métier
│   ├── urls.py           # Configuration des URLs
│   ├── serializers.py    # Sérialiseurs pour l'API
│   └── tests/            # Tests
│       ├── test_endpoints.py    # Tests d'intégration
│       ├── test_e2e.py          # Tests end-to-end
│       └── test_verify_mail.py  # Tests unitaires
└── requirements.txt      # Dépendances du projet
```


## 🔑 Authentification

L'API utilise JWT (JSON Web Tokens) pour l'authentification. Pour obtenir un token :

1. Créez un compte utilisateur via `/auth/register/`
2. Connectez-vous via `/auth/login/` pour obtenir vos tokens
3. Utilisez le token d'accès dans le header `Authorization: Bearer <token>`


## 📚 Endpoints principaux

- `/auth/register/` : Inscription d'un nouvel utilisateur
- `/auth/login/` : Connexion et obtention des tokens
- `/auth/refresh/` : Rafraîchissement du token
- `/personal-databases/` : Gestion des bases de données personnelles
- `/foods/` : Gestion des aliments
- `/meals/` : Gestion des repas


## 🧪 Tests

Le projet inclut trois types de tests :

1. **Tests unitaires** :
```bash
pytest dietetics/tests/test_verify_mail.py
```

2. **Tests d'intégration** :
```bash
pytest dietetics/tests/test_endpoints.py
```

3. **Tests End-to-End** :
```bash
pytest dietetics/tests/test_e2e.py
```

Pour exécuter tous les tests :
```bash
pytest
```


## 🤝 Contribution

1. Fork le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request