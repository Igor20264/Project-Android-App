import time

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import MDList
from kivymd.uix.picker import MDDatePicker

from menu.homepage.cardDz import carddZ

from Logic import getInternet
from Logic_Lite import Sessions_Lite
#
#MDRoundFlatButton
Builder.load_string("""
<caledare@BoxLayout>:
    orientation:"vertical"
    MDToolbar:
        title: "Домашнее задание на"
        MDRoundFlatButton:
            id: datee
            text: "Дата"
            text_color: app.theme_cls.accent_color
            line_color: app.theme_cls.accent_color
            pos_hint: {'center_x': .5, 'center_y': .5}
            on_release: root.show_date_picker()
    ScrollView:
        id: ScrView
""")

setting=False
internet = getInternet()

class caledare(BoxLayout):
    def __int__(self):
        # --- --- time --- ---
        t = time.localtime()
        c_t = str(int(time.strftime("%d", t)) + 1)
        cu_ti = time.strftime(f"20%y-%m-", t)
        if len(str(c_t)) == 1:
            c_t =str(0)+str(c_t)
        cuc = cu_ti + c_t
        # --- --- end --- ---
        if internet:
            self.box =BoxLayout(orientation='vertical')
            self.sess = Sessions_Lite(internet=getInternet())
            self.listen = listen(sess=self.sess, date=cuc)
            self.ids.ScrView.add_widget(self.listen.build())
            self.date = cuc
            self.ids.datee.text = self.date


    def on_save(self, instance,value,date_range):
        self.date = value
        self.ids.datee.text = str(self.date)
        self.list_remove()

    def list_remove(self):
        self.ids.datee.text = str(self.date)
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
        perms = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
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

