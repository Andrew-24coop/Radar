import sys
import serial
import serial.tools.list_ports
import pyqtgraph as pg
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
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
        self.serial.readyRead.connect(self.read_serial_port)

        # Radar Data
        self.angle_data = []
        self.distance_data = []
        self.max_distance = 40  # Max range in cm
        self.max_angle = 180  # Servo range
        self.setup_radar_graph()

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
                angle = int(data[1])
                distance = float(data[2])

                self.pos_l.setText(str(angle) + "°")
                self.dist_l.setText(str(distance) + " cm")

                self.update_radar(angle, distance)

    def setup_radar_graph(self):
        """Set up the pyqtgraph plot for radar visualization."""
        self.radar_plot = pg.PlotWidget()
        self.gridLayout.addWidget(self.radar_plot, 0, 0, 1, 1)  # Adjust layout accordingly

        self.radar_plot.setAspectLocked(True)
        self.radar_plot.setXRange(-self.max_distance, self.max_distance)
        self.radar_plot.setYRange(0, self.max_distance)

        self.radar_plot.getAxis('bottom').setLabel('Distance (cm)')
        self.radar_plot.getAxis('left').setLabel('Angle')
        self.radar_plot.showGrid(x=True, y=True)

        self.radar_curve = self.radar_plot.plot([], [], pen=None, symbol='o', symbolSize=5, symbolBrush=(0, 255, 0))

    def update_radar(self, angle, distance):
        """Update the radar plot with new data."""
        # Convert polar to Cartesian coordinates
        x = distance * np.cos(np.radians(angle))
        y = distance * np.sin(np.radians(angle))

        self.angle_data.append(x)
        self.distance_data.append(y)

        if len(self.angle_data) > 180:  # Keep only last 180 points
            self.angle_data.pop(0)
            self.distance_data.pop(0)

        self.radar_curve.setData(self.angle_data, self.distance_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SerialApp()
    window.show()
    sys.exit(app.exec())
