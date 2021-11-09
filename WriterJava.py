from PlantContent import PlantContent
from PlantContent import PlantMethod
from Utilities import *

class WriteJava():

    def write(self):
        print('Writing Golang ')
            
    def __init__(self, in_json_config, in_plant_structures: list[PlantContent]):
        self.json_config = in_json_config
        self.plant_structures = in_plant_structures
        self.package_path = ''