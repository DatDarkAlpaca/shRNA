from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

from src.driver import *

from dataclasses import dataclass, field
import logging
import re


# Todo: replace.
@dataclass
class SensoTargetHolder:
    number_targets: int
    targets: field(default_factory=list)


# Todo: rename to scrapper.
class SensoTargetScrapper(CustomDriver):
    def __init__(self, driver):
        super(SensoTargetScrapper, self).__init__(driver, 'https://www.genscript.com/tools/sirna-target-finder')
        self.logger = logging.getLogger('sh_rna')

    def get_senso_targets(self, sequences: list):
        results = []
        for sequence in sequences:
            variants_str = self._get_sequence_variants(sequence)
            print(variants_str)
            targets = re.findall('NM_[\d]+', variants_str)

            results.append(SensoTargetHolder(len(targets), targets))

        return results

    def _get_sequence_variants(self, sequence):
        # Send sequence:
        find_element_with_wait(self.driver, By.XPATH, '//*[@id="sequence"]').send_keys(sequence)

        # Press the submit button:
        find_element_with_wait(self.driver, By.XPATH, '//*[@id="mainContent2"]/div/div/form/div[11]/input[1]')\
            .click()

        # Todo: it throws exception
        variants = find_element_with_wait(self.driver, By.XPATH, '//*[@id="mainContent2"]/div/p[1]')
        self.go_back()

        return variants

    # Todo: extract method:
    def _wait_for_page_source(self):
        try:
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.XPATH, '//*[@id="mainContent2"]/div/p[1]')))

            return self.driver.page_source.encode('utf-8')
        except TimeoutException:
            self.logger.error('The page took too long to load. Retrying.')
            self._wait_for_page_source()
