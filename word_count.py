def word_count(file_path: str) -> dict:
    """
    Count the frequency of each word in a file.
    """
    counts = {}
    with open(file_path 'r') as f:
        for line in f:
            words = line.split()
            for w in words:
                word = word.lower()
                if word not in counts:
                    counts[word] = 1
                else:
                    counts[word] += 1

    return counts