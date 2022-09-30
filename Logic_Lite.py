import json
import os
import random
import time
from kivy.logger import Logger
import pickle
from bs4 import BeautifulSoup

def profiler(func):
    def wrapper(*args, **kwargs):
        before = time.time()
        retval = func(*args, **kwargs)
        after = time.time()
        Logger.warn(f"Lite Function: {func.__name__}| {after-before}")
        return retval
    return wrapper

class Sessions_Lite:
    _proxy = ["http://141.101.123.24:80", "http://203.30.191.33:80"]
    _dist = {"http": _proxy[random.randint(0, 1)]}

    @profiler
    def __init__(self,internet=False):
        import requests
        self.internet = internet

        self.session = requests.Session()

        if self.internet:
            self.__login()
            self.__MainParse()
            self.__userparse()
        else:
            self.__MainParse()
            self.__userparse()

    @profiler
    def __login(self):
        """Вход без пароля"""
        if os.path.exists('files/somefile.cookies'):
            with open('files/somefile.cookies', 'rb') as f:
                self.session.cookies.update(pickle.load(f))
            aa = self.session.get(url='https://school.mosreg.ru/feed/',timeout=100)
            if aa.headers['Cache-Control'] != "private, s-maxage=0":
                Logger.error('Ошибка во время входа в шп по куки файлам')
            else:
                return None
        else:
            Logger.warn(f"Login: Отсутствует файл с куки")
        if os.path.exists('files/data_file.json'):
            with open('files/data_file.json') as f:
                self.session.post('https://uslugi.mosreg.ru/api/school/user/login', json.load(f), proxies=self._dist)
            return None
        else:
            Logger.error(f"Login: Отсутствует файл с данными")
            raise FileNotFoundError("Ошибка отсутствует файл с данными")

    @profiler
    def DzApi(self, date):
        apijson = self.session.get(
            f'https://school.mosreg.ru/api/feed/schedule/{self.personId}/{self.shoolsId}/{date}/').json()
        returns = []
        for i in apijson['response']['items']:
            lesson = i['subject']
            homework = i['homeworkText']
            kabinet = i['schedulePlace']
            timelesson = i['lessonTime']
            url = i['lessonUrl']
            returns.append([lesson, homework, kabinet, timelesson, url])
        return returns

    @profiler
    def __MainParse(self):
        if self.internet == False:
            with open("files/backup.dit", "r") as f:
                self.parsed = json.load(f)
        else:
            mainpage = self.session.get('https://school.mosreg.ru/feed')
            try:
                soup = BeautifulSoup(mainpage.text, 'lxml')
            except:
                Logger.warn(f"Parser_Lite: Установите lxml для более быстрой работы")
                soup = BeautifulSoup(mainpage.text, "html.parser")

            for i in soup.find_all('script'):
                if 'window.__SURVEY_FORM_INITIAL_STATE__' in i.text:
                    a = i.text.strip().splitlines()
                    asd = []
                    for ii in a:
                        if ii == "" or len(ii) < 300:
                            pass
                        else:
                            asd.append(ii.strip())
                    self.parsed = json.loads(asd[0][47:len(asd[0]) - 1].replace("'", '"'))

    def __userparse(self):
        b = self.parsed
        self.personId,self.shoolsId = b['analytics']["personId"],b['analytics']["schoolId"]