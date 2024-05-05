import numpy as np
import cv2
from mss import mss
from PIL import ImageGrab
import base64, threading, datetime,time,json
import requests
counter = 0

compression_level = 50
resolution_w = 1280
resolution_h = 720

def pollForNewData(stopFlag):
    while True:
        if stopFlag.is_set():
            break
        global compression_level, resolution_h,resolution_w
        try:
            url = "http://randomurl.pythonanywhere.com/getDisplaySettings"
            response = requests.post(url)
            settings = json.loads(response.json())["settings"]
            settings_dict = json.loads("{" + settings + "}")
            compression_level = settings_dict["compression"]["level"]
            resolution_w = settings_dict["res"]["w"]
            resolution_h = settings_dict["res"]["h"]
            print(f"New Resolution: {resolution_w}, {resolution_h}.  Compression level: {compression_level}")
        except Exception as e:
            compression_level = 50
            resolution_w = 1280
            resolution_h = 720            
        time.sleep(30)

def displayVideo(stop_flag):
    def videoFeed(stop_flag):
        sct = mss()
        sct.with_cursor = True
        while True:
            start_time = time.time()
            global counter, compression_level, resolution_w,resolution_h
            if counter > 999999999999999:
                counter = 0
            counter = counter + 1
            sct_img = sct.grab(sct.monitors[1])
            np_img = np.array(sct_img)
            resized_img = cv2.resize(np_img, (resolution_w, resolution_h))
            _, png = cv2.imencode('.jpeg', resized_img,[cv2.IMWRITE_JPEG_QUALITY, compression_level])
            im_b64 = base64.b64encode(png).decode("utf-8")
            url = "http://randomurl.pythonanywhere.com/sendVideoData"
            payload = {"image": im_b64, "pw": "⠀⠀⠀⠀⠀", "timestamp": counter}
            requests.post(url, json=payload)
            print(time.time()-start_time)
            if stop_flag.is_set():
                counter = 0
                break


    num_threads = 5

    threads = []
    
    checkingThread = threading.Thread(target=pollForNewData, args=(stop_flag,))
    checkingThread.start()
    threads.append(checkingThread)
    for _ in range(num_threads):
        thread = threading.Thread(target=videoFeed, args=(stop_flag,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()