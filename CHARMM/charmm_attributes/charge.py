import re


class CharmmCharge:

    # (charge)\s+(\d+)\s+([-+]?[0-9]*\.?[0-9]+)

    def __init__(self, atom_number, charge):
        self.type = "charge"
        self.atom_number = int(atom_number)
        self.charge = float(charge)

    def __str__(self):
        # charge        1               0.0900
        return '{:>6}{:>9}{:>21.4f}'.format(self.type, self.atom_number, self.charge)

    @staticmethod
    def parse(string):
        match = re.match(r'(charge)\s+(\d+)\s+([-+]?[0-9]*\.?[0-9]+)', string)
        if match:
            return CharmmCharge(match.group(2), match.group(3))
        else:
            raise ValueError("Invalid Charge input: ", string)


# f = open('charmm22_2380.prm', 'r')
# param_file = f.read().split('\n')
#
# charmm_atoms = []
#
# for line in param_file:
#     if re.match(r'(charge)', line):
#         charmm_atoms.append(CharmmCharge.parse(line))
#
# for atom in charmm_atoms:
#     print(atom)
