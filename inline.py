import time
from time import sleep
import random
from multiprocessing import Process
import datetime

from mailbox import NoSuchMailboxError
from selenium import webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import Select
import selenium
import webdriver_manager
print(selenium.__version__)
print(webdriver_manager.__version__)

retryCount = 0
# TODO: button disable condition
# TODO: auto but slow, click when present button
# TODO: test internet influence
# TODO: update selenium version


def info_check(order_info):
    pass


def fill_adult(chrome):
    # fill in adult information
    try:
        select = Select(chrome.find_element_by_id("adult-picker"))
        select.select_by_index(order_info['adult'])
    except:
        pass


def fill_kid(chrome):
    # fill in kid information
    try:
        select = Select(chrome.find_element_by_id("kid-picker"))
        select.select_by_index(order_info['kid'])
    except NoSuchElementException:
        print("No kid field!")


def select_date(chrome, sleep_time):
    c = chrome.find_element(By.CSS_SELECTOR, value="div[id='date-picker']")
    d = chrome.find_element(
        By.CSS_SELECTOR, f"div[data-date='{order_info['date']}']")

    chrome.execute_script(f"window.scrollTo(0, {c.location['y']})")
    sleep(sleep_time)
    c.click()

    chrome.execute_script(f"window.scrollTo(0, {d.location['y']})")
    sleep(sleep_time)
    d.click()

    e = chrome.find_element(
        By.CSS_SELECTOR, f"button[data-cy='book-now-time-slot-box-{order_info['time']}']")
    chrome.execute_script(f"window.scrollTo(0, {e.location['y']})")
    sleep(sleep_time)
    e.click()


class InlineOrderMaker():
    def __init__(self, order_info):
        self.order_info = order_info
        options = Options()
        options.add_argument("--no-sandbox")
        # options.add_argument("--headless")
        info_check(order_info)
        sleep_time = 0.35

        # chrome = webdriver.Chrome(service=ChromeService(
        #     ChromeDriverManager().install()))
        self.chrome = webdriver.Chrome('./chromedriver', options=options)
        # chrome = webdriver.Chrome('./chromedriver', options=options)
        self.chrome.implicitly_wait(1)
        self.chrome.get(order_info['url'])

    def update_order_info(self, order_info):
        self.order_info = order_info

    def refresh(self):
        t1 = time.time()
        self.chrome.refresh()  # 0.5 ~ 0.7 sec
        t2 = time.time()
        print(f'Refresh time {t2-t1}')

    def run(self):
        self.refresh()

# def inlineFill(order_info):
#     options = Options()
#     options.add_argument("--no-sandbox")
#     # options.add_argument("--headless")
#     info_check(order_info)
#     sleep_time = 0.35

#     try:
#         # chrome = webdriver.Chrome(service=ChromeService(
#         #     ChromeDriverManager().install()))
#         chrome = webdriver.Chrome('./chromedriver', options=options)
#         # chrome = webdriver.Chrome('./chromedriver', options=options)
#         chrome.implicitly_wait(1)
#         chrome.get(order_info['url'])
#         t1 = time.time()
#         chrome.refresh()  # 0.5 ~ 0.7 sec
#         tt1 = time.time()
#         print(tt1-t1)

#         # select = Select(chrome.find_element_by_id("book-now"))

#         # # fill in date information
#         # try:
#         #     select = Select(chrome.find_element_by_id("date-picker"))
#         #     select.select_by_index(order_info['adult'])
#         # except:
#         #     pass

#         select = Select(chrome.find_element(By.ID, value="adult-picker"))
#         select.select_by_value(str(order_info['adult']))
#         select = Select(chrome.find_element(By.ID, value="kid-picker"))
#         select.select_by_value(str(order_info['kid']))

#         # # fill in adult information
#         # try:
#         #     # tt0 = time.time()
#         #     select = Select(chrome.find_element(By.ID, value="adult-picker"))
#         #     # tt1 = time.time()
#         #     select.select_by_value(str(order_info['adult']))
#         #     # tt2 = time.time()
#         #     # print(tt2-tt1)
#         #     # print(tt1-tt0)
#         # except:
#         #     pass

#         # # fill in kid information
#         # try:
#         #     select = Select(chrome.find_element(By.ID, value="kid-picker"))
#         #     select.select_by_value(str(order_info['kid']))
#         # except NoSuchElementException:
#         #     print("No kid field!")

#         # p1 = Process(target=fill_adult, args={'chrome': chrome})
#         # p2 = Process(target=fill_adult, args={'chrome': chrome})
#         # p1.start()
#         # p2.start()
#         # p1.join()
#         # p2.join()

#         # fill in adult information
#         # chrome.execute_script("document.body.style.zoom='50%'")

#         # chrome.execute_script("window.scrollTo(0, 0)")
#         # b = chrome.find_element_by_class_name("sc-dIouRR dlbwaR")
#         # b = chrome.find_element_by_class_name("sc-dIouRR fMba-De")
#         # b.click()

#         t2 = time.time()
#         # p1 = Process(target=select_date, args=(chrome, sleep_time))
#         # p1.start()
#         # p1.join()

#         # sleep(sleep_time)
#         chrome.execute_script(f"window.scrollTo(0, 915)")
#         # chrome.execute_script("document.body.style.zoom='33%'")
#         sleep(sleep_time)

#         # c = chrome.find_element(
#         #     By.CSS_SELECTOR, value="div[id='date-field, [div[id='date-picker']]")
#         c = chrome.find_element(By.ID, value="date-picker")
#         # print(c.location)
#         d = chrome.find_element(
#             By.CSS_SELECTOR, f"div[data-date='{order_info['date']}']")

#         # chrome.execute_script(f"window.scrollTo(0, {c.location['y']})")

#         # sleep(sleep_time)

#         c.click()

#         # chrome.execute_script(f"window.scrollTo(0, {d.location['y']})")
#         # sleep(sleep_time)
#         d.click()

#         e = chrome.find_element(
#             By.CSS_SELECTOR, f"button[data-cy='book-now-time-slot-box-{order_info['time']}']")
#         # chrome.execute_script(f"window.scrollTo(0, {e.location['y']})")
#         # e = WebDriverWait(chrome, 20).until(
#         #     EC.presence_of_element_located((By.CSS_SELECTOR, f"button[data-cy='book-now-time-slot-box-{order_info['time']}']")))
#         sleep(sleep_time*2)
#         # chrome.execute_script(
#         #     'document.getElementsByTagName("html")[0].style.scrollBehavior = "auto"')
#         e.click()

#         t3 = time.time()
#         f = chrome.find_element(
#             By.CSS_SELECTOR, "button[data-cy='book-now-action-button']")
#         f.click()

#         # TODO: the clickable situation will be influenced by the page position --> find_by_id?
#         # TODO: change implicity wait
#         # g = WebDriverWait(chrome, 20).until(
#         #     EC.presence_of_element_located((By.XPATH, '//input[@id="name"]')))
#         g = chrome.find_element(By.ID, value="name")
#         g.send_keys(order_info['name'])

#         # TODO: select gender
#         # k = WebDriverWait(chrome, 20).until(
#         #     EC.presence_of_element_located((By.XPATH, f'//input[@id="gender-{order_info["gender"]}"]')))
#         # k.click()

#         # h = WebDriverWait(chrome, 20).until(
#         #     EC.presence_of_element_located((By.XPATH, '//input[@id="phone"]')))
#         h = chrome.find_element(By.ID, value="phone")
#         h.send_keys(order_info['phone'])

#         # sleep(sleep_time)
#         submit = chrome.find_element(
#             By.CSS_SELECTOR, "button[data-cy='submit']")
#         t4 = time.time()
#         # print(f'Time: {t1-t0} sec')
#         print(f'Time: {t2-t1} sec')
#         print(f'Time: {t3-t2} sec')
#         print(f'Time: {t4-t3} sec')
#         print(20*'-')
#         print(f'Totla Time: {t4-t1} sec')
#         submit.click()

#         # TODO: 處理吧沐的confirm botton, data-cy="confirm-house-rule

#         # TODO:
#         sleep(10)
#         print('Complete!')
#         pass

#     except TimeoutException:
#         chrome.quit()
#         global retryCount
#         retryCount += 1
#         if (retryCount == 2):
#             print(id+" Write to error log")
#             retryCount = 0
#             pass
#         else:
#             print(id+" Try again")
#             inlineFill(id)


def readFile():
    fileHandler = open("Id.txt", "r")
    IdList = fileHandler.read().splitlines()
    fileHandler.close()
    return IdList


if __name__ == "__main__":
    # TODO: scripting
    # TODO: error handling
    # 國秀食堂
    url = rf"https://inline.app/booking/-MkBSdjj_81Mjn1vAZA6:inline-live-2/-MkBSdrkF0niJoOgE4yz?fbclid=IwAR0xEV5haTFwm7XnaU2lDpXXBL22UFkyavyFBZN3LEFE5LJfxXd4UerdTaA"

    # 青花驕
    url = r"https://inline.app/booking/-MaXEQcbiWaRjXyLytUu:inline-live-2/-MaXf4tGf3cunx-MStor?language=zh-tw"

    # The Antipodean
    # url = r'https://inline.app/booking/-L_qemGeN-S-qEAIAtd1:inline-live-2a466/-N0o8OYl1h-G6dH-bowt'

    # 海底撈
    # url = r'https://inline.app/booking/-LamXb5SAQN7JcJfyRKi:inline-live-2a466/-LamXbrHgLYzPCKRO3QD'

    # 詹紀
    # url = r'https://inline.app/booking/-KO9-zyZTRpTH7LNAe99/-LOcon_dHjl7H4_PR39w?language=zh-tw'

    # 酒灑
    url = r'https://inline.app/booking/-MyeIq6w0WlGH5oRFcd_:inline-live-2/-MyeIqIyLZ5S6ZK_Cke5?language=zh-tw'

    # 吧沐
    # url = r'https://inline.app/booking/-Mn4FfHBBwA49zeGtMrF:inline-live-2/-Mn4FfRSxcIrDcxydG0c'

    # Clock
    # url = r"https://tw.piliapp.com/time-now/tw/taipei/"

    order_info = {'name': '林敬翔',
                  'phone': "953216976",
                  'adult': 4,
                  'gender': 'male',
                  'kid': 0,
                  'url': url,
                  'date': '2022-12-28',
                  'time': '19-30'}

    start_time = datetime.datetime.today()
    start_time = start_time.replace(
        hour=11, minute=59, second=59, microsecond=int(6e5))
    # start_time = datetime.datetime(2022, 12, 14, hour=1, minute=4, second=50)

    maker = InlineOrderMaker()
    maker.update_order(order_info)
    last_sec = datetime.datetime.now().second
    while True:
        now = datetime.datetime.now()
        if now > start_time:
            print(now)
            inlineFill(order_info)
            maker.run()
            break

        # if now.second % 5 == 0 and now.second > last_sec:
        #     print(f'Current time is {now}. Wait until {start_time}.')
        #     last_sec = now.second if last_sec < 50 else 0
