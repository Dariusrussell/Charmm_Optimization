import re


class CharmmBiotype:

    # (biotype)\s+(\d+)\s+(\w+)\s+(\".+\")\s+([+|-]?\d+)

    def __init__(self, biotype_num, atom_type, atom_name, charmm_id):
        self.type = "biotype"
        self.biotype_num = int(biotype_num)
        self.atom_type = atom_type
        self.atom_name = atom_name
        self.charmm_id = charmm_id

    def __str__(self):
        # biotype       1    N       "Glycine"                          63
        return '{:>7}       {:<5}{:8}{:30}{:>7}'.format(self.type, self.biotype_num, self.atom_type, self.atom_name,
                                                        self.charmm_id)

    @staticmethod
    def parse(string):
        match = re.match(r'(biotype)\s+(\d+)\s+(\w+)\s+(\".+\")\s+([+|-]?\d+)', string)
        if match:
            return CharmmBiotype(match.group(2), match.group(3), match.group(4), match.group(5))
        else:
            raise ValueError("Invalid Biotype input: ", string)


# f = open('../charmm22_2380.prm', 'r')
# param_file = f.read().split('\n')
#
# charmm_atoms = []
#
# for line in param_file:
#     if re.match(r'(biotype)', line):
#         charmm_atoms.append(CharmmBiotype.parse(line))
#
# for atom in charmm_atoms:
#     print(atom)
