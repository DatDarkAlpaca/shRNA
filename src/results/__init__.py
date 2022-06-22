from src.GC import calculate_gc
import pandas as pd
import fnmatch
import os


def prepare_results():
    if not os.path.isdir('results'):
        os.mkdir('results')


def count_results() -> int:
    return len(fnmatch.filter(os.listdir('results'), '*.csv'))


def generate_results(app, si_direct_results, sequence_parser):
    first_sequence = True
    target_amount = len(si_direct_results.target_sequences)

    file_index = count_results()
    for i, sequence in enumerate(si_direct_results.target_sequences):
        si_rna_sequence = si_direct_results.si_rna[i]
        senso_sequence = sequence_parser.senso_sequences[i]
        guide_sequence = sequence_parser.guide_sequences[i]

        tm = str(si_direct_results.tm_guides[i])

        senso_gen_result = app.get_genscript_results(senso_sequence)
        guide_gen_result = app.get_genscript_results(guide_sequence)

        data = {
            'Index': [i],
            'Alvo': [sequence],
            'siRNA': [si_rna_sequence],
            'Senso': [senso_sequence],
            'GC Senso': [str(calculate_gc(senso_sequence)) + '%'],
            'Alvos em H. sapiens para o senso': [senso_gen_result.amount],
            'Genbank Senso': [str(senso_gen_result.genbank)],
            'Nome dos Genes do Senso': [str(senso_gen_result.gene_names)],

            'Guia': [guide_sequence],
            'Tm Guia': [tm],
            'GC Guia': [str(calculate_gc(guide_sequence)) + '%'],
            'Alvos em H. sapiens para a guia': [guide_gen_result.amount],
            'Genbank da Guia': [str(guide_gen_result.genbank)],
            'Nome dos Genes da Guia': [str(guide_gen_result.gene_names)],
            'shRNA': sequence_parser.rna_i[i]
        }

        pd.DataFrame(data).to_csv(f"./results/Result{file_index}.csv",
                                  mode='a', encoding='utf-8', header=first_sequence, index=False)
        first_sequence = False
        app.logger.info(f"Progress: {i + 1}/{target_amount}")
