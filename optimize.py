import math
import random

import rmsd
from CHARMM import Charmm
from Gaussian.freq import *
from Tinker.interface import *
from Tinker.xyz import *

runsize = 10000

# d_backbone = [['24', '10', '16', '27'], ['16', '10', '24', '14'], ['10', '14', '24', '10'], ['27', '10', '14', '24'],
#               ['14', '10', '27', '16'], ['10', '16', '27', '10']]
#
# # dihedral parameters that includes the carbonyl atoms in the backbone
# d_carbonyl = [['34', '10', '16', '27'], ['34', '10', '24', '14'], ['34', '10', '27', '16']]
#
# # dihedral parameters of the proline rings of the backbone
# d_ring = [['27', '16', '17', '17'], ['16', '17', '17', '18'], ['17', '17', '18', '27'], ['17', '18', '27', '16'],
#           ['17', '16', '27', '18']]
#
# # dihdral parameters that extend into both the proline ring and the backbone
# d_b_r = [['10', '16', '27', '18'], ['10', '16', '17', '17'], ['24', '10', '16', '27'], ['34', '10', '16', '17'],
#          ['14', '10', '27', '18'], ['17', '16', '27', '10'], ['34', '10', '27', '18']]
#
# # bond length parameters in the backbone
# b_backbone = [['16', '27'], ['10', '16'], ['10', '24'], ['14', '24'], ['10', '14'], ['10', '27']]
#
# # SETTINGS
# dihedrals = d_backbone + d_carbonyl + d_ring + d_b_r  # combines all the dihedral groups you want to parametrize
# bonds = b_backbone
maxpercent = 15.00  # max percent of the random change
metropolis_factor = 0.10
# 'temperature' value of metropolis condition; larger values
# of this variable results in accepting higher values more frequently

param = Charmm.from_file(os.path.join(os.getcwd(), 'charmm22_start.prm'), os.path.join(os.getcwd(), 'header.txt'))
tinker_xyz = TinkerXYZ.from_file(os.path.join(os.getcwd(), 'tinker_water.xyz'))
gauss_xyz = TinkerXYZ.from_file(os.path.join(os.getcwd(), 'dft_water.xyz'))
gauss_vibrations = GaussianFreq.from_file(os.path.join(os.getcwd(), 'gauss_freq.log'))


def calculatue_resid(gauss_xyz, tinker_xyz, vibration_pairs):
    resid = rmsd.quaternion_rmsd(gauss_xyz.position_vector(), tinker_xyz.position_vector())
    for pair in vibration_pairs:
        resid += rmsd.quaternion_rmsd(gauss_xyz.translate_by_vector(pair.gaussian_vibration.vector).position_vector(),
                                      tinker_xyz.translate_by_vector(pair.tinker_vibration.vector).position_vector())
    return resid


water_vibrations = Vibrate.from_file(tinker_xyz, param, "water_base_vibrations.xyz", "charmm22_base.prm",
                                     "base_calculation")

pairs = [(1, 7), (2, 8), (3, 9)]

vib_pairs = []
for pair in pairs:
    a = water_vibrations.vibration_list[pair[1] - 1]
    b = gauss_vibrations.vibrations_list[pair[0] - 1]
    vib_pairs.append(VibrationPair(a, b))

resid = calculatue_resid(gauss_xyz, tinker_xyz, vib_pairs)

dihedrals = []
bonds = [[41, 51]]

residualsFile = open("residuals.log", "w")  # output file name will be residuals.log
# writes the starting settings and the selected parameters
residualsFile.write(
    str(dihedrals) + "\n" + str(bonds) + "\nmax percent: " + str(maxpercent) + " metropolis factor: " + str(
        metropolis_factor) + "\n\n")
residualsFile.write("residual start: " + str(resid) + "\n\n")
residualsFile.flush()
os.fsync(residualsFile.fileno())
os.mkdir("charmm_trials")

for i in range(runsize):
    new_param = param.randomize_angles(dihedrals, maxpercent)
    new_param = new_param.randomize_bonds(bonds, maxpercent)

    water_vibrations = Vibrate.from_file(tinker_xyz, new_param, "water_base_vibrations.xyz",
                                         "charmm22_" + str(i) + ".prm",
                                         str(i))
    vib_pairs = []
    for pair in pairs:
        a = water_vibrations.vibration_list[pair[1] - 1]
        b = gauss_vibrations.vibrations_list[pair[0] - 1]
        vib_pairs.append(VibrationPair(a, b))

    new_resid = calculatue_resid(gauss_xyz, tinker_xyz, vib_pairs)

    if new_resid < resid:
        resid = new_resid
        residualsFile.write(str(i) + " residual: " + str(resid) + " new minimum \n\n")
        os.chdir("charmm_trials")
        new_param.write_to_file("charmm22" + str(i) + ".prm")
        os.chdir("..")
        param = new_param
    else:
        random_number = random.random()
        factor = math.exp(-(new_resid - resid) / metropolis_factor)  # calculates metropolis condition
        residualsFile.write(str(random_number) + " " + str(factor) + " test\n")
        if random_number < factor:
            resid = new_resid  # accept higher residual
            residualsFile.write(str(i) + " residual: " + str(new_resid) + " higher accepted \n\n")
            param = new_param
            os.chdir("charmm_trials")
            new_param.write_to_file("charmm22" + str(i) + ".prm")
            os.chdir("..")
        else:
            residualsFile.write(str(i) + " residual: " + str(new_resid) + " higher rejected \n\n")
    residualsFile.flush()
    os.fsync(residualsFile.fileno())
residualsFile.write("Total iterations: " + str(runsize))
residualsFile.close()
