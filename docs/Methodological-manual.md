# Радар на Arduino с визуализацией на PyQt

Этот проект представляет собой радар, основанный на Arduino, который собирает данные о расстоянии до объектов и визуализирует их с помощью PyQt. 
Проект состоит из двух частей: скетча для Arduino и приложения на Python с использованием библиотеки PyQt.

## Оборудование

- Плата Arduino (например, Arduino Uno)
- Ультразвуковой датчик HC-SR04
- Сервопривод MG90 или аналог
- Соединительные провода

## Схема подключения

Убедитесь, что ваш ультразвуковой датчик и сервопривод правильно подключены к Arduino согласно следующей схеме:

- VCC к 5V на Arduino
- GND к GND на Arduino
- ECHO к цифровому пину 2
- TRIG к цифровому пину 3
- Сервопривод к цифровому пину 4

## Создание программы

### Python и PyQt

1. Убедитесь, что у вас установлен [Python 3.6 или выше](https://www.python.org/downloads/).
2. Установите [Pycharm CE](https://www.jetbrains.com/pycharm/download/) `*пролистайте чуть ниже`.
3. Создайте новый проект ![Image](https://raw.githubusercontent.com/Andrew-24coop/Radar/refs/heads/main/docs/image/create_new_project.png "Создать новый проект")  
4. Поздравляю, можно начать программировать!

#### ```main.py```

- Установим все библиотеки
```import sys
import serial  # Библиотека Python для работы с последовательными соединениями
import serial.tools.list_ports  # Инструменты для перечисления доступных последовательных портов
import pyqtgraph as pg  # Библиотека для создания интерактивных графиков
import numpy as np  # Библиотека для численных операций
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox  # Компоненты для GUI
from PyQt6.QtSerialPort import QSerialPort  # Обработка последовательного порта для PyQt
from design import Ui_MainWindow  # Импорт класса дизайна UI
```
- Создадим структуру класса
```# Определение класса для основного приложения
class SerialApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Настройка UI компонентов
        self.serial = QSerialPort()  # Создание экземпляра последовательного порта
        self.setWindowTitle("Radar")  # Установка заголовка окна
    
    def populate_ports(self):
        return
    
    def connect_serial(self):
        return
        
    def disconnect_serial(self):
        return
    
    def read_serial_port(self):
        return
    
    def setup_radar_graph(self):
        return
    
    def update_radar(self):
        return


# Основной блок для запуска приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создание приложения
    window = SerialApp()  # Создание экземпляра SerialApp
    window.show()  # Показать основное окно
    sys.exit(app.exec())  # Выполнение приложения
```


#
## Arduino

1. Установите [Arduino IDE](https://www.arduino.cc/en/software).
2. Откройте файл `Radar.ino` и загрузите его на вашу плату Arduino.

## Запуск приложения

1. Подключите Arduino к компьютеру через USB-кабель.
2. Убедитесь, что вы знаете, какой COM-порт использует Arduino (например, /dev/ttyUSB0 на Linux/Mac или COM3 на Windows).
3. Убедитесь, что Arduino скетч запущен.
4. Запустите приложение PyQt:
`radar_pyqtgraph.py`

6. Введите COM-порт в диалоговом окне и нажмите "Подключиться".
7. Вы должны увидеть визуализацию данных радара в реальном времени.

## Лицензия

Этот проект лицензирован под [MIT License](LICENSE).

## Контакты

Если у вас есть вопросы, вы можете связаться со мной по [электронной почте](https://andyspacex10@gmail.com).
