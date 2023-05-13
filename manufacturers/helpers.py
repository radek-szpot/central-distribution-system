import random
from enum import Enum


def generate_random_number(start=1, end=100):
    return random.randint(start, end)


def generate_random_fruit():
    return list(ProductEnumType)[generate_random_number(0, 3)]


class ProductEnumType(str, Enum):
    APPLE = 'apple'
    BANANA = 'banana'
    ORANGE = 'orange'
    PEAR = 'pear'
