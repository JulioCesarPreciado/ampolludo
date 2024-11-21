import serial
from esp32_uploader import ESP32Uploader
from talking_ai import TalkingAi

# Configuración
ESP32_URL = ""
BASE_URL = ""
USERNAME = ""
PASSWORD = ""

# Configuración del puerto serial
SERIAL = serial.Serial('/dev/cu.usbmodemC04E301179B02', 9600)

# Inicializar TalkingAi
api_key = ""
talking_ai = TalkingAi(api_key)

if __name__ == "__main__":
    uploader = ESP32Uploader(ESP32_URL, BASE_URL, USERNAME, PASSWORD)

    # Obtener el token
    if uploader.get_token():
        while True:
            if SERIAL.in_waiting > 0:
                line = SERIAL.readline().decode('utf-8').strip()
                if line == "No hay objetos cerca":
                    continue
                # Capturar imagen del ESP32-CAM
                print("Objeto detectado cerca.")
                image = uploader.capture_image()
                if image:
                    print("Imagen capturada.")
                    # Subir la imagen a la API
                    talking_ai.get_response_and_play_audio(uploader.upload_file(image))