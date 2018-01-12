import re
from io import StringIO
from Tinker.tinker_atom import *


class TinkerXYZ:

    def __init__(self, size, comment, atoms):
        self.size = size
        self.comment = comment
        self.atoms = atoms

    @classmethod
    def from_file(cls, file_path):
        (size, comment, atoms) = cls.parse(file_path)
        return cls(size, comment, atoms)

    def __str__(self):
        ret = StringIO()

        ret.write(str(self.size))
        if self.comment:
            ret.write(self.comment)
        ret.write("\n")

        for atom in self.atoms:
            ret.write(str(atom))
            ret.write("\n")

        return ret.getvalue()

    @staticmethod
    def parse(file_path):
        f = open(file_path, 'r')
        contents = f.read()
        f.close()
        lines = contents.split("\n")

        file_header = lines[0].strip().split(" ")
        size = int(file_header[0])
        comment = " ".join(file_header[1:])

        atoms = []
        for line in lines[1:]:
            if line:
                atoms.append(TinkerAtom.parse(line.strip()))
        return size, comment, atoms

    def translate_by_vector(self, list_of_vectors):
        if len(list_of_vectors) != len(self.atoms):
            raise ValueError(
                "Vector List: " + str(len(list_of_vectors)) + " does not match the number of atoms: " + str(
                    len(self.atoms)))
        translated_atoms = []
        for i in range(0,len(list_of_vectors)):
            translated_atoms.append(self.atoms[i].translate(list_of_vectors[i]))

        return TinkerXYZ(len(translated_atoms), self.comment, translated_atoms)
