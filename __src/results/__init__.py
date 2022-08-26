from __src.GC import calculate_gc
import pandas as pd
import fnmatch
import os


def prepare_results_folder():
    if not os.path.isdir('results'):
        os.mkdir('results')


def count_results() -> int:
    return len(fnmatch.filter(os.listdir('results'), '*.csv'))


def generate_results(app, si_direct_results, sequence_parser, filename=None, start_at: int = 0):
    target_amount = len(si_direct_results.target_sequences)

    file_index = count_results()
    if filename:
        start_at += 1

    first_sequence = not filename

    for i in range(start_at, len(si_direct_results.target_sequences)):
        si_rna_sequence = si_direct_results.si_rna[i]
        passageira_sequence = sequence_parser.passageira_sequences[i]
        guia_sequence = sequence_parser.guia_sequences[i]

        tm = str(si_direct_results.tm_guides[i])

        senso_gen_result = app.get_genscript_results(passageira_sequence)
        guide_gen_result = app.get_genscript_results(guia_sequence)

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

        if not filename:
            pd.DataFrame(data).to_csv(f"./results/Result{file_index}.csv",
                                      mode='a', encoding='utf-8', header=first_sequence, index=False)
            app.logger.info(f"Progress: {i + 1}/{target_amount}")
            first_sequence = False
        else:
            pd.DataFrame(data).to_csv(filename, mode='a', encoding='utf-8', header=first_sequence, index=False)
            app.logger.info(f"Progress: {i}/{target_amount}")
            first_sequence = False
