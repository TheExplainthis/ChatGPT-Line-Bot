import json


class Storage():
    def __init__(self, file_name):
        self.fine_name = file_name

    def save(self, data):
        with open(self.fine_name, 'w', newline='') as f:
            json.dump(data, f)

    def load(self):
        with open(self.fine_name, newline='') as jsonfile:
            data = json.load(jsonfile)
        return data
