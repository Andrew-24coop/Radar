import sys
import serial
import serial.tools.list_ports
import pygame
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QVBoxLayout, QWidget
from PyQt6.QtSerialPort import QSerialPort
from PyQt6.QtCore import QTimer
from design import Ui_MainWindow


class SerialApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.serial = QSerialPort()
        self.populate_ports()
        self.setWindowTitle("Radar")
        self.connect_b.clicked.connect(self.connect_serial)
        self.disconnect_b.clicked.connect(self.disconnect_serial)

        self.pos = 0
        self.distance = 0.0
        self.serial.readyRead.connect(self.read_serial_port)

        # Pygame setup
        self.setMinimumSize(400, 400)
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))
        self.clock = pygame.time.Clock()
        self.points = []  # Store detected points
        self.current_point = (200, 200)

        # Timer to update pygame display
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(50)  # Refresh every 50ms

    def populate_ports(self):
        self.portlist.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.portlist.addItem(port.device)

    def connect_serial(self):
        selected_port = self.portlist.currentText()
        if not selected_port:
            QMessageBox.warning(self, "Error", "No port selected!")
            return

        self.serial.setPortName(selected_port)
        self.serial.setBaudRate(9600)

        if self.serial.open(QSerialPort.OpenModeFlag.ReadWrite):
            QMessageBox.information(self, "Success", f"Connected to {selected_port}")
        else:
            QMessageBox.critical(self, "Error", "Failed to open serial port")

    def disconnect_serial(self):
        if self.serial.isOpen():
            self.serial.close()
            QMessageBox.information(self, "Disconnected", "Serial port closed.")

    def read_serial_port(self):
        while self.serial.canReadLine():
            rx = self.serial.readLine()
            rxs = str(rx, 'utf-8').strip()
            data = rxs.split(',')
            if data[0] == '1':
                self.pos = int(data[1])
                self.distance = float(data[2])
                self.pos_l.setText(str(self.pos) + "°")
                self.dist_l.setText(str(self.distance))
                self.update_radar(self.pos, self.distance)

    def update_radar(self, angle, distance):
        if distance > 100:
            return  # Ignore invalid readings
        rad_angle = math.radians(angle)
        x = 200 + int(distance * math.cos(rad_angle))
        y = 200 - int(distance * math.sin(rad_angle))
        self.current_point = (x, y)
        self.points.append(self.current_point)
        if len(self.points) > 100:
            self.points.pop(0)  # Keep only the last 100 points

    def update_display(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.circle(self.screen, (0, 255, 0), (200, 200), 100, 1)
        pygame.draw.circle(self.screen, (0, 255, 0), (200, 200), 75, 1)
        pygame.draw.circle(self.screen, (0, 255, 0), (200, 200), 50, 1)
        pygame.draw.circle(self.screen, (0, 255, 0), (200, 200), 25, 1)
        pygame.draw.line(self.screen, (0, 255, 0), (200, 200), (200, 100), 1)
        pygame.draw.line(self.screen, (0, 255, 0), (200, 200), (300, 200), 1)
        pygame.draw.line(self.screen, (0, 255, 0), (200, 200), (100, 200), 1)
        pygame.draw.line(self.screen, (0, 255, 0), (200, 200), (200, 300), 1)

        # Draw green line from center to current point
        pygame.draw.line(self.screen, (0, 255, 0), (200, 200), self.current_point, 2)

        # Draw detected points in red
        for point in self.points:
            pygame.draw.circle(self.screen, (255, 0, 0), point, 3)

        pygame.display.flip()
        self.clock.tick(30)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SerialApp()
    window.show()
    sys.exit(app.exec())
