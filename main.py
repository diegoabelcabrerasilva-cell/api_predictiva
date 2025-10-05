from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from modelo_vertex import predict_temperature_max

app = FastAPI()

class DatosEntrada(BaseModel):
    fecha: str  # formato YYYY-MM-DD
    precipitacion_mm: float
    viento_mps: float

@app.post("/predict")
def predict(datos: DatosEntrada):
    fecha_dt = datetime.strptime(datos.fecha, "%Y-%m-%d")
    resultado = predict_temperature_max(
        year=fecha_dt.year,
        month=fecha_dt.month,
        day=fecha_dt.day,
        precipitacion_mm=datos.precipitacion_mm,
        viento_mps=datos.viento_mps
    )
    return {"prediccion": round(resultado, 2)}