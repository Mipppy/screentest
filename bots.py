from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json, random, threading, string,time, requests, sys
from selenium.webdriver.common.alert import Alert
from faker.providers.person.en import Provider
firstnames = list(set(Provider.first_names))
def randomName():
    return random.choice(firstnames)
bots = []
kahootbotdata = None
blooketbotdata = None
gimkitbotdata = None
def kahootBot(driver : WebDriver, gameId):
    try:
        driver.execute_script(f'''window.open("https://kahoot.it/?pin={gameId}&refer_method=link","_blank");''')
        time.sleep(.25)
        driver.switch_to.window(window_name=driver.window_handles[-1])
        try:
            WebDriverWait(driver, 1.5).until(EC.url_contains("join"))
            gameUsernameElement = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "nickname")))
            gameUsernameClick = driver.find_element(By.CSS_SELECTOR, ".nickname-form__SubmitButton-sc-1mjq176-1")
            gameUsernameElement.send_keys(randomName())
            gameUsernameClick.click()
        except Exception as e:
            spinner = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button__Button-sc-c6mvr2-0")))
            spinner.click()
            element =WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".udycg")))
            element.click()
    except Exception as e:
        return None
def blooketBot(driver : WebDriver, gameId):
    try:
        driver.execute_script(f'''window.open("https://play.blooket.com/play?id={gameId}","_blank");''')
        time.sleep(.25)
        driver.switch_to.window(window_name=driver.window_handles[-1])
        try:
            WebDriverWait(driver, 2.5).until(EC.url_contains("register"))
            gameUsernameElement = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "._nameInput_1pk02_71")))
            gameUsernameClick = driver.find_element(By.CSS_SELECTOR, "._joinIcon_1pk02_114")
            gameUsernameElement.send_keys(randomName())
            gameUsernameClick.click()
        except Exception as e:
            None
    except Exception as e:
        return None
def gimkitBot(driver : WebDriver, gameId):
    try:
        driver.execute_script(f'''window.open("https://www.gimkit.com/join?gc={gameId}","_blank");''')
        time.sleep(.25)
        driver.switch_to.window(window_name=driver.window_handles[-1])
        try:
            gameUsernameElement = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "player-name-input")))
            gameUsernameClick = driver.find_element(By.ID, "join-game-button")
            gameUsernameElement.send_keys(randomName())
            gameUsernameClick.click()
        except Exception as e:
            None
    except Exception as e:
        return None
    
def createDrivers(num: int, timeout: int):
    drivers = []
    
    def createDriver():
        drivers.append(webdriver.Firefox())
        
    threads = [threading.Thread(target=createDriver) for _ in range(num)]
    
    for thr in threads:
        thr.start()
    
    # Very poor hack to avoid joining threads, as some would get stuck for some reason and loop the program indefintly.  Should program timeout system instead, but this works.
    time.sleep(10)

    return drivers


def closeDrivers(drivers : list):
    def closeDriver(driver : WebDriver):
        for window_handle in driver.window_handles:
            driver.switch_to.window(window_handle)
            try:
                driver.close()
                alert = Alert(driver)
                alert.accept()
            except Exception:
                None
        driver.quit()
    [threading.Thread(target=closeDriver, args=(driver,)).start() for driver in drivers]

def createBotsForThread(num, driver : WebDriver, id, botType):
    [getattr(sys.modules[__name__], botType + "Bot")(driver, id) for _ in range(int(num))] 
def createBots(num, id, sec, botType : str):
    NUM_OF_DRIVERS = round(int(num) /10) + 1 
    drivers = createDrivers(NUM_OF_DRIVERS, 10)
    bots_per_driver = int(num) // len(drivers)
    remaining_bots = int(num) % len(drivers)
    threads = [threading.Thread(target=createBotsForThread, args=(bots_per_driver + remaining_bots if i == 0 else bots_per_driver, drivers[i], id, botType)) for i in range(len(drivers))]
    [thr.start() for thr in threads]
    [thread.join() for thread in threads]
    time.sleep(int(sec))
    closeDrivers(drivers)

def botData(stop_flag, botType : str):
    try:
        while True:
            if stop_flag.is_set():
                break
            payload = {"pw": "⠀⠀⠀⠀⠀"}
            response = requests.post(f"http://randomurl.pythonanywhere.com/{botType}BotterJSON", json=payload)
            if response.status_code != 200:
                setattr(sys.modules[__name__], botType + "botdata", None)
            response_json = json.loads(response.json())
            if not 'id' in response_json or len(response_json['id']) == 0:
                setattr(sys.modules[__name__], botType + "botdata", None)
            else:
                payload2 = {"pw": "⠀⠀⠀⠀⠀"}
                requests.post(f"http://randomurl.pythonanywhere.com/clear{botType.capitalize()}Botter", json=payload2)
                setattr(sys.modules[__name__], botType + "botdata", response_json)
            time.sleep(3)
    except Exception:
        None    
def botter(stop_flag, botType : str):
    threading.Thread(target=botData, args=(stop_flag, botType)).start()
    while True:
        if stop_flag.is_set():
            break
        if getattr(sys.modules[__name__], botType + "botdata") is not None:
            copiedBotData = getattr(sys.modules[__name__], botType + "botdata")
            setattr(sys.modules[__name__], botType + "botdata", None)
            print(f"Botting {botType.capitalize()} game: {copiedBotData["id"]} with {copiedBotData["num"]} bots, lasting {copiedBotData["sec"]} seconds")
            createBots(copiedBotData["num"] ,copiedBotData["id"], copiedBotData["sec"], botType)