import json

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton, QAction, QMenu, QFileDialog, QDialog
import os
recepies_in_folder = []
default_recipe_name = "recipes/Default.json"

class ReceipeSelector(QPushButton):
    on_receipe_changed = pyqtSignal()
    @property
    def receipe(self):
        return self._receipe
    def load_recipe(self, path):
        try:
            with open(path, 'r') as f:
                self._receipe = json.load(f)
        except Exception as ex:
            print(ex)
        self._full_receipe_name = path
        self.setText(self.receipe["name"])
        #print(self._receipe)
        self.methodscript1 = self.load_method_script_from_file(self._receipe["methodscript1_file"])
        self.methodscript2 = self.load_method_script_from_file(self._receipe["methodscript2_file"])
        self.on_receipe_changed.emit()
    def refresh(self):
        #print(self.current_recipe)
        self.action_triggered(self.current_recipe)

    def load_method_script_from_file(self, path):
        content = ""
        try:
            with open(path, "r") as f:
                content = f.readlines()
                content = [line.rstrip("\n") for line in content]
        except Exception as ex:
            print (ex)
        return content

    def action_triggered(self, __receipe):
        #__receipe is tupple containing short and full path
        self.current_recipe = __receipe
        if __receipe[0]=="Select":
            recipe_name = QFileDialog.getOpenFileName(self, "Select methodscript file",
                                        "recipes", "*.json")
            if recipe_name[0] == "": #if user pressed cancel
                self.load_recipe(default_recipe_name)
            else:   #user selected a valid file
                self.load_recipe(recipe_name[0])
            return
        if __receipe[0] ==  "Default":
            self.load_recipe(default_recipe_name)
            return
        self.load_recipe(__receipe[1])


    def shorten_receipe_name(self, name):
        if len(name)>24:
            return name[:10]+ "..." + name[-14:]
        else:
            return name

    def __init__(self, parent=None):
        super().__init__(parent)
        menu = QMenu()
        self.current_recipe = default_recipe_name
        self._full_receipe_name = default_recipe_name
        self.load_recipe(self._full_receipe_name)

        def build_action_triggered(receipe):
            def action():
                self.action_triggered(receipe)
            return action

        all_files_in_scripts_dir = os.listdir("recipes")
        for file in all_files_in_scripts_dir:
            split_file_name = file.split(".")
            if len(split_file_name) > 1:
                if split_file_name[-1] == "json":
                    short = self.shorten_receipe_name(file)
                    recepies_in_folder.append((short, "recipes/" + file))
        #print(recepies_in_folder)
        for receipe_short, receipe_full in recepies_in_folder:
            #print(receipe_short)
            action: QAction = menu.addAction(receipe_short)
            action.triggered.connect(build_action_triggered((receipe_short,receipe_full)))
        menu.addSeparator()
        action = menu.addAction("Default")
        action.triggered.connect(build_action_triggered(("Default", "Default")))
        action = menu.addAction("Select...")
        action.triggered.connect(build_action_triggered(("Select", "Select")))
        self.setMenu(menu)
