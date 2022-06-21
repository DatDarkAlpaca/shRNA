def calculate_gc(sequence: str) -> float:
    return (sequence.count('G') + sequence.count('C')) / len(sequence) * 100
