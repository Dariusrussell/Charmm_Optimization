import re


class CharmmAtom:
    # (atom)\s+(\d+)\s+(\d+)\s+(\w+)\s+(\".+\")\s+(\d+)\s+([-+]?[0-9]*\.?[0-9]+)\s+(\d+)

    def __init__(self, atom_id, atom_class, atom_type, atom_name, uk1, atomic_weight, uk2):
        self.type = "atom"
        self.atom_id = int(atom_id)
        self.atom_class = int(atom_class)
        self.atom_type = atom_type
        self.atom_name = atom_name
        self.uk1 = int(uk1)
        self.atom_weight = float(atomic_weight)
        self.uk2 = int(uk2)

    def __str__(self):
        # atom          1    1    HA    "Nonpolar Hydrogen"            1     1.008    1
        return '{:>4}{:>11}{:>5}    {:6}{:27}{:>5}{:>10.3f}{:>5}'.format(self.type, self.atom_id, self.atom_class,
                                                                             self.atom_type, self.atom_name, self.uk1,
                                                                             self.atom_weight, self.uk2)

    @staticmethod
    def parse(string):
        match = re.match(r'(atom)\s+(\d+)\s+(\d+)\s+(\w+)\s+(\".+\")\s+(\d+)\s+([-+]?[0-9]*\.?[0-9]+)\s+(\d+)', string)
        if match:
            return CharmmAtom(match.group(2), match.group(3), match.group(4), match.group(5),
                              match.group(6), match.group(7), match.group(8))
        else:
            raise ValueError("Invalid Atom Input: ", string)


# f = open('charmm22_2380.prm', 'r')
# param_file = f.read().split('\n')
#
# charmm_atoms = []
#
# for line in param_file:
#     if re.match(r'atom \s+\d+', line):
#         charmm_atoms.append(CharmmAtom.parse(line))
#
# for atom in charmm_atoms:
#     print(atom)
