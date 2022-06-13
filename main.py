from src.gene_search import get_gene_name, GenePageSearch
from src.GC.senso_target import SensoTargetScrapper
from src.siDirect import SiDirectCrawler
from src.results import ResultBuilder
from src.driver import open_driver
from src.RNAi import RNAiGenerator
from src.muscle_rna import *
from src.rna_utils import *
from src.GC import *

import logging
import os


def configure_logging(level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    file_handler = logging.FileHandler('log/debug.log')
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger('sh_rna')
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logging.getLogger('WDM').setLevel(logging.NOTSET)
    os.environ['WDM_LOG'] = "false"

    return logger


def main():
    # Logger:
    logger = configure_logging(logging.DEBUG)

    # Input:
    # gene_id = input("Enter the Gene's ID: ")

    # Driver:
    logger.info('Initializing webdriver')
    driver = open_driver()

    # Gene Name:
    # page_search = GenePageSearch(driver, gene_id)
    # gene_name = get_gene_name(page_search)
    # logger.info(f"Gene's Name: {gene_name.title()}")

    # RNA Retrieval:
    # logger.info('Retrieving RNA files')
    # rna_file = get_rna_from_transcriptions(gene_id)
    # rna_temp_file, rna_temp_filename = save_temp_rna_file(rna_file)

    # Temporary RNA:
    logger.info('Retrieving RNA files')
    rna_temp_filename = 'rna.fna'
    rna_temp_file = open(rna_temp_filename)

    # Muscle Setup:
    logger.info('Setting up Muscle')
    download_muscle()
    muscle_command = get_muscle_command()

    # Aligning RNA Sequence:
    logger.info('Aligning RNA sequence')
    output_filepath = 'output.fas'
    aligned = align_rna(muscle_command, rna_temp_filename, output_filepath)
    consensus = get_aligned_consensus(aligned)

    # Get SiDirect sequences:
    logger.info('Using siDirect crawler')
    si_crawler = SiDirectCrawler(driver)
    si_crawler.set_options(gc_range=(30, 50), custom_pattern='WWSNNNNNNNNNNNNNNNSNN')
    si_crawler.insert_sequence(consensus)
    sequences, guides = si_crawler.get_si_direct_data()

    # Generate RNAi sequences:
    logging.info('Generating RNAi sequences')
    rna_i_generator = RNAiGenerator(sequences)

    # Retrieving Final Results:
    rna_i = rna_i_generator.rna_i
    senso_sequences = rna_i_generator.senso_sequences
    gc_senso = fetch_gc_senso(senso_sequences)
    guide_tail = rna_i_generator.guide_tail
    gc_tail = fetch_gc_guide(guide_tail)

    # Searching for targets:
    # senso_target_scrapper = SensoTargetScrapper(driver)
    # senso_targets = senso_target_scrapper.get_senso_targets(sequences)

    # Add the results:
    r = ResultBuilder()
    r.add_result('shRNA', rna_i)

    r.add_result('Senso', senso_sequences)
    r.add_result('GC', gc_senso)

    r.add_result('Guia', guide_tail)
    r.add_result('GC', gc_tail)

    # r.add_result('Alvos em H. sapiens para a senso', alvos_senso)
    # r.add_result('Descrição', TOTAL_ALVOS_SENSO)
    # r.add_result('Alvos em H. sapiens para a guia', alvos_guia)
    # r.add_result('Descrição', TOTAL_ALVOS_GUIA)
    r.add_result('TM', guides)

    # Cleanup:
    os.remove(output_filepath)
    # os.close(rna_temp_file)

    # Final results:
    r.build_results('Resultados.csv')


if __name__ == '__main__':
    main()
