from src.application import Application, RNADownloadFetcher, RNAExplorerFetcher
from src.sequence_parser import SequenceParser
from src.results import generate_results, prepare_results
from tkinter.filedialog import askopenfilename


def get_fetcher():
    print('\n')

    while True:
        file_type = input('Do you want to enter the gene ID(1), RNA file(2) or text input(3)?: ')
        if file_type.lower() in ['1', 'gene', 'id']:
            gene_id = input('Enter the gene ID: ')

            return RNADownloadFetcher(gene_id)

        elif file_type.lower() in ['2', 'file']:
            return RNAExplorerFetcher()

        else:
            print('Please, use a valid identifier (\'1\' or \'2\')')


def main():
    app = Application()
    app.initialize()

    # Repair:
    repair = input('Do you want to repair an existing result? (y/n): ')
    if repair in ['y', 'yes', 's', 'sim', '1']:
        start_at = int(input('What is the index of the last result you have fetched? (only numbers): '))
        filename = askopenfilename()
    else:
        filename = None
        start_at = 0

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
    prepare_results()
    generate_results(app, si_direct_results, sequence_parser, filename, start_at)


if __name__ == '__main__':
    main()
