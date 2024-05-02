import numpy as np
import cv2
from mss import mss
from PIL import Image,ImageGrab
import requests

# def videoFeed(stop_flag):
#     width_pil, height_pil = ImageGrab.grab().size
#     bounding_box = {'top': 0, 'left': 0, 'width': width_pil, 'height': height_pil}

#     sct = mss()

#     while True:
#         # if stop_flag.is_set():
#         #     break
#         sct_img = sct.grab(bounding_box)
#         img_array = np.array(sct_img)

#     # Serialize the NumPy array to bytes
#         image_bytes = img_array.tobytes()

#     # Send the image data to the server
#         url = "http://randomurl.pythonanywhere.com/sendVideoData"
#         payload = {"pw": "⠀⠀⠀⠀⠀", "feed":image_bytes}
#         response = requests.post(url, json=payload)


#         # cv2.imshow('screen', np.array(sct_img))

#         # if (cv2.waitKey(1) & 0xFF) == ord('q'):
#         #     cv2.destroyAllWindows()
#         #     break

# videoFeed("d")
def videoFeed(stop_flag):
    width_pil, height_pil = ImageGrab.grab().size
    bounding_box = {'top': 0, 'left': 0, 'width': width_pil, 'height': height_pil}

    sct = mss()

    while True:
        sct_img = sct.grab(bounding_box)
        img_array = np.array(sct_img)

        # Serialize the NumPy array to bytes
        image_bytes = img_array.tobytes()

        # Send the image data to the server
        url = "http://randomurl.pythonanywhere.com/sendVideoData"
        response = requests.post(url, data=image_bytes, json={"pw": "⠀⠀⠀⠀⠀"})

        # Check response status
        if response.status_code == 200:
            print("Image sent successfully")
        else:
            print("Failed to send image")

        # Add a break condition if necessary
        # if stop_flag.is_set():
        #     break

# Call the function with a dummy stop_flag
videoFeed("dummy_stop_flag")