#include <LiquidCrystal.h>

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);


String leerString() {
  String message = "";
  while (Serial.available() > 0 && millis() < (unsigned long)(millis() + 1000)) {
    message += char(Serial.read());
  }
  return message;
}

void parseString(String message) {
  int Index = message.indexOf('/');
  if (Index != -1) {
    lcd.setCursor(0, 0);
    lcd.print(message.substring(0, Index)); 

    lcd.setCursor(0, 1);
    lcd.print(message.substring(Index + 1));
  } else {
    lcd.print("Invalid format");
  }
}

void setup() {
  lcd.begin(16, 2);
  lcd.print("hello, world!");
  Serial.begin(9600); 
	Serial.setTimeout(1);
  pinMode(boton, INPUT);

}

void loop() {
  if (Serial.available()) {
    delay(100);
    lcd.clear();
    String message = leerString();
    parseString(message);
    }
  }
}