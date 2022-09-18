import json
import smapi

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

class Mosreg_api:
    def __init__(self):
        with open('files/data_file.json') as f:
            a = json.load(f)
        client = smapi.Client(password='Igor20264Igor',login='i.tarasov.a')
        profil = client.get_me()
        g = client.get_my_context()
