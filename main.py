import pandas as pd

from application import Application, RNADownloadFetcher, RNAExplorerFetcher
from src.sequence_parser import SequenceParser
from src.GC import calculate_gc


def get_fetcher():
    while True:
        file_type = input('Do you want to enter the gene ID(1) or pass the RNA file(2)?: ')
        if file_type.lower() in ['1', 'gene', 'id']:
            gene_id = input('Enter the gene ID: ')

            return RNADownloadFetcher(gene_id)

        elif file_type.lower() in ['2', 'file']:
            return RNAExplorerFetcher()

        else:
            print('Use a valid identifier (1 / 2)')


def generate_results(app, si_direct_results):
    sequence_parser = SequenceParser(si_direct_results.target_sequences)

    first_sequence = True
    print('Amount of Targets:', len(si_direct_results.target_sequences))
    for i, sequence in enumerate(si_direct_results.target_sequences):
        senso_sequence = sequence_parser.senso_sequences[i]
        guide_sequence = sequence_parser.guide_sequences[i]
        tm = si_direct_results.tm_guides[i]

        senso_gen_result = app.get_genscript_results(senso_sequence)
        guide_gen_result = app.get_genscript_results(guide_sequence)

        data = {
            'Alvo': [sequence],
            'Senso': [senso_sequence],
            'GC Senso': [calculate_gc(senso_sequence)],
            'Alvos em H. sapiens para o senso': [senso_gen_result.amount],
            'Genbank Senso': [str(senso_gen_result.genbank)],
            'Nome dos Genes do Senso': [str(senso_gen_result.gene_names)],

            'Guia': [guide_sequence],
            'Tm Guia': [tm],
            'GC Guia': [calculate_gc(guide_sequence)],
            'Alvos em H. sapiens para a guia': [guide_gen_result.amount],
            'Genbank da Guia': [str(guide_gen_result.genbank)],
            'Nome dos Genes da Guia': [str(guide_gen_result.gene_names)],
            'shRNA': sequence_parser.rna_i[i]
        }

        pd.DataFrame(data).to_csv('R1.csv', mode='a', header=first_sequence)
        first_sequence = False
        app.logger.info('Added a sequence to the file')


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
    si_direct_results = app.get_si_direct_results(consensus)

    # Partial Result Generation:
    app.logger.info('Generating partial results')
    generate_results(app, si_direct_results)

    # Cleanup:
    app.clean_muscle_files()


if __name__ == '__main__':
    main()
