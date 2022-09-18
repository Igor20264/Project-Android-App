# -*- coding: utf-8 -*-
import json
import random
import logs
import requests

def getInternet():
    """вход с паролем"""
    import os
    try:
        a = requests.post('https://uslugi.mosreg.ru/api/school/user/login',timeout=100)
        if a.status_code == 405:
            return False
        else:
            return True
    except Exception as e:
        return False

log = logs.Logs('Logic.py')

class Sessions_Lite:
    _proxy = ["http://141.101.123.24:80", "http://203.30.191.33:80"]
    _dist = {"http": _proxy[random.randint(0, 1)]}

    def __init__(self,internet=True):
        import requests

        if internet:self.internet = True
        else:self.internet = False

        self.session = requests.Session()

        try:
            if self.internet:self.__login_with_pass()
        except:
            try:
                self.__MainParse()
                self.__userparse()
            except:exit()
        else:
            self.__MainParse()
            self.__userparse()

    def __login_with_pass(self):
        """Вход без пароля"""
        try:
            import pickle
            with open('files/somefile.cookies', 'rb') as f:
                self.session.cookies.update(pickle.load(f))
                aa = self.session.get(url='https://school.mosreg.ru/feed/')
            if aa.headers['Cache-Control'] != "private, s-maxage=0":
                raise Exception('Ошибка во время входа в шп по куки файлам')
        except:
            import os
            try:
                if os.path.exists('files/data_file.json'): # Получаем даныне пользователя
                    with open('files/data_file.json') as f:
                        self.session.post('https://uslugi.mosreg.ru/api/school/user/login', json.load(f),
                                          proxies=self._dist) #Отправляем запрос для авторизации.
                        # Ответ приходит в виде куки (печеньки с англ.)
                else:
                    log.add("Ошибка отсутствует файл с поролем", "Internet", "Exception")
                    exit()
            except Exception as e:
                log.add(e, "Internet", "Exception")

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

    def __MainParseMini(self, quotes):
        a = quotes.text.strip().splitlines()
        asd = []
        for i in a:
            if i == "" or len(i)<300:
                pass
            else:
                asd.append(i.strip())
        string = asd[0][47:len(asd[0])-1]
        self.parsed = json.loads(string.replace("'", '"'))

    def __MainParse(self):
        try:
            from bs4 import BeautifulSoup
            mainpage = self.session.get('https://school.mosreg.ru/feed')
            soup = BeautifulSoup(mainpage.text, 'lxml')

            quotes = soup.find_all('script')
            self.__MainParseMini(quotes[27])
        except:
            try:
                with open("files/backup.dit", "r") as f:
                    self.parsed = json.load(f)
            except:
                exit()
        return self.parsed

    def __userparse(self):
        b = self.parsed
        self.personId,self.shoolsId = b['analytics']["personId"],b['analytics']["schoolId"]


class Sessions:
    _proxy = ["http://141.101.123.24:80", "http://203.30.191.33:80"]
    _dist = {"http": _proxy[random.randint(0, 1)]}

    def __init__(self, debug=False,internet=True):
        import os
        import requests

        # Проверка на отладку
        if debug:self.debug = True
        else:self.debug = False

        if internet:self.internet = True
        else:self.internet = False

        # Создание сессии
        self.session = requests.Session()

        try:
            if self.internet:
                if not debug:
                    try:
                        self.__login_with_pass()
                    except:
                        self.__login()
                    if not os.path.exists('files/profil.jpg'):
                        self.__get_image()
        except:
            try:
                log.add("No connect to server", "Internet", "Exception")
                self.__MainParse()
                self.__userparse()
            except Exception as e:
                log.add(f"Ошибка в коде:\n{e}", "Not exist", "Normal important")
                exit()
        else:
            self.__MainParse()
            self.__userparse()

    def __login_with_pass(self):
        """Вход без пароля"""
        import pickle
        try:
            with open('files/somefile.cookies', 'rb') as f:
                self.session.cookies.update(pickle.load(f))
                aa = self.session.get(url='https://school.mosreg.ru/feed/')
            if aa.headers['Cache-Control'] != "private, s-maxage=0":
                raise Exception('Ошибка во время входа в шп по куки файлам')
        except Exception as e:
            log.add(e, "Internet", "Non")
            raise Exception('Ошибка во время входа в шп по куки файлам')

    def __login(self):
        """вход с паролем"""
        import os
        try:
            if os.path.exists('files/data_file.json'):
                with open('files/data_file.json') as f:
                    self.session.post('https://uslugi.mosreg.ru/api/school/user/login', json.load(f),
                                      proxies=self._dist)
                self.__cookies()
            else:
                log.add("Ошибка отсутствует файл с поролем", "Internet", "Exception")
        except Exception as e:
            log.add(e, "Internet", "Exception")

    def __cookies(self):
        """получение куки файлов и сохранение"""
        import pickle
        with open('files/somefile.cookies', 'wb') as f:
            pickle.dump(self.session.cookies, f)
        return self.session.cookies

    #Работает.
    def DzApi(self, date):
        """получение дз\n
        date=2022-02-11
        """
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

    def __get_image(self):
        '''получение изображения'''
        image = self.session.get("https://static.school.mosreg.ru/images/avatars/user/a.s.jpg")
        with open('files/profil.jpg', 'wb') as f:
            f.write(image.content)

    def __MainParseMini(self, quotes):
        a = quotes.text.strip().splitlines()

        asd = []
        for i in a:
            if i == "" or len(i)<300:
                pass
            else:
                asd.append(i.strip())
        string_user = asd[1][34:len(asd[1])-1]
        string = asd[0][47:len(asd[0])-1]
        self.parsed = json.loads(string.replace("'", '"'))
        self.parsed_user = json.loads(string_user.replace("'", '"'))
        with open("files/backup.dit", "w") as f:
            json.dump(self.parsed, f)

    def __MainParse(self):
        try:
            if self.debug:
                with open("files/backup.dit", "r") as f:
                    self.parsed = a = json.load(f)
                log.add("Загружен с бекапа оценок", "Not exist", "except")
                return a

            from bs4 import BeautifulSoup
            #mainpage = self.session.get('https://school.mosreg.ru/feed')
            with open("hasd.html",'r')as f:
                mainpage = f.read()
            #soup = BeautifulSoup(mainpage.text, 'lxml')
            soup = BeautifulSoup(mainpage, 'lxml')
            quotes = soup.find_all('script')
            self.__MainParseMini(quotes[27])

        except Exception as e:
            try:
                log.add(e,'Warning','Zero')
                with open("files/backup.dit", "r") as f:
                    self.parsed = a = json.load(f)
                log.add("Загружен с бекапа оценок", "Not exist", "Normal important")
            except Exception as e:
                log.add(e, "Not exist", "Normal important")
                exit()
            return a
        return self.parsed

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
            date = b['date']
            marks.append(
                {'predmet': predmet, 'typework': typework, 'value': value, 'date': date})
            # Это всё подрят
            dates.append(
                {'type': 'mark', 'predmet': predmet, 'typework': typework, 'value': value,
                 'date': date})
        return [marks, None, dates]

    def __feedparse_old(self):
        marks = []  # оценки
        kent = []  # контрольные
        dates = []  # всё подрят

        WeekSummary = 0
        ImportantWork = 0

        _dict = {'type': None, 'order': None, 'id': None, 'date': None, 'content': None, 'mobileAdvSettings': None}

        def Mark():
            try:
                if len(b['content']['marks']) > 1:
                    value = [i['value'] for i in b['content']['marks']]
                else:
                    value = b['content']['marks'][0]['value']  # оценка

                typework = b['content']['work']['name']  # тип работы
                predmet = b['content']['subject']['name']  # предмет
                power = b['content']['work']['workType']['value']  # сила влияния
                date = b['date']  # Дата

            except Exception as e:
                text = b['content']['comment']['text']
                author = b['content']['comment']['author']
                predmet = b['content']['subject']['name']
                dates.append({'type': 'comment','predmet': predmet,'text':text,'autor':author})
            else:
                # Это для запроса оценок
                marks.append(
                    {'predmet': predmet, 'typework': typework, 'value': value, 'power': power, 'date': date})
                # Это всё подрят
                dates.append(
                    {'type': 'mark', 'predmet': predmet, 'typework': typework, 'value': value, 'power': power,
                     'date': date})

        def ImortantWork():
            obj = b['content']['works']
            for item in obj:
                targetDate = item['targetDate']  # когда
                typework = item['name']  # тип работы
                predmet = item['subject']  # предмет
                url = item['url']
                # Ближайшие кр
                kent.append({'targetDate': targetDate, 'typework': typework, 'predmet': predmet, 'url': url})
                # Это всё подрят
                dates.append(
                    {'type': 'imwork', 'targetDate': targetDate,'typework': typework, 'predmet': predmet, 'url': url})

        def WeekSum():
            effcit = []  # оценки за неделю
            effecit = []  # оценки за неделю ТО что надо исправить
            for item in b['content']['averageSubjects']:
                predmet = item['subjectName']
                # Оценки полученные за неделю (прошедшию) print(item['marks'])
                try:
                    for ite in item['averageMarks']:
                        try:
                            value = ite['value']
                            trend = ite['trend']
                        except:
                            log.add(f'Оценка отсутствует', 'weekly ass', 'No influence')
                            value = None
                            trend = None
                        effcit.append({'predmet': predmet, 'value': value, 'trend': trend})
                except:
                    log.add(f'Ошибка обработки', 'weekly ass', 'No influence')
            try:
                for item in b['content']['badSubjects']:
                    predmet = item['subjectName']
                    value = item['average']['value']
                    effecit.append({'predmet': predmet, 'value': value})
            except:
                log.add(f'Ошибка обработки', 'weekly ass', 'No influence')
                effecit = [{'predmet': "Молодец", 'value': "Так держать"},
                           {'predmet': "Молодец", 'value': "Так держать"},
                           {'predmet': "Молодец", 'value': "Так держать"}]
            # Это всё подрят
            dates.append({'type': 'weksum', 'normal': effcit, 'critical': effecit})
            return effecit,effcit
        #print(self.parsed['userMarks']['children'][0]['marks'].keys())
        for b in self.parsed['userMarks']['children'][0]['marks']:
            if b.keys() == _dict.keys() and(not b['type'] == 'ManyHomeworks' and not b['type'] == 'FeedFinished'):
                if b['type'] == "Mark":  # оценка
                    Mark()

                elif b['type'] == 'ImportantWork' and ImportantWork < 1:  # ближайшие контрольные - проверочные
                    ImportantWork += 1
                    ImortantWork()

                elif b['type'] == 'WeekSummary' and WeekSummary < 1:
                    WeekSummary += 1
                    effecit, effcit = WeekSum()

                elif b['type'] == 'FinalMark':
                    date = b['date']
                    value = b["content"]["marks"][0]['value']
                    predmet = b["content"]["subject"]['name']
                    type = b["content"]['work']['name']

                    # Это всё подрят
                    dates.append(
                        {'type': 'FinalMark', 'predmet': predmet, 'typework': type, 'value': value, 'power': None,
                         'date': date})

                else:
                    if b['type'] == "WeekSummary" or b['type'] == "ImportantWork" or b['type'] == 'FinalMark':
                        pass
                    else:
                        log.add(f'Новый тип | {b["type"]}|', 'New type', 'Very important')

            else:
                pass
                #print("Ошибка",b)
        return [marks, kent, dates, effcit, effecit]

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

    def newsparse(self):
        "https://school.mosreg.ru/api/userfeed/posts"
        a = self.parsed
        news = []
        for i in range(len(a['news']['news'])):
            asd = a['news']['news'][i]['createdDate'].split('&nbsp;')

            date = asd[0] + " " + asd[1] + " " + asd[2]
            title, url, = a['news']['news'][i]['title'], a['news']['news'][i]['networkNewsUrl']
            news.append([title, date, url])