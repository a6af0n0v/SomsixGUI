from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton, QAction, QMenu, QFileDialog, QDialog
import os

recepies_in_folder = []

default_method_script = [
    "e",
    "var c",
    "var p",
    "set_pgstat_chan 1",
    "set_pgstat_mode 0",
    "set_pgstat_chan 0",
    "set_pgstat_mode 2",
    "set_max_bandwidth 40",
    "set_range_minmax da -500m -500m",
    "set_range ba 590u",
    "set_autoranging ba 590u 590u",
    "set_e -500m",
    "cell_on",
    "meas_loop_ca p c -500m 500m 1",
    "pck_start",
    "pck_add p",
    "pck_add c",
    "pck_end",
    "endloop",
    "meas_loop_ca p c -500m 100m 3100m",
    "pck_start",
    "pck_add p",
    "pck_add c",
    "pck_end",
    "endloop",
    "on_finished:",
    "set_e -500m",
    "cell_on",
    ""
    ]


class ReceipeSelector(QPushButton):
    on_receipe_changed = pyqtSignal()
    @property
    def receipe(self):
        return self._receipe

    @property
    def method_script(self):
        return self._method_script
    def load_method_script_from_file(self, path):
        f = open(path, "r")
        content = f.readlines()
        content = [line.rstrip("\n") for line in content]
        return content
    def action_triggered(self, __receipe):
        if __receipe[0]=="Select":
            script_name = QFileDialog.getOpenFileName(self, "Select methodscript file",
                                        "scripts", "*.methodscript")
            if script_name[0] == "":
                __receipe = ("Default", "Default")
            else:
                __receipe = (script_name[0], script_name[0])
        if __receipe[0] ==  "Default":
            self._method_script = default_method_script
        else:
            self._method_script = self.load_method_script_from_file(__receipe[1])
        self.setText(self.shorten_receipe_name(__receipe[0]))
        self._receipe = __receipe[0]
        self._full_receipe_name = __receipe[1]
        self.on_receipe_changed.emit()

    def shorten_receipe_name(self, name):
        if len(name)>24:
            return name[:10]+ "..." + name[-14:]
        else:
            return name
    def __init__(self, parent=None):
        super().__init__(parent)
        menu = QMenu()
        self._receipe = "Default"
        self._full_receipe_name = "Default"
        self._method_script = default_method_script
        def build_action_triggered(receipe):
            def action():
                self.action_triggered(receipe)
            return action
        all_files_in_scripts_dir = os.listdir("scripts")
        for file in all_files_in_scripts_dir:
            split_file_name = file.split(".")
            if len(split_file_name) > 1:
                if split_file_name[-1] == "methodscript":
                    short = self.shorten_receipe_name(file)
                    recepies_in_folder.append((short, "scripts/" + file))
        #print(recepies_in_folder)
        for receipe_short, receipe_full in recepies_in_folder:
            #print(receipe_short)
            action: QAction = menu.addAction(receipe_short)
            action.triggered.connect(build_action_triggered((receipe_short,receipe_full)))
        action = menu.addAction("Default")
        action.triggered.connect(build_action_triggered(("Default", "Default")))
        action = menu.addAction("Select...")
        action.triggered.connect(build_action_triggered(("Select", "Select")))
        self.setMenu(menu)
