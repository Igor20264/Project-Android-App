import time

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import MDList
from kivymd.uix.pickers import MDDatePicker
import datetime
from menu.homepage.cardDz import carddZ
from Logic import getInternet
from Logic_Lite import Sessions_Lite

Builder.load_string("""
<caledare@BoxLayout>:
    orientation:"vertical"
    MDTopAppBar:
        title: "Домашнее задание"
        right_action_items:
            [["calendar-range",lambda x: root.show_date_picker(),"Выбрать дату","mdiCalendarRange"],]
    ScrollView:
        id: ScrView
""")

setting=False
internet = getInternet()

class caledare(BoxLayout):
    sess = lambda x:None
    def __int__(self):
        # --- --- time --- ---
        cuc = datetime.date.today() + datetime.timedelta(days=1)
        cuc.strftime('20%y-%m-%d')
        # --- --- end --- ---
        if internet:
            self.box =BoxLayout(orientation='vertical')
            self.listen = listen(sess=self.sess, date=cuc)
            self.ids.ScrView.add_widget(self.listen.build())
            self.date = cuc


    def on_save(self, instance,value,date_range):
        self.date = value
        self.list_remove()

    def list_remove(self):
        self.ids.ScrView.remove_widget(self.ids.ScrView.children[0])
        self.listen = listen(sess=self.sess,date=self.date)
        self.ids.ScrView.add_widget(self.listen.build())

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        if internet:
            date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

class listen:
    def __init__(self,sess,date):
        self.liste = sess.DzApi(date=date)
    def build(self):
        grid = MDList()
        for i in self.liste:
            predmet = i[0]
            dz = i[1]
            kab = i[2]
            timee = i[3]
            url = i[4]
            ad = carddZ()
            if len(dz) >= 5:
                grid.add_widget(ad.boxdze(url=url,predmet=predmet, dz=dz, kab=kab,timee=timee))
            elif setting == True:
                grid.add_widget(ad.boxdze(url=url,predmet=predmet, dz=dz, kab=kab,timee=timee))
            else:
                pass

        return grid

