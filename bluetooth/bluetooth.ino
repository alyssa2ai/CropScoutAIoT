#include <SoftwareSerial.h>
#include <DHT.h>
#include <LiquidCrystal.h>

// --- Pin Setup ---
SoftwareSerial Blue(7, 8); // Rx, Tx
#define DHTPIN 12
#define DHTTYPE DHT22
#define MQ6_PIN A0

// LCD pins: RS, EN, D4, D5, D6, D7
LiquidCrystal lcd(9, 4, A1, A2, A3, A4);
DHT dht(DHTPIN, DHTTYPE);

String readdata;

// --- Motor Pins ---
int en1 = 2, en2 = 3;
int m1a = 5, m1b = 6, m2a = 10, m2b = 11;

void setup() {
  pinMode(m1a, OUTPUT);
  pinMode(m1b, OUTPUT);
  pinMode(m2a, OUTPUT);
  pinMode(m2b, OUTPUT);
  pinMode(en1, OUTPUT);
  pinMode(en2, OUTPUT);

  digitalWrite(en1, HIGH);
  digitalWrite(en2, HIGH);

  Blue.begin(9600);
  Serial.begin(9600);
  dht.begin();
  lcd.begin(16, 2);
  lcd.clear();

  lcd.print("CropScout Bot");
  lcd.setCursor(0, 1);
  lcd.print("Initializing...");
  delay(2000);
  lcd.clear();
}

// --- Movement Functions ---
void forward() {
  analogWrite(m1a, 255); analogWrite(m1b, 0);
  analogWrite(m2a, 255); analogWrite(m2b, 0);
  Serial.println("Forward");
}

void backward() {
  analogWrite(m1a, 0); analogWrite(m1b, 255);
  analogWrite(m2a, 0); analogWrite(m2b, 255);
  Serial.println("Backward");
}

void left() {
  analogWrite(m1a, 255); analogWrite(m1b, 0);
  analogWrite(m2a, 0); analogWrite(m2b, 0);
  Serial.println("Left");
}

void right() {
  analogWrite(m1a, 0); analogWrite(m1b, 0);
  analogWrite(m2a, 255); analogWrite(m2b, 0);
  Serial.println("Right");
}

void stop() {
  analogWrite(m1a, 0); analogWrite(m1b, 0);
  analogWrite(m2a, 0); analogWrite(m2b, 0);
  Serial.println("Stop");
}

// --- Sensor Display Function ---
void displaySensorData() {
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  int gasValue = analogRead(MQ6_PIN);

  // Print to Serial Monitor
  Serial.print("Temp: "); Serial.print(temp);
  Serial.print("°C  | Hum: "); Serial.print(hum);
  Serial.print("%  | Gas: "); Serial.println(gasValue);

  // Print to LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("T:"); lcd.print(temp, 1);
  lcd.print("C H:"); lcd.print(hum, 0);
  lcd.print("%");
  
  lcd.setCursor(0, 1);
  lcd.print("Gas:"); lcd.print(gasValue);
}

void loop() {
  // --- Bluetooth Control ---
  while (Blue.available()) {
    delay(10);
    char c = Blue.read();
    readdata += c;

    if (readdata.length() > 0) {
      if (readdata == "F") forward();
      else if (readdata == "B") backward();
      else if (readdata == "L") left();
      else if (readdata == "R") right();
      else if (readdata == "S") stop();

      readdata = "";
    }
  }

  // --- Update sensor data every 2 seconds ---
  static unsigned long lastUpdate = 0;
  if (millis() - lastUpdate > 2000) {
    displaySensorData();
    lastUpdate = millis();
  }
}
