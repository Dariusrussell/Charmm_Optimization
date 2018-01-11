import re


class CharmmBond:

    # (bond)\s+(\d+)\s+(\d+)\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)

    def __init__(self, atom_class1, atom_class2, uk1, uk2):
        self.type = "bond"
        self.atom_class1 = int(atom_class1)
        self.atom_class2 = int(atom_class2)
        self.uk1 = float(uk1)
        self.uk2 = float(uk2)

    def __str__(self):

        # bond          1   10          330.00     1.1000
        return '{:>4}      {:>5}{:>5}     {:>11.2f}     {:>11.4f}'.format(self.type, self.atom_class1, self.atom_class2,
                                                                          self.uk1, self.uk2)

    @staticmethod
    def parse(string):
        match = re.match(r'(bond)\s+(\d+)\s+(\d+)\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)', string)
        if match:
            return CharmmBond(match.group(2), match.group(3), match.group(4), match.group(5))
        else:
            raise ValueError("Invalid Bond input: ", string)


# f = open('charmm22_2380.prm', 'r')
# param_file = f.read().split('\n')
#
# charmm_atoms = []
#
# for line in param_file:
#     if "bond " in line:
#         charmm_atoms.append(CharmmBond.parse(line))
#
# for atom in charmm_atoms:
#     print(atom)