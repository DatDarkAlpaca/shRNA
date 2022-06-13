from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

from src.driver import *
import logging


# Todo: rename to scrapper.
class GenePageSearch(CustomDriver):
    def __init__(self, driver, gene_id: int):
        super(GenePageSearch, self).__init__(driver, 'https://www.ncbi.nlm.nih.gov/datasets/tables/genes/')
        self.logger = logging.getLogger('sh_rna')
        self.gene_id = gene_id

        self._navigate_to_gene_page()

    def get_page_source(self):
        return self.driver.page_source.encode('utf-8')

    def _navigate_to_gene_page(self):
        find_element_with_wait(self.driver, By.ID, 'btn-get-started').click()
        find_element_with_wait(self.driver, By.ID, 'id-type-select').click()
        find_element_with_wait(self.driver, By.ID, 'gene_id').click()
        gene_id_list = find_element_with_wait(self.driver, By.ID, 'id-list-text')
        gene_id_list.send_keys(self.gene_id)

        find_element_with_wait(self.driver, By.ID, 'dlg-add-genes-button').click()

        self._wait_for_page_source()

    def _wait_for_page_source(self):
        try:
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'mdc-data-table__cell')))

            return self.driver.page_source.encode('utf-8')
        except TimeoutException:
            self.logger.error('The page took too long to load. Retrying.')
            self._wait_for_page_source()
