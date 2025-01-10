import requests
import random
import time
from datetime import datetime
from utils import write_bytes
from common import NX_ENDPOINT
from data_models import NxParams, TokenNX, RecordData

def get_nx_token(data: NxParams) -> TokenNX:
    """Obtiene un token de autenticación del servidor NX Witness."""
    resp = requests.post(
        NX_ENDPOINT + '/rest/v1/login/sessions',
        verify=False,
        json={"username": data.username, "password": data.password, "setCookie": True}
    )
    if resp.status_code == 200:
        auth = {"token": resp.json()["token"]}
        return auth
    else:
        print("Error al obtener el token:", resp.status_code, resp.content)
        return {"token": ""}

def process(token: TokenNX, data: RecordData):
    """Descarga un video desde el sistema NX y lo guarda en una ubicación específica."""
    print("Descargando video desde", data.start, "hasta", int(data.start) + data.duration*1000)
    resp = requests.get(
        NX_ENDPOINT + f"/hls/{data.camera_id}.mkv?pos={data.start}&duration={data.duration}&{data.quality}=true",
        headers={"Authorization": f'Bearer {token["token"]}'},
        verify=False
    )
    print("Respuesta:", resp.status_code)
    if resp.status_code == 200 and resp.content:
        write_bytes(data.path, resp.content)
        print("Video descargado correctamente en:", data.path)
    elif resp.status_code == 200 and not resp.content:
        print("La respuesta fue exitosa, pero no se encontraron datos en el rango especificado.")
    else:
        print("Error al descargar el video:", resp.status_code, resp.content)

def convert_to_epoch(day: int, month: int, year: int) -> int:
    """Convierte una fecha en formato día/mes/año a milisegundos desde epoch."""
    dt = datetime(year, month, day, 0, 0, 0)
    return int(dt.timestamp() * 1000)

def record_video(nx_params: NxParams, camera_id: str, output_path: str, quality: str = "lo", start_date: tuple = None, end_date: tuple = None):
    """Extrae un video de 2 minutos desde el sistema NX."""
    # Obtiene el token de autenticación
    token = get_nx_token(nx_params)
    if not token["token"]:
        print("No se pudo autenticar con el servidor NX.")
        return

    if start_date is None or end_date is None:
        print("Debe proporcionar un rango de tiempo manual para la cámara en formato día/mes/año.")
        return

    # Convierte las fechas a milisegundos desde epoch
    start_time = convert_to_epoch(*start_date)
    end_time = convert_to_epoch(*end_date)

    # Elige un inicio aleatorio dentro del rango proporcionado
    random_start = random.randint(start_time, end_time - 120000)  # 2 minutos antes del final
    print("Inicio aleatorio:", datetime.fromtimestamp(random_start / 1000))
    # Configura los datos del video a descargar
    data = RecordData(
        camera_id=camera_id,
        start=str(random_start),  # Convertir a cadena
        duration=120,  # 2 minutos en segundos
        quality=quality,
        path=output_path
    )
    print("Descargando video a:", output_path)
    # Descarga el video
    process(token, data)

if __name__ == "__main__":
    # Configuración de parámetros
    nx_params = NxParams(username="admin", password="easeefyPT01")
    camera_id = "8f8946e0-f298-43a4-932f-0c6f866b3b30"
    output_path = "./output/video_descargado.mkv"

    # Rango de tiempo manual (en formato día/mes/año)
    start_date = (19, 11, 2024)  # Ejemplo: 01/01/2023
    end_date = (9, 1, 2025)    # Ejemplo: 02/01/2023

    # Ejecuta la extracción del video
    record_video(nx_params, camera_id, output_path, start_date=start_date, end_date=end_date)
