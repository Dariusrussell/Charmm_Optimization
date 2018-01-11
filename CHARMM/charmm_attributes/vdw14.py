import re


class CharmmVDW14:

    # (vdw14)\s+(\d+)\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)

    def __init__(self, atom_class, uk1, uk2):
            self.type = "vdw14"
            self.atom_class = int(atom_class)
            self.uk1 = float(uk1)
            self.uk2 = float(uk2)

    def __str__(self):
            # vdw14        13               1.9000    -0.0100
            return '{:>5}{:>10}          {:>11.4f}{:>11.4f}'.format(self.type, self.atom_class, self.uk1, self.uk2)

    @staticmethod
    def parse(string):
        match = re.match(r'(vdw14)\s+(\d+)\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)', string)
        if match:
            return CharmmVDW14(match.group(2), match.group(3), match.group(4))
        else:
            raise ValueError("Invalid VDW14 input: ", string)


# f = open('charmm22_2380.prm', 'r')
# param_file = f.read().split('\n')
#
# charmm_atoms = []
#
# for line in param_file:
#     if "vdw14 " in line:
#         charmm_atoms.append(CharmmVDW14.parse(line))
#
# for atom in charmm_atoms:
#     print(atom)
