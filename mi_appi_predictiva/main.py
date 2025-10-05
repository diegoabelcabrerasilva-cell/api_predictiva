from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from modelo_vertex import predecir_temperatura_max

app = FastAPI()

class DatosEntrada(BaseModel):
    fecha: str  # formato YYYY-MM-DD
    temp_min_c: float
    precipitacion_mm: float
    viento_mps: float

@app.post("/predecir")
def predecir(datos: DatosEntrada):
    fecha_obj = datetime.strptime(datos.fecha, "%Y-%m-%d")
    resultado = predecir_temperatura_max(
        fecha_obj,
        datos.temp_min_c,
        datos.precipitacion_mm,
        datos.viento_mps
    )
    return {"prediccion": round(resultado, 2)}