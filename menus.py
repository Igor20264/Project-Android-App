# -*- coding: utf-8 -*-
from kivymd.uix.bottomnavigation import MDBottomNavigation

from menu.homepage.homepage import homepage
from menu.mainpage import mainapge

from core import settigs
loads = settigs()
data = loads.load()

class menu:
    def build(self,session):
        homepa= homepage(session)
        mainapa = mainapge.mainpage(session, data)
        mbbottonnav = MDBottomNavigation()

        mbbottonnav.add_widget(mainapa.build())
        mbbottonnav.add_widget(homepa.build())

        return mbbottonnav