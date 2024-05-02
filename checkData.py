import requests

def updateData():
    try:
        url = "http://randomurl.pythonanywhere.com/managementData"
        payload = {"pw": "⠀⠀⠀⠀⠀"}
        response = requests.post(url, json=payload)

        # Check the response status code
        if response.status_code == 200:
            return response.json()
        else:
            print("Request failed with status code:", response.status_code)
            return None
    except Exception as e:
        return None