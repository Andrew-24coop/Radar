import sys
import serial  # Библиотека Python для работы с последовательными соединениями
import serial.tools.list_ports  # Инструменты для перечисления доступных последовательных портов
import pyqtgraph as pg  # Библиотека для создания интерактивных графиков
import numpy as np  # Библиотека для численных операций
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox  # Компоненты для GUI
from PyQt6.QtSerialPort import QSerialPort  # Обработка последовательного порта для PyQt
from design import Ui_MainWindow  # Импорт класса дизайна UI


# Определение класса для основного приложения
class SerialApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()  # Инициализация базового класса
        self.radar_curve = None  # Заглушка для графика радара
        self.radar_plot = None  # Заглушка для виджета графика
        self.setupUi(self)  # Настройка UI компонентов
        self.serial = QSerialPort()  # Создание экземпляра последовательного порта
        self.populate_ports()  # Заполнение доступных последовательных портов в UI
        self.setWindowTitle("Radar")  # Установка заголовка окна
        self.connect_b.clicked.connect(self.connect_serial)  # Соединение кнопки с функцией
        self.disconnect_b.clicked.connect(self.disconnect_serial)  # Функциональность кнопки отключения
        self.serial.readyRead.connect(self.read_serial_port)  # Чтение данных из последовательного порта при наличии

        self.angle_data = []  # Список для хранения данных угла
        self.distance_data = []  # Список для хранения данных расстояния
        self.max_distance = 100  # Максимальное значение расстояния для графика, см
        self.max_angle = 180  # Максимальное значение угла для графика, градусы
        self.setup_radar_graph()  # Инициализация графика радара

    def populate_ports(self):
        self.portlist.clear()  # Очистка существующего списка портов
        ports = serial.tools.list_ports.comports()  # Перечисление всех доступных последовательных портов
        for port in ports:
            self.portlist.addItem(port.device)  # Добавление каждого порта в выпадающий список

    def connect_serial(self):
        selected_port = self.portlist.currentText()  # Получение текущего выбранного порта
        if not selected_port:
            QMessageBox.warning(self, "Error", "No port selected!")  # Предупреждение, если порт не выбран
            return

        self.serial.setPortName(selected_port)  # Установка имени выбранного порта
        self.serial.setBaudRate(9600)  # Установка скорости передачи данных

        # Попытка открыть последовательный порт
        if self.serial.open(QSerialPort.OpenModeFlag.ReadWrite):
            QMessageBox.information(self, "Success",
                                    f"Connected to {selected_port}")  # Сообщение об успешном подключении
        else:
            QMessageBox.critical(self, "Error",
                                 "Failed to open serial port")  # Сообщение об ошибке, если не удалось открыть

    def disconnect_serial(self):
        if self.serial.isOpen():  # Проверка, открыт ли порт
            self.serial.close()  # Закрытие последовательного порта
            QMessageBox.information(self, "Disconnected", "Serial port closed.")  # Уведомление пользователя

    def read_serial_port(self):
        # Проверка, есть ли данные для чтения
        while self.serial.canReadLine():
            rx = self.serial.readLine()  # Чтение строки данных
            rxs = str(rx, 'utf-8').strip()  # Декодирование байтов в строку и удаление пробелов
            data = rxs.split(',')  # Разделение строки на компоненты

            # Проверка формата данных

            if data[0] == '1':
                angle = int(data[1])  # Преобразование угла из строки в целое число
                distance = float(data[2])  # Преобразование расстояния из строки в число с плавающей точкой

                self.pos_l.setText(str(angle) + "°")  # Обновление метки угла в UI
                self.dist_l.setText(str(distance) + " cm")  # Обновление метки расстояния в UI

                self.update_radar(angle, distance)  # Обновление графика радара новыми данными

    def setup_radar_graph(self):
        self.radar_plot = pg.PlotWidget()  # Создание виджета графика
        self.gridLayout.addWidget(self.radar_plot, 0, 0, 1, 1)  # Добавление виджета графика в сеточный макет

        self.radar_plot.setAspectLocked(True)  # Блокировка соотношения сторон для сохранения круговой формы радара
        self.radar_plot.setXRange(-self.max_distance, self.max_distance)  # Установка диапазона по оси X
        self.radar_plot.setYRange(0, self.max_distance)  # Установка диапазона по оси Y

        self.radar_plot.getAxis('bottom').setLabel('Distance (cm)')  # Подпись для оси X
        self.radar_plot.getAxis('left').setLabel('Angle')  # Подпись для оси Y
        self.radar_plot.showGrid(x=True, y=True)  # Отображение сетки на графике

        # Инициализация пустого графика с точками, представленными зелеными кругами
        self.radar_curve = self.radar_plot.plot([], [], pen=None, symbol='o', symbolSize=5, symbolBrush=(0, 255, 0))

    def update_radar(self, angle, distance):
        # Вычисление координат в декартовой системе для построения
        x = distance * np.cos(np.radians(angle))  # X-координата на основе угла и расстояния
        y = distance * np.sin(np.radians(angle))  # Y-координата на основе угла и расстояния

        self.angle_data.append(x)  # Добавление X-координаты в список данных угла
        self.distance_data.append(y)  # Добавление Y-координаты в список данных расстояния

        # Ограничение размера списков данных до 180 элементов для поддержания производительности
        if len(self.angle_data) > 180:
            self.angle_data.pop(0)  # Удаление старой точки данных по X
            self.distance_data.pop(0)  # Удаление старой точки данных по Y

        # Обновление графика радара с новыми данными
        self.radar_curve.setData(self.angle_data, self.distance_data)


# Основной блок для запуска приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создание приложения
    window = SerialApp()  # Создание экземпляра SerialApp
    window.show()  # Показать основное окно
    sys.exit(app.exec())  # Выполнение приложения
