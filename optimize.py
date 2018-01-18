import rmsd
from CHARMM import Charmm
from Gaussian.freq import *
from Tinker.interface import *
from Tinker.xyz import *

runsize = 10000

param = Charmm(os.path.join(os.getcwd(), 'charmm22_start.prm'), os.path.join(os.getcwd(), 'header.txt'))
water_xyz = TinkerXYZ.from_file(os.path.join(os.getcwd(), 'tinker_water.xyz'))
gauss_xyz = TinkerXYZ.from_file(os.path.join(os.getcwd(), 'gauss_water.xyz'))
gauss_vibrations = GaussianFreq.from_file(os.path.join(os.getcwd(), 'gauss_freq.log'))


# tinker_calc_freq = Vibrate.from_file(water_xyz, param, 'tinker_water.xyz', 'charmm_water.prm', 'tinker_water_freq')

# path, result = minimize(os.path.join(os.getcwd(), 'tinker_water.xyz'), os.path.join(os.getcwd(), 'charmm22_start.prm'),
#                         0.01)


def calculatue_resid(gauss_xyz, tinker_xyz, vibration_pairs):
    resid = rmsd.quaternion_rmsd(gauss_xyz.position_vector(), tinker_xyz.position_vector())
    for pair in vibration_pairs:
        resid += rmsd.quaternion_rmsd(gauss_xyz.translate_by_vector(pair.gauss_vibration).position_vector(),
                                      tinker_xyz.translate_by_vector(pair.tinkter_vibration))
    return resid
