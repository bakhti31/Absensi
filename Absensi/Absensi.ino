#include <ArduinoJson.h>
#include <ArduinoJson.hpp>

#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <LiquidCrystal_I2C.h>

#define SS_PIN 5     // GPIO pin untuk SS (SDA) pada modul MFRC522
#define RST_PIN 15   // GPIO pin untuk RST pada modul MFRC522
// #define LED_PIN 1    // GPIO pin untuk LED indikator

MFRC522 mfrc522(SS_PIN, RST_PIN);

const char *ssid = "Elek";
const char *password = "password";
const char *serverAddress = "192.168.1.200";  // Ganti dengan alamat IP atau nama domain server Flask

int lcdColumns = 16;
int lcdRows = 2;
LiquidCrystal_I2C lcd(0x27, lcdColumns, lcdRows);  

int display = 1;
void Display(String line1, String line2){
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(line1);
  lcd.setCursor(0, 1);
  lcd.print(line2);
}

void setup() {
  Serial.begin(115200);
  // pinMode(LED_PIN, OUTPUT);
  // digitalWrite(LED_PIN, LOW);
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Connecting Wifi...");
  // Inisialisasi koneksi WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting Wifi...");
  }
  
  lcd.setCursor(0, 1);
  lcd.print("Connected.");
  Serial.println("Connected to WiFi");

  // Inisialisasi modul MFRC522
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("Selesai");
}

void loop() {
  WiFiClient client;
  int Tdisplay = 0;
  if (client.connect(serverAddress, 5000)) {
    Tdisplay = 0;
    client.stop();
  }else{
    Tdisplay = 1;
  }
  // Cek apakah ada kartu RFID
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    // Baca data kartu RFID
    String rfidData = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      rfidData += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
      rfidData += String(mfrc522.uid.uidByte[i], HEX);
    }
    // Serial.println("RFID Data: " + rfidData);
    // Kirim data ke server Flask
    kirimDataKeServer(rfidData);
    Tdisplay = 2;
  }
  if(Tdisplay != display){
    display = Tdisplay;
    switch(display){
      case 0:
        Display(" Selamat Datang ","Scan Kartu Anda");
        break;
      case 1:
        Display("Gagal Terkoneksi"," Server Offline ");
        delay(200);
        break;
      case 2:
        Display("Selamat Pagi", " Silahkan Masuk ");
        delay(500);
        break;
    }
  }
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
}

void kirimDataKeServer(String rfidData) {
  WiFiClient client;

  // Buat koneksi ke server
  if (client.connect(serverAddress, 5000)) {
    // Buat HTTP POST request dengan data RFID
    String postData = "rfid_data=" + rfidData;
    client.println("POST /absensi HTTP/1.1");
    client.println("Host: " + String(serverAddress));
    client.println("Content-Type: application/x-www-form-urlencoded");
    client.println("Content-Length: " + String(postData.length()));
    client.println();
    client.print(postData);

    // Tunggu hingga respons diterima
    while (!client.available()) {
      delay(1);
    }
    String jsonResponse ="";
    // Baca respons dari server
    while (client.available()) {
      String c = client.readStringUntil('\r');
      jsonResponse += c;
    }
    // Serial.println(jsonResponse);
    int valueIndex = jsonResponse.indexOf("{");
    String valueString = jsonResponse.substring(valueIndex);
    Serial.print(valueString);
    // Tutup koneksi
    client.stop();
  } else {
    Serial.println("Unable to connect to Server");
  }
}
