from selenium.webdriver.common.by import By
from src.custom_driver import CustomDriver
from utils.logger import Logger


class NCBIGeneScrapper(CustomDriver):
    def __init__(self, driver, gene_id: int):
        super(NCBIGeneScrapper, self).__init__(driver, 'https://www.ncbi.nlm.nih.gov/datasets/tables/genes/')
        self.logger = Logger('ncbi-gene-scrapper')
        self.gene_id = gene_id

        self._navigate_to_gene_page()

    def get_page_source(self):
        return self.driver.page_source.encode('utf-8')

    def _navigate_to_gene_page(self):
        self.find_element_with_wait(By.ID, 'btn-get-started').click()
        self.find_element_with_wait(By.ID, 'id-type-select').click()
        self.find_element_with_wait(By.ID, 'gene_id').click()

        gene_id_list = self.find_element_with_wait(By.ID, 'id-list-text')
        gene_id_list.send_keys(self.gene_id)

        self.find_element_with_wait(By.ID, 'dlg-add-genes-button').click()

        self.wait_for_page_source(By.CLASS_NAME, 'mdc-data-table__cell')
