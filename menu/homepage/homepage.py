# -*- coding: utf-8 -*-

from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from menu.homepage.calendare import caledare

setting=False
data = False
class homepage:
    def __init__(self,session):
        self.workpage = MDBottomNavigationItem(name='screen 2', text="HomeWork", icon='text-box')
        self.session = session
    def build(self):
        #self.workpage.md_bg_color = (255 / 255, 186 / 255, 3 / 255, 1)
        a = caledare()
        a.sess = self.session
        a.__int__()
        self.workpage.add_widget(
            a
        )
        return self.workpage
