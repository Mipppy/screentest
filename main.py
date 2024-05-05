from checkData import updateData
from schooltool import schooltoolLocker
from arraydata import displayVideo
from bots import botter
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
        "stopflag" : threading.Event(),
        "args" : None
    },
    "displayVideo" : {
        "func" : displayVideo,
        "thread" : None,
        "stopflag" : threading.Event(),
        "args" : None
    },
    "kahootBotter" : {
        "func" : botter,
        "thread" : None,
        "stopflag" : threading.Event(),
        "args" : "kahoot"
    },
    "blooketBotter" : {
        "func" : botter,
        "thread" : None,
        "stopflag" : threading.Event(),
        "args" : "blooket"
    },
    "gimkitBotter" : {
        "func" : botter,
        "thread" : None,
        "stopflag" : threading.Event(),
        "args" : "gimkit"
    }
}

while True:
    if currentTasks is not None:
        try:
            for task in currentTasks:
                for key, item in chart.items():
                    if key == task:
                        if item["thread"] is None or not item["thread"].is_alive():
                            print(f"Starting {item['func'].__name__}('{item['args']}')")
                            item["thread"] = StoppableThread(target=item["func"], args=(item["stopflag"], item["args"]))
                            item["thread"].start()
            for key, item in chart.items():
                if key not in currentTasks and item["thread"] is not None:
                    print(f"Ending {item['func'].__name__}('{item['args']}')")
                    item["stopflag"].set()
                    item["thread"].join()
                    item["stopflag"].clear()
                    item["thread"] = None
        except Exception:
            None