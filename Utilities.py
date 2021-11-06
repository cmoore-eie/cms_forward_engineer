import os
from PlantContent import PlantContent

def extract_name(in_line: str) -> str:
    types = {'package', 'class', 'abstract', 'interface'
    , 'enum', 'abstract class', 'entity'}
    process_type: str = ''
    for type in types:
        if in_line.startswith(type):
            process_type = type
            break
    
    process_line = in_line.replace(' ', '')
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
    if not '.' in in_line:
        return namespace
    line_split = in_line.split('.')
    for idx, part in enumerate(line_split):
        if (idx + 1) < len(line_split):
            namespace = namespace + part
            if (idx + 1) < len(line_split) -1:
                namespace = namespace + '.'
    return namespace

def get_scope(in_name: str) -> str:
        scope_types = {'+', '-', '~', '#'}
        scope_type = 'public'
        test_name = in_name
        if test_name[0] in scope_types:
            if test_name[0] == '+':
                scope_type = 'public'
            elif test_name[0] == '-':
                scope_type = 'private'
            elif test_name[0] == '~':
                scope_type = 'protected'
            elif test_name[0] == '#':
                scope_type = 'protected'
            test_name = test_name[1:]

        return scope_type, test_name

