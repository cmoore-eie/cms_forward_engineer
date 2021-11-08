from PlantContent import PlantContent
from Utilities import *


class ProcessInput:

    def process_input(self):
        print('Processing Source File')
        with open(self.json_config['source_document']) as input_file:
            for line in input_file:
                self.lines.append(line.strip())
        self.process_lines()

    def process_lines(self):
        for line in self.lines:
            if line.startswith('package'):
                self.process_package(line)
            elif line.startswith('class'):
                self.process_type(line, 'class')
            elif line.startswith('abstract'):
                self.process_type(line, 'abstract')
            elif line.startswith('abstract class'):
                self.process_type(line, 'abstract')
            elif line.startswith('interface'):
                self.process_type(line, 'interface')
            elif line.startswith('enum'):
                self.process_type(line, 'enum')
            else:
                self.process_line(line)

    def process_line(self, in_line: str):
        if self.current_type == '':
            return
        if in_line == '}':
            return
        if isvariable(in_line):
            self.process_variable(in_line)
        if ismethod(in_line):
            self.process_method(in_line)
        if isextends(in_line):
            self.process_extends(in_line)
        if isimplements(in_line):
            self.process_implements(in_line)
        if isuses(in_line):
            self.process_uses(in_line)
        if iscomposition(in_line):
            self.process_composition(in_line)

    def process_uses(self, in_line):
        process_line = in_line.replace(' ', '')
        line_split = process_line.split('-->')
        alternate, uses_name = alternate_name(line_split[1])
        namespace = get_namespace(uses_name)
        parent_name = line_split[0]
        self.current_structure = find_plant_structure(self.plant_structures, self.current_package, parent_name)
        if self.current_structure.type == '':
                self.current_structure.type = 'class'
        uses_short_name = ''
        if namespace == '':
            uses_short_name = uses_name
        else:
            uses_short_name = uses_name.split('.')[-1] 
            self.current_structure.add_import(uses_name)
        self.current_structure.add_variable(alternate, uses_short_name)
        self.current_structure.add_uses(uses_short_name)

    def process_implements(self, in_line):
        process_line = in_line.replace(' ', '')
        implements_name = process_line.split('..>')[1]
        parent_name = process_line.split('..>')[0]
        structure = find_plant_structure(self.plant_structures, self.current_package, parent_name)
        if not structure == self.current_structure:
            self.current_structure = structure
            if structure.type == '':
                structure.type = 'class'   
        self.current_structure.add_implement(implements_name)        

    def process_extends(self, in_line):
        process_line = in_line.replace(' ', '')
        extends_name = process_line.split('--|>')[1]
        parent_name = process_line.split('--|>')[0]
        structure = find_plant_structure(self.plant_structures, self.current_package, parent_name)
        if not structure == self.current_structure:
            self.current_structure = structure
            if structure.type == '':
                structure.type = 'class'   
        self.current_structure.add_extension(extends_name)

    def process_composition(self, in_line):
        process_line = in_line.replace(' ', '')
        alternate, composition_name = alternate_name(process_line.split('*--')[1])
        parent_name = process_line.split('*--')[0]
        structure = find_plant_structure(self.plant_structures, self.current_package, parent_name)
        namespace = get_namespace(composition_name)
        if not structure == self.current_structure:
            self.current_structure = structure
            if structure.type == '':
                structure.type = 'class'
        composition_short_name = ''
        if namespace == '':
            composition_short_name = composition_name
            find_plant_structure(self.plant_structures, self.current_package, composition_short_name)
        else:
            composition_short_name = composition_name.split('.')[-1] 
            self.current_structure.add_import(composition_name)
            find_plant_structure(self.plant_structures, namespace, composition_short_name)
        if alternate == composition_name:
            self.current_structure.add_variable(composition_short_name, f'{composition_short_name}[]')
        else:
            self.current_structure.add_variable(alternate, f'{composition_short_name}[]')
        self.current_structure.add_composition(composition_short_name, alternate)

    def process_variable(self, in_line):
        process_line = in_line.replace(' ', '')
        variable_name = process_line.split(':')[0]
        if len(process_line.split(':')) == 1:
            variable_type = 'None'
        else:
            variable_type = process_line.split(':')[1]
        self.current_structure.add_variable(variable_name, variable_type)

    def process_method(self, in_line):
        process_line = in_line.replace(' ', '')
        method_name = process_line.split('(')[0]
        method_split_return = process_line.split('):')
        if len(method_split_return) == 2:
            method_return_type = method_split_return[1]
        else:
            method_return_type = ''
        found_method = self.current_structure.add_method(
            method_name, method_return_type)
        method_params = process_line.replace('(', '~')
        if method_return_type == '':
            method_params = method_params.replace(')', '~')
        else:
            method_params = method_params.replace('):', '~')
        method_params = method_params.split('~')
        if not method_params[1] == '':
            for param in method_params[1].split(','):
                param_name = param.split(':')[0]
                if len(param.split(':')) == 1:
                    param_type = 'None'
                else:
                    param_type = param.split(':')[1]
                found_method.add_parameter(param_name, param_type)

        self.current_structure.add_method(method_name, method_return_type)

    def process_package(self, in_line: str):
        package_name = extract_name(in_line)
        self.current_package = package_name
        self.current_type = ''
        self.current_structure = None

    def process_type(self, in_line: str, in_type: str):
        self.current_type = extract_name(in_line)
        namespace = get_namespace(self.current_type)
        if not namespace == '':
            if not self.current_package == namespace:
                self.current_type = self.current_type.split('.')[-1] 
                self.current_package = namespace
        
        self.current_structure = find_plant_structure(
            self.plant_structures, self.current_package, self.current_type)
        if self.current_structure.type == '':
            self.current_structure.type = in_type
        else:
            if not self.current_structure.type == in_type:
                self.current_structure.type = in_type

    def __init__(self, in_json_config):
        """
        default_package should be passed in the configuration file, it will be used where there is no package defined in the puml file.
        """
        self.json_config = in_json_config
        self.default_package = 'cms.test'
        self.current_package = self.default_package
        self.current_type = ''
        self.current_structure: PlantContent
        self.plant_structures: list[PlantContent] = list()
        self.lines: list[str] = list()
