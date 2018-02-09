from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options

import bs4
import logging
import os
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt='%Y-%m-%d | %H:%M:%S'
    )
logger = logging.getLogger(__name__)

"""
TODO:
 - Logging, in file or in console.
 - Untangle the scraped table.
 - Make it pretty somehow. How do I present the data to myself? a website?
"""

def assignment_scraper(usr, pwd):
    # Uncomment for headless setting ctrl+'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")

    logger.info('Starting browser.')
    browser = webdriver.Chrome(executable_path=basedir+"/chromedriver.exe", chrome_options=chrome_options)
    url = "http://start.vucfyn.net/"
    url2 = "https://login.emu.dk/"


    logger.info('Going to url: {}'.format(url))
    browser.get(url) #navigate to the page

    def login(browser, usr, pwd):
        try:
            wait = WebDriverWait(browser, 5)
            element = wait.until(EC.element_to_be_clickable((By.ID, 'login')))
            username = browser.find_element_by_id("user") #username form field
            password = browser.find_element_by_id("pass") #password form field

            username.send_keys(usr)
            password.send_keys(pwd)

            button = browser.find_element_by_id("login")
            button.click()
            return 1
        except NoSuchElementException:
            logger.debug('Current site: {}'.format(browser.current_url))
            logger.error("Could not log in. Am I on the wrong webpage?")
            return

    logger.info('Login in to {}'.format(url2))
    p = login(browser, usr, pwd)


    scrape_url = 'https://start.vucfyn.net/Task/Student'
    logger.info('Going to url: {}'.format(scrape_url))
    browser.get(scrape_url)

    wait = WebDriverWait(browser, 5)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'TaskStatusID')))

    text_to_select = ['Ikke afleveret', 'Vurderet', 'Afleveret']

    logger.info('Scraping data from: {}'.format(text_to_select))
    sdata = []
    for text in text_to_select:
        try:
            pp = Select(browser.find_element_by_id('TaskStatusID'))
            pp.select_by_visible_text(text)

        except:
            logger.exception('Error when scraping.')
        hw = browser.find_element_by_id('tblTasks').get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(hw, 'lxml')
        hmwrk = soup.find_all('tr')

        for tr in hmwrk:
            td = tr.find_all('td')
            if td:
                d = {
                    'date':td[1]['oldtitle'],
                    'subject':td[2].text,
                    'name':td[3].text,
                    'status':text
                    }
                sdata.append(d)

    logger.info('Done!')

    logger.info('Exiting browser.')
    browser.quit()

    return sdata


if __name__ == '__main__':
    assignment_scraper('aviv0001', 'qwe123qwe')
