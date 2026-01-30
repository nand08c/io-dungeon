import random
import re

class Dice:
    rd = random.Random()

    def roll(self, numDsides: str) -> int|None:
        if re.fullmatch(r'[0-9]+d[0-9]+', numDsides):
            num, sides = map(int, numDsides.split('d'))
            total = sum(self.rd.randint(1, sides) for _ in range(num))
            return total
        else:
            return None

_default_dice = Dice()

def roll(spec: str) -> int | None:
    return _default_dice.roll(spec)
