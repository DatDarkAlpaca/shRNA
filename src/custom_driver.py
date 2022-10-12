from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webdriver import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium import webdriver

from utils.logger import Logger


class CustomDriver:
    def __init__(self, driver: webdriver.Chrome, url: str):
        self.driver = driver
        self._initialize_driver(url)

        self.logger = Logger('custom-driver')

    def _initialize_driver(self, url):
        try:
            self.driver.get(url)
        except WebDriverException:
            self._initialize_driver(url)

    def go_back(self):
        self.driver.execute_script('window.history.go(-1)')

    def wait_for_page_source(self, by: By, element: str, timeout: int = 10):
        try:
            WebDriverWait(self.driver, timeout).until(ec.presence_of_element_located((by, element)))
            return self.driver.page_source.encode('utf-8')

        except exceptions.TimeoutException:
            self.logger.error(f"The page '{self.driver.current_url}' took too long to load element '{element}'. "
                              f"Retrying...")
            self.wait_for_page_source(by, element, timeout)

    def find_element_with_wait(self, by: By, element: str, timeout: int = 10, retry=True) -> WebElement:
        try:
            return WebDriverWait(self.driver, timeout).until(lambda d: d.find_element(by, element))
        except TimeoutException:
            if retry:
                self.logger.error(f"Failed to find_element_with_wait: {element}. Retrying")
                self.find_element_with_wait(by, element, timeout)

    def wait_for_element_clickable(self, by: By, element: str, timeout: int = 10):
        try:
            WebDriverWait(self.driver, timeout).until(ec.element_to_be_clickable((by, element)))
            return self.driver.page_source.encode('utf-8')

        except exceptions.TimeoutException:
            self.logger.error(f"Could not click the element '{element}'. Retrying...")
            self.wait_for_page_source(by, element, timeout)


def open_driver():
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--disable-gpu')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                         + "AppleWebKit/537.36 (KHTML, like Gecko)"
                         + "Chrome/87.0.4280.141 Safari/537.36")

    return webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
