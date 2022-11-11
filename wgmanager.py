import wglive
import wgsche2
from threading import Thread
from time import sleep


class WgManager():
    managerThread = None
    Scheduler : wgsche2.WgScheduler = None
    timeInterval = 200 # seconds
    isworking = True

    def __del__(self):
        print("Del")
        pass

    def wgsche(self):
        while(self.isworking):
            for i in range(int(self.timeInterval/5)):
                if(self.isworking):
                    sleep(5)
                else:
                    break
            if(self.isworking):
                self.Scheduler.wgSche2()

    def kill(self):
        self.isworking = False
        self.Scheduler.ForceCloseAllClient()
        if(self.managerThread):
            self.managerThread.join()

    def __init__(self) -> None:
        print("Init")
        self.Scheduler = wgsche2.WgScheduler()
        self.managerThread = Thread(target=self.wgsche)
        self.managerThread.start()

    pass

wgmanager : WgManager = None