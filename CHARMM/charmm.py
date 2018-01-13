from io import StringIO

from CHARMM.charmm_attributes import *


class Charmm:

    def __init__(self, file_path, header_path):
        header_file = open(header_path, 'r')
        self.header = header_file.read()
        header_file.close()
        self.atoms = []
        self.vdws = []
        self.vdw14s = []
        self.bonds = []
        self.angles = []
        self.ureybrads = []
        self.torsions = []
        self.impropers = []
        self.charges = []
        self.biotypes = []
        self.parse(file_path)

    def __str__(self):
        ret = StringIO()
        ret.write(self.header)
        for atom in self.atoms:
            ret.write(str(atom) + "\n")
        ret.write("\n\n\n")
        for vdw in self.vdws:
            ret.write(str(vdw) + "\n")
        ret.write("\n\n\n")
        for vdw14 in self.vdw14s:
            ret.write(str(vdw14) + "\n")
        ret.write("\n\n\n")
        for bond in self.bonds:
            ret.write(str(bond) + "\n")
        ret.write("\n\n\n")
        for angle in self.angles:
            ret.write(str(angle) + "\n")
        ret.write("\n\n\n")
        for ureybrad in self.ureybrads:
            ret.write(str(ureybrad) + "\n")
        ret.write("\n\n\n")
        for torsion in self.torsions:
            ret.write(str(torsion) + "\n")
        ret.write("\n\n\n")
        for improper in self.impropers:
            ret.write(str(improper) + "\n")
        ret.write("\n\n\n")
        for charge in self.charges:
            ret.write(str(charge) + "\n")
        ret.write("\n\n\n")
        for biotype in self.biotypes:
            ret.write(str(biotype) + "\n")

        return ret.getvalue()

    def parse(self, file_path):
        file = open(file_path, 'r')
        file_contents = file.read()
        file.close()
        lines = file_contents.split('\n')

        for line in lines:
            if re.match(r'atom ', line):
                self.atoms.append(CharmmAtom.parse(line))
            elif re.match(r'vdw ', line):
                self.vdws.append(CharmmVDW.parse(line))
            elif re.match(r'vdw14 ', line):
                self.vdw14s.append(CharmmVDW14.parse(line))
            elif re.match(r'bond ', line):
                self.bonds.append(CharmmBond.parse(line))
            elif re.match(r'angle ', line):
                self.angles.append(CharmmAngle.parse(line))
            elif re.match(r'ureybrad ', line):
                self.ureybrads.append(CharmmUreyBrad.parse(line))
            elif re.match(r'torsion ', line):
                self.torsions.append(CharmmTorsion.parse(line))
            elif re.match(r'improper ', line):
                self.impropers.append(CharmmImproper.parse(line))
            elif re.match(r'charge ', line):
                self.charges.append(CharmmCharge.parse(line))
            elif re.match(r'biotype ', line):
                self.biotypes.append(CharmmBiotype.parse(line))

    def write_to_file(self, file_name):
        f = open(file_name, 'w')
        f.write(str(self))
        f.close()
        return file_name

# charmm = Charmm('../charmm22_start.prm', '../header.txt')
# file = open('../charmm22_test.prm', 'w')
# file.write(str(charmm))
# file.close()
