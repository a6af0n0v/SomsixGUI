from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton, QMenu, QAction
import serial
import serial.tools.list_ports
from enum import Enum
import Styles
version_string = b"pico"
class PORT_STATE(Enum):
    PORT_CLOSED = 0
    PORT_OPEN   = 1
    PORT_ERROR  = 2

class PortSelector(QPushButton):
    on_port_changed = pyqtSignal()
    @property
    def is_palmsens(self):
        try:
            self.port.timeout = 0.5
            self.port.write_timeout = 0.5
            self.port.write(b"t\n")
            response = self.port.readline()
            print(response)
            if response.find(version_string)!=-1:
                return True
        except Exception as ex:
            print(ex)
        return False

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
            print (ex)
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
            print("Opeining port... wait")
            if self.is_palmsens == True:
                self.state = PORT_STATE.PORT_OPEN
            else:
                self.state = PORT_STATE.PORT_ERROR

    def build_action_triggered(self, port):
        def action():
            self.action_triggered(port)
        return action

    def refresh_comports_list(self):
        self.build_menu()

    def build_menu(self):
        ports = serial.tools.list_ports.comports()
        self.menu.clear()
        refresh_action: QAction = self.menu.addAction("Refresh...")
        refresh_action.triggered.connect(self.refresh_comports_list)
        self.menu.addSeparator()
        for port, desc, hwid in sorted(ports):
            action: QAction = self.menu.addAction(port)
            action.triggered.connect(self.build_action_triggered(port))

    def __init__(self, parent=None):
        super().__init__(parent)
        self.port:serial.Serial = None
        self._state = PORT_STATE.PORT_CLOSED
        self.menu = QMenu()
        self.build_menu()
        self.setMenu(self.menu)
