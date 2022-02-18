import os

import PUMLTemplate
from PlantContent import PlantContent
from Cheetah.Template import Template

relationships = {'-->', '..>', '*--'}


def extract_name(in_line: str) -> str:
    """
    Extracts the name from the type construct. Information that is not needed will be removed
    such as the stereotype.
    """
    types = {'package', 'class', 'abstract', 'interface',
             'enum', 'abstract class', 'entity'}
    process_type: str = ''
    for item_type in types:
        if in_line.startswith(item_type):
            process_type = item_type
            break

    process_line = in_line.replace(' ', '')
    if '<<' in process_line:
        process_line = process_line.split('<<')[0]
    process_line = process_line.replace(process_type, '')
    found_name = process_line.split('{')[0]
    return found_name


def find_plant_structure(plant_structures: list[PlantContent], in_package: str, in_name: str) -> PlantContent:
    """
    Finds the structure in the structure list, if there is no match for the name of the structure
    then a new structure is created and added to the list. Both the name and the package are used
    to identify the structure, this alows for a class with the same name to exist in differnt packages
    """
    for structure in plant_structures:
        if structure.name == in_name and structure.package == in_package:
            return structure
    structure = PlantContent()
    structure.name = in_name
    structure.package = in_package
    plant_structures.append(structure)
    return structure


def isvariable(in_line: str) -> bool:
    for relationship in relationships:
        if relationship in in_line:
            return False
    if '(' in in_line:
        return False
    elif ':' in in_line:
        return True
    else:
        return False


def ismethod(in_line: str) -> bool:
    if '(' in in_line:
        return True
    else:
        return False


def isextends(in_line: str) -> bool:
    if '--|>' in in_line:
        return True
    else:
        return False


def isimplements(in_line: str) -> bool:
    if '..>' in in_line:
        return True
    else:
        return False


def isuses(in_line: str) -> bool:
    if '-->' in in_line:
        return True
    else:
        return False


def iscomposition(in_line: str) -> bool:
    if '*--' in in_line:
        return True
    else:
        return False


def maybe_create_package(in_target: str, in_package: str) -> str:
    package_path = in_package.replace('.', '/')
    package_path = in_target + '/' + package_path
    if not os.path.exists(package_path):
        os.makedirs(package_path)
    return package_path


def create_wording(file, in_comment_start: str, in_comment_end: str, in_comment_middle: str):
    file.write(f'{in_comment_start}\n')
    file.write(f'{in_comment_middle} Created with CMS Community forward engineering\n')
    file.write(f'{in_comment_end}\n')


def get_namespace(in_line: str) -> str:
    namespace = ''
    if '.' not in in_line:
        return namespace
    line_split = in_line.split('.')
    for idx, part in enumerate(line_split):
        if (idx + 1) < len(line_split):
            namespace = namespace + part
            if (idx + 1) < len(line_split) - 1:
                namespace = namespace + '.'
    return namespace


def alternate_name(in_line: str):
    """
    Alternate name came come in two forms (1) The label at the end of the
    relationship definition the other is for cardinality where the lable can be defined
    before the child class.
    """
    if '"' in in_line:
        return_value_alternative, return_value_name = __process_mid_label(in_line)
    else:
        return_value_alternative, return_value_name = __process_end_label(in_line)
    return return_value_alternative, return_value_name


def __process_mid_label(in_line: str):
    return_value_alternative = in_line
    return_value_name = in_line
    line_split = in_line.split('"')
    if len(line_split) > 1:
        return_value_name = line_split[2]
        return_value_alternative = line_split[1]
    return return_value_alternative, return_value_name


def __process_end_label(in_line: str):
    return_value_alternative = in_line
    return_value_name = in_line
    line_split = in_line.split(':')
    if len(line_split) > 1:
        return_value_name = line_split[0]
        return_value_alternative = line_split[1]
    return return_value_alternative, return_value_name


def build_template(template_name, namespace) -> str:
    if template_name == 'addto':
        template_str = PUMLTemplate.get_addto_template()
    elif template_name == 'removefrom':
        template_str = PUMLTemplate.get_removefrom_template()

    template = Template(template_str, searchList=[namespace])
    return str(template)
