import numpy as np


def rp_hash(person):
    person_hash = 5381
    value = person.upper()
    for char in value:
        person_hash = ((np.left_shift(person_hash, 5) + person_hash) + ord(char))
    person_hash = np.int32(person_hash)
    return str(person_hash)
