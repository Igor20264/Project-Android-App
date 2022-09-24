# -*- coding: utf-8 -*-
import os
from inspect import getframeinfo, stack


class Logs:
    def __init__(self,__name__):
        import time
        self.locate = __name__
        times = time.localtime()
        self.time = str(times[0]) + "_" + str(times[1]) + "_" + str(times[2]) + "-" + str(times[3]) + ";" + str(times[4])+ ";" + str(times[5])
        with open(f"log/{self.time}-{self.locate}.logs", 'w') as f:
            f.write(f"")
        self.Logschek()

    def add(self,text,type=0,priority=0):
        with open(f"log/{self.time}-{self.locate}.logs", 'a')as f:
            caller = getframeinfo(stack()[1][0])
            messeg = f"{text}-{type}-{caller.lineno}-{priority}\n"
            f.write(messeg)
        print(messeg,end="")

    def Logschek(self):
        for file in os.listdir('log'):
            if file == f"{self.time}-{self.locate}.logs":
                pass
            else:
                with open(f'log/{file}', 'r',encoding='latin-1') as f:
                    a = f.read()
                if a == '':
                    os.remove(f'log/{file}')