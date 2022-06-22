import pandas as pd

from src.application import Application, RNADownloadFetcher, RNAExplorerFetcher
from src.sequence_parser import SequenceParser
from src.GC import calculate_gc


def get_fetcher():
    print('\n')

    while True:
        file_type = input('Do you want to enter the gene ID(1) or pass the RNA file(2)?: ')
        if file_type.lower() in ['1', 'gene', 'id']:
            gene_id = input('Enter the gene ID: ')

            return RNADownloadFetcher(gene_id)

        elif file_type.lower() in ['2', 'file']:
            return RNAExplorerFetcher()

        else:
            print('Please, use a valid identifier (\'1\' or \'2\')')


def generate_results(app, si_direct_results, sequence_parser):
    first_sequence = True
    target_amount = len(si_direct_results.target_sequences)
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

        pd.DataFrame(data).to_csv('R2.csv', mode='a', encoding='utf-8', header=first_sequence, index=False)
        first_sequence = False
        app.logger.info(f"Progress: {i + 1}/{target_amount}")


def main():
    app = Application()
    app.initialize()

    # RNA Fetcher:
    fetcher = get_fetcher()

    # NCBI Gene Information:
    if app.gene_id:
        name, symbol = app.get_ncbi_gene_information()
        app.logger(f"NCBI Gene Information | Name: {name} ({symbol})")

    # Muscle
    consensus = app.get_muscle_consensus(fetcher)

    # SiDirect:
    app.logger.info('Waiting siDirect to load')
    si_direct_results = app.get_si_direct_results(consensus)
    app.clean_muscle_files()

    # Sequence Parser:
    app.logger.info('Parsing sequences')
    sequence_parser = SequenceParser(si_direct_results.target_sequences)

    # Partial Result Generation:
    app.logger.info('Generating partial results')
    generate_results(app, si_direct_results, sequence_parser)


if __name__ == '__main__':
    main()
