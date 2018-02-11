import os
import re
import subprocess
from io import StringIO

import numpy as np


def tinker_energy(file_path, parameter_path):  # TODO make Energy interface a class
    result = subprocess.run(["analyze", file_path, parameter_path, "E"], stdout=subprocess.PIPE)
    result_string = result.stdout.decode('utf-8')
    lines = result_string.split("\n")

    energy = None
    for line in lines:
        match = re.match(r'\s?Total Potential Energy :\s+?([-+]?[0-9]*\.?[0-9]+)', line)
        if match:
            energy = match.group(1)

    return energy


class Vibrate:

    def __init__(self, vibration_list, folder_basepath, xyz_path, param_path, xyz, param):
        self.vibration_list = vibration_list
        self.folder_basepath = folder_basepath
        self.xyz_path = xyz_path
        self.param_path = param_path
        self.xyz = xyz
        self.param = param

    def __str__(self):
        buf = StringIO()
        buf.write("Tinker-Generated Vibration\n")
        buf.write("Located in Folder: ")
        buf.write(self.folder_basepath)
        buf.write("\n")
        buf.write("Generated from XYZ File: ")
        buf.write(self.xyz_path)
        buf.write("\n")
        buf.write("Generated from Parameter File: ")
        buf.write(self.param_path)
        buf.write("\n\n\n")
        buf.write(str(self.xyz))
        buf.write("\n\n\n")
        buf.write(str(self.param))

        for vibration in self.vibration_list:
            buf.write(str(vibration))
            buf.write("\n")

        return buf.getvalue()

    @classmethod
    def from_file(cls, xyz, param, xyz_name, param_name, folder_name):
        os.mkdir(os.path.join(os.getcwd(), folder_name))
        folder_basepath = os.path.join(os.getcwd(), folder_name)
        os.chdir(os.path.join(os.getcwd(), folder_name))
        xyz_path = os.path.join(os.getcwd(), xyz_name)
        param_path = os.path.join(os.getcwd(), param_name)
        xyz_file = xyz.write_to_file(os.path.join(os.getcwd(), xyz_name))
        param_file = param.write_to_file(os.path.join(os.getcwd(), param_name))
        result = subprocess.run(["vibrate", xyz_file, param_file, "all"], stdout=subprocess.PIPE)
        result_string = result.stdout.decode('utf-8')
        lines = result_string.split("\n")

        vibrations_list = []
        current_vector = None
        current_id = None
        current_frequency = None
        # print(result_string)
        for line in lines:
            match = re.match(r'Vibrational Normal Mode\s+(\d+) with Frequency\s+([-+]?[0-9]*\.?[0-9]+) cm-1',
                             line.strip())
            if match:
                if current_vector is not None:
                    vibrations_list.append(Vibration(current_id, current_frequency, current_vector))
                current_id = match.group(1)
                current_frequency = match.group(2)
                current_vector = None

            vector_match = re.match(r'\d+\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)$',
                                    line.strip())

            if vector_match:
                if current_vector is None:
                    current_vector = np.array([np.float64(vector_match.group(1)), np.float64(vector_match.group(2)),
                                               np.float64(vector_match.group(3))])
                else:
                    current_vector = np.vstack([current_vector,
                                                [np.float64(vector_match.group(1)), np.float64(vector_match.group(2)),
                                                 np.float64(vector_match.group(3))]])
        vibrations_list.append(Vibration(current_id, current_frequency, current_vector))

        os.chdir('..')
        return cls(vibrations_list, folder_basepath, xyz_path, param_path, xyz, param)


class Vibration:

    def __init__(self, vibration_id, frequency, vector):
        self.vibration_id = int(vibration_id)
        self.frequency = float(frequency)
        if type(vector) != np.ndarray:
            raise ValueError("Vector must be of type np.ndarray")
        else:
            self.vector = np.squeeze(vector)

    def __str__(self):
        buf = StringIO()
        buf.write(str(self.vibration_id))
        buf.write("\n")
        buf.write(str(self.frequency))
        buf.write("\n")
        buf.write(str(self.vector))
        buf.write("\n")
        return buf.getvalue()


def minimize(file_path, parameter_path, cutoff):
    result = subprocess.run(["minimize", file_path, parameter_path, str(cutoff)], stdout=subprocess.PIPE)
    result_string = result.stdout.decode('utf-8')
    new_name = file_path[:-4] + "_min.xyz"
    os.rename(file_path + '_2', new_name)

    return new_name, result_string


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
