from checkData import updateData
from schooltool import schooltoolLocker
from stoppableThread import StoppableThread
import threading,time,random,json, multiprocessing
from queue import Queue

currentTasks = None

def checkForNewData():
    while True:
        global currentTasks
        currentTasks = json.loads(updateData())
        time.sleep(25)

thread = threading.Thread(target=checkForNewData)
thread.daemon = True
thread.start()

schooltoolThread = None
schoolToolStopFlag = threading.Event()
while True:
    if currentTasks is not None:
        try:
            if currentTasks["schooltoolLocker"] == 0:
                if schooltoolThread is None or not schooltoolThread.is_alive():
                    schooltoolThread = StoppableThread(target=schooltoolLocker, args=(schoolToolStopFlag,))
                    schooltoolThread.start()
        except Exception as e:
            if schooltoolThread is not None:
                schoolToolStopFlag.set()
                schooltoolThread.join()
                schoolToolStopFlag.clear()
                schooltoolThread = None