#include <Servo.h>
Servo myservo; // подключение серво как myservo
#define HC_TRIG 3
#define HC_ECHO 2
float distFilt = 0;
int pos = 23; //начальная позиция
bool direction = true; // изначальное напрваление движения 
void setup() {
  Serial.begin(9600); // подключение порта на частоте 9600 бод (бит/сек)
  pinMode(HC_TRIG, OUTPUT); // назначение пина TRIG на вывод
  pinMode(HC_ECHO, INPUT);  // назначение пина ECHO на ввод
  myservo.attach(4); // подключение серво на пин 4
  delay(500);
}

void loop() {
  float dist = getDist(); // получение сырого расстояния
  distFilt += (dist - distFilt) * 0.2; // фильтрация

  if (direction && pos <= 157) {
    pos++;
    myservo.write(pos);
  } else if (pos >= 23) {
    pos--;
    direction = false;
    myservo.write(pos);
  } else {
    direction = true;
  }
  Serial.print("1,");
  Serial.print(pos);
  Serial.print(",");
  Serial.println(distFilt);
  delay(50);
}

float getDist() { // функция получения сырого значения с датчика
  digitalWrite(HC_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(HC_TRIG, LOW);
  uint32_t us = pulseIn(HC_ECHO, HIGH);
  return (us / 58.3);
}