from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton, QMenu, QAction
import serial
import serial.tools.list_ports
from enum import Enum
import Styles

class PORT_STATE(Enum):
    PORT_CLOSED = 0
    PORT_OPEN   = 1
    PORT_ERROR  = 2

class PortSelector(QPushButton):
    on_port_changed = pyqtSignal()
    @property
    def palmsens_handle(self):
        return self.port

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        if value == PORT_STATE.PORT_CLOSED:
            self.setObjectName("closed")
        elif value == PORT_STATE.PORT_OPEN:
            self.setObjectName("open")
        elif value == PORT_STATE.PORT_ERROR:
            self.setObjectName("error")
        self.setStyleSheet(Styles.style)
        self.on_port_changed.emit()

    def action_triggered(self, port):
        self.setText(port)
        self.open_port(port)

    def open_port(self, port):
        if self.port != None:
            self.port.close() #closing currently open port
            print(f"Previous port closed, trying to open port {port}")
        try:
            self.port = serial.Serial(port, baudrate=230400)
        except Exception as ex:
            self.state = PORT_STATE.PORT_ERROR
            return
        if self.port.is_open:
            self.port.close()
        try:
            self.port.open()
        except Exception as ex:
            print(f"Can't open port {ex}")
            self.state = PORT_STATE.PORT_ERROR
            return
        if self.port.is_open:
            self.state = PORT_STATE.PORT_OPEN

    def build_action_triggered(self, port):
        def action():
            self.action_triggered(port)
        return action

    def __init__(self, parent=None):
        super().__init__(parent)
        self.port = None

        self._state = PORT_STATE.PORT_CLOSED
        ports = serial.tools.list_ports.comports()
        menu = QMenu()
        for port, desc, hwid in sorted(ports):
            action:QAction = menu.addAction(port)
            action.triggered.connect(self.build_action_triggered(port))
        self.setMenu(menu)
