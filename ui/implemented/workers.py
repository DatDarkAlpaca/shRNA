from PySide6.QtCore import QObject, Slot, Signal
from selenium.webdriver.chromium.webdriver import ChromiumDriver

from src.ncbi_information import get_ncbi_gene_information
from src.siDirect.scrapper import SiDirectScrapper
from src.custom_driver import open_driver

from src.fetcher.muscle_fetcher import MuscleFetcher
from src.shrna_results import *

from src.muscle import download_muscle

from src.ncbi_information import NCBIInformation
from src.siDirect import SiDirectResult

import zipfile


class DriverWorker(QObject):
    ready = Signal(ChromiumDriver)
    finished = Signal()

    @Slot()
    def initialize_driver(self):
        driver = open_driver()
        self.ready.emit(driver)
        self.finished.emit()


class NCBIWorker(QObject):
    ready = Signal(NCBIInformation)
    finished = Signal()

    def __init__(self):
        super().__init__()
        self.driver = None
        self.gene_id = None

    @Slot()
    def fetch_information(self):
        information = get_ncbi_gene_information(self.driver, self.gene_id)
        self.ready.emit(information)
        self.finished.emit()


class MuscleWorker(QObject):
    muscle_downloaded = Signal()
    finished = Signal(str)
    error = Signal()

    def __init__(self):
        super().__init__()
        self.gene_id = None
        self.input_file = None

    def download_muscle(self):
        download_muscle()
        self.muscle_downloaded.emit()

    @Slot()
    def run(self):
        self.download_muscle()

        muscle_fetcher = MuscleFetcher(self.gene_id, self.input_file)

        try:
            consensus = muscle_fetcher.fetch_results()
            self.finished.emit(consensus)
            muscle_fetcher.clean_files()
        except zipfile.BadZipFile:
            self.error.emit()


class SiDirectWorker(QObject):
    finished = Signal(SiDirectResult)

    def __init__(self):
        super().__init__()
        self.consensus = None
        self.driver = None

    @Slot()
    def run(self):
        si_crawler = SiDirectScrapper(self.driver)
        si_crawler.set_options(gc_range=(30, 50), custom_pattern='WWSNNNNNNNNNNNNNNNSNN')
        si_crawler.insert_sequence(self.consensus)

        si_direct_results = si_crawler.get_si_direct_data()
        self.finished.emit(si_direct_results)


class ResultsWorker(QObject):
    finished = Signal()
    result_ready = Signal(int, int, dict)

    def __init__(self):
        super().__init__()
        self.genscript_scrapper = None
        self.si_direct_results = None
        self.sequence_parser = None

    @Slot()
    def run(self):
        results = ShRNAResults()
        generator = results.generate_results(self.genscript_scrapper,
                                             self.si_direct_results,
                                             self.sequence_parser, None, 0)

        for current, amount, data in generator:
            self.result_ready.emit(current, amount, data)

        self.finished.emit()