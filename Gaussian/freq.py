import re
from io import StringIO

import numpy as np

from Tinker.interface import Vibration


class GaussianFreq:

    def __init__(self, vibrations_list, log_file_path):
        self.vibrations_list = vibrations_list
        self.log_file_path = log_file_path

    @classmethod
    def from_file(cls, log_file_path):
        f = open(log_file_path, 'r')
        file = f.read()
        f.close()
        lines = file.split("\n")

        vibrations = []
        vibration1_id = None
        vibration2_id = None
        vibration3_id = None
        vibration1_frequency = None
        vibration2_frequency = None
        vibration3_frequency = None
        vibration1_vector = None
        vibration2_vector = None
        vibration3_vector = None
        for line in lines:
            header_match = re.match(r'^(\d+)\s+(\d+)\s+(\d+)$', line.strip())

            if header_match:
                if vibration1_id is not None:
                    if int(vibration1_id) > int(header_match.group(1)):
                        break
                    vibrations.append(Vibration(vibration1_id, vibration1_frequency, vibration1_vector))
                    vibrations.append(Vibration(vibration2_id, vibration2_frequency, vibration2_vector))
                    vibrations.append(Vibration(vibration3_id, vibration3_frequency, vibration3_vector))
                vibration1_id = header_match.group(1)
                vibration2_id = header_match.group(2)
                vibration3_id = header_match.group(3)
                vibration1_frequency = None
                vibration2_frequency = None
                vibration3_frequency = None
                vibration1_vector = None
                vibration2_vector = None
                vibration3_vector = None

            frequency_match = re.match(
                r'^Frequencies --\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)$',
                line.strip())

            if frequency_match:
                vibration1_frequency = frequency_match.group(1)
                vibration2_frequency = frequency_match.group(2)
                vibration3_frequency = frequency_match.group(3)

            vector_re = re.compile(
                r'^\d+\s+\d+\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)'
                r'\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)'
                r'\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)'
                r'\s+([-+]?[0-9]*\.?[0-9]+)$')

            vector_match = vector_re.match(line.strip())

            if vector_match:
                if vibration1_vector is None:
                    vibration1_vector = np.array([np.float64(vector_match.group(1)), np.float64(vector_match.group(2)),
                                                  np.float64(vector_match.group(3))])
                    vibration2_vector = np.array([np.float64(vector_match.group(4)), np.float64(vector_match.group(5)),
                                                  np.float64(vector_match.group(6))])
                    vibration3_vector = np.array([np.float64(vector_match.group(7)), np.float64(vector_match.group(8)),
                                                  np.float64(vector_match.group(9))])
                else:
                    vibration1_vector = np.vstack(
                        [vibration1_vector, [np.float64(vector_match.group(1)), np.float64(vector_match.group(2)),
                                             np.float64(vector_match.group(3))]])
                    vibration2_vector = np.vstack(
                        [vibration2_vector, [np.float64(vector_match.group(4)), np.float64(vector_match.group(5)),
                                             np.float64(vector_match.group(6))]])
                    vibration3_vector = np.vstack(
                        [vibration3_vector, [np.float64(vector_match.group(7)), np.float64(vector_match.group(8)),
                                             np.float64(vector_match.group(9))]])
        vibrations.append(Vibration(vibration1_id, vibration1_frequency, vibration1_vector))
        vibrations.append(Vibration(vibration2_id, vibration2_frequency, vibration2_vector))
        vibrations.append(Vibration(vibration3_id, vibration3_frequency, vibration3_vector))

        return cls(vibrations, log_file_path)

    def __str__(self):
        buf = StringIO()
        buf.write("Gaussian-Generated Vibrations\n")
        buf.write("Generated from: ")
        buf.write(self.log_file_path)
        buf.write("\n")
        for vibration in self.vibrations_list:
            buf.write(str(vibration))
            buf.write("\n")

        return buf.getvalue()
