import re
from io import StringIO
from Tinker.tinker_atom import *


class TinkerXYZ:

    def __init__(self, file_path):
        self.file_path = file_path
        self.size = None
        self.comment = None
        self.atoms = []
        self.parse(self.file_path)

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

    def parse(self, file_path):
        f = open(file_path, 'r')
        contents = f.read()
        f.close()
        lines = contents.split("\n")

        file_header = lines[0].strip().split(" ")
        self.size = int(file_header[0])
        self.comment = " ".join(file_header[1:])

        for line in lines[1:]:
            if line:
                self.atoms.append(TinkerAtom.parse(line.strip()))