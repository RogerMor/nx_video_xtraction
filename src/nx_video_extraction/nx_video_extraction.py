"""Main module."""
import requests
import random
import datetime
import os

# Configuración del servidor Nx Witness
NX_SERVER_URL = "http://192.168.1.135:7001"
USERNAME = "admin"
PASSWORD = "easeefyPT01"
CAMERA_ID = "8f8946e0-f298-43a4-932f-0c6f866b3b30"  # ID de la cámara (obtén esto desde el API)

# Directorio donde guardar los clips exportados
EXPORT_DIRECTORY = "./exports/"

# Número de videos a extraer
NUM_VIDEOS = 30

# Autenticación básica
def authenticate():
    """Verifica si las credenciales son válidas."""
    response = requests.get(f"{NX_SERVER_URL}/rest/v1/devices", auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        print("Autenticado correctamente.")
        return True
    else:
        print(f"Error al autenticar: {response.status_code}, {response.text}")
        return False

# Obtener un rango de tiempo de grabaciones
def get_camera_recordings(camera_id):
    """Obtiene el rango de tiempo disponible para las grabaciones de la cámara."""
    response = requests.get(
        f"{NX_SERVER_URL}/rest/v1/cameras/{camera_id}/media",
        auth=(USERNAME, PASSWORD)
    )
    if response.status_code == 200:
        data = response.json()
        start_time = datetime.datetime.fromtimestamp(data["startTimeMs"] / 1000)
        end_time = datetime.datetime.fromtimestamp(data["endTimeMs"] / 1000)
        return start_time, end_time
    else:
        print(f"Error al obtener grabaciones: {response.status_code}, {response.text}")
        return None, None

# Exportar un clip aleatorio de 2 minutos
def export_random_clip(camera_id, start_time, end_time, index):
    """Exporta un clip aleatorio de 2 minutos dentro del rango de tiempo disponible."""
    # Seleccionar un inicio aleatorio dentro del rango disponible
    random_start = start_time + datetime.timedelta(
        seconds=random.randint(0, int((end_time - start_time).total_seconds()) - 120)
    )
    random_end = random_start + datetime.timedelta(seconds=120)  # Duración fija de 2 minutos

    print(f"[{index+1}/{NUM_VIDEOS}] Extrayendo clip desde {random_start} hasta {random_end}...")

    export_payload = {
        "cameraId": camera_id,
        "startTimeMs": int(random_start.timestamp() * 1000),
        "endTimeMs": int(random_end.timestamp() * 1000),
        "format": "mp4"
    }

    response = requests.post(
        f"{NX_SERVER_URL}/rest/v1/exports",
        json=export_payload,
        auth=(USERNAME, PASSWORD)
    )

    if response.status_code == 200:
        download_url = response.json().get("url")
        if download_url:
            download_clip(download_url, index)
        else:
            print(f"No se encontró la URL de descarga en la respuesta: {response.json()}")
    else:
        print(f"Error al exportar el clip: {response.status_code}, {response.text}")

# Descargar el clip exportado
def download_clip(url, index):
    """Descarga el clip exportado desde la URL proporcionada."""
    response = requests.get(url, auth=(USERNAME, PASSWORD), stream=True)
    if response.status_code == 200:
        # Crear directorio si no existe
        os.makedirs(EXPORT_DIRECTORY, exist_ok=True)
        filename = f"{EXPORT_DIRECTORY}clip_{index+1}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"Clip descargado: {filename}")
    else:
        print(f"Error al descargar el clip: {response.status_code}, {response.text}")

# Ejecutar el flujo principal
if __name__ == "__main__":
    if authenticate():
        start_time, end_time = get_camera_recordings(CAMERA_ID)
        if start_time and end_time:
            print(f"Grabaciones disponibles desde {start_time} hasta {end_time}")
            for i in range(NUM_VIDEOS):
                export_random_clip(CAMERA_ID, start_time, end_time, i)
        else:
            print("No se pudo obtener el rango de tiempo de grabaciones.")
