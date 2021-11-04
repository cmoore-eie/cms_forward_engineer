class PlantMethod:

    def add_parameter(self, in_parameter_name: str, in_parameter_type: str):
        if in_parameter_name not in self.parameters:
            self.parameters[in_parameter_name] = in_parameter_type

    def __init__(self):
        self.name: str = ''
        self.parameters: dict[str, str] = dict()
        self.return_type: str = ''



class PlantContent:

    def add_variable(self, in_variable_name: str, in_variable_type: str):
        if in_variable_name not in self.variables:
            self.variables[in_variable_name] = in_variable_type

    def add_composition(self, in_composition_name: str):
        if not in_composition_name in self.compositions:
            self.compositions.append(in_composition_name)

    def add_extension(self, in_extension_name: str):
        if not in_extension_name in self.extensions:
            self.extensions.append(in_extension_name)

    def add_import(self, in_import_name: str):
        if not in_import_name in self.imports:
            self.imports.append(in_import_name)

    def add_implement(self, in_implement_name: str):
        if in_implement_name not in self.implements:
            self.implements.append(in_implement_name)

    def add_uses(self, in_uses_name: str):
        if not in_uses_name in self.extensions:
            self.uses.append(in_uses_name)

    def add_method(self, in_method_name: str, in_method_return_type: str) -> PlantMethod:
        method_found = False
        for method in self.methods:
            if in_method_name == method.name:
                method_found = True
                return method
        if method_found == False:
            new_method = PlantMethod()
            new_method.name = in_method_name
            new_method.return_type = in_method_return_type
            self.methods.append(new_method)
            return new_method

    def __init__(self):
        self.name: str = ''
        self.type: str = ''
        self.package: str = ''
        self.stereotype: str = ''
        self.variables: dict[str, str] = dict()
        self.methods: list[PlantMethod] = list()
        self.extensions: list[str] = list()
        self.implements: list[str] = list()
        self.uses: list[str] = list()
        self.imports: list[str] = list()
        self.compositions: list[str] = list()
