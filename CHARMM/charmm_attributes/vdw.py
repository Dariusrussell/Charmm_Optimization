import re


class CharmmVDW:

    # (vdw)\s+(\d+)\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)

    def __init__(self, atom_class, uk1, uk2):
        self.type = "vdw"
        self.atom_class = int(atom_class)
        self.uk1 = float(uk1)
        self.uk2 = float(uk2)

    def __str__(self):

        # vdw           1               1.3200    -0.0220
        # vdw          80               2.1500    -0.5850
        return '{:>3}{:>12}          {:>11.4f}{:>11.4f}'.format(self.type, self.atom_class, self.uk1, self.uk2)

    @staticmethod
    def parse(string):
        match = re.match(r'(vdw)\s+(\d+)\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)', string)
        if match:
            return CharmmVDW(match.group(2), match.group(3), match.group(4))
        else:
            raise ValueError("Invalid VDW input: ", string)


# f = open('charmm22_2380.prm', 'r')
# param_file = f.read().split('\n')
#
# charmm_atoms = []
#
# for line in param_file:
#     if "vdw " in line:
#         charmm_atoms.append(CharmmVDW.parse(line))
#
# for atom in charmm_atoms:
#     print(atom)
