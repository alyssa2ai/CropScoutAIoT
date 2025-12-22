#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

// ----- Object Initialization -----
LiquidCrystal_I2C lcd(0x27, 16, 2);  // Change to 0x3F if LCD doesn't work
#define DHTPIN 12
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// ----- Motor Pins -----
int EN1 = 2, EN2 = 3;
int M1A = 5, M1B = 6;
int M2A = 10, M2B = 11;

// ----- Sensor Pins -----
int mq6Pin = A0;

String readdata;

void setup() {
  // ----- Motor Setup -----
  pinMode(M1A, OUTPUT);
  pinMode(M1B, OUTPUT);
  pinMode(M2A, OUTPUT);
  pinMode(M2B, OUTPUT);
  pinMode(EN1, OUTPUT);
  pinMode(EN2, OUTPUT);
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);

  // ----- Serial (Bluetooth via RX0/TX1) -----
  Serial.begin(9600);

  // ----- LCD Setup -----
  Wire.begin();
  lcd.begin();
  lcd.backlight();

  // ----- DHT Setup -----
  dht.begin();

  // ----- Startup Message -----
  lcd.setCursor(0, 0);
  lcd.print("CropScout AiOT");
  lcd.setCursor(0, 1);
  lcd.print("Initializing...");
  delay(2000);
  lcd.clear();
}

// ----- Movement Functions -----
void forward() {
  analogWrite(M1A, 255); analogWrite(M1B, 0);
  analogWrite(M2A, 255); analogWrite(M2B, 0);
  lcd.clear();
  lcd.print("Moving: Forward");
}

void backward() {
  analogWrite(M1A, 0); analogWrite(M1B, 255);
  analogWrite(M2A, 0); analogWrite(M2B, 255);
  lcd.clear();
  lcd.print("Moving: Backward");
}

void left() {
  analogWrite(M1A, 255); analogWrite(M1B, 0);
  analogWrite(M2A, 0); analogWrite(M2B, 0);
  lcd.clear();
  lcd.print("Turning: Left");
}

void right() {
  analogWrite(M1A, 0); analogWrite(M1B, 0);
  analogWrite(M2A, 255); analogWrite(M2B, 0);
  lcd.clear();
  lcd.print("Turning: Right");
}

void stopBot() {
  analogWrite(M1A, 0); analogWrite(M1B, 0);
  analogWrite(M2A, 0); analogWrite(M2B, 0);
  lcd.clear();
  lcd.print("Bot Stopped");
}

// ----- Sensor Display -----
void displaySensorData() {
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  int gas = analogRead(mq6Pin);

  // Display only pure values — no text fluff
  Serial.print(temp);
  Serial.print(",");
  Serial.print(hum);
  Serial.print(",");
  Serial.println(gas);

  // LCD output
  lcd.setCursor(0, 0);
  if (!isnan(temp) && !isnan(hum)) {
    lcd.print("T:"); lcd.print(temp, 1);
    lcd.print("C H:"); lcd.print(hum, 0);
    lcd.print("% ");
  } else {
    lcd.print("T:N/A H:N/A   ");
  }

  lcd.setCursor(0, 1);
  lcd.print("Gas:"); lcd.print(gas);
  lcd.print("     ");
}

// ----- Main Loop -----
void loop() {
  // Bluetooth commands from RX0/TX1
  while (Serial.available()) {
    delay(10);
    char c = Serial.read();
    readdata += c;

    if (readdata.length() > 0) {
      if (readdata == "F") forward();
      else if (readdata == "B") backward();
      else if (readdata == "L") left();
      else if (readdata == "R") right();
      else if (readdata == "S") stopBot();
      readdata = "";
    }
  }

  // Sensor readings
  displaySensorData();
  delay(2000);
}
