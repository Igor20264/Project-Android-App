import json
import random
import logs
log = logs.Logs('Logic.py')

class Sessions_Lite:
    _proxy = ["http://141.101.123.24:80", "http://203.30.191.33:80"]
    _dist = {"http": _proxy[random.randint(0, 1)]}

    def __init__(self,internet=True):
        import requests
        self.internet = internet

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
