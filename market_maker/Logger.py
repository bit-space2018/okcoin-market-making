"""
@author: bit-space
@email: yi.huang@bit-space.net
@created: 2018/9/6 16:57
"""

import os
import datetime
import queue
import threading

import settings

class Logger:

    def __init__(self):
        self.que = queue.Queue()
        os.makedirs('./Logs', exist_ok=True)
        self.logfile = settings.LOGS_PATH + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.txt'
        self.warningfile = './Logs/Warnings.txt'
        with open(self.warningfile, 'w') as file: pass
        self.working = None
        self.que_thread = None


    def start(self):
        self(0b011, 'Starting Logger')
        self.working = True
        self.que_thread = threading.Thread(target=self.start_queue)
        self.que_thread.start()
        self(0b011, 'Started Logger')


    def stop(self):
        self(0b011, 'Stopping Logger')
        self.working = False
        self(0b011, 'Stopped Logger')
        self.que_thread.join()


    def __call__(self, dest, *args, sep=' ', end='\n'):
        # dest: binary lower to higher: screen, logfile, warningfile
        time = datetime.datetime.now()
        thread_id = threading.current_thread().ident
        content = sep.join([str(arg) for arg in args]) + end
        self.que.put((dest, time, thread_id, content))


    def start_queue(self):
        while True:
            if not self.working and self.que.empty(): break
            dest, time, thread_id, content = self.que.get()
            logstring = '[{}]({:5d}) {}'.format(time, thread_id, content)
            if dest & 0b100:
                with open(self.warningfile, 'a') as file:
                    file.write(logstring)
            if dest & 0b010:
                with open(self.logfile, 'a') as file:
                    file.write(logstring)
            if dest & 0b001:
                print(logstring, end='')




if __name__ == '__main__':

    logger = Logger()
    logger.start()

    logger(1, 'Only to screen', 1)
    logger(2, 'Only to logfile', 1, 2)
    logger(4, 'Only to warningfile', 1, 2, 3)
    logger(3, 'To screen and logfile', 1, 2, 3, 4)
    logger(6, 'To logfile and warningfile', 1, 2, 3, 4, 5)
    logger(7, 'To ALL', 1, 2, 3, 4, 5, 6)

    def example(logger):
        logger(7, 'In example')
    t = threading.Thread(target=example, args=(logger,))
    t.start()
    t.join()

    logger.stop()

