#include <Servo.h>

#define TRIG_PIN 9   // Pin conectado a TRIG del sensor
#define ECHO_PIN 10  // Pin conectado a ECHO del sensor
#define SERVO_PIN 6  // Pin conectado al servomotor

Servo myServo; // Crear objeto servomotor

void setup() {
  // Configuración de pines
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Configurar el pin del servomotor
  myServo.attach(SERVO_PIN);
  myServo.write(0); // Inicialmente, el servomotor estará en posición 0

  // Iniciar comunicación serial
  Serial.begin(9600);
  Serial.println("Iniciando sensor HC-SR04 y servomotor...");
}

void loop() {
  long duration;
  float distance;

  // Enviar un pulso de 10 microsegundos en el pin TRIG
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Leer el tiempo del pulso de ECHO
  duration = pulseIn(ECHO_PIN, HIGH);

  // Convertir el tiempo a distancia en cm
  distance = (duration * 0.034) / 2;

  // Activar el servomotor si está a menos de 20 cm
  if (distance <= 60.0) {
    Serial.println("Objeto cerca");
    myServo.write(160); // Mover servomotor a 90 grados
    delay(1000);       // Esperar 1 segundo
  } else {
    Serial.println("No hay objetos cerca");
    myServo.write(0); // Retornar servomotor a posición 0
  }

  // Esperar un momento antes de la siguiente lectura
  delay(3000);
}