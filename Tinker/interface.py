import re
import subprocess


def tinker_energy(file_path, parameter_path):
    result = subprocess.run(["analyze", file_path, parameter_path, "E"], stdout=subprocess.PIPE)
    result_string = result.stdout.decode('utf-8')
    lines = result_string.split("\n")

    energy = None
    for line in lines:
        match = re.match(r'\s?Total Potential Energy :\s+?([-+]?[0-9]*\.?[0-9]+)', line)
        if match:
            energy = match.group(1)

    return energy
