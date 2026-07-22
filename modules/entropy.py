import math


def calculate_entropy(password_length: int, charset_size: int) -> float:
    """
    Hitung entropy password dalam bit.
    Entropy = length * log2(charset_size)
    """
    if password_length <= 0 or charset_size <= 0:
        return 0.0

    return password_length * math.log2(charset_size)
