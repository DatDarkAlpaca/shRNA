import logging

from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver


class CustomDriver:
    def __init__(self, driver: webdriver.Chrome, url: str):
        self.driver = driver
        self._get_driver(url)

    def go_back(self):
        self.driver.execute_script('window.history.go(-1)')

    def _get_driver(self, url):
        try:
            self.driver.get(url)
        except WebDriverException:
            self._get_driver(url)


def open_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.headless = False

    return webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))


def find_element_with_wait(driver, by: By, element: str, timeout: int = 10) -> WebElement:
    try:
        return WebDriverWait(driver, timeout).until(lambda d: d.find_element(by, element))
    except TimeoutException:
        logger = logging.getLogger('sh_rna')
        logger.error(f"Failed to find_element_with_wait: {element}. Retrying")

        find_element_with_wait(driver, by, element, timeout)
