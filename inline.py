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
print(f'selenium version ({selenium.__version__})')
print(f'webdriver_manager version ({webdriver_manager.__version__})')

retryCount = 0
# TODO: button disable condition
# TODO: auto but slow, click when present button
# TODO: test internet influence
# TODO: update selenium version


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
    def __init__(self, order_info: dict, driver_path='./chromedriver', sleep_time: float = 0.5):
        self.driver_path = driver_path
        self.update_order_info(order_info, self.driver_path)
        self.sleep_time = sleep_time

    def get_chrome(self, driver_path, url):
        options = Options()
        options.add_argument("--no-sandbox")
        # options.add_argument("--headless")

        chrome = webdriver.Chrome(driver_path, options=options)
        chrome.implicitly_wait(1)
        chrome.get(url)
        return chrome

    @staticmethod
    def inspect_order(order_info):
        if order_info is not None:
            return True

    def update_order_info(self, order_info: dict, driver_path=None):
        self.order_info = order_info
        if driver_path is not None:
            driver_path = self.driver_path
        assert self.inspect_order(self.order_info), 'Legal input order'
        self.chrome = self.get_chrome(driver_path, self.order_info['url'])

    def refresh(self):
        t1 = time.time()
        self.chrome.refresh()  # 0.5 ~ 0.7 sec
        t2 = time.time()
        print(f'Refresh time {t2-t1}')

    def run(self):
        try:
            self.refresh()

            t1 = time.time()
            select = Select(self.chrome.find_element(
                By.ID, value="adult-picker"))
            select.select_by_value(str(order_info['adult']))
            select = Select(self.chrome.find_element(
                By.ID, value="kid-picker"))
            select.select_by_value(str(order_info['kid']))

            t2 = time.time()
            self.chrome.execute_script(f"window.scrollTo(0, 915)")
            # TODO: zoom out sol. for show all the elements for clicking -> problem is the location isn't correct
            # chrome.execute_script("document.body.style.zoom='33%'")
            sleep(self.sleep_time)

            c = self.chrome.find_element(By.ID, value="date-picker")
            d = self.chrome.find_element(
                By.CSS_SELECTOR, f"div[data-date='{order_info['date']}']")
            c.click()
            d.click()

            while True:
                try:
                    e = self.chrome.find_element(
                        By.CSS_SELECTOR, f"button[data-cy='book-now-time-slot-box-{order_info['time']}']")
                    # e = WebDriverWait(self.chrome, 20).until(
                    #     EC.elementToBeClickable((By.CSS_SELECTOR, f"button[data-cy='book-now-time-slot-box-{order_info['time']}']")))
                    # WebDriverWait(self.chrome, 20).until(ExpectedConditions.elementToBeClickable(By.xpath("(//div[@id='brandSlider']/div[1]/div/div/div/img)[50]")))
                    # element.click()
                    # sleep(0.7)
                    e.click()
                    break
                except:
                    pass

            t3 = time.time()
            f = self.chrome.find_element(
                By.CSS_SELECTOR, "button[data-cy='book-now-action-button']")
            f.click()

            # TODO: the clickable situation will be influenced by the page position
            # TODO: change implicity wait
            g = self.chrome.find_element(By.ID, value="name")
            g.send_keys(order_info['name'])

            # # TODO: select gender, need to scroll up
            # k = WebDriverWait(self.chrome, 20).until(
            #     EC.presence_of_element_located((By.XPATH, f'//input[@id="gender-{order_info["gender"]}"]')))
            # k.click()

            h = self.chrome.find_element(By.ID, value="phone")
            h.send_keys(order_info['phone'])

            submit = self.chrome.find_element(
                By.CSS_SELECTOR, "button[data-cy='submit']")
            t4 = time.time()
            print(f'Time: {t2-t1} sec')
            print(f'Time: {t3-t2} sec')
            print(f'Time: {t4-t3} sec')
            print(20*'-')
            print(f'Totla Time: {t4-t1} sec')
            submit.click()

            # TODO: 處理吧沐的confirm botton, data-cy="confirm-house-rule
            sleep(10)
            print('Complete!')

        # TODO: not workable currently
        except TimeoutException:
            # self.chrome.quit()
            global retryCount
            retryCount += 1
            if (retryCount == 2):
                print(" Write to error log")
                retryCount = 0
                pass
            else:
                print(" Try again")
                self.run()


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
                  'adult': 4,
                  'gender': 'male',
                  'kid': 0,
                  'url': url,
                  'date': '2022-12-28',
                  'time': '19-30'}
    driver_path = './chromedriver'
    sleep_time = 0.35

    start_time = datetime.datetime.today()
    start_time = start_time.replace(
        hour=11, minute=59, second=59, microsecond=int(7.5e5))
    start_time = datetime.datetime(2022, 12, 14, hour=1, minute=4, second=50)

    maker = InlineOrderMaker(
        order_info=order_info,
        driver_path=driver_path,
        sleep_time=sleep_time
    )
    last_sec = datetime.datetime.now().second
    while True:
        now = datetime.datetime.now()
        if now > start_time:
            print(now)
            # inlineFill(order_info)
            maker.run()
            break

        # if now.second % 5 == 0 and now.second > last_sec:
        #     print(f'Current time is {now}. Wait until {start_time}.')
        #     last_sec = now.second if last_sec < 50 else 0
