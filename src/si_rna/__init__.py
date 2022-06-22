from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as ec
from src.driver import *
import logging
import re


class GenScriptScrapper(CustomDriver):
    def __init__(self, driver):
        super(GenScriptScrapper, self).__init__(driver, 'https://www.genscript.com/tools/sirna-target-finder')
        self.logger = logging.getLogger('sh_rna')

    def get_sequence_variants(self, sequence) -> list:
        # Send target sequence:
        sequence_input = find_element_with_wait(self.driver, By.XPATH, '//*[@id="sequence"]')
        sequence_input.clear()
        sequence_input.send_keys(sequence)

        # Press the button:
        try:
            find_element_with_wait(self.driver, By.XPATH, '//*[@id="mainContent2"]/div/div/form/div[11]/input[1]') \
                .click()
        except ElementClickInterceptedException:
            self.logger.info('Unable to press the submit button. Retrying')
            return self.driver.refresh()

        # Variants (NM results):
        variants = self._wait_for_page_results()
        if not variants:
            return self.get_sequence_variants(sequence)

        self.go_back()

        return re.findall('\w{2}_[\d]+', variants)

    def _wait_for_page_results(self):
        try:
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.XPATH, '//*[@id="mainContent2"]/div/p[1]')))

            return find_element_with_wait(self.driver, By.XPATH, '//*[@id="mainContent2"]/div/p[1]').text
        except TimeoutException:
            self.logger.error('The page took too long to load. Retrying.')
            return
