-- Initialisation de la base de données ecommerce
-- Ce fichier sera exécuté lors du premier démarrage du conteneur PostgreSQL

-- Créer la base de données si elle n'existe pas
SELECT 'CREATE DATABASE ecommerce_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ecommerce_db')\gexec

-- Se connecter à la base de données
\c ecommerce_db;

-- Créer les extensions nécessaires
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Créer un utilisateur pour l'application (optionnel)
-- CREATE USER ecommerce_app WITH PASSWORD 'app_password';
-- GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_app;

-- Commentaires pour les développeurs
COMMENT ON DATABASE ecommerce_db IS 'Base de données pour l''application ecommerce'; 