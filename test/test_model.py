import pytest
import os
import joblib
import pandas as pd

@pytest.mark.model
def test_presence_et_inference_modele():
    nom_modele = "catboost_prod.joblib"
    
    # 1. Verification de la presence du modele telecharge depuis S3
    assert os.path.exists(nom_modele), "Le fichier du modele est introuvable."

    # 2. Chargement du pipeline complet
    pipeline = joblib.load(nom_modele)

    # 3. Donnees types avec les noms de colonnes d origine attendus
    entree = pd.DataFrame([{
        "Area": "France",
        "Item": "Wheat",
        "Nutrient nitrogen N (total)": 100.0,
        "Nutrient phosphate P2O5 (total)": 50.0,
        "Nutrient potash K2O (total)": 50.0,
        "Fungicides and Bactericides": 10.0,
        "Herbicides": 10.0,
        "Insecticides": 5.0,
        "Pesticides (total)": 25.0,
        "Rodenticides": 1.0
    }])

    # 4. Calcul de la prediction et validation du resultat numerique
    prediction = pipeline.predict(entree)
    assert len(prediction) == 1
    assert float(prediction[0]) > 0.0