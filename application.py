from src.gene_search import get_gene_name, get_gene_symbol, NCBIGeneSearch
from src.si_rna import GenScriptScrapper
from src.siDirect import SiDirectScrapper
from src.nuccore import get_nuccore_name
from src.driver import open_driver
from src.sequence_parser import SequenceParser
from src.muscle_rna import *
from src.rna_utils import *
from src.GC import calculate_gc

import pandas as pd
import logging
import os

from tkinter import filedialog
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


def create_logger():
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    file_handler = logging.FileHandler('log/debug.log')
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger('sh_rna')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logging.getLogger('WDM').setLevel(logging.NOTSET)
    os.environ['WDM_LOG'] = 'false'

    return logger


@dataclass
class NCBIGeneResult:
    name: str
    symbol: str


@dataclass
class SiDirectResult:
    si_rna: field(default_factory=list)
    target_sequences: field(default_factory=list)
    tm_guides: field(default_factory=list)


@dataclass
class GenscriptResult:
    genbank: field(default_factory=list)
    gene_names: field(default_factory=list)
    amount: int


class RNAFileFetcher(ABC):
    @abstractmethod
    def fetch(self) -> str:
        pass


class RNADownloadFetcher(RNAFileFetcher):
    def __init__(self, gene_id):
        self.gene_id = gene_id

    def fetch(self) -> str:
        rna_file = get_rna_from_transcriptions(self.gene_id)
        _, filepath = save_temp_rna_file(rna_file)
        return filepath


class RNAExplorerFetcher(RNAFileFetcher):
    def fetch(self):
        return filedialog.askopenfilename()


class Application:
    def __init__(self, gene_id=None):
        self.gene_id = gene_id
        self.logger = None
        self.driver = None

        # Muscle:
        self.muscle_output_filepath = 'output.fas'
        self.muscle_command = None

        # SiDirect:
        self.si_crawler = None

        # GenScript Scrapper:
        self.genscript_scrapper = None

    def initialize(self):
        # Initialize logger:
        self.logger = create_logger()

        # Initialize driver:
        self.logger.info('Initializing webdriver')
        self.driver = open_driver()

        # Initialize Muscle:
        self.logger.info('Initializing Muscle')
        download_muscle()
        self.muscle_command = get_muscle_command()

    # NCBI Gene:
    def get_ncbi_gene_information(self) -> NCBIGeneResult:
        page_search = NCBIGeneSearch(self.driver, self.gene_id)
        name = get_gene_name(page_search)
        symbol = get_gene_symbol(page_search)

        return NCBIGeneResult(name, symbol)

    # Muscle:
    def get_muscle_consensus(self, fetcher: RNAFileFetcher) -> str:
        self.logger.info('Fetching RNA file')
        rna_filepath = fetcher.fetch()

        if rna_filepath:
            aligned_rna = self._align_using_muscle(rna_filepath)
        else:
            raise FileNotFoundError('No file was passed to the muscle alignment.')

        return get_aligned_consensus(aligned_rna)

    def _align_using_muscle(self, rna_filepath):
        self.logger.info('Aligning RNA sequence using Muscle')
        return align_rna(self.muscle_command, rna_filepath, self.muscle_output_filepath)

    def clean_muscle_files(self):
        os.remove(self.muscle_output_filepath)

    # SiDirect:
    def get_si_direct_results(self, consensus) -> SiDirectResult:
        if not self.si_crawler:
            self.si_crawler = SiDirectScrapper(self.driver)

        self.logger.info('Fetching SiDirect Results')
        self.si_crawler.set_options(gc_range=(30, 50), custom_pattern='WWSNNNNNNNNNNNNNNNSNN')
        self.si_crawler.insert_sequence(consensus)

        si_rna, target_sequences, tm_guides = self.si_crawler.get_si_direct_data()
        return SiDirectResult(si_rna, target_sequences, tm_guides)

    # GenScript:
    def get_genscript_results(self, sequence):
        if not self.genscript_scrapper:
            self.genscript_scrapper = GenScriptScrapper(self.driver)

        # Genbank:
        variants = self.genscript_scrapper.get_sequence_variants(sequence)

        # Variant Gene Name:
        nuccore_results = []
        for nuccore_name in variants:
            nuccore_results.append(get_nuccore_name(nuccore_name))

        return GenscriptResult(variants, nuccore_results, len(variants))
