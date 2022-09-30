# -*- coding: utf-8 -*-
import json
import random
import time

import requests
from datetime import datetime
import locale
import os
from kivy.logger import Logger
from bs4 import BeautifulSoup

def profiler(func):
    def wrapper(*args, **kwargs):
        before = time.time()
        retval = func(*args, **kwargs)
        after = time.time()
        Logger.warn(f"Function: {func.__name__}| {after-before}")
        return retval
    return wrapper

locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)
@profiler
def getInternet():
    """вход с паролем"""
    try:
        a = requests.post('https://uslugi.mosreg.ru/api/school/user/login',timeout=100)
        if a.status_code == 405:
            return False
        else:
            return True
    except Exception as e:
        return False

class Sessions:
    _proxy = ["http://141.101.123.24:80", "http://203.30.191.33:80"]
    _dist = {"http": _proxy[random.randint(0, 1)]}

    def __init__(self, debug=False, internet=True):
        import requests

        self.debug = debug
        self.internet = internet

        # Создание сессии
        self.session = requests.Session()

        if self.internet:
            self.__login()
            self.__MainParse()
            self.__userparse()
        else:
            self.load_backup()
    @profiler
    def __login(self):
        """Вход без пароля"""
        import pickle

        if os.path.exists('files/somefile.cookies'):
            with open('files/somefile.cookies', 'rb') as f:
                self.session.cookies.update(pickle.load(f))
            aa = self.session.get(url='https://school.mosreg.ru/feed/')
            if aa.headers['Cache-Control'] != "private, s-maxage=0":
                Logger.error('Ошибка во время входа в шп по куки файлам')
            else:
                return None
        else:
            Logger.warn(f"Login: Отсутствует файл с куки")

        if os.path.exists('files/data_file.json'):
            with open('files/data_file.json') as f:
                self.session.post('https://uslugi.mosreg.ru/api/school/user/login', json.load(f),proxies=self._dist)
            self.__cookies()
            return None
        else:
            Logger.error(f"Login: Отсутствует файл с данными")
            raise FileNotFoundError("Ошибка отсутствует файл с данными")

    @profiler
    def __cookies(self):
        """получение куки файлов и сохранение"""
        import pickle
        with open('files/somefile.cookies', 'wb') as f:
            pickle.dump(self.session.cookies, f)
        return self.session.cookies

    @profiler
    def DzApi(self, date):
        api = self.session.get(f'https://school.mosreg.ru/api/feed/schedule/{self.personId}/{self.shoolsId}/{date}/')
        if api.status_code == 500:
            Logger.warn("Api 500")
        apijson = api.json()
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
    def __get_image(self):
        '''получение изображения'''
        image = self.session.get("https://static.school.mosreg.ru/images/avatars/user/a.s.jpg")
        with open('files/profil.jpg', 'wb') as f:
            f.write(image.content)

    @profiler
    def save_backup(self):
        with open("files/backup.dit", "w") as f:
            json.dump([self.parsed,self.parsed_user], f)

    @profiler
    def load_backup(self):
        with open("files/backup.dit", "r") as f:
            a = json.load(f)
            self.parsed = a[0]
            self.parsed_user = a[1]

    @profiler
    def __MainParse(self):
        mainpage = self.session.get('https://school.mosreg.ru/feed')
        try:
            soup = BeautifulSoup(mainpage.text, 'lxml')
        except:
            Logger.warn(f"Parser: Установите lxml для более быстрой работы")
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
                self.parsed_user = json.loads(asd[1][34:len(asd[1]) - 1].replace("'", '"'))
                self.save_backup()
                break
        if self.internet == False:
            with open("files/backup.dit", "r") as f,open('files/backups.dit', "r")as fa:
                self.parsed = json.load(f)
                self.parsed_user = json.load(fa)

    def feedparse(self):
        marks = []
        dates=[]
        def Mark():
            try:
                if len(b['content']['marks']) > 1:
                    value = [i['value'] for i in b['content']['marks']]
                else:
                    value = b['content']['marks'][0]['value']  # оценка

                typework = b['content']['work']['name']  # тип работы
                predmet = b['content']['subject']['name']  # предмет
                #power = b['content']['work']['workType']['value']  # сила влияния
                date = b['date']  # Дата
            except:
                pass


        for b in self.parsed['userMarks']['children'][0]['marks']:
            if len(b['marks']) > 1:
                value = [i['value'] for i in b['marks']]
            else:
                value = b['marks'][0]['value']

            predmet = b['subject']['name']
            hz = b['subject']['knowledgeArea']
            type = b['markType']
            typework = b['markTypeText']
            date = int(b['date'])

            date=datetime.fromtimestamp(date)
            date = date.strftime(f"%B")[:4] + " " + date.strftime('%d')
            marks.append(
                {'predmet': predmet, 'typework': typework, 'value': value, 'date': date})
            # Это всё подрят
            dates.append(
                {'type': 'mark', 'predmet': predmet, 'typework': typework, 'value': value,
                 'date': date})
        return [marks, None, dates]

    def __userparse(self):
        a = self.parsed_user
        b = self.parsed

        self.UserName = a['user']['name']  # имя
        self.shoolsId = a['user']["schoolIds"][0]
        self.sex = a['user']['sex']  # пол

        self.shoolsgroopid = b['userSchedule']['children'][0]['groupId']  # 1821894698216843712
        self.personId = b['userSchedule']['children'][0]['personId']
        self.personId,self.UserId,self.shoolsId,self.groupId = b['analytics']["personId"],b['analytics']["userId"],b['analytics']["schoolId"],b['analytics']["groupId"]
        self.lang = b['userContext']["userContextInfo"]["currentCultureCode"] # ru-RU
        self.Parante = b['userContext']["userContextInfo"]["isParent"]
        self.name = b['userContext']["userContextInfo"]["name"]
        self.sex = b['userContext']["userContextInfo"]["sex"]
        self.ClassTeacher = b['userContext']["currentContextPerson"]["classTeacherName"]

        self.shoolsName = b['userContext']["currentContextPerson"]["school"]['id'],b['userContext']["currentContextPerson"]["school"]['name']
        self.userParams = b['userContext']["currentContextPerson"]['group']['name'],b['userContext']["currentContextPerson"]['group']['parallel']

    @profiler
    def newsparse(self):
        "https://school.mosreg.ru/api/userfeed/posts"
        a = self.parsed
        news = []
        for i in range(len(a['news']['news'])):
            asd = a['news']['news'][i]['createdDate'].split('&nbsp;')

            date = asd[0] + " " + asd[1] + " " + asd[2]
            title, url, = a['news']['news'][i]['title'], a['news']['news'][i]['networkNewsUrl']
            news.append([title, date, url])