import logging
import re
import time

from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

from src.driver import *


# Todo: rename to scrapper.
# Todo: make siDirect refresh.
class SiDirectCrawler(CustomDriver):
    def __init__(self, driver: webdriver.Chrome):
        super(SiDirectCrawler, self).__init__(driver, 'http://sidirect2.rnai.jp')
        self.logger = logging.getLogger('sh_rna')

        self.sequence_input = None
        self._clear_default_sequence()

    # Methods:
    def set_options(self, gc_range: tuple, custom_pattern):
        find_element_with_wait(self.driver, By.XPATH, '/html/body/form/h3/font/a/img').click()
        time.sleep(3)
        find_element_with_wait(self.driver, By.XPATH, '//*[@id="more1"]').click()
        time.sleep(3)

        # Unchecking 'Ui-Tei et al., Nucleic Acids Res 32, 936-948':
        find_element_with_wait(self.driver, By.XPATH, '//*[@id="options"]/div[1]/table/tbody/tr/td[1]/p[2]/input')\
            .click()
        time.sleep(3)

        # Checking 'Ui-Tei + Reynolds + Amarzguioui':
        find_element_with_wait(self.driver, By.XPATH, '//*[@id="functional_options"]/p[2]/input[3]').click()
        time.sleep(3)
        # Setting 'Specificity Check' to 'none':
        select = Select(find_element_with_wait(self.driver, By.ID, 'nrdbSpe'))
        select.select_by_value('none')
        time.sleep(3)
        # Set gc_content:
        find_element_with_wait(self.driver, By.XPATH, '//*[@id="options"]/div[4]/p[4]/input[1]').click()

        gc_content_element = find_element_with_wait(self.driver, By.XPATH, '//*[@id="options"]/div[4]/p[4]/input[2]')
        gc_content_element.clear()
        gc_content_element.click()
        gc_content_element.send_keys(gc_range[0])
        time.sleep(3)
        gc_content_element = find_element_with_wait(self.driver, By.XPATH, '//*[@id="options"]/div[4]/p[4]/input[3]')
        gc_content_element.clear()

        gc_content_element.click()
        gc_content_element.send_keys(gc_range[1])
        time.sleep(3)
        # Set custom pattern:
        find_element_with_wait(self.driver, By.XPATH, '//*[@id="options"]/div[4]/p[5]/input[1]').click()
        custom_pattern_element = find_element_with_wait(self.driver, By.XPATH,
                                                        '//*[@id="options"]/div[4]/p[5]/input[2]')
        custom_pattern_element.clear()
        custom_pattern_element.send_keys(custom_pattern)

        time.sleep(3)

    def insert_sequence(self, sequence: str):
        if self.sequence_input:
            self.sequence_input.send_keys(sequence)

    def get_si_direct_data(self):
        self.driver.find_element(By.XPATH, '/html/body/form/p[2]/input').click()
        self._wait_for_page_results()

        page = self.driver.page_source.encode('utf-8')
        soup = BeautifulSoup(page, 'html.parser')
        table_body = soup.find('table').find('tbody')

        sequences, guides = [], []
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]

            for element in cols:
                if re.search('\\b\w{23}\\b', element):
                    sequences.append(element)
                elif re.search('-?\d+.\d+ °C', element):
                    guides.append(element)

        return sequences, guides

    def _wait_for_page_results(self) -> str:
        try:
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, 'table')))
        except TimeoutException:
            self.logger.error('The page took too long to load. Retrying.')
            self.driver.refresh()
            self._wait_for_page_results()

    # Helpers:
    def _clear_default_sequence(self):
        self.sequence_input = find_element_with_wait(self.driver, By.ID, 'useq')
        self.sequence_input.clear()