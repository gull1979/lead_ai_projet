# Image de base Linux contenant un environnement Conda et Python
FROM continuumio/miniconda3:25.3.1-1

# Installation des outils systeme indispensables
# curl est obligatoire pour le test d'attente de FastAPI dans start.sh
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Repertoire de travail dans le conteneur
WORKDIR /app

# Copie des dependances en premier pour exploiter le cache des couches Docker
COPY requirements.txt requirements.txt

# Mise a jour de pip et installation des dependances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copie de l'ensemble des fichiers du projet dans /app
COPY . /app

# Droits d'execution sur le script de demarrage
RUN chmod +x start.sh

# Ports ouverts sur l'instance EC2 (FastAPI: 8000, Streamlit: 8501)
EXPOSE 8000 8501

# Variables d'environnement globales
# MODEL_BUCKET fournit le nom par defaut de ton bucket S3 AWS
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_TELEMETRY_DISABLE=true \
    MODEL_BUCKET=agritech-model-prod-lead-2026

# Commande de lancement executant start.sh
CMD ["./start.sh"]