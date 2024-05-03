from checkData import updateData
from schooltool import schooltoolLocker
from arraydata import displayVideo
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
displayThread = None
displayStopFlag = threading.Event()
while True:
    if currentTasks is not None:
        try:
            if currentTasks["schooltoolLocker"] == 0:
                if schooltoolThread is None or not schooltoolThread.is_alive():
                    print("Starting Locker")
                    schooltoolThread = StoppableThread(target=schooltoolLocker, args=(schoolToolStopFlag,))
                    schooltoolThread.start()
        except Exception as e:
            if schooltoolThread is not None:
                print("Ending Locker")
                schoolToolStopFlag.set()
                schooltoolThread.join()
                schoolToolStopFlag.clear()
                schooltoolThread = None
        
        try:
            if currentTasks["displayVideo"] == 0:
                if displayThread is None or not displayThread.is_alive():
                    print("Starting Video")
                    displayThread = StoppableThread(target=displayVideo, args=(displayStopFlag,))
                    displayThread.start()
        except Exception as e:
            if displayThread is not None:
                print("Ending Video")
                displayStopFlag.set()
                displayThread.join()
                displayStopFlag.clear()
                displayThread = None
                