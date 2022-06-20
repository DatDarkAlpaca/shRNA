from src.gene_search import get_gene_name, get_gene_symbol, GenePageSearch
from src.si_rna import GenScriptScrapper
from src.siDirect import SiDirectCrawler
from src.nuccore import get_nuccore_name
from src.driver import open_driver
from src.RNAi import RNAiGenerator
from src.muscle_rna import *
from src.rna_utils import *
from src.GC import calculate_gc

import pandas as pd
import logging
import os

from tkinter import filedialog


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


def retrieve_gene_results(driver, gene_id):
    page_search = GenePageSearch(driver, gene_id)
    gene_name = get_gene_name(page_search)
    gene_symbol = get_gene_symbol(page_search)

    return gene_symbol, gene_name


def retrieve_consensus(logger, gene_id):
    logger.info('Retrieving RNA files')
    rna_file = get_rna_from_transcriptions(gene_id)
    rna_temp_file, rna_temp_filename = save_temp_rna_file(rna_file)

    # Muscle Setup:
    logger.info('Setting up Muscle')
    download_muscle()
    muscle_command = get_muscle_command()

    # Aligning RNA Sequence:
    logger.info('Aligning RNA sequence')
    output_filepath = 'output.fas'
    aligned = align_rna(muscle_command, rna_temp_filename, output_filepath)

    return output_filepath, get_aligned_consensus(aligned)


def retrieve_consensus_with_file(logger):
    # Muscle Setup:
    logger.info('Setting up Muscle')
    download_muscle()
    muscle_command = get_muscle_command()

    # File:
    fasta_file = filedialog.askopenfilename()

    # Aligning RNA Sequence:
    logger.info('Aligning RNA sequence')
    output_filepath = 'output.fas'

    if fasta_file:
        aligned = align_rna(muscle_command, fasta_file, output_filepath)
    else:
        raise FileNotFoundError("No fasta file was provided.")

    return output_filepath, get_aligned_consensus(aligned)


def retrieve_target_and_tm(driver, consensus):
    si_crawler = SiDirectCrawler(driver)
    si_crawler.set_options(gc_range=(30, 50), custom_pattern='WWSNNNNNNNNNNNNNNNSNN')
    si_crawler.insert_sequence(consensus)

    target_sequences, tm_guides = si_crawler.get_si_direct_data()
    return target_sequences, tm_guides


def retrieve_variants_and_gene_name(gen_scrapper, sequence_list):
    gen_bank_senso, senso_variant_gene_name = [], []
    targets_in_h_sapien_senso = []

    for senso in sequence_list:
        result = gen_scrapper.get_si_rna_result_for_sequence(senso)
        gen_bank_senso.append(result)
        targets_in_h_sapien_senso.append(len(result))

        nuccore_results = []
        for nuccore_name in result:
            nuccore_results.append(get_nuccore_name(nuccore_name))

        senso_variant_gene_name.append(nuccore_results)

    return {'genbank': gen_bank_senso, 'gene_names': senso_variant_gene_name, 'amount': targets_in_h_sapien_senso}


def without_external():
    # Logger:
    logger = configure_logging(logging.DEBUG)

    # Input:
    gene_id = input("Enter the Gene's ID: ")

    # Driver:
    logger.info('Initializing webdriver')
    driver = open_driver()

    # Gene Results (First website that looks like an android app):
    logger.info('Collecting gene results')
    gene_symbol, gene_name = retrieve_gene_results(driver, gene_id)
    logger.info(f"Gene's Name: {gene_name.title()} ({gene_symbol})")

    # RNA Retrieval (Straight from a request):
    output_filepath, consensus = retrieve_consensus(logger, gene_id)

    # Get SiDirect sequences (Japanese Website):
    logger.info('Using siDirect crawler')
    target_sequences, tm_guides = retrieve_target_and_tm(driver, consensus)

    # Generate RNAi/Guide/Tail/Gc sequences (uses the information from the jp website table):
    logger.info('Generating RNAi sequences')
    rna_i_generator = RNAiGenerator(target_sequences)
    senso_sequences = rna_i_generator.senso_sequences
    guide_sequences = rna_i_generator.guide_sequences

    # Initialize the GenScript Scrapper:
    logger.info('Initializing the genscript scrapper')
    gen_scrapper = GenScriptScrapper(driver)

    # Get Variants/GeneName:
    senso_results = retrieve_variants_and_gene_name(gen_scrapper, senso_sequences[:2])
    guide_results = retrieve_variants_and_gene_name(gen_scrapper, guide_sequences[:2])

    # Final Results:
    results = pd.DataFrame(list(zip(
        senso_sequences[:2],  # Alvo
        senso_sequences[:2],  # Senso
        calculate_gc(senso_sequences[:2]),  # GC
        senso_results['amount'],  # Alvos
        senso_results['genbank'],  # Genbank
        senso_results['gene_names'],  # Nome dos Genes

        guide_sequences[:2],  # Guia
        tm_guides[:2],  # TM Guia
        calculate_gc(guide_sequences[:2]),  # GC
        guide_results['amount'],  # Alvos
        guide_results['genbank'],  # Genbank
        guide_results['gene_names'],  # Nome dos Genes

        rna_i_generator.rna_i[:2]  # shRNA
    )), columns=['Alvo', 'Senso', 'GC', 'Alvos em H. sapiens para o senso', 'Genbank', 'Nome do Gene',
                 'Guia', 'Tm Guia', 'GC', 'Alvos em H. sapiens para a guia', 'Genbank', 'Nome do Gene', 'shRNA'])

    print(results)

    results.to_csv('Results.csv')

    # Cleanup:
    os.remove(output_filepath)


def with_external():
    # Logger:
    logger = configure_logging(logging.DEBUG)

    # Driver:
    logger.info('Initializing webdriver')
    driver = open_driver()

    # File Retrieval:
    output_filepath, consensus = retrieve_consensus_with_file(logger)

    # Get SiDirect sequences (Japanese Website):
    logger.info('Using siDirect crawler')
    target_sequences, tm_guides = retrieve_target_and_tm(driver, consensus)

    # Generate RNAi/Guide/Tail/Gc sequences (uses the information from the jp website table):
    logger.info('Generating RNAi sequences')
    rna_i_generator = RNAiGenerator(target_sequences)
    senso_sequences = rna_i_generator.senso_sequences
    guide_sequences = rna_i_generator.guide_sequences

    # Initialize the GenScript Scrapper:
    logger.info('Initializing the genscript scrapper')
    gen_scrapper = GenScriptScrapper(driver)

    # Get Variants/GeneName:
    senso_results = retrieve_variants_and_gene_name(gen_scrapper, senso_sequences[:2])
    guide_results = retrieve_variants_and_gene_name(gen_scrapper, guide_sequences[:2])

    # Final Results:
    results = pd.DataFrame(list(zip(
        senso_sequences[:2],  # Alvo
        senso_sequences[:2],  # Senso
        calculate_gc(senso_sequences[:2]),  # GC
        senso_results['amount'],  # Alvos
        senso_results['genbank'],  # Genbank
        senso_results['gene_names'],  # Nome dos Genes

        guide_sequences[:2],  # Guia
        tm_guides[:2],  # TM Guia
        calculate_gc(guide_sequences[:2]),  # GC
        guide_results['amount'],  # Alvos
        guide_results['genbank'],  # Genbank
        guide_results['gene_names'],  # Nome dos Genes

        rna_i_generator.rna_i[:2]  # shRNA
    )), columns=['Alvo', 'Senso', 'GC', 'Alvos em H. sapiens para o senso', 'Genbank', 'Nome do Gene',
                 'Guia', 'Tm Guia', 'GC', 'Alvos em H. sapiens para a guia', 'Genbank', 'Nome do Gene', 'shRNA'])

    print(results)

    results.to_csv('Results.csv')

    # Cleanup:
    os.remove(output_filepath)


def main():
    file_option = input('Do you want to use an external .fas file? (y/n): ')
    if file_option.lower() in ['y', 'yes', '1', 'true', 't', 'sim', 's']:
        with_external()
    else:
        without_external()



if __name__ == '__main__':
    main()
