from io import StringIO

from Tinker.atom import *


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

    def translate_by_vector(self, np_array):
        if type(np_array) != np.ndarray:
            raise ValueError("Vector: " + str(type(np_array)) + " is not a numpy array")

        if np_array.shape[0] != len(self.atoms):
            raise ValueError(
                "Vector List: " + str(np_array.shape[0]) + " does not match the number of atoms: " + str(
                    len(self.atoms)))

        if np_array.shape[1] != 3:
            raise ValueError("Vector List does not have a 2nd dimension of length 3 corresponding to xyz direction")

        translated_atoms = []
        for i in range(0, len(np_array)):
            translated_atoms.append(self.atoms[i].translate(np_array[i]))

        return TinkerXYZ(len(translated_atoms), self.comment, translated_atoms)

    def write_to_file(self, file_name):
        f = open(file_name, 'w')
        f.write(str(self))
        f.close()
        return file_name

# tinker = TinkerXYZ.from_file('../cyclohexane.xyz')
#
# vector = np.array([10, 10, 10])
#
# for i in range(1, tinker.size):
#     vector = np.vstack((vector, [10, 10, 10]))
#
# translated_tinker = tinker.translate_by_vector(vector)
# print(translated_tinker)
