from Bio.Seq import MutableSeq
from Bio.Seq import reverse_complement


class SequenceParser:
    loop = MutableSeq('UUCAAGAGA')

    def __init__(self, sequences: list):
        self.sequences = sequences
        self.sequence_results = {}

        self._generate_passageira()
        self._generate_guia()

    def _generate_passageira(self):
        self.sequence_results['passageira'] = []
        for sequence in self.sequences:
            passageira = list(sequence)
            del passageira[:2]
            del passageira[19:]
            passageira = ''.join(passageira)
            passageira = MutableSeq(passageira)
            passageira = passageira.transcribe()
            self.sequence_results['passageira'].append(passageira)

    def _generate_guia(self):
        self.sequence_results['guia'] = []
        for sequence in self.sequences:
            guia = list(sequence)
            del guia[21:]
            guia = ''.join(guia)
            guia = MutableSeq(guia)
            guia = reverse_complement(guia)
            guia = guia.transcribe()
            self.sequence_results['guia'].append(guia)

    @property
    def passageira_sequences(self) -> list:
        return self.sequence_results['passageira']

    @property
    def guia_sequences(self):
        return self.sequence_results['guia']

    @property
    def sh_rna(self):
        results = []
        for i in range(self.sequences):
            passageira = self.sequence_results['passageira'][i]
            guia = self.sequence_results['guia'][i]

            results.append(MutableSeq(passageira + SequenceParser.loop + guia))

        return results
