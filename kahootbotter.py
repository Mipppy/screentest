from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json, random, threading, string,time, requests
from selenium.webdriver.common.alert import Alert
bots = []
botdata = None

def botData(stop_flag):
    global botdata
    while True:
        if stop_flag.is_set():
            break
        url = "http://randomurl.pythonanywhere.com/kahootBotterJSON"
        payload = {"pw": "⠀⠀⠀⠀⠀"}
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            botdata = None
        response_json = json.loads(response.json())
        if not 'id' in response_json or len(response_json['id']) == 0:
            botdata = None
        else:
            payload2 = {"pw": "⠀⠀⠀⠀⠀"}
            requests.post("http://randomurl.pythonanywhere.com/clearKahootBotter", json=payload2)
            botdata = response_json
        time.sleep(4)
    
def kahootBot(driver : WebDriver, gameId):
    try:
        driver.execute_script(f'''window.open("https://kahoot.it/?pin={gameId}&refer_method=link","_blank");''')
        time.sleep(.75)
        driver.switch_to.window(window_name=driver.window_handles[-1])
        try:
            WebDriverWait(driver, .45).until(EC.url_contains("join"))
            gameUsernameElement = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "nickname")))
            gameUsernameClick = driver.find_element(By.CSS_SELECTOR, ".nickname-form__SubmitButton-sc-1mjq176-1")
            gameUsernameElement.send_keys(''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(4,8))))
            gameUsernameClick.click()
        except Exception:
            spinner = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button__Button-sc-c6mvr2-0")))
            spinner.click()
            element =WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".udycg")))
            element.click()
    except Exception as e:
        return None


def createKahootBots(num, gameId, timeToExist):
    driver = webdriver.Firefox()
    [kahootBot(driver, gameId) for _ in range(int(num))]
    time.sleep(int(timeToExist))
    for window_handle in driver.window_handles:
        driver.switch_to.window(window_handle)
        try:
            driver.close()
            alert = Alert(driver)
            alert.accept()
        except Exception:
            # This exists to handle some funny selenium jank
            None
    driver.quit()
    
def kahootBotter(stop_flag):
    botDataThread = threading.Thread(target=botData, args=(stop_flag,))
    botDataThread.start()
    global botdata
    while True:
        if stop_flag.is_set():
            break
        if botdata is not None:
            copiedBotData = botdata
            botdata = None
            print(f"Botting Kahoot game: {copiedBotData["id"]} with {copiedBotData["num"]} bots, lasting {copiedBotData["sec"]} seconds")
            createKahootBots(copiedBotData["num"] ,copiedBotData["id"], copiedBotData["sec"])