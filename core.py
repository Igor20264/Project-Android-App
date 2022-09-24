import json

class settigs:
    def __init__(self, namefile='setting.json'):
        self.file = namefile

    def save(self, data="None"):
        if data == "None":
            data = {'main': {'bedozenka': True}, 'home': {None: None}}
        with open(f'settings/{self.file}', 'w') as setfile:
            json.dump(data, setfile)

    def load(self):
        with open(f'settings/{self.file}', 'r') as setfile:
            self.setlist = json.load(setfile)
            return self.setlist
