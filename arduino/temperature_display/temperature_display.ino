#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

#define DHT_PIN 2
#define DHT_TYPE DHT11

#define LCD_I2C_ADDR 0x27
#define LCD_COLS 16
#define LCD_ROWS 2

const char CANDIDATE_NAME[] = "Rutaganira Yanis Ntwali";

LiquidCrystal_I2C lcd(LCD_I2C_ADDR, LCD_COLS, LCD_ROWS);
DHT dht(DHT_PIN, DHT_TYPE);

unsigned long lastScrollMs = 0;
const unsigned long SCROLL_INTERVAL = 300;
int scrollOffset = 0;
int nameLen = 0;

void updateNameRow() {
  lcd.setCursor(0, 0);

  if (nameLen <= LCD_COLS) {
    lcd.print(CANDIDATE_NAME);
    for (int i = nameLen; i < LCD_COLS; i++) {
      lcd.print(' ');
    }
    return;
  }

  char window[LCD_COLS + 1];
  for (int i = 0; i < LCD_COLS; i++) {
    int idx = (scrollOffset + i) % nameLen;
    window[i] = CANDIDATE_NAME[idx];
  }
  window[LCD_COLS] = '\0';
  lcd.print(window);
}

void updateTemperatureRow() {
  float tempC = dht.readTemperature();

  lcd.setCursor(0, 1);

  if (isnan(tempC)) {
    lcd.print("Temp: ERROR   ");
    Serial.println("ERROR");
    return;
  }

  lcd.print("Temp: ");
  lcd.print(tempC, 1);
  lcd.print(" C  ");
  Serial.println(tempC, 1);
}

void setup() {
  Serial.begin(9600);

  lcd.init();
  lcd.backlight();
  dht.begin();

  nameLen = strlen(CANDIDATE_NAME);
  updateNameRow();
  lcd.setCursor(0, 1);
  lcd.print("Temp: --.- C");

  Serial.println("Sensor: DHT11 on D2");
}

void loop() {
  updateTemperatureRow();

  if (nameLen > LCD_COLS) {
    unsigned long now = millis();
    if (now - lastScrollMs >= SCROLL_INTERVAL) {
      lastScrollMs = now;
      scrollOffset = (scrollOffset + 1) % nameLen;
      updateNameRow();
    }
  } else {
    updateNameRow();
  }

  delay(2000);
}
