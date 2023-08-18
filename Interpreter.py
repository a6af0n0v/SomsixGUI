current_range = ["100nA", "1.95uA", "3.91uA", "7.81uA", "15.63uA",
                 "31.25uA", "62.5uA", "125uA", "250uA", "500uA", "1mA",
                 "5mA"]
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
            result = f"{measurement_id_types[self.id]} current_range: {current_range[self.current_range]}"
        return  result

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
    def __str__(self):
        result = ""
        for variable in self.variables:
            result = result + str(variable) + "; "
        return result


class Interpreter:
    def init(self):
        self.readings = []

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
        return package