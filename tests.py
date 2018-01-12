from CHARMM import *
from Tinker.interface import *
from Tinker.xyz import *

xyz = TinkerXYZ.from_file(os.path.join(os.getcwd(), 'cyclohexane.xyz'))
prm = Charmm(os.path.join(os.getcwd(), 'charmm22_2380.prm'), os.path.join(os.getcwd(), 'header.txt'))

cyclohex_vib = Vibrate.from_file(xyz, prm, 'cyc_test.xyz', 'charmm22_test.prm', 'test')

print(cyclohex_vib)
