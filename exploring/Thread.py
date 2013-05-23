import threading
import time

class UpdatePriceMonitor(threading.Thread):
    def __init__(self, name = ''):
        threading.Thread.__init__(self)
        self.name = name
        self.Terminated = False
    def run(self):
        i = 0
        while not self.Terminated:
            #code
            time.sleep(2)
    def stop(self):
        self.Terminated = True



a = UpdatePriceMonitor('Thread A')
b = UpdatePriceMonitor('Thread B')
c = UpdatePriceMonitor('Thread C')

a.start()
time.sleep(6.5)
a._Thread__stop()
