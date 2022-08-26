from PySide6.QtWidgets import QMainWindow, QFileDialog
from PySide6.QtCore import QFileInfo
from ui.compiled.shrna_window import Ui_shRNAWindow

from utils.logger.qlistlogger import QListLogger

from src.ncbi_information import get_ncbi_gene_information
from src.siDirect.scrapper import SiDirectScrapper
from src.custom_driver import open_driver

from typing import Optional
from enum import Enum

from src.fetcher.muscle_fetcher import MuscleFetcher
from src.genscript.scrapper import GenScriptScrapper
from src.sequence_parser import SequenceParser
from src.shrna_results import *


class ErrorCode(Enum):
    valid = 0
    invalid = -1


class ShRNAWindow(QMainWindow, Ui_shRNAWindow):
    def __init__(self, parent=None):
        super(ShRNAWindow, self).__init__(parent)
        self.setupUi(self)

        # Logger:
        self.logger_filepath = './res/client.log'
        self.main_logger = Logger('main-app')
        self.connect_buttons()

        # Appending QLogger:
        q_logger = QListLogger()
        q_logger.set_widget(self.debug_log_list)
        self.main_logger.logger.addHandler(q_logger)

        # Driver:
        self.driver = open_driver()

        # State:
        self.execution_state = ErrorCode.valid

        # Muscle:
        self.input_file = None

    # Initializers:
    def connect_buttons(self):
        self.fetch_button.released.connect(self.fetch_button_action)
        self.load_rna_button.released.connect(self.load_rna_action)
        self.debug_clear_button.released.connect(lambda: self.debug_log_list.clear())

    # Functions:
    def load_rna_action(self):
        filepath, check = QFileDialog.getOpenFileName(self, 'Open RNA file', '', 'Text files (*.txt)')
        if not check:
            # Todo: implement file type implementation
            return self.main_logger.error(f"Invalid file: {filepath}.")

        filename = QFileInfo(filepath).fileName()
        self.input_edit.setPlaceholderText(f"<Loaded file: {filename}>")

    def fetch_button_action(self):
        # 1.1. Gene ID:
        gene_id = self.get_gene_id()
        if self.execution_state == ErrorCode.invalid:
            return

        # 1.2. NCBI Information (Only if gene_id is present):
        if gene_id:
            # Todo: execute in a separate thread.
            information = get_ncbi_gene_information(self.driver, gene_id=gene_id)
            self.main_logger.info(f"NCBI Gene Information | Name: {information.name} ({information.symbol})")

        # 2.1. Muscle Input:
        self.main_logger.info('Obtaining RNA file')
        muscle_fetcher = MuscleFetcher(gene_id, self.input_file)
        consensus = muscle_fetcher.fetch_results()

        muscle_fetcher.clean_files()

        # 3. siDirect Fetch:
        self.main_logger.info('Waiting for siDirect to load.')
        si_crawler = SiDirectScrapper(self.driver)
        si_crawler.set_options(gc_range=(30, 50), custom_pattern='WWSNNNNNNNNNNNNNNNSNN')
        si_crawler.insert_sequence(consensus)

        self.main_logger.info('Fetching SiDirect Results')
        si_direct_results = si_crawler.get_si_direct_data()

        # 4. Sequence Parser (consensus):
        self.main_logger.info('Initializing the sequence parser')
        sequence_parser = SequenceParser(si_direct_results.target_sequences)

        # 5. Genscript:
        self.main_logger.info('Initializing the genscrapper')
        genscript_scrapper = GenScriptScrapper(self.driver)

        # 6. Partial Result Generation:
        self.main_logger.info('Generating results')
        prepare_results_folder()
        results = ShRNAResults()
        results.generate_results(genscript_scrapper, si_direct_results, sequence_parser, None, 0)

    # Input:
    def get_gene_id(self) -> Optional[int]:
        input_text = self.input_edit.text()

        if not input_text and not self.input_file:
            self.execution_state = ErrorCode.invalid
            return self.main_logger.error('No gene id or RNA file was provided.')

        try:
            return int(input_text)
        except ValueError:
            self.input_edit.clear()
            self.execution_state = ErrorCode.invalid
            self.main_logger.error('This gene id is invalid. Please enter only numbers.')
