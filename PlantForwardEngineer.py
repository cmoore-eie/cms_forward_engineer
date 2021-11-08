import os
import sys
import getopt
import json
from ProcessInput import ProcessInput
from WriterGosu import WriteGosu

help_str = '''

Please supply the arguments for -c
        -c, --configuration - path to the configuration file
        -h, --help - displays this text

        '''

process_errors = dict()
json_errors = dict()
json_defaults = dict()


def main(argv):
    config_file: str = ''

    try:
        opts, args = getopt.getopt(argv, 'c:', ['help', 'config ='])
        for opt, arg in opts:
            if opt in ['-c', '--config']:
                config_file = arg.strip()
            elif opt in ['-h', '--help']:
                print(help_str)
                sys.exit()
            else:
                sys.exit()
    except getopt.GetoptError:
        print(help_str)
        sys.exit(2)

    if config_file == '':
        process_errors[len(process_errors) +
                       1] = "-c (--config) missing and is required"
        sys.exit(1)

    if len(process_errors) > 0:
        print("")
        print("Missing Parameter Information")
        print("=============================")
        for error_item in process_errors:
            print(f"({error_item}) : {process_errors[error_item]}")
    else:
        try:
            file = open(config_file)
        except FileNotFoundError:
            print(f'The configuration file {config_file} has not been found')
            sys.exit(1)
        config_json = checkAndFixJson(json.load(file))
        process = ProcessInput(config_json)
        process.process_input()
        if config_json['output_type'].lower() == 'gosu':
            writer = WriteGosu(config_json, process.plant_structures)
            writer.write()

def checkAndFixJson(config_json):
    if 'default_package' not in config_json:
        config_json['default_package'] = 'cms.unknown'
        json_defaults[len(json_defaults) + 1] = f'Defaulting default_package to cms.unknown'

    if 'output_type' not in config_json:
        config_json['output_type'] = 'gosu'
        json_defaults[len(json_defaults) + 1] = f'Defaulting output_type to gosu'

    if not config_json['output_type'] == 'gosu':
        json_errors[len(json_errors) + 1] = f'output_type may only have the value "gosu"'

    if 'source_document' in config_json:
        source_path = config_json['source_document']
        if not os.path.exists(source_path):
            json_errors[len(json_errors) + 1] = f'source_document {source_path} is invalid'
    else:
        json_errors[len(json_errors) + 1] = f'source_document has not been set'

    if 'target_directory' in config_json:
        target_path = config_json['target_directory']
        if not os.path.exists(target_path):
            json_errors[len(json_errors) + 1] = f'target_directory {target_path} is invalid'
    else:
        json_errors[len(json_errors) + 1] = f'target_directory has not been set'

    if len(json_errors) > 0:
        print("")
        print("Configuration issues")
        print("====================")
        for error_item in json_errors:
            print(f"({error_item}) : {json_errors[error_item]}")
        sys.exit(1)

    if len(json_defaults) > 0:
        print("")
        print("Configuration settings defaulted")
        print("================================")
        for default_item in json_defaults:
            print(f"({default_item}) : {json_defaults[default_item]}")
    return config_json

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(help_str)
        sys.exit()
    main(sys.argv[1:])