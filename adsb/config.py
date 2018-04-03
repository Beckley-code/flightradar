import json

class Config():

    """ Application configuration """

    def __init__(self):
        self.data_folder = ''
        self.service_url = ''
        self.military_only = True
        self.type = 'mm2'
        self.delete_after = 1440

    def from_file(self, filename):
        with open(filename, 'r') as json_file:
            config = json.load(json_file)

            if 'dataFolder' in config:
                self.data_folder = config['dataFolder']
            else:
                raise ValueError('dataFolder not specified in config')

            if 'type' in config:
                self.type = config['type']
            else:
                raise ValueError('type not specified in config')

            if 'serviceUrl' in config:
                url = config['serviceUrl']
                self.service_url = url[:-1] if url[-1] == "/" else url                

            if 'militaryOnly' in config:
                self.military_only = config['militaryOnly']

            if 'deleteAfterMinutes' in config:
                self.delete_after = config['deleteAfterMinutes']
    