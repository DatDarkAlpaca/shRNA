def calculate_gc(sequence: str) -> float:
    return round((sequence.count('G') + sequence.count('C')) / len(sequence) * 100, 2)
