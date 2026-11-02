from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os
import boto3

# Initialisation de l'API
app = FastAPI()

MODEL_PATH = "catboost_prod.joblib"
BUCKET_NAME = os.getenv("MODEL_BUCKET", "julien-agritech-model-prod-2026")
MODEL_KEY = "catboost_prod.joblib"

# Telechargement automatique du modele depuis le bucket S3 prive via boto3
if not os.path.exists(MODEL_PATH):
    try:
        s3 = boto3.client("s3")
        s3.download_file(BUCKET_NAME, MODEL_KEY, MODEL_PATH)
    except Exception as e:
        raise RuntimeError(f"Impossible de recuperer le modele depuis S3 : {e}")

# Chargement du pipeline global en RAM
pipeline = joblib.load(MODEL_PATH)

# Definition de la structure des donnees d'entree attendue (10 features)
class PredictionInput(BaseModel):
    Area: str
    Item: str
    Nutrient_nitrogen_N_total: float
    Nutrient_phosphate_P2O5_total: float
    Nutrient_potash_K2O_total: float
    Fungicides_and_Bactericides: float
    Herbicides: float
    Insecticides: float
    Pesticides_total: float
    Rodenticides: float

@app.post("/predict")
def predict(input_data: PredictionInput):
    # 1. Conversion du JSON recu en dictionnaire
    data_dict = input_data.model_dump()
    
    # 2. Restructuration des cles pour correspondre aux noms des colonnes d'entrainement
    formatted_dict = {
        "Area": data_dict["Area"],
        "Item": data_dict["Item"],
        "Nutrient nitrogen N (total)": data_dict["Nutrient_nitrogen_N_total"],
        "Nutrient phosphate P2O5 (total)": data_dict["Nutrient_phosphate_P2O5_total"],
        "Nutrient potash K2O (total)": data_dict["Nutrient_potash_K2O_total"],
        "Fungicides and Bactericides": data_dict["Fungicides_and_Bactericides"],
        "Herbicides": data_dict["Herbicides"],
        "Insecticides": data_dict["Insecticides"],
        "Pesticides (total)": data_dict["Pesticides_total"],
        "Rodenticides": data_dict["Rodenticides"]
    }
    
    # 3. Conversion en DataFrame Pandas
    df_features = pd.DataFrame([formatted_dict])
    
    # 4. Inference : Calcul de la prediction via le pipeline global
    prediction = pipeline.predict(df_features)
    
    # 5. Renvoi du resultat converti en type natif Python
    return {"prediction": float(prediction[0])}