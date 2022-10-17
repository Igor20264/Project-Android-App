# -*- coding: utf-8 -*-
import os
import threading

from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.uix.label import MDLabel

Window.size = (414, 728) # Размер окна
Window.clearcolor = (255/255,186/255,3/255,1) # Цвет окна
Window.title = "Школьный дневник" # Название окна

from Logic import Sessions

file = None

class MainApp(MDApp):
    def __init__(self):
        super().__init__()
        self.box = BoxLayout(orientation='vertical')
        self.sess = Sessions()
        self.potok = threading.Thread(target=self.sess.auth)
        self.potok.start()

    def create(self):
        self.SM = ScreenManager()  # Создание менеджера окон
        self.download = Screen(name='down')  # заглушка
        self.screen = Screen(name='auth')  # Создание окна авторизации
        self.screen1 = Screen(name='data')  # Создание окна с данными
        self.SM.add_widget(self.screen)  # Добавление созданного окна под управление менеджера
        self.SM.add_widget(self.screen1)  # тоже самое
        self.SM.add_widget(self.download)

        box = BoxLayout()
        my_label = MDLabel(text='hello', halign="center", )
        box.add_widget(my_label)
        self.download.add_widget(box)
        self.box.add_widget(self.SM)  # Добовлям в главный экрна менеджер окон
        self.SM.current = 'down'
        self.post()

    def build(self):
        self.create()
        return self.box # Выводим на экран полученный интерфейс

    def post(self):
        if os.path.exists('files/data_file.json') == False: # Если нету файла с данными пользователя то выводим окно авторизации
            from menu.Auth.auth import auth
            auth = auth(self.SM) # Вызов функции для создания эскиза полей и кнопок с передачей Менеджера окно
            self.SM.current = 'auth'
            self.screen.add_widget(auth.build()) # Добавление на экран, собранный эскиз для отабражения кнопок и полей

        else: # если файл существует
            self.SM.current = 'data' # Переключаем октивное окно
            import menus
            #self.sess = Sessions(internet=False) # Вызываем класс для работы со школьным порталом
            men = menus.menu() #Вызываем функцию для создания эскизов
            #self.potok.join()
            self.screen1.add_widget(men.build(self.sess)) # Добавлям собранные эскизы на экран.