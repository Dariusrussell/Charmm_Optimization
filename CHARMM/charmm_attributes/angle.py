import re


class CharmmAngle:

    # (angle)\s+(\d+)\s+(\d+)\s+(\d+)\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)

    def __init__(self, atom_class1, atom_class2, atom_class3, uk1, uk2):
        self.type = "angle"
        self.atom_class1 = int(atom_class1)
        self.atom_class2 = int(atom_class2)
        self.atom_class3 = int(atom_class3)
        self.uk1 = float(uk1)
        self.uk2 = float(uk2)

    def __str__(self):
        # angle         3   10   34      50.00     121.70
        return '{:>5}     {:>5}{:>5}{:>5}{:>11.2f}{:>11.2f}'.format(self.type, self.atom_class1, self.atom_class2,
                                                                    self.atom_class3, self.uk1,self.uk2)

    @staticmethod
    def parse(string):
        match = re.match(r'(angle)\s+(\d+)\s+(\d+)\s+(\d+)\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)', string)
        if match:
            return CharmmAngle(match.group(2), match.group(3), match.group(4), match.group(5), match.group(6))
        else:
            raise ValueError("Invalid Angle input: ", string)

# f = open('charmm22_start.prm', 'r')
# param_file = f.read().split('\n')
#
# charmm_atoms = []
#
# for line in param_file:
#     if re.match(r'(angle)\s+(\d+)\s+(\d+)\s+(\d+)', line):
#         charmm_atoms.append(CharmmAngle.parse(line))
#
# for atom in charmm_atoms:
#     print(atom)
