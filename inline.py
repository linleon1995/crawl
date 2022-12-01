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


def info_check(order_info):
    pass


def inlineFill(order_info):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    info_check(order_info)

    try:
        chrome = webdriver.Chrome(ChromeDriverManager().install())
        chrome.implicitly_wait(1)
        # chrome = webdriver.Chrome(options=options)
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

        c = chrome.find_element_by_css_selector("div[id='date-picker']")
        d = chrome.find_element_by_css_selector(
            f"div[data-date='{order_info['date']}']")

        chrome.execute_script(f"window.scrollTo(0, {c.location['y']})")
        sleep(1)
        c.click()

        chrome.execute_script(f"window.scrollTo(0, {d.location['y']})")
        sleep(1)
        d.click()

        e = chrome.find_element_by_css_selector(
            f"button[data-cy='book-now-time-slot-box-{order_info['time']}']")
        chrome.execute_script(f"window.scrollTo(0, {e.location['y']})")
        sleep(1)
        e.click()

        c_click = False
        d_click = False
        e_click = False
        height = 0
        h = 200
        timeout = 5

        f = chrome.find_element_by_css_selector(
            "button[data-cy='book-now-action-button']")
        f.click()
        # select = chrome.find_element_by_id("date-picker")
        # select.text = '5月27日 週四'

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

        submit = chrome.find_element_by_css_selector(
            "button[data-cy='submit']")
        submit.click()

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


def autoFill(id):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")

    chrome = webdriver.Chrome(ChromeDriverManager().install())

    chrome.get("https://inline.app/booking/-MkBSdjj_81Mjn1vAZA6:inline-live-2/-MkBSdrkF0niJoOgE4yz?fbclid=IwAR0xEV5haTFwm7XnaU2lDpXXBL22UFkyavyFBZN3LEFE5LJfxXd4UerdTaA")
    sleep(3)
    select = Select(chrome.find_element_by_id("adult-picker"))
    for op in select.options:
        print(op.text)
    select.select_by_index(8)
    print(3)
    try:
        chrome = webdriver.Chrome(ChromeDriverManager().install())
        # chrome = webdriver.Chrome(options=options)
        chrome.get("https://zh.surveymonkey.com/r/EmployeeHealthCheck")
        # chrome.get("https://inline.app/booking/-MkBSdjj_81Mjn1vAZA6:inline-live-2/-MkBSdrkF0niJoOgE4yz?fbclid=IwAR0xEV5haTFwm7XnaU2lDpXXBL22UFkyavyFBZN3LEFE5LJfxXd4UerdTaA")
        agreexpath = "//div[contains(@class,'radio-button-container')]//label//span[contains(@class,'radio-button-display')]"
        agreeCheck = WebDriverWait(chrome, 15).until(
            EC.visibility_of_element_located((By.XPATH, agreexpath)))
        # agreeCheck
        agreeCheck.click()

        employeeId = chrome.find_elements_by_xpath(
            "//div[contains(@class,'question-fieldset question-legend')]")
        employeeId.send_keys(id)

        # employId
        employeeId = chrome.find_elements_by_xpath(
            "//div[contains(@class,'question-body open-ended-single')]//input")[0]
        employeeId.send_keys(id)

        # foreheadTemp check
        foreheadCheckBtn = chrome.find_elements_by_xpath(
            "//div[contains(@class,'radio-button-container')]//label//span[contains(@class,'radio-button-display')]")[2]
        foreheadCheckBtn.click()

        # foreheadTemp
        Temperature = chrome.find_elements_by_xpath(
            "//div[contains(@class,'question-body open-ended-single')]//input")[1]
        foreheadDegree = str(round(random.uniform(34.1, 36.9), 1))
        Temperature.send_keys(foreheadDegree)

        # contacted people who returned from aboard in the last 14 days
        noContactBtn = chrome.find_elements_by_xpath(
            "//div[contains(@class,'radio-button-container')]//label//span[contains(@class,'radio-button-display')]")[5]
        noContactBtn.click()

        # declaration radio button
        declarationBtn = chrome.find_elements_by_xpath(
            "//div[contains(@class,'radio-button-container')]//label//span[contains(@class,'radio-button-display')]")[6]
        declarationBtn.click()

        # submit btn to next page
        submitBtn = chrome.find_elements_by_xpath(
            "//button[contains(text(), '下一頁')]")[0]
        submitBtn.click()

        # successful landing page
        compleredTxtPath = "(//span[@class='title-text'])"
        compleredTxt = WebDriverWait(chrome, 10, 1).until(
            EC.visibility_of_element_located((By.XPATH, compleredTxtPath))).text
        print(compleredTxt+id+" degree :"+foreheadDegree)
        chrome.quit()

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
            autoFill(id)


def readFile():
    fileHandler = open("Id.txt", "r")
    IdList = fileHandler.read().splitlines()
    fileHandler.close()
    return IdList


if __name__ == "__main__":
    # 國秀食堂
    url = rf"https://inline.app/booking/-MkBSdjj_81Mjn1vAZA6:inline-live-2/-MkBSdrkF0niJoOgE4yz?fbclid=IwAR0xEV5haTFwm7XnaU2lDpXXBL22UFkyavyFBZN3LEFE5LJfxXd4UerdTaA"

    # 青花驕
    url = r"https://inline.app/booking/-MaXEQcbiWaRjXyLytUu:inline-live-2/-MaXER3I3tbJ6YWZIFGu"

    # The Antipodean
    url = r'https://inline.app/booking/-L_qemGeN-S-qEAIAtd1:inline-live-2a466/-N0o8OYl1h-G6dH-bowt'

    # 海底撈
    # url = r'https://inline.app/booking/-LamXb5SAQN7JcJfyRKi:inline-live-2a466/-LamXbrHgLYzPCKRO3QD'

    # 詹紀
    # url = r'https://inline.app/booking/-KO9-zyZTRpTH7LNAe99/-LOcon_dHjl7H4_PR39w?language=zh-tw'

    order_info = {'name': '林敬翔',
                  'phone': "953216976",
                  'adult': 2,
                  'gender': 'male',
                  'kid': 0,
                  'url': url,
                  'date': '2022-12-16',
                  'time': '10-00'}
    inlineFill(order_info)
    # autoFill('a')
