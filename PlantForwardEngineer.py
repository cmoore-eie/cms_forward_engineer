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
        print(config_json)
        process = ProcessInput(config_json)
        process.process_input()
        writer = WriteGosu(config_json, process.plant_structures)
        writer.write()

def checkAndFixJson(config_json):
    return config_json

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(help_str)
        sys.exit()
    main(sys.argv[1:])