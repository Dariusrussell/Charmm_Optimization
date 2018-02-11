import re

from CHARMM.charmm_attributes.torsion_subgroup import *


class CharmmTorsion:

    # (torsion)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)
    # ([-+]?[0-9]*\.?[0-9]{3})\s+([-+]?[0-9]*\.?[0-9])\s+(\d+)

    def __init__(self, atom_class1, atom_class2, atom_class3, atom_class4, subgroups):
        self.type = "torsion"
        self.atom_class1 = int(atom_class1)
        self.atom_class2 = int(atom_class2)
        self.atom_class3 = int(atom_class3)
        self.atom_class4 = int(atom_class4)
        self.subgroups = subgroups

    def __str__(self):
        # torsion      13   14   35    3            1.300    0.0  1   0.300    0.0  2   0.420    0.0  3
        substr = '{:>7}   {:>5}{:>5}{:>5}{:>5}'.format(self.type, self.atom_class1, self.atom_class2, self.atom_class3,
                                                       self.atom_class4)
        for subgroup in self.subgroups:
            substr += subgroup.__str__()
        return substr

    @staticmethod
    def parse(string):
        part1 = re.match(r'(torsion)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', string)
        part2 = re.findall(r'([-+]?[0-9]*\.?[0-9]{3})\s+([-+]?[0-9]*\.?[0-9])\s+(\d+)', string)
        subgroups = []

        if part2:
            for subgroup in part2:
                subgroups.append(CharmmTorsionSubgroup(subgroup[0], subgroup[1], subgroup[2]))
        if part1:
            return CharmmTorsion(part1.group(2), part1.group(3), part1.group(4), part1.group(5), subgroups)
        else:
            raise ValueError("Invalid Torsion input: ", string)

    def random_edit(self, percentage):
        return CharmmTorsion(self.atom_class1, self.atom_class2, self.atom_class3, self.atom_class4,
                             [subgroup.random_edit(percentage) for subgroup in self.subgroups])
# f = open('charmm22_2380.prm', 'r')
# param_file = f.read().split('\n')
#
# charmm_atoms = []
#
# for line in param_file:
#     if re.match(r'(torsion)', line):
#         charmm_atoms.append(CharmmTorsion.parse(line))
#
# for atom in charmm_atoms:
#     print(atom)
