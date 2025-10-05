# archivo: main.py
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
import math
from google.cloud import aiplatform
from google.oauth2 import service_account
import os

# ------------------------------
# Configuración segura de Service Account
# ------------------------------
# Render permite subir secretos, por ejemplo: GOOGLE_APPLICATION_CREDENTIALS_JSON
# Guardamos el contenido del JSON como variable de entorno y lo escribimos temporalmente
service_account_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")

if service_account_json is None:
    raise Exception("❌ No se encontró la variable de entorno GOOGLE_APPLICATION_CREDENTIALS_JSON")

# Guardamos el JSON en un archivo temporal para usarlo
KEY_PATH = "/tmp/service_account.json"
with open(KEY_PATH, "w") as f:
    f.write(service_account_json)

credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH

# ------------------------------
# Configuración del proyecto y modelo
# ------------------------------
PROJECT_ID = "nasa-weather-prediction-app"
ENDPOINT_ID = "7544016459496685568"
LOCATION = "us-central1"

# ------------------------------
# Inicializa FastAPI
# ------------------------------
app = FastAPI(title="API de Predicción de Temperatura")

# ------------------------------
# Modelo de entrada
# ------------------------------
class PrediccionRequest(BaseModel):
    fecha: str               # Formato "YYYY-MM-DD"
    temp_min_c: float = 0
    precipitacion_mm: float = 0
    viento_mps: float = 0

# ------------------------------
# Endpoint para predicción
# ------------------------------
@app.post("/predecir")
def predecir(req: PrediccionRequest):
    # Inicializa Vertex AI
    aiplatform.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)
    endpoint_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}"
    endpoint = aiplatform.Endpoint(endpoint_name)
    
    # Procesa la fecha
    fecha_obj = date.fromisoformat(req.fecha)
    dia_del_ano = fecha_obj.timetuple().tm_yday
    dia_del_ano_sin = math.sin(2 * math.pi * dia_del_ano / 366)
    dia_del_ano_cos = math.cos(2 * math.pi * dia_del_ano / 366)
    
    # Prepara la entrada para el modelo
    instancia = {
        "dia_del_ano_sin": dia_del_ano_sin,
        "dia_del_ano_cos": dia_del_ano_cos,
        "temp_min_c": req.temp_min_c,
        "precipitacion_mm": req.precipitacion_mm,
        "viento_mps": req.viento_mps
    }
    
    # Llama al endpoint
    prediction = endpoint.predict(instances=[instancia])
    valor_predicho = prediction.predictions[0]['value']
    
    return {"fecha": req.fecha, "temp_max_predicha": valor_predicho}
