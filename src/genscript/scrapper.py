from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from src.custom_driver import CustomDriver
import logging
import re


class GenScriptScrapper(CustomDriver):
    def __init__(self, driver):
        super(GenScriptScrapper, self).__init__(driver, 'https://www.genscript.com/tools/sirna-target-finder')
        self.logger = logging.getLogger('genscript-scrapper')

    def get_sequence_variants(self, sequence) -> list:
        # Send target sequence:
        self.wait_for_element_clickable(By.XPATH, '//*[@id="sequence"]')

        sequence_input = self.find_element_with_wait(By.XPATH, '//*[@id="sequence"]')
        sequence_input.clear()
        sequence_input.send_keys(sequence)

        # Press the button:
        try:
            element = self.find_element_with_wait(By.XPATH, '//*[@id="mainContent2"]/div/div/form/div[11]/input[1]')
            self.driver.execute_script('arguments[0].click();', element)
        except ElementClickInterceptedException:
            self.logger.info('Unable to press the submit button. Retrying')
            self.get_sequence_variants(sequence)

        # Variants (NM results):
        self.wait_for_page_source(By.XPATH, '//*[@id="mainContent2"]/div/p[1]')
        variants = self.find_element_with_wait(By.XPATH, '//*[@id="mainContent2"]/div/p[1]').text

        self.go_back()

        return re.findall('\w{2}_[\d]+', variants)
