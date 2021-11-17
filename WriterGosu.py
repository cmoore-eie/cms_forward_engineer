from Utilities import *


def convert_type(in_type: str) -> str:
    if in_type == 'bit':
        return 'boolean'
    if in_type == 'datetime':
        return 'Date'
    if in_type == 'mediumtext':
        return 'String'
    if in_type == 'nonnegativeinteger':
        return 'int'
    if in_type == 'phone':
        return 'String'
    if in_type == 'shorttext':
        return 'String'
    if in_type == 'spatialpoint':
        return 'String'
    if in_type == 'varchar':
        return 'String'
    if in_type == 'year':
        return 'int'
    return in_type


class WriteGosu:

    def write(self):
        print('Writing Gosu Classes')
        for structure in self.plant_structures:
            self.package_path = maybe_create_package(self.json_config['target_directory'], structure.package)
            self.create_class(structure)

    def create_class(self, in_structure: PlantContent):
        class_file_name = self.package_path
        class_file_name = class_file_name + '/' + in_structure.name + '.gs'
        file = open(class_file_name, 'w')
        file.write(f'package {in_structure.package}\n')
        file.write('\n')
        self.create_uses(file, in_structure)
        create_wording(file, '/**', '/*', ' * ')
        class_type = in_structure.type
        if class_type == 'abstract':
            file.write('abstract class ' + in_structure.name)
        elif class_type == 'interface':
            file.write('interface ' + in_structure.name)
        else:
            file.write('class ' + in_structure.name)
        if len(in_structure.extensions) > 0:
            file.write(' extends ')
            for idx, extends_name in enumerate(in_structure.extensions):
                file.write(extends_name)
                if idx + 1 < len(in_structure.extensions):
                    file.write(', ')
        if len(in_structure.implements) > 0:
            file.write(' implements ')
            for idx, implements_name in enumerate(in_structure.implements):
                file.write(implements_name)
                if idx + 1 < len(in_structure.implements):
                    file.write(', ')
        file.write(' { \n\n')
        if len(in_structure.variables) > 0:
            self.create_variables(file, in_structure)
            file.write('\n')
        if not class_type == "interface":
            file.write('  construct() {\n')
            file.write('  }\n')
            file.write('\n')
        if len(in_structure.methods) > 0:
            self.create_methods(file, in_structure)
            file.write('\n')
        file.write('}')
        file.close()

    def create_uses(self, file, in_structure: PlantContent):
        """
        Create the uses statements, while there are some that have been created during the processing
        of the puml some additional ones are needed for some of the data types, these are added here.
        """
        for var in in_structure.variables:
            if var.type == 'BigDecimal':
                in_structure.add_implement('java.math,BigDecimal')
            if var.type == 'Date':
                in_structure.add_implement('java.util.Date')
        if len(in_structure.imports) == 0:
            return
        for uses in in_structure.imports:
            file.write(f'uses {uses}\n')
        file.write('\n')
        return self

    def create_variables(self, file, in_structure: PlantContent):
        for variable in in_structure.variables:
            var_name = '_' + variable.name[0].lower() + variable.name[1:]
            var_as = variable.name[0].upper() + variable.name[1:]
            var_type = convert_type(variable.type)
            if variable.scope == 'protected':
                file.write(f'  protected var {var_name} : {var_type} as {var_as}\n')
            if variable.scope == 'private':
                file.write(f'  var {var_name} : {var_type}\n')
            if variable.scope == 'public':
                file.write(f'  var {var_name} : {var_type} as {var_as}\n')
        return self

    def create_methods(self, file, in_structure: PlantContent):
        for method in in_structure.methods:
            method_name = method.name
            method_return_type = convert_type(method.return_type)
            method_scope = method.scope
            file.write(f'  {method_scope} function ' + method_name + ' (')
            for idx, param in enumerate(method.parameters):
                param_type = method.parameters[param]
                file.write(f'{param} : {param_type}')
                if idx + 1 < len(method.parameters):
                    file.write(', ')
            file.write(') ')
            if not method_return_type == '':
                file.write(': ' + method_return_type + ' ')
            file.write('{\n')
            if not method_return_type == '':
                file.write('    return null\n')
            file.write('  }\n\n')
        for composition in in_structure.compositions:
            method_name = 'addTo' + composition.alternate[0].upper() + composition.alternate[1:]
            file.write('  public function ' + method_name + ' (')
            file.write('inItem : ' + composition.type + ') {\n')
            file.write('  }\n')
            file.write('\n')
            method_name = 'removeFrom' + composition.alternate[0].upper() + composition.alternate[1:]
            file.write('  public function ' + method_name + ' (')
            file.write('inItem : ' + composition.type + ') {\n')
            file.write('  }\n')
        return self

    def create_composition(self, file, in_structure: PlantContent):
        pass

    def __init__(self, in_json_config, in_plant_structures: list[PlantContent]):
        self.json_config = in_json_config
        self.plant_structures = in_plant_structures
        self.package_path = ''
