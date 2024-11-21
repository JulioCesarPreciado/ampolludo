#include "esp_camera.h"
#include <WiFi.h>

// Pines del ESP32-CAM (AI Thinker)
#define CAMERA_MODEL_AI_THINKER
#include "camera_pins.h"

// Configuración WiFi
const char* ssid = "INFINITUM847A";
const char* password = "AMJsvRLY54";

WiFiServer server(80); // Puerto del servidor web

void setupCamera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;  // Formato JPEG para imágenes
  config.frame_size = FRAMESIZE_QVGA;    // Resolución QVGA (320x240)
  config.jpeg_quality = 12;              // Calidad media
  config.fb_count = 1;

  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Error al inicializar la cámara");
    while (true);
  }
}

void handleClient(WiFiClient client) {
  // Capturar una foto
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Error al capturar la foto");
    client.println("HTTP/1.1 500 Internal Server Error");
    client.println("Content-Type: text/plain");
    client.println();
    client.println("Error al capturar la foto");
    return;
  }

  // Enviar encabezados HTTP
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: image/jpeg");
  client.println("Content-Length: " + String(fb->len));
  client.println();
  
  // Enviar la imagen al cliente
  client.write(fb->buf, fb->len);

  // Liberar el buffer de la cámara
  esp_camera_fb_return(fb);
}

void setup() {
  Serial.begin(115200);

  // Configurar la cámara
  setupCamera();

  // Conexión WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi conectado");
  Serial.print("Visita: http://");
  Serial.println(WiFi.localIP());

  // Iniciar el servidor web
  server.begin();
}

void loop() {
  // Esperar conexión de un cliente
  WiFiClient client = server.available();
  if (!client) return;

  // Leer la solicitud del cliente
  String request = client.readStringUntil('\r');
  client.flush();

  // Procesar la solicitud
  if (request.startsWith("GET /")) {
    Serial.println("Cliente conectado. Tomando foto...");
    handleClient(client);
  }

  client.stop(); // Cerrar la conexión
}