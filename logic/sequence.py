import random
from config import SIMILAR_MAP, CHARSETS

def get_alphabet(charset_name: str) -> str:
    return CHARSETS[charset_name]

def generate_sequence(length: int, alphabet: str) -> list[str]:
    return [random.choice(alphabet) for _ in range(length)]

def maybe_mutate_sequence(sequence, probability, alphabet):
    # If no mutation should happen, return original sequence
    if random.random() >= probability:
        return sequence.copy(), None

    # Choose a random position to mutate
    index = random.randrange(len(sequence))
    original = sequence[index]
    
    new_value = random.choice(SIMILAR_MAP[original])

    
    mutated = sequence.copy()
    mutated[index] = new_value
    return mutated, index