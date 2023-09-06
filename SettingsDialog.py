from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QSpinBox, QHBoxLayout, QFormLayout, QPushButton

class SettingsDialog(QDialog):
    def on_cancel_clicked(self):
        self.reject()
    def on_ok_clicked(self):
        self.settings["polling_interval"] = self.sb_polling_interval.value()
        self.settings["points_on_chart"] = self.sb_n_points_on_chart.value()
        for key in self.settings:
            self.persistant_settings.setValue(key, self.settings[key])
            #print(f"{key} - {self.settings[key]}")
        self.persistant_settings.sync()


        self.accept()
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.persistant_settings = QSettings(QSettings.Scope.UserScope,
        #            "FaradaIC", "SomsixGUI", self)
        self.persistant_settings = QSettings(".conf.ini", QSettings.IniFormat)
        self.settings = {
            "polling_interval": 30,
            "points_on_chart":  100,
        }

        #self.persistant_settings.clear()
        self.settings["polling_interval"] = self.persistant_settings.value("polling_interval",30, type=int)
        self.settings["points_on_chart"]  = self.persistant_settings.value("points_on_chart", 60, type=int)

        self.resize(300,300)
        self.setWindowTitle("Settings")
        v_layout = QVBoxLayout()
        layout = QFormLayout()

        self.sb_polling_interval = QSpinBox()
        self.sb_polling_interval.setMinimum(1)
        self.sb_polling_interval.setValue(self.settings["polling_interval"])
        self.sb_polling_interval.setMaximum(1000000)
        layout.addRow("Polling interval, s", self.sb_polling_interval)
        self.sb_n_points_on_chart = QSpinBox()
        self.sb_n_points_on_chart.setMinimum(10)
        self.sb_n_points_on_chart.setMaximum(1000)
        self.sb_n_points_on_chart.setValue(self.settings["points_on_chart"])
        layout.addRow("Points on chart", self.sb_n_points_on_chart)
        h_layout = QHBoxLayout()
        self.pb_cancel = QPushButton("Cancel")
        self.pb_cancel.clicked.connect(self.on_cancel_clicked)
        self.pb_ok = QPushButton("Apply")
        self.pb_ok.clicked.connect(self.on_ok_clicked)
        h_layout.addWidget(self.pb_cancel)
        h_layout.addWidget(self.pb_ok)
        v_layout.addLayout(layout)
        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)
