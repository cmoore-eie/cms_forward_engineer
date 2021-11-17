
from Utilities import *


class WriteJava:

    def write(self):
        print('Writing Java ')
        return self

    def __init__(self, in_json_config, in_plant_structures: list[PlantContent]):
        self.json_config = in_json_config
        self.plant_structures = in_plant_structures
        self.package_path = ''
