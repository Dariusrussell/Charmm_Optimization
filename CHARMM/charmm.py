from io import StringIO

from CHARMM.charmm_attributes import *


class Charmm:

    def __init__(self, file_path, header_path, atoms, vdws, vdw14s, bonds, angles, ureybrads, torsions,
                 impropers, charges, biotypes):
        self.header_path = header_path
        header_file = open(header_path, 'r')
        self.header = header_file.read()
        header_file.close()
        self.file_path = file_path
        self.atoms = atoms
        self.vdws = vdws
        self.vdw14s = vdw14s
        self.bonds = bonds
        self.angles = angles
        self.ureybrads = ureybrads
        self.torsions = torsions
        self.impropers = impropers
        self.charges = charges
        self.biotypes = biotypes

    @classmethod
    def from_file(cls, file_path, header_path):
        atoms, vdws, vdw14s, bonds, angles, ureybrads, torsions, impropers, charges, biotypes = cls.parse(file_path)
        return cls(file_path, header_path, atoms, vdws, vdw14s, bonds, angles, ureybrads, torsions, impropers, charges,
                   biotypes)

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

    @staticmethod
    def parse(file_path):
        file = open(file_path, 'r')
        file_contents = file.read()
        file.close()
        lines = file_contents.split('\n')
        atoms = []
        vdws = []
        vdw14s = []
        bonds = []
        angles = []
        ureybrads = []
        torsions = []
        impropers = []
        charges = []
        biotypes = []
        for line in lines:
            if re.match(r'atom ', line):
                atoms.append(CharmmAtom.parse(line))
            elif re.match(r'vdw ', line):
                vdws.append(CharmmVDW.parse(line))
            elif re.match(r'vdw14 ', line):
                vdw14s.append(CharmmVDW14.parse(line))
            elif re.match(r'bond ', line):
                bonds.append(CharmmBond.parse(line))
            elif re.match(r'angle ', line):
                angles.append(CharmmAngle.parse(line))
            elif re.match(r'ureybrad ', line):
                ureybrads.append(CharmmUreyBrad.parse(line))
            elif re.match(r'torsion ', line):
                torsions.append(CharmmTorsion.parse(line))
            elif re.match(r'improper ', line):
                impropers.append(CharmmImproper.parse(line))
            elif re.match(r'charge ', line):
                charges.append(CharmmCharge.parse(line))
            elif re.match(r'biotype ', line):
                biotypes.append(CharmmBiotype.parse(line))
        return atoms, vdws, vdw14s, bonds, angles, ureybrads, torsions, impropers, charges, biotypes

    def write_to_file(self, file_name):
        f = open(file_name, 'w')
        f.write(str(self))
        f.close()
        return file_name

    def randomize_bonds(self, bonds, percentage):
        new_bonds = []
        for bond in self.bonds:
            found = False
            for tbr_bond in bonds:
                if {bond.atom_class1, bond.atom_class2} in set([int(i) for i in tbr_bond]):
                    new_bonds.append(bond.random_edit(percentage))
                    found = True
                    break
            if not found:
                new_bonds.append(bond)
        return Charmm(self.file_path, self.header_path, self.atoms, self.vdws, self.vdw14s, new_bonds, self.angles,
                      self.ureybrads, self.torsions, self.impropers, self.charges, self.biotypes)

    def randomize_angles(self, angles, percentage):
        new_angles = []
        new_torsions = []
        for angle in self.impropers:
            found = False
            for tbr_angle in angles:
                if {angle.atom_class1, angle.atom_class2, angle.atom_class3, angle.atom_class4} in set(
                        [int(i) for i in tbr_angle]):
                    new_angles.append(angle.random_edit(percentage))
                    found = True
                    break
            if not found:
                new_angles.append(angle)
        for torsion in self.torsions:
            found = False
            for tbr_angle in angles:
                if {torsion.atom_class1, torsion.atom_class2, torsion.atom_class3, torsion.atom_class4} in set(
                        [int(i) for i in tbr_angle]):
                    new_torsions.append(torsion.random_edit(percentage))
                    found = True
                    break
            if not found:
                new_torsions.append(torsion)
        return Charmm(self.file_path, self.header_path, self.atoms, self.vdws, self.vdw14s, self.bonds, self.angles,
                      self.ureybrads, new_torsions, new_angles, self.charges, self.biotypes)

# charmm = Charmm('../charmm22_start.prm', '../header.txt')
# file = open('../charmm22_test.prm', 'w')
# file.write(str(charmm))
# file.close()
