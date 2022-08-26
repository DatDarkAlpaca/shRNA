from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

from src.custom_driver import *
import re

from . import SiDirectResult


class SiDirectScrapper(CustomDriver):
    def __init__(self, driver: webdriver.Chrome):
        super(SiDirectScrapper, self).__init__(driver, 'http://sidirect2.rnai.jp')
        self.logger = Logger('si-direct-scrapper')

        self.sequence_input = None
        self._clear_default_sequence()

    # Methods:
    def set_options(self, gc_range: tuple, custom_pattern):
        self.find_element_with_wait(By.XPATH, '/html/body/form/h3/font/a/img').click()
        self.find_element_with_wait(By.XPATH, '//*[@id="more1"]').click()

        # Unchecking 'Ui-Tei et al., Nucleic Acids Res 32, 936-948':
        self.find_element_with_wait(By.XPATH, '//*[@id="options"]/div[1]/table/tbody/tr/td[1]/p[2]/input').click()

        # Checking 'Ui-Tei + Reynolds + Amarzguioui':
        self.find_element_with_wait(By.XPATH, '//*[@id="functional_options"]/p[2]/input[3]').click()
        # Setting 'Specificity Check' to 'none':
        select = Select(self.find_element_with_wait(By.ID, 'nrdbSpe'))
        select.select_by_value('none')

        # Set gc_content:
        self.find_element_with_wait(By.XPATH, '//*[@id="options"]/div[4]/p[4]/input[1]').click()

        gc_content_element = self.find_element_with_wait(By.XPATH, '//*[@id="options"]/div[4]/p[4]/input[2]')
        gc_content_element.clear()
        gc_content_element.click()
        gc_content_element.send_keys(gc_range[0])

        gc_content_element = self.find_element_with_wait(By.XPATH, '//*[@id="options"]/div[4]/p[4]/input[3]')
        gc_content_element.clear()

        gc_content_element.click()
        gc_content_element.send_keys(gc_range[1])

        # Set custom pattern:
        self.find_element_with_wait(By.XPATH, '//*[@id="options"]/div[4]/p[5]/input[1]').click()
        custom_pattern_element = self.find_element_with_wait(By.XPATH, '//*[@id="options"]/div[4]/p[5]/input[2]')
        custom_pattern_element.clear()
        custom_pattern_element.send_keys(custom_pattern)

    def insert_sequence(self, sequence: str):
        if self.sequence_input:
            self.sequence_input.send_keys(sequence)

    def get_si_direct_data(self) -> SiDirectResult:
        self.driver.find_element(By.XPATH, '/html/body/form/p[2]/input').click()
        self.wait_for_page_source(By.TAG_NAME, 'table')

        page = self.driver.page_source.encode('utf-8')
        soup = BeautifulSoup(page, 'html.parser')
        table_body = soup.find('table').find('tbody')

        target_sequences, tm_guides, si_rna = [], [], []
        rows = table_body.find_all('tr')
        i = 0
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]

            for element in cols:
                if re.search('\\b\w{42}\\b', element):
                    si_rna.append(element[:21] + ' ' + element[21:])
                elif re.search('\\b\w{23}\\b', element):
                    target_sequences.append(element)
                elif re.search('-?\d+.\d+ °C', element):
                    if i % 2 == 0:
                        tm_guides.append(element)
                    i += 1

        return SiDirectResult(si_rna, target_sequences, tm_guides)

    # Helpers:
    def _clear_default_sequence(self):
        self.sequence_input = self.find_element_with_wait(By.ID, 'useq')
        self.sequence_input.clear()
