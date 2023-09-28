from enum import Enum
import time
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QBrush, QColor, QPen, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDialog

from SettingsDialog import SettingsDialog
from PortSelector import PortSelector, PORT_STATE
from ReceipeSelector import ReceipeSelector
import PyQt5.Qt
import Styles
from PyQt5.QtChart import QLineSeries, QChart, QChartView
from Interpreter import Interpreter

main_wnd_size = (800, 600)
main_wnd_title = "Somsix GUI"


class STATUS(Enum):
    STOPPED = 0
    RUNNING = 1
    NOT_CONNECTED = 2

class ChartWidget(QWidget):
    def append(self, value, channel):
        is_first_point = (len(self.line.points()) == 0) and (len(self.line2.points())==0)
        if is_first_point:
            MainWidget.start_time = time.time()
        time_elapsed = time.time() - MainWidget.start_time
        #value_uA = value * 1E6
        if channel==0:
            self.line.append(time_elapsed, value)
        elif channel==1:
            self.line2.append(time_elapsed, value)
        b_range_changed = False
        if value < self.min_value:
            self.min_value = value
            b_range_changed = True
        if value > self.max_value:
            self.max_value = value
            b_range_changed = True
        if b_range_changed:
            self.chart.axisY().setRange(self.min_value * 1.1, self.max_value * 1.1)
        self.chart.axisX().setRange(self.t_min_value, time_elapsed)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.min_value = -0
        self.max_value = 0
        self.t_min_value = 0
        self.t_max_value = 40
        self.chart = QChart()
        self.chartview = QChartView(self.chart)
        self.chart.setTheme(6)
        self.n = 0
        # Customize chart title
        font = QFont()
        font.setItalic(Styles.chart_styles["title_bold"])
        font.setPixelSize(Styles.chart_styles["title_font_size"])
        self.chart.setTitleBrush(QBrush(QColor(Styles.chart_styles["title_color"])))
        self.chart.setTitleFont(font)
        # self.chart.setTitleBrush(QBrush(QColor(34,34,34), ))
        # Customize chart background
        self.chart.setBackgroundBrush(QBrush(QColor(Styles.chart_styles["chart_background_color"])))
        # Plot area background
        self.chart.setPlotAreaBackgroundBrush(QBrush(QColor(Styles.chart_styles["plot_area_bkg_brush"])))
        self.chart.setPlotAreaBackgroundVisible(True)
        # Legend
        # self.chart.legend().hide()
        # self.chart.legend().detachFromChart()
        # self.chart.legend().setPos(100,0)
        self.chart.legend().setAlignment(PyQt5.Qt.Qt.AlignRight)
        legend_font = QFont("Arial", Styles.chart_styles['legend_font_size'])
        legend_font.setItalic(Styles.chart_styles["legend_italic"])
        self.chart.legend().setLabelColor(QColor(Styles.chart_styles["legend_color"]))
        self.chart.legend().setFont(legend_font)
        if Styles.chart_styles["legend_visible"] == False:
            self.chart.legend().hide()
        self.line = QLineSeries()
        self.line2 = QLineSeries()
        self.line.setPointsVisible(Styles.chart_styles["set_points_visible"])
        self.line2.setPointsVisible(Styles.chart_styles["set_points_visible"])
        self.line.setName("ch0")
        self.line2.setName("ch1")
        # Customize series
        pen = QPen(QColor(Styles.chart_styles["series_line_color"]))
        pen.setWidth(Styles.chart_styles["series_line_width"])
        pen2 = QPen(QColor(Styles.chart_styles["series_line2_color"]))
        pen2.setWidth(Styles.chart_styles["series_line2_width"])
        self.line.setPen(pen)
        self.line2.setPen(pen2)

        self.chart.addSeries(self.line)
        self.chart.addSeries(self.line2)
        self.chart.createDefaultAxes()

        # Axis colors
        axis_pen = QPen(QColor(Styles.chart_styles["axis_color"]))
        axis_pen.setWidth(Styles.chart_styles["axis_width"])

        self.chart.axisX().setLinePen(axis_pen)
        self.chart.axisY().setLinePen(axis_pen)
        # Axis label colors
        self.chart.axisY().setLabelsBrush(QBrush(QColor(Styles.chart_styles["label_color"])))
        self.chart.axisX().setLabelsBrush(QBrush(QColor(Styles.chart_styles["label_color"])))
        labels_font = QFont("Arial", Styles.chart_styles["label_font_size"])
        self.chart.axisX().setLabelsFont(labels_font)
        self.chart.axisY().setLabelsFont(labels_font)
        # Labels format
        self.chart.axisX().setLabelFormat("%.0f")

        self.chart.axisX().setRange(self.t_min_value, self.t_max_value)
        self.chart.axisY().setLabelFormat("%.3f")
        self.chart.axisY().setRange(self.min_value, self.max_value)
        # Grid lines and shades
        self.chart.axisX().setGridLineVisible(True)
        self.chart.axisX().setGridLineColor(QColor(Styles.chart_styles["grid_line_color"]))
        self.chart.axisX().setShadesColor(QColor(Styles.chart_styles["grid_shade_color"]))
        self.chart.axisX().setShadesVisible(Styles.chart_styles["grid_shades_visible"])
        self.chart.axisY().setGridLineVisible(Styles.chart_styles["grid_line_visible"])
        self.chart.axisY().setGridLineColor(QColor(Styles.chart_styles["grid_line_color"]))
        # axis titles
        axis_title_font = QFont()
        axis_title_font.setItalic(Styles.chart_styles["axis_title_italic"])
        axis_title_font.setPixelSize(Styles.chart_styles["axis_title_font_size"])
        axis_title_font.setBold(Styles.chart_styles["axis_title_bold"])
        self.chart.axisX().setTitleFont(axis_title_font)
        self.chart.axisX().setTitleBrush(QBrush(QColor(Styles.chart_styles["axis_title_color"])))
        self.chart.axisY().setTitleBrush(QBrush(QColor(Styles.chart_styles["axis_title_color"])))
        self.chart.axisX().setTitleText("t / sec")
        self.chart.axisY().setTitleFont(axis_title_font)
        #self.chart.axisY().setTitleText("I / uA")
        self.chart.setTitle("Default")
        self.chart.resize(300, 300)

        # AntiAlias
        self.chartview.setRenderHint(QPainter.Antialiasing, True)
        self.chartview.setRubberBand(QChartView.HorizontalRubberBand)

        layout = QVBoxLayout()
        layout.addWidget(self.chartview)
        self.setLayout(layout)


class MainWidget(QWidget):
    start_time = time.time()
    def timeout(self):
        if self.cbb_port_selector.palmsens_handle != None:
            while self.cbb_port_selector.palmsens_handle.in_waiting > 0:
                line = self.cbb_port_selector.palmsens_handle.readline()
                pkg = self.interpreter.interpret(line.decode(), self.channel)
                if pkg:
                    #print(pkg)
                    if pkg.value_valid == True:
                        self.WE_currents.append(pkg.value)
                    if self.cbb_receipe_selector.receipe["save_csv_while_measuring"]=="Yes":
                        try:
                            self.interpreter.save_temp(pkg, self.cbb_receipe_selector.receipe["max_points_in_chapter"])
                        except Exception as ex:
                            print(ex)
                if line == b'\n':
                    if len(self.WE_currents) != 0:
                        avg = sum(self.WE_currents[-self.cbb_receipe_selector.receipe["number_of_points_to_average"]:]) / len(self.WE_currents[-self.cbb_receipe_selector.receipe["number_of_points_to_average"]:])
                        print(f"Method script for channel {self.channel} finished, average value {avg}, number of points: {self.cbb_receipe_selector.receipe['number_of_points_to_average']}")
                        cal_func =self.cbb_receipe_selector.receipe[f"calibration{self.channel+1}"]
                        if cal_func !="":
                            try:
                                y = eval(cal_func, {"x": avg})
                                #print(f"converted value {y}")
                                self.cw_charts.append(y, self.channel)
                            except Exception as ex:
                                print(f"Error while calibration {ex}")
                        else:
                            self.cw_charts.append(avg, self.channel)
                        self.channel +=1
                        if self.channel > 1 or self.cbb_receipe_selector.receipe["methodscript2_enabled"]==False:
                            self.timer.stop()
                            #print("Timer stopped")
                        else:
                            self.read_channel(self.channel)

    def start_clicked(self):
        if self.status == STATUS.STOPPED:
            self.status = STATUS.RUNNING
        else:
            self.status = STATUS.STOPPED

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value == STATUS.NOT_CONNECTED:
            self.pb_start.setEnabled(False)
            # self.pb_save.setEnabled(False)
            self.cbb_receipe_selector.setEnabled(True)
            self.cbb_receipe_selector.setObjectName("")
            self.pb_settings.setEnabled(True)
            self.pb_settings.setObjectName("")
            self.pb_start.setObjectName("disabled")
            # self.pb_save.setObjectName("disabled")
        elif value == STATUS.STOPPED:
            self.pb_start.setEnabled(True)
            self.pb_start.setObjectName("")
            self.pb_start.setText("Start")
            self.cbb_receipe_selector.setEnabled(True)
            self.cbb_receipe_selector.setObjectName("")
            self.pb_settings.setEnabled(True)
            self.pb_settings.setObjectName("")
            self.main_timer.stop()
            self._status = STATUS.STOPPED
        elif value == STATUS.RUNNING:
            self.pb_start.setEnabled(True)
            self.cbb_receipe_selector.setEnabled(False)
            self.pb_settings.setEnabled(False)
            self.pb_settings.setObjectName("disabled")
            self.cbb_receipe_selector.setObjectName("disabled")
            self.pb_start.setText("Stop")
            self.main_timer.start(self.cbb_receipe_selector.receipe["polling_interval"]*1000)
            self.on_timeout()
            self._status = STATUS.RUNNING
        self.setStyleSheet(Styles.style)

    def read_channel(self, channel):
        if channel==0 and self.cbb_receipe_selector.receipe["methodscript1_enabled"] == True:
            self.channel = 0
            for line in self.cbb_receipe_selector.methodscript1:
                self.cbb_port_selector.palmsens_handle.write(line.encode() + b"\x0a")
        else:
            self.channel = 1
            if self.cbb_receipe_selector.receipe["methodscript2_enabled"] == True:
                for line in self.cbb_receipe_selector.methodscript2:
                    self.cbb_port_selector.palmsens_handle.write(line.encode() + b"\x0a")

    def on_timeout(self):
        print(f"Flushing input buffer of port {self.cbb_port_selector.palmsens_handle.name}")
        self.WE_currents = []
        self.cbb_port_selector.palmsens_handle.flush()
        self.read_channel(0)
        self.timer.start(200)

    def on_port_changed(self):
        if self.cbb_port_selector.state == PORT_STATE.PORT_OPEN:  # port open
            self.status = STATUS.STOPPED

    def on_settings_clicked(self):
        self.settings_dlg = SettingsDialog(self, self.cbb_receipe_selector._full_receipe_name)
        if self.settings_dlg.exec() == QDialog.Accepted:
            self.cbb_receipe_selector.refresh()

    def on_save_clicked(self):
        self.interpreter.save()

    def receipe_changed(self):
        self.cw_charts.chart.setTitle(self.cbb_receipe_selector.receipe["name"])
        self.interpreter.MAX_READINGS = self.cbb_receipe_selector.receipe["max_points_to_keep_in_memory"]
        self.cw_charts.line.setName(f"ch0, {self.cbb_receipe_selector.receipe['units1']}")
        self.cw_charts.line2.setName(f"ch1, {self.cbb_receipe_selector.receipe['units2']}")

    def __init__(self, parent):
        super().__init__(parent)
        self._status = None
        self.channel = -1
        self.main_timer = QTimer()
        self.main_timer.timeout.connect(self.on_timeout)
        layout = QVBoxLayout()
        self.interpreter = Interpreter()
        self.WE_currents = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeout)
        toolbar_layout = QHBoxLayout()
        self.cbb_port_selector = PortSelector()
        self.cbb_port_selector.on_port_changed.connect(self.on_port_changed)
        self.cbb_port_selector.setText("Select Port")
        self.cbb_receipe_selector = ReceipeSelector()
        self.cbb_receipe_selector.setText("Receipe")
        self.cbb_receipe_selector.on_receipe_changed.connect(self.receipe_changed)
        self.pb_start = QPushButton("Start")
        self.pb_start.clicked.connect(self.start_clicked)
        self.pb_save = QPushButton("Save")
        self.pb_save.clicked.connect(self.on_save_clicked)
        self.pb_settings = QPushButton("Settings")
        self.pb_settings.clicked.connect(self.on_settings_clicked)
        toolbar_layout.addWidget(self.cbb_port_selector)
        toolbar_layout.addWidget(self.cbb_receipe_selector)
        toolbar_layout.addWidget(self.pb_start)
        toolbar_layout.addWidget(self.pb_save)
        toolbar_layout.addWidget(self.pb_settings)
        self.cw_charts = ChartWidget()
        layout.addLayout(toolbar_layout)
        layout.addWidget(self.cw_charts)
        self.setLayout(layout)
        self.status = STATUS.NOT_CONNECTED



if __name__ == "__main__":
    app = QApplication([])
    main_window = QMainWindow()
    Styles.init()
    app.setStyleSheet(Styles.style)
    main_window.resize(*main_wnd_size)
    main_window.setWindowTitle(main_wnd_title)
    main_widget = MainWidget(main_window)
    main_window.setCentralWidget(main_widget)
    main_window.show()
    app.exec()
