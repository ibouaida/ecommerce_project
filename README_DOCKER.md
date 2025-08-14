# Architecture Microservices Ecommerce avec Docker

## Vue d'ensemble

Cette application ecommerce utilise une architecture microservices containerisée avec Docker et Docker Compose. L'architecture sépare clairement les responsabilités entre les différents services.

## Architecture des Microservices

### Services Principaux

1. **Frontend (React)** - Port 3000
   - Interface utilisateur React
   - Served par Nginx en production
   - Communique avec le backend via API REST

2. **Backend (Django)** - Port 8000
   - API REST Django
   - Gestion des produits, commandes, utilisateurs
   - Base de données PostgreSQL

3. **Base de données (PostgreSQL)** - Port 5432
   - Stockage persistant des données
   - Optimisé pour les applications ecommerce

4. **Cache (Redis)** - Port 6379
   - Cache de session
   - Cache d'application
   - Queue de tâches (optionnel)

### Services de Support

5. **Reverse Proxy (Nginx)** - Port 80/443
   - Routage intelligent entre frontend et backend
   - Load balancing
   - SSL/TLS termination
   - Compression et optimisation

6. **Monitoring (Prometheus)** - Port 9090
   - Collecte de métriques
   - Surveillance des services
   - Alertes (optionnel)

7. **Logs (Elasticsearch)** - Port 9200
   - Centralisation des logs
   - Recherche et analyse
   - Kibana (optionnel)

## Structure des Fichiers

```
ecommerce_project/
├── docker-compose.yml          # Configuration principale
├── backend/
│   ├── Dockerfile             # Image du backend Django
│   ├── .dockerignore          # Fichiers exclus du build
│   └── requirements.txt       # Dépendances Python
├── frontend/
│   ├── Dockerfile             # Image du frontend React
│   ├── .dockerignore          # Fichiers exclus du build
│   ├── nginx.conf             # Configuration Nginx pour React
│   └── package.json           # Dépendances Node.js
├── nginx/
│   └── nginx.conf             # Configuration du reverse proxy
├── monitoring/
│   └── prometheus.yml         # Configuration Prometheus
├── init.sql                   # Initialisation de la base de données
└── README_DOCKER.md          # Ce fichier
```

## Commandes Docker

### Démarrage de l'application

```bash
# Construire et démarrer tous les services
docker-compose up --build

# Démarrer en arrière-plan
docker-compose up -d --build

# Démarrer seulement certains services
docker-compose up backend frontend db
```

### Gestion des services

```bash
# Voir les logs
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f backend

# Arrêter tous les services
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v

# Redémarrer un service
docker-compose restart backend
```

### Maintenance

```bash
# Mettre à jour les images
docker-compose pull

# Reconstruire les images
docker-compose build --no-cache

# Nettoyer les images non utilisées
docker system prune -a

# Voir l'utilisation des ressources
docker stats
```

## Configuration des Variables d'Environnement

### Backend (Django)

```bash
DEBUG=False
DJANGO_SETTINGS_MODULE=ecommerce.settings
DATABASE_URL=postgresql://ecommerce_user:ecommerce_password@db:5432/ecommerce_db
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,backend
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://frontend:80
```

### Frontend (React)

```bash
REACT_APP_API_URL=http://localhost:8000/api
NODE_ENV=production
```

### Base de données (PostgreSQL)

```bash
POSTGRES_DB=ecommerce_db
POSTGRES_USER=ecommerce_user
POSTGRES_PASSWORD=ecommerce_password
```

## Accès aux Services

- **Application principale** : http://localhost
- **Frontend direct** : http://localhost:3000
- **Backend API** : http://localhost:8000
- **Admin Django** : http://localhost/admin/
- **Prometheus** : http://localhost:9090
- **Elasticsearch** : http://localhost:9200

## Sécurité

### Bonnes Pratiques Implémentées

1. **Utilisateurs non-root** : Les conteneurs utilisent des utilisateurs non-privilégiés
2. **Health checks** : Surveillance automatique de l'état des services
3. **Headers de sécurité** : Protection XSS, CSRF, etc.
4. **Isolation réseau** : Réseau Docker dédié
5. **Volumes persistants** : Données séparées des conteneurs

### Recommandations de Production

1. **Variables d'environnement** : Utiliser des secrets Docker ou des fichiers .env
2. **SSL/TLS** : Configurer les certificats SSL dans nginx/ssl/
3. **Backup** : Automatiser les sauvegardes des volumes
4. **Monitoring** : Configurer Grafana avec Prometheus
5. **Logs** : Configurer ELK Stack (Elasticsearch, Logstash, Kibana)

## Développement

### Mode Développement

Pour le développement, vous pouvez utiliser des volumes pour le hot-reload :

```bash
# Démarrer en mode développement
docker-compose -f docker-compose.dev.yml up
```

### Debugging

```bash
# Accéder à un conteneur
docker-compose exec backend bash
docker-compose exec frontend sh

# Voir les logs en temps réel
docker-compose logs -f --tail=100

# Inspecter un service
docker-compose ps
docker inspect ecommerce_backend
```

## Performance

### Optimisations Implémentées

1. **Multi-stage builds** : Images plus légères
2. **Compression gzip** : Réduction de la bande passante
3. **Cache des assets** : Optimisation des performances
4. **Load balancing** : Distribution de la charge
5. **Health checks** : Détection rapide des problèmes

### Monitoring

- **Prometheus** : Métriques système et application
- **Health checks** : Surveillance automatique
- **Logs centralisés** : Elasticsearch pour l'analyse

## Troubleshooting

### Problèmes Courants

1. **Ports déjà utilisés** : Vérifier les ports 80, 3000, 8000, 5432
2. **Problèmes de permissions** : Vérifier les volumes Docker
3. **Connexion base de données** : Attendre que PostgreSQL soit prêt
4. **Build échoué** : Vérifier les Dockerfiles et .dockerignore

### Commandes de Diagnostic

```bash
# Vérifier l'état des services
docker-compose ps

# Voir les logs d'erreur
docker-compose logs --tail=50

# Tester la connectivité
docker-compose exec backend python manage.py check

# Vérifier la base de données
docker-compose exec db psql -U ecommerce_user -d ecommerce_db
```

## Évolutivité

Cette architecture permet une évolution facile :

1. **Scaling horizontal** : Ajouter des instances de services
2. **Nouveaux services** : Intégrer facilement de nouveaux microservices
3. **Technologies** : Changer de technologie par service
4. **Déploiement** : Déploiement indépendant des services

## Support

Pour toute question ou problème :
1. Vérifier les logs : `docker-compose logs`
2. Consulter la documentation Docker
3. Vérifier la configuration des services 