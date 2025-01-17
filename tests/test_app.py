import os
import pytest
from fastapi.testclient import TestClient
from api.main import app

# Initialisation du client de test
client = TestClient(app)

# Définition des chemins relatifs robustes
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../data/X_test.npy")
MODEL_PATH = os.path.join(BASE_DIR, "../model/model.h5")


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "API en ligne"}

def test_model_loading():
    from api.model import load_model
    try:
        model = load_model(MODEL_PATH)
        assert model is not None
    except Exception as e:
        pytest.fail(f"Erreur lors du chargement du modèle: {e}")

def test_prediction():
    assert os.path.exists(DATA_PATH), f"Le fichier {DATA_PATH} est introuvable"

    with open(DATA_PATH, "rb") as f:
        response = client.post("/predict", files={"file": f})

    assert response.status_code == 200, f"Échec de la requête: {response.text}"
    json_response = response.json()

    assert "prediction" in json_response, "La clé 'prediction' est absente dans la réponse"
    assert isinstance(json_response["prediction"], int), "La prédiction doit être un entier"
