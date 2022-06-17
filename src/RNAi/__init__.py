from Bio.Seq import MutableSeq


# Todo: rename to multi-result generator or something
class RNAiGenerator:
    tail = 'TT'
    loop = 'TTCAAGAGA'

    def __init__(self, sequences: list):
        self.sequences = sequences
        self.sequence_results = {}

        self._generate_senso()
        self._attach_loop()
        self._get_reverse_complement()
        self._add_tail_to_reversed_complement()

    @property
    def rna_i(self):
        with_loop = self.sequence_results['with_loop']
        with_tail = self.sequence_results['with_tail']

        return [sequence[0] + sequence[1] for sequence in zip(with_loop, with_tail)]

    @property
    def senso_sequences(self):
        return self.sequence_results['senso']

    @property
    # Todo: check whether the guide(guia) has the tail:
    def guide_sequences(self):
        return self.sequence_results['with_tail']

    # Helpers:
    def _generate_senso(self):
        self.sequence_results['senso'] = []
        for sequence in self.sequences:
            self.sequence_results['senso'].append(sequence[:-2])

    def _attach_loop(self):
        self.sequence_results['with_loop'] = []
        for senso in self.sequence_results['senso']:
            self.sequence_results['with_loop'].append(senso + RNAiGenerator.loop)

    def _get_reverse_complement(self):
        self.sequence_results['reversed_complement'] = []
        for sequence in self.sequence_results['senso']:
            mutable_sequence = MutableSeq(sequence)
            mutable_sequence.reverse_complement()
            self.sequence_results['reversed_complement'].append(mutable_sequence)

    def _add_tail_to_reversed_complement(self):
        self.sequence_results['with_tail'] = []
        for sequence in self.sequence_results['reversed_complement']:
            self.sequence_results['with_tail'].append(str(sequence) + RNAiGenerator.tail)
