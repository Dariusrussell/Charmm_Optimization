import random
import re


class CharmmImproper:

    # (improper)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)

    def __init__(self, atom_class1, atom_class2, atom_class3, atom_class4, uk1, uk2):
        self.type = "improper"
        self.atom_class1 = int(atom_class1)
        self.atom_class2 = int(atom_class2)
        self.atom_class3 = int(atom_class3)
        self.atom_class4 = int(atom_class4)
        self.uk1 = float(uk1)
        self.uk2 = float(uk2)

    def __str__(self):
        # improper     10   13   24   34           120.00       0.00
        return '{:>8}  {:>5}{:>5}{:>5}{:>5}      {:>11.2f}{:>11.2f}'.format(self.type, self.atom_class1,
                                                                            self.atom_class2, self.atom_class3,
                                                                            self.atom_class4, self.uk1, self.uk2)

    @staticmethod
    def parse(string):
        match = re.match(r'(improper)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)'
                         , string)
        if match:
            return CharmmImproper(match.group(2), match.group(3), match.group(4), match.group(5), match.group(6),
                                  match.group(7))
        else:
            raise ValueError("Invalid UreyBrad input: ", string)

    def random_edit(self, percentage):
        rand = random.uniform(-percentage, percentage)
        change = rand / 100.0
        return CharmmImproper(self.atom_class1, self.atom_class2, self.atom_class3, self.atom_class4,
                              (1 + change) * self.uk1,
                              (1 + change) * self.uk2)

# f = open('charmm22_2380.prm', 'r')
# param_file = f.read().split('\n')
#
# charmm_atoms = []
#
# for line in param_file:
#     if re.match(r'(improper)\s+(\d+)\s+(\d+)\s+(\d+)', line):
#         charmm_atoms.append(CharmmImproper.parse(line))
#
# for atom in charmm_atoms:
#     print(atom)
