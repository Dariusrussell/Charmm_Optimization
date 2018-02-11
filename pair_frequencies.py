import sys

from CHARMM import Charmm
from Gaussian.freq import *
from Tinker.interface import *
from Tinker.xyz import *


def normalize(a, axis=-1, order=1):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2 == 0] = 1
    return a / np.expand_dims(l2, axis)


def compute_dot_product(a, b):
    a_u = np.squeeze(normalize(a))
    b_u = np.squeeze(normalize(b))
    return np.arccos(np.clip(np.dot(a_u, b_u), -1.0, 1.0))


class VibrationPair:

    def __init__(self, gaussian_vibration, tinker_vibration, angle_diff=None):
        self.gaussian_vibration = gaussian_vibration
        self.tinker_vibration = tinker_vibration
        self.angle_diff = angle_diff

    def __str__(self):
        buf = StringIO()
        buf.write("Gaussian Vector: ")
        buf.write(str(self.gaussian_vibration.vibration_id))
        buf.write("\n")
        buf.write(str(self.gaussian_vibration))
        buf.write("\n\n")
        buf.write("Tinker Vector: ")
        buf.write(str(self.tinker_vibration.vibration_id))
        buf.write("\n")
        buf.write(str(self.tinker_vibration))
        buf.write("\n")
        buf.write(str(self.angle_diff))
        buf.write("\n")
        buf.write("------------------\n")
        return buf.getvalue()


# Check if vectors are out of phase by 180

def pair_vibrations(gaussian_freq, tinker_freq):
    vibration_pairs = []
    for gauss in gaussian_freq.vibrations_list:
        min_angle_sum = sys.float_info.max
        best_match = None
        for tinker in tinker_freq.vibration_list[6:]:
            current_angle_sum = 0
            for i in range(0, gauss.vector.shape[0]):
                angle = compute_dot_product(gauss.vector[i], tinker.vector[i])
                angle_rot_180 = compute_dot_product(gauss.vector[i], tinker.vector[i] * -1)
                if angle_rot_180 < angle:
                    angle = angle_rot_180
                current_angle_sum += angle
            if current_angle_sum < min_angle_sum:
                min_angle_sum = current_angle_sum
                best_match = tinker
        vibration_pairs.append(VibrationPair(gauss, best_match, angle_diff=min_angle_sum))
    return vibration_pairs


param = Charmm.from_file(os.path.join(os.getcwd(), 'charmm22_start.prm'), os.path.join(os.getcwd(), 'header.txt'))
water_xyz = TinkerXYZ.from_file(os.path.join(os.getcwd(), 'tinker_water.xyz'))
gauss_vibrations = GaussianFreq.from_file(os.path.join(os.getcwd(), 'gauss_freq.log'))
tinker_calc_freq = Vibrate.from_file(water_xyz, param, 'tinker_water.xyz', 'charmm_water.prm', 'tinker_water_freq')

water_xyz.translate_by_vector(tinker_calc_freq.vibration_list[7].vector).write_to_file("tinker_water_vib8.xyz")
water_xyz.translate_by_vector(gauss_vibrations.vibrations_list[1].vector).write_to_file("gauss_water_vib2.xyz")

pairs = pair_vibrations(gauss_vibrations, tinker_calc_freq)

for pair in pairs:
    print(pair)
