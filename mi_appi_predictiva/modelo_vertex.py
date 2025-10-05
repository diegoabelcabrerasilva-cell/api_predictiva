from google.cloud import aiplatform
import math

def predecir_temperatura_max(fecha_prediccion, temp_min_c, precipitacion_mm, viento_mps):
    project_id = "TU_PROJECT_ID"
    location = "us-central1"
    endpoint_id = "TU_ENDPOINT_ID"

    aiplatform.init(project=project_id, location=location)
    endpoint = aiplatform.Endpoint(f"projects/{project_id}/locations/{location}/endpoints/{endpoint_id}")

    dia_del_ano = fecha_prediccion.timetuple().tm_yday
    dia_del_ano_sin = math.sin(2 * math.pi * dia_del_ano / 366)
    dia_del_ano_cos = math.cos(2 * math.pi * dia_del_ano / 366)

    instancia = {
        "dia_del_ano_sin": dia_del_ano_sin,
        "dia_del_ano_cos": dia_del_ano_cos,
        "temp_min_c": temp_min_c,
        "precipitacion_mm": precipitacion_mm,
        "viento_mps": viento_mps
    }

    prediction = endpoint.predict(instances=[instancia])
    return prediction.predictions[0]['value']