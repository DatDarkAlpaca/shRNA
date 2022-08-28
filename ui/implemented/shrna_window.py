from PySide6.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem
from PySide6.QtCore import QFileInfo, QObject, Slot, Signal, QThread
from selenium.webdriver.chromium.webdriver import ChromiumDriver

from ui.compiled.shrna_window import Ui_shRNAWindow

from utils.logger.qlistlogger import QListLogger

from src.ncbi_information import get_ncbi_gene_information
from src.siDirect.scrapper import SiDirectScrapper
from src.custom_driver import open_driver

from typing import Optional
from enum import Enum
import zipfile

from src.fetcher.muscle_fetcher import MuscleFetcher
from src.genscript.scrapper import GenScriptScrapper
from src.sequence_parser import SequenceParser
from src.shrna_results import *

from src.muscle import download_muscle

from src.ncbi_information import NCBIInformation
from src.siDirect import SiDirectResult


class ErrorCode(Enum):
    valid = 0
    invalid = -1


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


class ShRNAWindow(QMainWindow, Ui_shRNAWindow):
    def __init__(self, parent=None):
        super(ShRNAWindow, self).__init__(parent)
        self.setupUi(self)

        self.connect_buttons()

        # Logger:
        self.logger_filepath, self.main_logger = [None] * 2
        self.initialize_logger()

        # Threads:
        self.driver_object, self.ncbi_object, self.muscle_object = DriverWorker(), NCBIWorker(), MuscleWorker()
        self.si_direct_object, self.results_object = SiDirectWorker(), ResultsWorker()

        self.driver_thread, self.ncbi_thread, self.muscle_thread = QThread(), QThread(), QThread()
        self.si_direct_thread, self.results_thread = QThread(), QThread()
        self.initialize_threads()
        self.driver_thread.start()

        # Driver:
        self.driver = None

        # Muscle:
        self.input_file = None

        # State:
        self.execution_state = ErrorCode.valid

    # Thread slots:
    def on_driver_ready(self, driver):
        self.driver = driver
        self.main_logger.info('Successfully created a driver instance.')

    def on_ncbi_information_ready(self, information: NCBIInformation):
        self.ncbi_result_label.setText(f"NCBI Gene Information: Name: {information.name} | ({information.symbol})")

    def on_muscle_finished(self, consensus):
        self.main_logger.info('Fetching SiDirect Results')
        self.si_direct_object.driver = self.driver
        self.si_direct_object.consensus = consensus
        self.si_direct_thread.start()

    def on_muscle_error(self):
        self.main_logger.error('This gene id has no zip file attached to it.')

    def on_si_direct_finished(self, si_direct_results: SiDirectResult):
        # Sequence Parser:
        self.main_logger.info('Initializing the sequence parser')
        sequence_parser = SequenceParser(si_direct_results.target_sequences)

        # Genscript:
        self.main_logger.info('Initializing the genscrapper')
        genscript_scrapper = GenScriptScrapper(self.driver)

        # Results:
        self.main_logger.info('Generating results')
        prepare_results_folder()

        self.results_object.genscript_scrapper = genscript_scrapper
        self.results_object.si_direct_results = si_direct_results
        self.results_object.sequence_parser = sequence_parser

        self.results_thread.start()

    def on_partial_result_ready(self, current, target, data):
        self.main_logger.info(f"Progress: {current}/{target}")
        self.add_to_result_table(data)

    # Initializers:
    def initialize_logger(self):
        self.logger_filepath = './res/client.log'
        self.main_logger = Logger('main-app')

        # Appending QLogger:
        q_logger = QListLogger()
        q_logger.set_widget(self.debug_log_list)
        self.main_logger.logger.addHandler(q_logger)

    # noinspection PyUnresolvedReferences
    def initialize_threads(self):
        # Driver Thread:
        self.driver_object.ready.connect(self.on_driver_ready)
        self.driver_object.moveToThread(self.driver_thread)
        self.driver_object.finished.connect(self.driver_thread.quit)
        self.driver_thread.started.connect(self.driver_object.initialize_driver)

        self.ncbi_object.ready.connect(self.on_ncbi_information_ready)
        self.ncbi_object.moveToThread(self.ncbi_thread)
        self.ncbi_object.finished.connect(self.ncbi_thread.quit)
        self.ncbi_thread.started.connect(self.ncbi_object.fetch_information)

        # Muscle:
        self.muscle_object.finished.connect(self.on_muscle_finished)
        self.muscle_object.error.connect(self.on_muscle_error)

        self.muscle_object.moveToThread(self.muscle_thread)
        self.muscle_object.finished.connect(self.muscle_thread.quit)
        self.muscle_thread.started.connect(self.muscle_object.run)

        # SiDirect:
        self.si_direct_object.finished.connect(self.on_si_direct_finished)
        self.si_direct_object.moveToThread(self.si_direct_thread)
        self.si_direct_object.finished.connect(self.si_direct_thread.quit)
        self.si_direct_thread.started.connect(self.si_direct_object.run)

        # Results:
        self.results_object.result_ready.connect(self.on_partial_result_ready)
        self.results_object.moveToThread(self.results_thread)
        self.results_object.finished.connect(self.results_thread.quit)
        self.results_thread.started.connect(self.results_object.run)

    def connect_buttons(self):
        self.fetch_button.released.connect(self.fetch_button_action)
        self.load_rna_button.released.connect(self.load_rna_action)
        self.debug_clear_button.released.connect(lambda: self.debug_log_list.clear())

    # Functions:
    def load_rna_action(self):
        filepath, check = QFileDialog.getOpenFileName(self, 'Open Sequence file', '', 'Text files (*.txt)')
        if not check:
            # Todo: implement file type implementation
            return self.main_logger.error(f"Invalid file: {filepath}.")

        filename = QFileInfo(filepath).fileName()
        self.input_edit.setPlaceholderText(f"<Loaded file: {filename}>")

    def fetch_button_action(self):
        if not self.driver:
            return self.main_logger.info("The chromium driver isn't ready yet.")

        gene_id = self.get_gene_id()
        if self.execution_state == ErrorCode.invalid:
            self.execution_state = ErrorCode.valid
            return

        if gene_id:
            self.main_logger.info('Acquiring gene information')
            self.ncbi_object.driver = self.driver
            self.ncbi_object.gene_id = gene_id
            self.ncbi_thread.start()

            self.gene_id_label.setText(f"Gene ID: {gene_id}")
        else:
            self.gene_id_label.setText(f"Gene ID: External")

        # 2.1. Muscle Input:
        self.main_logger.info('Initializing muscle')
        self.muscle_object.gene_id = gene_id
        self.muscle_object.input_file = self.input_file
        self.muscle_thread.start()

        return

    # Input:
    def get_gene_id(self) -> Optional[int]:
        input_text = self.input_edit.text()

        if not input_text and not self.input_file:
            self.execution_state = ErrorCode.invalid
            return self.main_logger.error('No gene id or sequence file was provided.')

        try:
            return int(input_text)
        except ValueError:
            self.input_edit.clear()
            self.execution_state = ErrorCode.invalid
            self.main_logger.error('This gene id is invalid. Please enter only numbers.')

    # Table:
    def add_to_result_table(self, data):
        row_position = self.results_table.rowCount()
        self.results_table.insertRow(row_position)

        self.results_table.setItem(row_position, 0, QTableWidgetItem(str(data['Index'][0])))
        self.results_table.setItem(row_position, 1, QTableWidgetItem(str(data['Alvo'][0])))

        self.results_table.setItem(row_position, 2, QTableWidgetItem(str(data['siRNA'][0])))
        self.results_table.setItem(row_position, 3, QTableWidgetItem(str(data['Passageira'][0])))
        self.results_table.setItem(row_position, 4, QTableWidgetItem(str(data['GC Senso'][0])))
        self.results_table.setItem(row_position, 5, QTableWidgetItem(str(data['Alvos em H. sapiens para o senso'][0])))
        self.results_table.setItem(row_position, 6, QTableWidgetItem(str(data['Genbank Senso'][0])))
        self.results_table.setItem(row_position, 7, QTableWidgetItem(str(data['Nome dos Genes do Senso'][0])))

        self.results_table.setItem(row_position, 8, QTableWidgetItem(str(data['Guia'][0])))
        self.results_table.setItem(row_position, 9, QTableWidgetItem(str(data['Tm Guia'][0])))
        self.results_table.setItem(row_position, 10, QTableWidgetItem(str(data['GC Guia'][0])))
        self.results_table.setItem(row_position, 11, QTableWidgetItem(str(data['Alvos em H. sapiens para a guia'][0])))

        self.results_table.setItem(row_position, 12, QTableWidgetItem(str(data['Genbank da Guia'][0])))
        self.results_table.setItem(row_position, 13, QTableWidgetItem(str(data['Nome dos Genes da Guia'][0])))
        self.results_table.setItem(row_position, 14, QTableWidgetItem(str(data['shRNA'])))
