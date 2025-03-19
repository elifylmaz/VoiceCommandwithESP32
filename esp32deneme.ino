#include <WiFi.h>
#include <ArduinoJson.h>
#include <WebServer.h>

// Wi-Fi ağ bilgileri
const char* ssid = "neslihan-Vivobook-ASUSLaptop-X34";  // Wi-Fi ağınızın adı
const char* password = "lXrBCi9j"; // Wi-Fi şifreniz

// ESP32 IP adresi
IPAddress local_IP(10, 42, 0, 217);  // IP adresinizi buraya yazın
IPAddress gateway(10, 42, 0, 1);     // Gateway IP adresi
IPAddress subnet(255, 255, 255, 0);  // Subnet mask

// Web sunucusu oluşturma
WebServer server(80);

// LED pinleri
const int redLedPin = 2;    // Kırmızı LED pinini kullanıyoruz
const int greenLedPin = 5;  // Yeşil LED pinini kullanıyoruz
const int blueLedPin = 15;  // Mavi LED pinini kullanıyoruz

// Wi-Fi bağlantısını başlatma
void setup() {
  Serial.begin(115200);

  // LED pinlerini çıkış olarak ayarla
  pinMode(redLedPin, OUTPUT);
  pinMode(greenLedPin, OUTPUT);
  pinMode(blueLedPin, OUTPUT);

  // Wi-Fi bağlantısını başlat
  WiFi.config(local_IP, gateway, subnet);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("Bağlantı başarılı.");
  Serial.print("ESP32 IP adresi: ");
  Serial.println(WiFi.localIP());

  // POST isteği için /command yolunu işleme
  server.on("/command", HTTP_POST, handleCommand);

  // Sunucuyu başlat
  server.begin();
}

// POST isteği işleme fonksiyonu
void handleCommand() {
  String message = "Komut geçersiz.";
  
  // JSON verisi almak için
  if (server.hasArg("plain")) {
    String body = server.arg("plain");  // Gelen JSON verisi
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, body);
    
    // JSON içeriğini kontrol et
    const char* command = doc["command"];
    if (command != nullptr) {
      if (strcmp(command, "turn_on") == 0) {
        // Tüm LED'leri aç
        digitalWrite(redLedPin, HIGH);
        digitalWrite(greenLedPin, HIGH);
        digitalWrite(blueLedPin, HIGH);
        message = "Tüm LED'ler açıldı!";
      }
      else if (strcmp(command, "turn_off") == 0) {
        // Tüm LED'leri kapat
        digitalWrite(redLedPin, LOW);
        digitalWrite(greenLedPin, LOW);
        digitalWrite(blueLedPin, LOW);
        message = "Tüm LED'ler kapalı!";
      }
      else if (strcmp(command, "red") == 0) {
        // Yalnızca kırmızı LED'i aç
        digitalWrite(redLedPin, HIGH);
        digitalWrite(greenLedPin, LOW);
        digitalWrite(blueLedPin, LOW);
        message = "Kırmızı LED açıldı!";
      }
      else if (strcmp(command, "green") == 0) {
        // Yalnızca yeşil LED'i aç
        digitalWrite(redLedPin, LOW);
        digitalWrite(greenLedPin, HIGH);
        digitalWrite(blueLedPin, LOW);
        message = "Yeşil LED açıldı!";
      }
      else if (strcmp(command, "blue") == 0) {
        // Yalnızca mavi LED'i aç
        digitalWrite(redLedPin, LOW);
        digitalWrite(greenLedPin, LOW);
        digitalWrite(blueLedPin, HIGH);
        message = "Mavi LED açıldı!";
      }
    }
  }

  // Yanıt gönderme
  server.send(200, "text/plain", message);
}

void loop() {
  // Sunucuyu çalıştır
  server.handleClient();
}
