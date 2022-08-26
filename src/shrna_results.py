from src.gc import calculate_gc
import pandas as pd
import fnmatch
import os

from src.genscript import GenscriptResult
from src.nuccore import get_nuccore_name
from utils.logger import Logger


def prepare_results_folder():
    if not os.path.isdir('results'):
        os.mkdir('results')


def count_results() -> int:
    return len(fnmatch.filter(os.listdir('results'), '*.csv'))


class ShRNAResults:
    def __init__(self):
        self.logger = Logger('shrna-results')

    @staticmethod
    def _get_genscript_results(genscript_scrapper, sequence):
        # Genbank:
        variants = genscript_scrapper.get_sequence_variants(sequence)

        # Variant Gene Name:
        nuccore_results = []
        for nuccore_name in variants:
            nuccore_results.append(get_nuccore_name(nuccore_name))

        return GenscriptResult(variants, nuccore_results, len(variants))

    def generate_results(self, gen_scrapper, si_direct_results, sequence_parser, filename=None, start_at: int = 0):
        file_index = count_results()
        if filename:
            start_at += 1

        first_sequence = not filename

        for i in range(start_at, len(si_direct_results.target_sequences)):
            si_rna_sequence = si_direct_results.si_rna[i]
            passageira_sequence = sequence_parser.passageira_sequences[i]
            guia_sequence = sequence_parser.guia_sequences[i]

            tm = str(si_direct_results.tm_guides[i])

            senso_gen_result = ShRNAResults._get_genscript_results(gen_scrapper, passageira_sequence)
            guide_gen_result = ShRNAResults._get_genscript_results(gen_scrapper, guia_sequence)

            data = {
                'Index': [i],
                'Alvo': [si_direct_results.target_sequences[i]],
                'siRNA': [si_rna_sequence],
                'Passageira': [passageira_sequence],
                'GC Senso': [str(calculate_gc(passageira_sequence)) + '%'],
                'Alvos em H. sapiens para o senso': [senso_gen_result.amount],
                'Genbank Senso': [str(senso_gen_result.genbank)],
                'Nome dos Genes do Senso': [str(senso_gen_result.gene_names)],

                'Guia': [guia_sequence],
                'Tm Guia': [tm],
                'GC Guia': [str(calculate_gc(guia_sequence)) + '%'],
                'Alvos em H. sapiens para a guia': [guide_gen_result.amount],
                'Genbank da Guia': [str(guide_gen_result.genbank)],
                'Nome dos Genes da Guia': [str(guide_gen_result.gene_names)],
                'shRNA': sequence_parser.sh_rna[i]
            }

            target_amount = len(si_direct_results.target_sequences)

            if not filename:
                pd.DataFrame(data).to_csv(f"./results/Result{file_index}.csv",
                                          mode='a', encoding='utf-8', header=first_sequence, index=False)
                self.logger.info(f"Progress: {i + 1}/{target_amount}")
                first_sequence = False
            else:
                pd.DataFrame(data).to_csv(filename, mode='a', encoding='utf-8', header=first_sequence, index=False)
                self.logger.info(f"Progress: {i}/{target_amount}")
                first_sequence = False
