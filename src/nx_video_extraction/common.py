import os

# development environments.
ENV = os.environ.get("ENV", "local")
# sentry url.
SENTRY_ENDPOINT = os.environ.get("SENTRY_ENDPOINT")
TIMELAPSED_ALARM = float(os.environ.get("TIMELAPSED_ALARM", 2))
MQTT_HOST = os.environ.get("MQTT_HOST", "0.0.0.0")
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT",
                                      "easeefy-development")
GOOGLE_CLOUD_BUCKET_PATH = os.environ.get("GOOGLE_CLOUD_BUCKET_PATH",
                                          "gs://easeefy-videos/demo-videos/")

CONFIGURATION_DEFAULT = {
    "mqtt_client_id": "connector_db",
    "mqtt_host": MQTT_HOST,
    "mqtt_topic": "lossPrevention/1/ai/alarm",
    "mqtt_qos": 1,  # sub
    "mqtt_retain": False,
    "mqtt_clean_session": True
}

NX_CAMERA_ID = os.environ.get("NX_CAMERA_ID", "df0a5534-2438-5fe4-cfd9-e8035611fe1e")
NX_SERVER_IP = os.environ.get("NX_SERVER_IP", "192.168.1.135")
NX_ENDPOINT = "https://{}:7001".format(NX_SERVER_IP)
NX_USERNAME = os.environ.get("NX_USERNAME", 'admin')
NX_PASSWORD = os.environ.get("NX_PASSWORD", 'PerAdmin92')
ZEROTIER_SERVER_IP = "10.147.20.92"

# output = os.popen('ifconfig').readlines()
# for i in range(len(output)):
#     first = output[i].split(' ')
#     if len(first) == 5:
#         name = first[0]
#         if (name[0:2] == 'zt'):
#             ip = output[i + 1].split(' ')[9]
#             if '192.168.192.' in ip:
#                 ZEROTIER_SERVER_IP = ip
#                 print(ZEROTIER_SERVER_IP)
#                 break