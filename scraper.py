import selenium.common
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
from csv import writer

print("please provide stream name")
stream = input()
print("creating file, please provide name")
file_name = input()

# settings
ser = Service("chromedriver/chromedriver.exe")
op = webdriver.ChromeOptions()
# op.headless = True  # doesn't work
driver = webdriver.Chrome(service=ser, options=op)


driver.get(f'https://www.twitch.tv/{stream}')  # link to twitch streamer
with open(f'{file_name}.csv', 'w+', encoding="utf-8") as file:
    writer_object = writer(file)
    while True:
        try:
            a = driver.find_elements(By.CLASS_NAME, "chat-line__message")
            b = driver.find_elements(By.CLASS_NAME, "chat-line__message")
            for i in b:
                if i not in a:  # avoid adding copies of the same message
                    username = i.find_element(By.CLASS_NAME, "chat-author__display-name").text
                    message_text = i.find_element(By.CLASS_NAME, "text-fragment").text
                    time = datetime.now()
                    day_string = time.strftime("%d/%m/%Y")  # format datetime
                    time_string = time.strftime("%H:%M:%S")  # format datetime
                    row = [day_string, time_string, username, message_text]
                    writer_object.writerow(row)

        except selenium.common.NoSuchElementException:  # continue working even without messages
            pass




