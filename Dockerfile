# Utiliser une image Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers
COPY ./backend /app/backend
COPY ./frontend /app/frontend
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer les ports (Django = 8000, Flask = 3000)
EXPOSE 8000 3000

# Lancer à la fois Django et Flask (ex. pour test)
CMD ["sh", "-c", "python frontend/app.py & python backend/manage.py runserver 0.0.0.0:8000"]
