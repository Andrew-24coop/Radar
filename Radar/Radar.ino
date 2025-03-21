#include <Servo.h>  // Подключаем библиотеку для работы с сервоприводом
Servo myservo;      // Создаем объект myservo для управления сервоприводом

#define HC_TRIG 3   // Определяем пин для TRIG ультразвукового датчика
#define HC_ECHO 2   // Определяем пин для ECHO ультразвукового датчика

float distFilt = 0; // Переменная для хранения отфильтрованного расстояния
int pos = 23;       // Начальная позиция сервопривода (в градусах)
bool direction = true; // Флаг направления движения сервопривода (true - против часовой, false - по часовой)

void setup() {
  Serial.begin(9600);   // Инициализация последовательного порта со скоростью 9600 бод
  pinMode(HC_TRIG, OUTPUT); // Устанавливаем TRIG как выход
  pinMode(HC_ECHO, INPUT);  // Устанавливаем ECHO как вход
  myservo.attach(4);    // Подключаем сервопривод к пину 4
  delay(500);           // Небольшая задержка для стабилизации
}

void loop() {
  float dist = getDist(); // Получаем необработанное расстояние с датчика
  distFilt += (dist - distFilt) * 0.2; // Применяем фильтрацию (экспоненциальное сглаживание)

  // Двигаем сервопривод в пределах от 23 до 157 градусов (угол обзора 135 градусов)
  if (direction && pos <= 157) { 
    pos++;               // Увеличиваем угол поворота
    myservo.write(pos);  // Устанавливаем новую позицию сервопривода
  } else if (pos >= 23) { 
    pos--;               // Уменьшаем угол поворота
    direction = false;   // Меняем направление движения
    myservo.write(pos);  // Устанавливаем новую позицию сервопривода
  } else {
    direction = true;    // Возвращаем направление в исходное
  }

  // Отправляем данные через Serial в формате "1,угол,расстояние"
  Serial.print("1,");
  Serial.print(pos);
  Serial.print(",");
  Serial.println(distFilt);

  delay(50); // Небольшая задержка для плавности работы
}

// Функция получения расстояния с ультразвукового датчика
float getDist() {
  digitalWrite(HC_TRIG, HIGH);  // Посылаем короткий импульс 10 мкс на TRIG
  delayMicroseconds(10);
  digitalWrite(HC_TRIG, LOW);   // Завершаем импульс

  uint32_t us = pulseIn(HC_ECHO, HIGH); // Измеряем длительность импульса на ECHO

  return (us / 58.3); // Преобразуем время в микросекундах в расстояние в сантиметрах
}
