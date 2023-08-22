#current_range = ["100nA", "1.95uA", "3.91uA", "7.81uA", "15.63uA",
#                 "31.25uA", "62.5uA", "125uA", "250uA", "500uA", "1mA",
#                 "5mA"]
import time

from PyQt5.QtWidgets import QFileDialog
column_names = ["Time", "Type", "Value", "Units", "Type", "Value", "Units",
                "MetaID", "Status", "I_Range",
                "MetaID", "Status", "I_Range"]
separator = ","
current_range = {
    0x0: "100nA",
    0x1: "1.9uA",
    0x2: "3.91uA",
    0x3: "7.81uA",
    0x4: "15.63uA",
    0x5: "31.25uA",
    0x6: "62.5uA",
    0x7: "125uA",
    0x8: "250uA",
    0x9: "500uA",
    0xA: "1mA",
    0xB: "5mA",
    0x80: "100nA",
    0x81: "1uA",
    0x82: "6.25uA",
    0x83: "12.5uA",
    0x84: "25uA",
    0x85: "50uA",
    0x86: "100uA",
    0x87: "200uA",
    0x88: "1mA",
    0x89: "5mA",

}


measurement_status = {
    "0":"OK",
    "1":"timing not met",
    "2":"overload",
    "4":"underload",
    "8":"overload warning"
}
measurement_types = {
    "da": "V cell",
    "ba": "WE current"
}
measurement_id_types ={
    1: "Status",
    2: "Current range",
    4: "Noise"
}
si_factor = {
    "a": 1E-18,
    "f": 1E-15,
    "p": 1E-12,
    "n": 1E-9,
    "u": 1E-6,
    "m": 1E-3,
    " ": 1,
    "k": 1E3,
    "M": 1E6,
    "G": 1E9,
    "T": 1E12,
    "P": 1E15,
    "E": 1E18,

}

class Meta:
    def __init__(self):
        self.id = 0
        self.status = 0
        self.current_range = 0
        self.noise = 0
    def __str__(self):
        if self.id == 1:
            result = f"{measurement_id_types[self.id]}: {measurement_status[self.status]}"
        elif self.id == 2:
            current_range_txt = ""
            try:
                current_range_txt = current_range[self.current_range]
            except:
                pass
            result = f"{measurement_id_types[self.id]} current_range: {current_range_txt}"
        return  result
    def to_csv(self):
        csv = f"{measurement_id_types[self.id]}{separator}{self.status}{separator}{self.current_range}{separator}"
        return  csv

class Varialble:
    def __init__(self):
        self.type:str = ""
        self.value:int = 0
        self.value_prefix:str = ""
        self.metas = []
    def __str__(self):
        result = f"type: {measurement_types[self.type]}, value: {self.value}{self.value_prefix}"
        for meta in self.metas:
            result = result + ", " + str(meta)
        return result
    def to_csv(self):
        csv = f"{measurement_types[self.type]}{separator}{self.value}{separator}{self.value_prefix}{separator}"
        if len(self.metas):
            for meta in self.metas:
                csv = csv + meta.to_csv()
        return csv

class Package:
    @property
    def value_valid(self):
        for var in self.variables:
            if var.type == "ba":
                for meta in var.metas:
                    if meta.id == 1 and meta.status == "0":
                        return True
        return False
    @property
    def value(self):
        for var in self.variables:
            if var.type == "ba":
                return var.value * si_factor[var.value_prefix];
        return 0
    def __init__(self):
        self.variables = []
        self.time = time.time()
    def __str__(self):
        result = ""
        for variable in self.variables:
            result = result + str(variable) + "; "
        return result

    def to_csv(self):
        csv = f"{self.time}{separator}"
        for variable in self.variables:
            csv = csv +variable.to_csv()
        return  csv


class Interpreter:
    MAX_READINGS = 100000
    def __init__(self):
        self.readings = []
    def csv_table_headers(self):
        return separator.join(column_names) + "\n"

    def save(self):
        file_name = QFileDialog.getSaveFileName(None, "Save readings to ...", "/", "*.csv")
        if file_name[0] != "":
            try:
                with open(file_name[0], "w+") as f:
                    f.write(self.csv_table_headers())
                    for reading in self.readings:
                        f.write(reading.to_csv())
                        f.write("\n")
            except Exception as ex:
                print(ex)

    def add_reading(self, reading: Package):
        self.readings.append(reading)
        if len(self.readings)>=Interpreter.MAX_READINGS:
            self.readings.pop()

    def interpret(self, response: str):
        package = None
        if (response[0] == 'P') and (response[-1] == "\n"):
            #print(response)
            package = Package()
            # valid response
            variables = response[1:-1].split(";")
            for var in variables:
                variable = Varialble()
                variable.type = var[:2]
                if variable.type == "da":  # Set control value for cell potential
                    try:
                        variable.value = int(var[2:-1], 16) - 2 ** 27
                        variable.value_prefix = var[-1]
                    except Exception as ex:
                        print(f"Conversion failed {var}")
                elif variable.type == "ba":  # Measured WE current
                    metas = var.split(",")
                    try:
                        variable.value = int(metas[0][2:-1], 16) - 2 ** 27
                        variable.value_prefix = metas[0][-1]
                        for meta_raw in metas[1:]:
                            meta = Meta()
                            meta.id = int(meta_raw[0])
                            if meta.id  == 1:  # status
                                meta.status = meta_raw[1]
                            elif meta.id  == 2:  # current range
                                meta.current_range = int(meta_raw[1:], 16)
                            elif meta.id  == 4:  # noise
                                pass
                            variable.metas.append(meta)
                    except Exception as ex:
                        print(f"Conversion failed {var}")
                package.variables.append(variable)
                self.add_reading(package)
        return package