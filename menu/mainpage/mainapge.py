# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.list import ThreeLineListItem, MDList
from kivymd.uix.toolbar import MDTopAppBar

from menu.mainpage.dialogs import dialog
data = False

class mainpage:
    def __init__(self,sess,settings):
        self.liste = sess.feedparse()
        self.grid = MDList()
        self.data = settings["main"]["bedozenka"]
    def boxocenka(self, predmet,text2,ozenka, date):
        try:
            ozenkaa = int(ozenka[0:1])

            if text2 == None:
                if ozenkaa < 3:
                    item = ThreeLineListItem(text=predmet, secondary_text=f"[color=CC0000]{ozenka}[/color]", tertiary_text=date,
                                             secondary_theme_text_color="Custom") #, secondary_text_color=c_red
                elif ozenkaa == 3:
                    item = ThreeLineListItem(text=predmet, secondary_text=f"[color=FF6600]{ozenka}[/color]", tertiary_text=date,
                                             secondary_theme_text_color="Custom") #, secondary_text_color=c_orenge
                else:
                    item = ThreeLineListItem(text=predmet, secondary_text=f"[color=00CC00]{ozenka}[/color]", tertiary_text=date,
                                             secondary_theme_text_color="Custom") #, secondary_text_color=c_gren
            else:
                if ozenkaa < 3:
                    item = ThreeLineListItem(text=predmet, secondary_text=f"[color=CC0000]{ozenka}[/color] | {text2}", tertiary_text=date,
                                             secondary_theme_text_color="Custom") #, secondary_text_color=c_red
                elif ozenkaa == 3:
                    item = ThreeLineListItem(text=predmet, secondary_text=f"[color=FF6600]{ozenka}[/color] | {text2}", tertiary_text=date,
                                             secondary_theme_text_color="Custom") #, secondary_text_color=c_orenge
                else:
                    item = ThreeLineListItem(text=predmet, secondary_text=f"[color=00CC00]{ozenka}[/color] | {text2}", tertiary_text=date,
                                             secondary_theme_text_color="Custom") #, secondary_text_color=c_gren

        except:
            if ozenka == 'imwork':
                item = ThreeLineListItem(text=predmet,secondary_text=f"{text2}",tertiary_text=date,secondary_theme_text_color="Custom")
            else:
                item = ThreeLineListItem(text='Error', secondary_text="Неверный формат оценки\nСвяжитесь с разработчиком", tertiary_text="None")

        return item

    def types(self):
        a = self.liste[2]
        for i in a:
            if i['type'] == 'mark':
                a, b, d, z = i['predmet'], i['typework'], i['value'], i['date']
                if type(d) == list:
                    self.grid.add_widget(self.boxocenka(a, None, f'{d[0]}/{d[1]}', f"{z[0:10]} | {b} "))
                elif self.data == True and (int(d[0:1]) < 3 or int(d[0:1]) == 3):
                    pass
                    #self.grid.add_widget(self.boxocenka(a, f"Сила: {e}", d, f"{z[0:10]} | {b} "))
                else:
                    pass
                    self.grid.add_widget(self.boxocenka(a, None, d, f"{z[0:10]} | {b} "))

            elif i['type'] == 'comment':
                a, b, d= i['predmet'], i['text'], i['autor']
                self.grid.add_widget(self.boxocenka(a, b, 'imwork',d))
            elif i['type'] == 'FinalMark':
                a, b, d, e, z = i['predmet'], i['typework'], i['value'], i['power'], i['date']
                self.grid.add_widget(self.boxocenka(a, None, d, f"{z[0:10]} | {b} "))

            elif i['type'] == 'imwork':
                a,b,c,d  = i['targetDate'],i['typework'],i['predmet'],i['url']
                self.grid.add_widget(self.boxocenka(c, b, 'imwork', a[0:10]))

    def build(self):
        values = []
        predmet = []
        try:
            for i in self.liste[4]:
                values.append(i['value'])
                predmet.append(i['predmet'])
            dial = dialog(valse=f'{predmet[0]} | Ср. балл: {values[0]}\n{predmet[1]} | Ср. балл: {values[1]}\n{predmet[2]} | Ср. балл: {values[2]}')
        except:
            dial = dialog(
                valse=f'Ничего | Ср. балл: Ничего\nНичего | Ср. балл: Ничего\nНичего | Ср. балл: Ничего')

        mainpage = MDBottomNavigationItem(name='screen 1', text='Main', icon='home')
        #mainpage =BoxLayout(orientation='vertical')
        #mainpage.md_bg_color = (255 / 255, 186 / 255, 3 / 255, 1)
        tools = MDTopAppBar(title="Последние оценки")
        #tools.right_action_items=[["dots-vertical", lambda x: dial.open()]]
        self.types()

        dathe = ScrollView()
        dathe.add_widget(self.grid)

        box = BoxLayout(orientation='vertical')
        box.add_widget(tools)
        box.add_widget(dathe)
        mainpage.add_widget(box)
        return mainpage