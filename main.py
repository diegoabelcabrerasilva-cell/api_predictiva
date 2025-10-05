import os
import json
from fastapi import FastAPI, HTTPException
from google.cloud import aiplatform
from pydantic import BaseModel

# Verificar variable de entorno
if "GOOGLE_APPLICATION_CREDENTIALS_JSON" not in os.environ:
    raise Exception("❌ No se encontró la variable de entorno GOOGLE_APPLICATION_CREDENTIALS_JSON")

# Cargar credenciales de Google Cloud
credentials_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
aiplatform.init(credentials=credentials_info, project=credentials_info["project_id"], location="us-central1")

app = FastAPI(title="API Predictiva")

# Modelo de ejemplo para request
class PredictRequest(BaseModel):
    feature1: float
    feature2: float

@app.get("/")
def root():
    return {"message": "API Predictiva corriendo en Render!"}

@app.post("/predict")
def predict(data: PredictRequest):
    # Aquí pondrías tu lógica real de predicción con Vertex AI
    result = data.feature1 + data.feature2  # ejemplo de operación
    return {"prediction": result}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)


