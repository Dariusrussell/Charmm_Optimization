import re

import numpy as np


class TinkerAtom:

    def __init__(self, atom_id, atom_type, xyz, ff_type, partners):
        self.atom_id = int(atom_id)
        self.atom_type = atom_type
        if type(xyz) != np.ndarray:
            self.xyz = np.array([float(i) for i in xyz])
        else:
            self.xyz = xyz
        self.ff_type = int(ff_type)
        self.partners = [int(i) for i in partners]
        self.partners_by_ref = []
        self.partners_by_ref_populated = False

    def __str__(self):
        #   1 N      -2.305000   -4.660000   -1.525000     66    2    8  122
        ret = '{:>5} {:<6}{:>9.6f}   {:>9.6f}   {:>9.6f}{:>6}'.format(self.atom_id, self.atom_type, self.xyz[0],
                                                                      self.xyz[1], self.xyz[2], self.ff_type)
        if self.partners:
            for partner in self.partners:
                ret += '{:>6}'.format(int(partner))

        return ret

    @staticmethod
    def parse(line):
        attributes = re.split(r'\s+', line)
        if len(attributes) > 6:
            return TinkerAtom(attributes[0], attributes[1], attributes[2:5], attributes[5], attributes[6:])
        else:
            return TinkerAtom(attributes[0], attributes[1], attributes[2:5], attributes[5], [])

    def translate(self, vector):
        if type(vector) != np.ndarray:
            raise ValueError("Vector: " + str(type(vector)) + " is not a numpy array")
        if self.xyz.shape != vector.shape:
            raise ValueError("Vector: " + vector + " is not a valid xyz vector")
        new_vector = self.xyz + vector
        return TinkerAtom(self.atom_id, self.atom_type, new_vector, self.ff_type, self.partners)
