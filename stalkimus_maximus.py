from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import time
import json

SEARCH_STRING = "Search or start new chat"
TIMEOUT = 10
REFRESH_RATE = 0.2
ONLINE_TEXT = "[*] Target has connected - {} [*]"
TYPING_TEXT = "[*] Target started typing - {} [*]"
OFFLINE_TEXT = "[*] Target has disconnected - {} [*]"

driver_path = ""
target_name = ""
print_func = print
log_file = ""

def log_and_print(text):
    print_func(text)
    with open(log_file, 'a', encoding="utf-8") as log:
        log.write(text + "\n")

with open("config.json", 'r', encoding="utf-8") as config_file:
    config = json.load(config_file)
    driver_path = config['chromedriver_path']
    target_name = config['contact_name']
    if config['logging_enabled']:
        log_file = config['log_filepath']
        print(f"[*] Logging to {log_file} [*]")
        print = log_and_print

driver = webdriver.Chrome(executable_path=driver_path)
driver.get("https://web.whatsapp.com/")
input("[*] Waiting for WhatsApp Web login. Hit enter when finished. [*]")
search_box = driver.find_element_by_xpath(f"//input[@title=\'{SEARCH_STRING}\']")
search_box.send_keys(target_name)
try:
    chat = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, f"//span[@title=\"{target_name}\"]")))
    chat.click()
    state = "disconnected"
    print(f"[*] Stalkimus Maximus is now activated - Target is {target_name}[*]")
    while True:
        time.sleep(REFRESH_RATE)
        online = driver.find_elements_by_xpath("//span[@title=\"online\"]")
        typing = driver.find_elements_by_xpath("//span[@title=\"typing…\"]")
        if online:
            if state is "online":
                continue
            print(ONLINE_TEXT.format(datetime.datetime.now()))
            state = "online"
        elif typing:
            if state is "typing":
                continue
            print(TYPING_TEXT.format(datetime.datetime.now()))
            state = "typing"
        elif state:
            if state is "disconnected":
                continue
            print(OFFLINE_TEXT.format(datetime.datetime.now()))
            state = "disconnected"
except KeyboardInterrupt:
    print("[*] Logging out... [*]")
finally:
    driver.quit()
    print("[*] Stalkimus Maximus is now deactivated [*]")