def calculate_gc(sequences: list):
    results = []

    for senso in sequences:
        results.append(((senso.count('G')) + (senso.count('C'))) / len(senso) * 100)

    return results
