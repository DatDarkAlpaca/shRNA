from utils.logger import Logger
from src.muscle import *
from . import Fetcher


class MuscleFetcher(Fetcher):
    def __init__(self, gene_id: int, input_filepath: str):
        super().__init__()

        self.logger = Logger('muscle-fetcher')

        self.gene_id, self.input_filepath = gene_id, input_filepath
        self.muscle_output_filepath = 'output.fas'

        self.muscle_command = None

        self.muscle_command = get_muscle_command()

    def fetch_results(self):
        """Fetches Muscle alignment consensus results."""

        self._get_muscle_input()
        aligned_rna = self._use_muscle_alignment()

        return get_aligned_consensus(aligned_rna)

    def clean_files(self):
        os.remove(self.muscle_output_filepath)

    def _get_muscle_input(self):
        if not self.input_filepath:
            rna_filepath = get_rna_from_transcriptions(self.gene_id)
            _, self.input_filepath = save_temp_rna_file(rna_filepath)

    def _use_muscle_alignment(self):
        # Todo: run in a separate thread.
        self.logger.info('Aligning RNA sequence')
        return align_rna(self.muscle_command, self.input_filepath, self.muscle_output_filepath)
