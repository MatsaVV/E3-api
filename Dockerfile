# Utilisation de l'image Python légère
FROM python:3.10-slim

# Définition du répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances et les installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers du projet
COPY . .

# Exposer le port de l'API
EXPOSE 8000

# Lancer Uvicorn correctement
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
