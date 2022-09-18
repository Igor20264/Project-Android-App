import requests
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField
import json

class auth:
    def __init__(self,SM):
        super(auth, self).__init__()
        self.sm = SM
        self.box = MDBoxLayout(orientation='vertical')
        self.box1 = MDBoxLayout(size_hint=(1, .2))
        self.mdlist = AnchorLayout(anchor_y='center', anchor_x='center')

        self.textinput()
        self.button()
        self.chek()
    def textinput(self): #1 2
        self.user=MDTextField(hint_text="Введите логин", size=[1, .5])
        self.passwd=MDTextField(hint_text="Введите пароль", size=[1, .5], password=True)
        self.box.add_widget(self.user)
        self.box.add_widget(self.passwd)

    def chek(self): # 4
        self.chek = MDCheckbox(size_hint=[None, None], size=["48dp", "48dp"], pos_hint={'center_x': .5, 'center_y': .5})

        lab = Label(text="Запомнить пользователя", color=[0, 0, 0, 1])
        self.box1.add_widget(lab)
        self.box1.add_widget(self.chek)

    def button(self):
        def press(instance):
            if self.chek.active == True:
                print(self.chek.active)
                loggindat={
                        'login': self.user.text,
                        'password': self.passwd.text
                    }
                session = requests.Session()
                d = session.post('https://uslugi.mosreg.ru/api/school/user/login', loggindat)
                #a = session.get('https://school.mosreg.ru/userfeed/')
                if d.status_code == 200:
                    with open("data_file.json", "w") as write_file:
                        json.dump(loggindat, write_file)
                    self.sm.current = 'auth1'
            else:

                print(self.user.text)
                print(self.passwd.text)

        btn = MDRoundFlatButton(text="Войти", font_size="32sp", on_press=press)
        self.mdlist.add_widget(btn)

    def chekpaswd(self):
        try:
            with open("data_file.json", "r") as write_file:
                file = json.load(write_file)
                print(file)
                return file
        except:
            return self.build

    def build(self):
        self.box.add_widget(self.box1)
        self.box.add_widget(self.mdlist)
        return self.box