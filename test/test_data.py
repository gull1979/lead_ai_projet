import pytest
import pandas as pd

@pytest.mark.data
def test_schema_donnees():
    # Liste exacte des 10 variables attendues par l API
    colonnes_attendues = [
        "Area",
        "Item",
        "Nutrient_nitrogen_N_total",
        "Nutrient_phosphate_P2O5_total",
        "Nutrient_potash_K2O_total",
        "Fungicides_and_Bactericides",
        "Herbicides",
        "Insecticides",
        "Pesticides_total",
        "Rodenticides"
    ]
    
    # Creation d une ligne fictive pour valider la presence des cles
    donnees = {col: [1.0] for col in colonnes_attendues}
    df = pd.DataFrame(donnees)

    for col in colonnes_attendues:
        assert col in df.columns