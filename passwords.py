from string import ascii_letters, digits, punctuation
from random import choice

gen: list = list(ascii_letters + digits + punctuation)

class Generator:
    def __init__(self):
        pass

    def get(self) -> str:
        return "".join(choice(gen) for _ in range(8))
