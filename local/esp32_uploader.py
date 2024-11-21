import requests

class ESP32Uploader:
    def __init__(self, esp32_url, base_url, username, password):
        """
        Inicializa la clase con la configuración necesaria.
        """
        self.esp32_url = esp32_url
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = None

    def get_token(self):
        """
        Obtiene un token de acceso desde el endpoint /token.
        """
        token_url = f"{self.base_url}/token"
        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
        }
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            self.token = response.json().get("access_token")
            print(f"Token obtenido: {self.token}")
            return self.token
        else:
            print(f"Error al obtener token: {response.status_code}, {response.text}")
            return None

    def capture_image(self):
        """
        Captura una imagen desde el ESP32-CAM.
        """
        try:
            response = requests.get(self.esp32_url, stream=True, timeout=10)
            response = requests.get(self.esp32_url, stream=True, timeout=10)
            if response.status_code == 200:
                print("Imagen capturada desde ESP32-CAM.")
                return response.content
            else:
                print(f"Error al capturar imagen: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            print(f"Error al conectar con ESP32-CAM: {str(e)}")
            return None

    def upload_file(self, image_content):
        """
        Sube una imagen al endpoint /upload usando el token.
        """
        if not self.token:
            print("No se encontró un token válido. Llama primero a get_token().")
            return

        upload_url = f"{self.base_url}/upload"
        headers = {
            "Authorization": f"Bearer {self.token}",
        }
        files = {
            "file": ("esp32_image.jpg", image_content, "image/jpeg"),
        }
        response = requests.post(upload_url, headers=headers, files=files)
        if response.status_code == 200:
            print("Archivo subido con éxito:")
            return response.json().get("dominant_color")
        else:
            print(f"Error al subir archivo: {response.status_code}, {response.text}")