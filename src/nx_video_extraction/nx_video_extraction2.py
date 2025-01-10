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
    print("Descargando video desde", data.start, "hasta", int(data.start) + data.duration * 1000)
    resp = requests.get(
        NX_ENDPOINT + f"/hls/{data.camera_id}.mkv?pos={data.start}&duration={data.duration}&resolution=highest",
        headers={"Authorization": f'Bearer {token["token"]}'},
        verify=False
    )
    print("Respuesta:", resp.status_code)
    if resp.status_code == 200 and resp.content:
        write_bytes(data.path, resp.content)
        print("Video descargado correctamente en:", data.path)
        return True
    elif resp.status_code == 200 and not resp.content:
        print("La respuesta fue exitosa, pero no se encontraron datos en el rango especificado.")
        return False
    else:
        print("Error al descargar el video:", resp.status_code, resp.content)
        return False

def convert_to_epoch(day: int, month: int, year: int) -> int:
    """Convierte una fecha en formato día/mes/año a milisegundos desde epoch."""
    dt = datetime(year, month, day, 0, 0, 0)
    return int(dt.timestamp() * 1000)

def record_video(nx_params: NxParams, camera_id: str, output_path: str, quality: str = "lo", start_date: tuple = None, end_date: tuple = None, video_count: int = 30):
    """Extrae múltiples videos de 2 minutos desde el sistema NX."""
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

    videos_downloaded = 0
    attempt = 0

    while videos_downloaded < video_count:
        random_start = random.randint(start_time, end_time - 120000)  # 2 minutos antes del final
        print(f"Intento {attempt + 1}: Inicio aleatorio:", datetime.fromtimestamp(random_start / 1000))

        # Configura los datos del video a descargar
        output_file = output_path.replace(
            ".mkv", f"_{videos_downloaded + 1}.mkv")  # Agrega un índice al archivo
        data = RecordData(
            camera_id=camera_id,
            start=str(random_start),  # Convertir a cadena
            duration=120,  # 2 minutos en segundos
            quality="hi",
            path=output_file
        )

        # Descarga el video
        if process(token, data):
            videos_downloaded += 1
            print(f"Video {videos_downloaded}/{video_count} descargado correctamente.")
        else:
            print("Reintentando con un nuevo rango aleatorio.")

        attempt += 1

if __name__ == "__main__":
    # Configuración de parámetros
    nx_params = NxParams(username="admin", password="easeefyPT01")
    camera_id = "8f8946e0-f298-43a4-932f-0c6f866b3b30"
    output_path = "./output/video_descargado.mkv"

    # Rango de tiempo manual (en formato día/mes/año)
    start_date = (19, 11, 2024)  # Ejemplo: 19/11/2024
    end_date = (9, 1, 2025)    # Ejemplo: 09/01/2025

    # Ejecuta la extracción de 30 videos
    record_video(nx_params, camera_id, output_path, start_date=start_date, end_date=end_date, video_count=30)
