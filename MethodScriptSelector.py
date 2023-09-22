from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QCheckBox, QPushButton, QFileDialog
class MethodScriptSelector(QWidget):
    def setText(self, text):
        self.le_path.setText(text)
    def setEnabled(self, enabled):
        self.cb_enabled.setEnabled(enabled)
    def on_select_clicked(self):
        script_path = QFileDialog.getOpenFileName(self, "Select methodscript file",
                                                  "MethodScript", "*.methodscript")
        if script_path[0] != "":
            self.setText(script_path[0])
    @property
    def text(self):
        return self.le_path.text()

    @property
    def isEnabled(self):
        return self.cb_enabled.isChecked()
    @isEnabled.setter
    def isEnabled(self, value):
        self.cb_enabled.setChecked(value)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.le_path = QLineEdit()
        self.cb_enabled = QCheckBox()
        self.pb_select = QPushButton("Select...")
        self.pb_select.clicked.connect(self.on_select_clicked)
        layout.addWidget(self.le_path)
        layout.addWidget(self.pb_select)
        layout.addWidget(self.cb_enabled)
        self.setLayout(layout)