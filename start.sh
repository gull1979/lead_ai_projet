#!/bin/bash

# Lancement de FastAPI en tâche de fond (le & met fin au prompt)
uvicorn api_app:app --host 0.0.0.0 --port 8000 &

# test si l'api (endpoint /docs) est disponible avant de lancer streamlit
while ! curl -s http://localhost:8000/docs > /dev/null; do
    sleep 2
done

# Streamlit au premier plan sur le port 8501 avec désactivation de l'interactivité d'installation
exec streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0