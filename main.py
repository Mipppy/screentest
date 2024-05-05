from checkData import updateData
from schooltool import schooltoolLocker
from arraydata import displayVideo
from kahootbotter import kahootBotter
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

chart = {
    "schooltoolLocker" : {
        "func" : schooltoolLocker,
        "thread" : None,
        "stopflag" : threading.Event()
    },
    "displayVideo" : {
        "func" : displayVideo,
        "thread" : None,
        "stopflag" : threading.Event()
    },
    "kahootBotter" : {
        "func" : kahootBotter,
        "thread" : None,
        "stopflag" : threading.Event()
    }
}

while True:
    if currentTasks is not None:
        try:
            for task in currentTasks:
                for key, item in chart.items():
                    if key == task:
                        if item["thread"] is None or not item["thread"].is_alive():
                            print(f"Starting {item['func'].__name__}")
                            item["thread"] = StoppableThread(target=item["func"], args=(item["stopflag"],))
                            item["thread"].start()
            for key, item in chart.items():
                if key not in currentTasks and item["thread"] is not None:
                    print(f"Ending {item['func'].__name__}")
                    item["stopflag"].set()
                    item["thread"].join()
                    item["stopflag"].clear()
                    item["thread"] = None
        except Exception:
            None

# while True:
#     if currentTasks is not None:
#         try:
#             if currentTasks["schooltoolLocker"] == 0:
#                 if schooltoolThread is None or not schooltoolThread.is_alive():
#                     print("Starting Locker")
#                     schooltoolThread = StoppableThread(target=schooltoolLocker, args=(schoolToolStopFlag,))
#                     schooltoolThread.start()
#         except Exception as e:
#             if schooltoolThread is not None:
#                 print("Ending Locker")
#                 schoolToolStopFlag.set()
#                 schooltoolThread.join()
#                 schoolToolStopFlag.clear()
#                 schooltoolThread = None
        
#         try:
#             if currentTasks["displayVideo"] == 0:
#                 if displayThread is None or not displayThread.is_alive():
#                     print("Starting Video")
#                     displayThread = StoppableThread(target=displayVideo, args=(displayStopFlag,))
#                     displayThread.start()
#         except Exception as e:
#             if displayThread is not None:
#                 print("Ending Video")
#                 displayStopFlag.set()
#                 displayThread.join()
#                 displayStopFlag.clear()
#                 displayThread = None
        
#         try:
#             if currentTasks["kahootBotter"] == 0:
#                 if kahootBotThread is None or not kahootBotThread.is_alive():
#                     print("Starting Kahoot Botter")
#                     kahootBotThread = StoppableThread(target=overallKahootBotter, args=(kahootBotStopFlag,))
#                     kahootBotThread.start()
#         except Exception as e:
#             if kahootBotThread is not None:
#                 print("Ending Kahoot Botter")
#                 kahootBotStopFlag.set()
#                 kahootBotThread.join()
#                 kahootBotStopFlag.clear()
#                 kahootBotThread = None