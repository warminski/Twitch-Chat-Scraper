import selenium.common
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
from csv import writer
import time as t

#provide stream name
stream = "https://www.twitch.tv/xqc"

#provide file name
file_name = "xqc.csv"

# settings
ser = Service("chromedriver/chromedriver.exe")
op = webdriver.ChromeOptions()
op.add_argument('--headless')
op.add_argument('window-size=1920x1080')

driver = webdriver.Chrome(service=ser, options=op)


driver.get(f'{stream}')  # link to twitch streamer
with open(f'{file_name}', 'a+', newline='', encoding="utf-8") as file:
    writer_object = writer(file)
    while True:
        try:
            if len(driver.find_elements(By.CLASS_NAME, "chat-line__message")) == 0:
                pass
            else:
                old_messages = driver.find_elements(By.CLASS_NAME, "chat-line__message")
                t.sleep(3)  # wait for new messages
                new_messages = driver.find_elements(By.CLASS_NAME, "chat-line__message")
                for i in new_messages:
                    if i not in old_messages:  # avoid adding copies of the same message
                        username = i.find_element(By.CLASS_NAME, "chat-author__display-name").text
                        message_text = i.find_element(By.CLASS_NAME, "text-fragment").text
                        time = datetime.now()
                        day_string = time.strftime("%d/%m/%Y")  # format datetime
                        time_string = time.strftime("%H:%M:%S")  # format datetime
                        row = [day_string, time_string, username, message_text]
                        writer_object.writerow(row)

        except selenium.common.NoSuchElementException:  # continue working even without messages
            pass




