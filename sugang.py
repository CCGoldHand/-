from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
import pyautogui
import time
import sys

def get_ID_PW() -> str:
    id = input("ID : ")
    pw = input("PW : ")
    return id, pw

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

def main():
    ID, PW = get_ID_PW()

    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options = options)
    driver.get("https://sugang.kangwon.ac.kr/")
    
    driver.find_element(By.ID, "USER_ID").send_keys(ID)
    driver.find_element(By.ID, "PWD").send_keys(PW)
    driver.find_element(By.ID, "button_login").click()
    driver.implicitly_wait(10)
    try:
        alert = WebDriverWait(driver, 2).until(EC.alert_is_present(), "Login Failed")
        print("Wrong ID or PW!")
        sys.exit()
    except:
        pass

    driver.find_element(By.XPATH, '//*[@id="topMnu"]/li[2]/a').click()
    driver.implicitly_wait(100)

    while True:
        buttons = driver.find_elements(By.CSS_SELECTOR, ".btn_appli")
        classes = [cls.text for cls in driver.find_elements(By.CSS_SELECTOR, ".left_txt.bold")]
        
        buttons_to_apply, classes_to_apply = make_list_to_apply(buttons, classes)
        print(f'신청해야 할 강의 : {classes_to_apply}')
        if classes_to_apply:
            for btn, cls in zip(buttons_to_apply, classes_to_apply):
                btn.click()
                time.sleep(0.5)
                pyautogui.press('enter')
                print(f'{cls} 신청 완료. 신청이 정상적으로 되었는지 확인해 보세요.')
                time.sleep(0.5)
        else:
            break

if __name__ == '__main__':
    main()