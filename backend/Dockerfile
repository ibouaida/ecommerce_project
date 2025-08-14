# Stage de build
FROM python:3.11-slim as builder

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les dépendances Python
COPY requirements.txt .

# Installer les dépendances Python globalement
RUN pip install --no-cache-dir -r requirements.txt

# Stage de production
FROM python:3.11-slim

# Installer les dépendances système minimales
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Créer un utilisateur non-root
RUN groupadd -r django && useradd -r -g django django

# Définir le répertoire de travail
WORKDIR /app

# Copier les dépendances Python installées
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copier tout le projet Django depuis la racine
COPY . .

# Créer le répertoire media et définir les permissions
RUN mkdir -p /app/media && chown -R django:django /app

# Changer vers l'utilisateur django
USER django

# Exposer le port
EXPOSE 8000

# Commande par défaut - utiliser une commande directe
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"] 