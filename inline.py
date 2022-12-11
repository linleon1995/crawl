import time
from time import sleep
import random

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
# TODO: wait until scroll down
# TODO: auto but slow, click when present button
# TODO: test internet influence
# TODO: update selenium version


def info_check(order_info):
    pass


def inlineFill(order_info):
    options = Options()
    options.add_argument("--no-sandbox")
    # options.add_argument("--headless")
    info_check(order_info)
    sleep_time = 0.3

    try:
        # chrome = webdriver.Chrome(service=ChromeService(
        #     ChromeDriverManager().install()))
        t1 = time.time()
        chrome = webdriver.Chrome('./chromedriver')
        # chrome = webdriver.Chrome('./chromedriver', options=options)
        chrome.implicitly_wait(1)
        chrome.get(order_info['url'])
        # select = Select(chrome.find_element_by_id("book-now"))

        # fill in adult information
        try:
            select = Select(chrome.find_element_by_id("adult-picker"))
            select.select_by_index(order_info['adult'])
        except:
            pass

        # fill in date information
        try:
            select = Select(chrome.find_element_by_id("date-picker"))
            select.select_by_index(order_info['adult'])
        except:
            pass

        # fill in kid information
        try:
            select = Select(chrome.find_element_by_id("kid-picker"))
            select.select_by_index(order_info['kid'])
        except NoSuchElementException:
            print("No kid field!")

        # fill in adult information
        # chrome.execute_script("document.body.style.zoom='50%'")

        # chrome.execute_script("window.scrollTo(0, 0)")
        # b = chrome.find_element_by_class_name("sc-dIouRR dlbwaR")
        # b = chrome.find_element_by_class_name("sc-dIouRR fMba-De")
        # b.click()

        t2 = time.time()
        c = chrome.find_element_by_css_selector("div[id='date-picker']")
        d = chrome.find_element_by_css_selector(
            f"div[data-date='{order_info['date']}']")

        chrome.execute_script(f"window.scrollTo(0, {c.location['y']})")
        sleep(sleep_time)
        c.click()

        chrome.execute_script(f"window.scrollTo(0, {d.location['y']})")
        sleep(sleep_time)
        d.click()

        e = chrome.find_element_by_css_selector(
            f"button[data-cy='book-now-time-slot-box-{order_info['time']}']")
        chrome.execute_script(f"window.scrollTo(0, {e.location['y']})")
        sleep(sleep_time)
        e.click()
        t3 = time.time()

        f = chrome.find_element_by_css_selector(
            "button[data-cy='book-now-action-button']")
        f.click()

        # TODO: the clickable situation will be influenced by the page position --> find_by_id?
        # TODO: change implicity wait
        g = WebDriverWait(chrome, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="name"]')))
        g.send_keys(order_info['name'])
        # TODO: select gender
        # k = WebDriverWait(chrome, 20).until(
        #     EC.presence_of_element_located((By.XPATH, f'//input[@id="gender-{order_info["gender"]}"]')))
        # k.click()
        h = WebDriverWait(chrome, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="phone"]')))
        h.send_keys(order_info['phone'])

        sleep(sleep_time)
        submit = chrome.find_element_by_css_selector(
            "button[data-cy='submit']")
        t4 = time.time()
        print(f'Time: {t1-t0} sec')
        print(f'Time: {t2-t1} sec')
        print(f'Time: {t3-t2} sec')
        print(f'Time: {t4-t3} sec')
        print(f'Time: {t4-t0} sec')
        submit.click()

        # TODO: 處理吧沐的confirm botton, data-cy="confirm-house-rule

        # TODO:
        sleep(100)
        print('Complete!')
        pass

    except TimeoutException:
        chrome.quit()
        global retryCount
        retryCount += 1
        if (retryCount == 2):
            print(id+" Write to error log")
            retryCount = 0
            pass
        else:
            print(id+" Try again")
            inlineFill(id)


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
    # url = r'https://inline.app/booking/-MyeIq6w0WlGH5oRFcd_:inline-live-2/-MyeIqIyLZ5S6ZK_Cke5?language=zh-tw'

    # 吧沐
    # url = r'https://inline.app/booking/-Mn4FfHBBwA49zeGtMrF:inline-live-2/-Mn4FfRSxcIrDcxydG0c'

    # Clock
    # url = r"https://tw.piliapp.com/time-now/tw/taipei/"

    order_info = {'name': '林敬翔',
                  'phone': "953216976",
                  'adult': 2,
                  'gender': 'male',
                  'kid': 0,
                  'url': url,
                  'date': '2022-12-28',
                  'time': '19-30'}
    inlineFill(order_info)
    # autoFill('a')
