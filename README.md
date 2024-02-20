# Absensi
Jangan Lupa mengganti Nama Wifi,password WiFi, dan Alamat IP dibagian 
```
const char *ssid = "Elek";
const char *password = "password";
const char *serverAddress = "192.168.1.200";  // Ganti dengan alamat IP atau nama domain server Flask
```

untuk LCD dibagian 
```
int lcdColumns = 16;
int lcdRows = 2;
LiquidCrystal_I2C lcd(0x27, lcdColumns, lcdRows);  

```

ESP32 berfungsi untuk mengirim alamat RFID dan menerima respon dari server, yang dimana jika server memberikan respon, esp akan menanggapi dibagian LCD
Server berfungsi untuk menyimpan dan membuat user yang akan di absensi
