#include <Servo.h>
Servo myservo;
#define HC_TRIG 3
#define HC_ECHO 2
float distFilt = 0;
int pos = 23;
bool direction = true;
void setup() {
  Serial.begin(9600);
  pinMode(HC_TRIG, OUTPUT);
  pinMode(HC_ECHO, INPUT);
  myservo.attach(4);
  delay(500);
}

void loop() {
  float dist = getDist();
  distFilt += (dist - distFilt) * 0.2;

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

float getDist() {
  digitalWrite(HC_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(HC_TRIG, LOW);
  uint32_t us = pulseIn(HC_ECHO, HIGH);
  return (us / 58.3);
}