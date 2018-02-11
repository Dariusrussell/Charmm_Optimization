import random

class CharmmTorsionSubgroup:

    def __init__(self, uk1, uk2, number):
        self.uk1 = float(uk1)
        self.uk2 = float(uk2)
        self.number = int(number)

    def __str__(self):

        # 1.300    0.0  1
        return '  {:>6.3f}{:>7.1f}{:>3}'.format(self.uk1, self.uk2, self.number)

    def random_edit(self, percentage):
        rand = random.uniform(-percentage, percentage)
        change = rand / 100.0
        return CharmmTorsionSubgroup((1 + change) * self.uk1, (1 + change) * self.uk2, self.number)
