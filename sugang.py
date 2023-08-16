from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller
from webdriver_manager.core.driver_cache import DriverCacheManager
import pyautogui
from datetime import datetime
import time
import gui
from gui import resource_path
import sys
import os

driver = None
loggedIn = False

# def get_chromedriver():
#     global driver
#     # 현재 사용중인 크롬 버전에 맞는 드라이버 받아오기
#     chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0] 
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option('detach', True)
#     options.add_experimental_option("excludeSwitches", ["enable-logging"])

#     # 사용중인 크롬 버전에 맞는 드라이버 적용
#     try:
#         driver = webdriver.Chrome(executable_path = f'./{chrome_ver}/chromedriver', options = options)
#     except:
#         chromedriver_autoinstaller.install(True)
#         driver = webdriver.Chrome(executable_path = f'./{chrome_ver}/chromedriver', options = options)
    
#     driver.implicitly_wait(10)

def get_osName():
    return os.getenv('USERNAME')

def get_chrome_driver():
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0:4]
    str = ''.join(chrome_ver)
    return str

def get_chromedriver():
    global driver
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    cache_manager = DriverCacheManager(
        root_dir=resource_path("./")
    )
    service = Service(ChromeDriverManager(cache_manager = cache_manager).install())

    driver = webdriver.Chrome(service = service, options = options)

def make_list_to_apply(buttons:list, classes:list) -> list:
    buttons_apply = []
    buttons_applied = []
    classes_apply = []
    classes_applied = []
    for btn, cls in zip(buttons, classes):
        print(btn.text)
        time.sleep(1)
        if btn.text == "신청":
            buttons_apply.append(btn)
            classes_apply.append(cls)
        elif btn.text == "삭제":
            buttons_applied.append(btn)
            classes_applied.append(cls)
    
    buttons_to_apply = []
    classes_to_apply = []
    for btn, cls in zip(buttons_apply, classes_apply):
        if cls not in classes_applied:
            buttons_to_apply.append(btn)
            classes_to_apply.append(cls)
    print(f'신청할 강의 : {classes_to_apply}')
    print(f'신청된 강의 : {classes_applied}')
    return buttons_to_apply, classes_to_apply

def check_isSugangtime():
    global loggedIn
    global driver
    start_time = driver.find_element(By.XPATH, '//*[@id="aside"]/div[3]/div[2]/strong').text
    end_time = driver.find_element(By.XPATH, '//*[@id="aside"]/div[3]/div[3]/strong').text
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    if time_now < start_time or time_now > end_time:
        gui.warning_not_sugang_time()
        driver.close()
        driver = None
        loggedIn = False

def main():
    global loggedIn
    global isMainGUIRunning
    while True:
        while not loggedIn:
            gui.login_gui()
            if gui.program_end:
                sys.exit(0)
            id = gui.ID
            pw = gui.PW

            if not driver:
                get_chromedriver()
            else:
                pass
            driver.get("https://sugang.kangwon.ac.kr/")
            
            driver.find_element(By.ID, "USER_ID").send_keys(id)
            driver.find_element(By.ID, "PWD").send_keys(pw)
            driver.find_element(By.ID, "button_login").click()
            driver.implicitly_wait(10)
            try:
                WebDriverWait(driver, 0.5).until(EC.alert_is_present(), "Login Failed")
                alert = driver.switch_to.alert
                if alert:
                    print(alert.text)
                    print("Wrong ID or PW!")
                    alert.accept()
                    driver.close()
            except:
                loggedIn = True
                pass

        check_isSugangtime()
        if loggedIn:
            break

    driver.find_element(By.XPATH, '//*[@id="topMnu"]/li[2]/a').click()
    driver.implicitly_wait(100)

    for i in range(100):
        buttons = driver.find_elements(By.CSS_SELECTOR, ".btn_appli")
        classes = [cls.text for cls in driver.find_elements(By.CSS_SELECTOR, ".left_txt.bold")]
        
        buttons_to_apply, classes_to_apply = make_list_to_apply(buttons, classes)
        print(f'신청해야 할 강의 : {classes_to_apply}')
        if classes_to_apply:
            for btn, cls in zip(buttons_to_apply, classes_to_apply):
                btn.click()
                time.sleep(0.05)
                pyautogui.press('enter')
                print(f'{cls} 신청 완료. 신청이 정상적으로 되었는지 확인해 보세요.')
                time.sleep(0.1)
        else:
            print(f"신청이 전부 완료된 것 같습니다. 직접 확인해 보세요!")
            sys.exit(0)
    print(f"부정 수강신청 감지 방지를 위해 100회 시도 후 프로그램이 종료됩니다..")

if __name__ == '__main__':
    main()