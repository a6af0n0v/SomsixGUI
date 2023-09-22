from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QSpinBox, QHBoxLayout, QFormLayout, QPushButton, QLineEdit, QComboBox
import json
from MethodScriptSelector import MethodScriptSelector

class SettingsDialog(QDialog):
    def on_cancel_clicked(self):
        self.reject()
    def save(self):
        json_obj = json.dumps(self.settings, indent=4)
        with open(self.json_path, "w") as f:
            f.write(json_obj)

    def on_ok_clicked(self):
        self.settings["name"] = self.le_name.text()
        self.settings["methodscript1_file"] = self.fs_methodscript1.text
        self.settings["methodscript2_file"] = self.fs_methodscript1.text
        self.settings["methodscript1_enabled"] = self.fs_methodscript1.isEnabled
        self.settings["methodscript2_enabled"] = self.fs_methodscript2.isEnabled
        self.settings["output_raw_current"] = self.cb_output_raw_current.currentText()
        self.settings["number_of_points_to_average"] = self.sb_number_of_points_to_average.value()
        self.settings["save_csv_while_measuring"] = self.cb_save_csv_while_measuring.currentText()
        self.settings["max_points_in_chapter"] = self.sb_n_points_in_chapter.value()
        self.settings["csv_file_name"] = self.le_csv_file_name.text()
        self.settings["calibration"] = self.le_calibration_function.text()
        self.settings["polling_interval"] = self.sb_polling_interval.value()
        self.settings["max_points_to_keep_in_memory"] = self.sb_n_points_in_memory.value()
        self.save()
        self.accept()

    def __init__(self, parent, settings_file):
        super().__init__(parent)
        self.json_path = settings_file
        with open(settings_file, "r") as f:
            self.settings = json.load(f)

        self.resize(600,300)
        self.setWindowTitle("Settings")
        v_layout = QVBoxLayout()
        layout = QFormLayout()
        self.le_name = QLineEdit()
        self.le_name.setText(self.settings["name"])
        layout.addRow("Name", self.le_name)
        self.fs_methodscript1 = MethodScriptSelector()
        self.fs_methodscript1.setText(self.settings["methodscript1_file"])
        self.fs_methodscript1.isEnabled = self.settings["methodscript1_enabled"]
        layout.addRow("Channel 0", self.fs_methodscript1)
        self.fs_methodscript2 = MethodScriptSelector()
        self.fs_methodscript2.setText(self.settings["methodscript2_file"])
        self.fs_methodscript2.isEnabled = self.settings["methodscript2_enabled"]
        layout.addRow("Channel 1", self.fs_methodscript2)

        self.sb_number_of_points_to_average = QSpinBox()
        self.sb_number_of_points_to_average.setMaximum(50)
        self.sb_number_of_points_to_average.setMinimum(2)
        self.sb_number_of_points_to_average.setValue(self.settings["number_of_points_to_average"])
        layout.addRow("Points to average", self.sb_number_of_points_to_average)

        self.cb_output_raw_current = QComboBox()
        self.cb_output_raw_current.addItems(["Current", "Concentration"])
        layout.addRow("Value to plot", self.cb_output_raw_current)
        self.cb_output_raw_current.setEnabled(False)

        self.le_calibration_function = QLineEdit()
        self.le_calibration_function.setEnabled(False)
        layout.addRow("Calibration function", self.le_calibration_function)

        self.cb_save_csv_while_measuring = QComboBox()
        self.cb_save_csv_while_measuring.addItems(["Yes", "No"])
        layout.addRow("Save csv while measuring", self.cb_save_csv_while_measuring)

        self.le_csv_file_name = QLineEdit()
        self.le_csv_file_name.setText(self.settings["csv_file_name"])
        #layout.addRow("CSV filename", self.le_csv_file_name)

        self.sb_n_points_in_chapter = QSpinBox()
        self.sb_n_points_in_chapter.setRange(1,100000)
        self.sb_n_points_in_chapter.setValue(self.settings["max_points_in_chapter"])
        layout.addRow("Max points in chapter", self.sb_n_points_in_chapter)

        self.sb_polling_interval = QSpinBox()
        self.sb_polling_interval.setMinimum(1)
        self.sb_polling_interval.setValue(self.settings["polling_interval"])
        self.sb_polling_interval.setMaximum(1000000)
        layout.addRow("Polling interval, s", self.sb_polling_interval)
        self.sb_n_points_in_memory = QSpinBox()
        self.sb_n_points_in_memory.setMinimum(100000)
        self.sb_n_points_in_memory.setMaximum(10000000)
        self.sb_n_points_in_memory.setValue(self.settings["max_points_to_keep_in_memory"])
        layout.addRow("Points in memory", self.sb_n_points_in_memory)
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
