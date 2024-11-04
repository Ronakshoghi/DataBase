import numpy as np
import pylabfea as FE
from matplotlib import pyplot as plt

"""
This script is used to transform the cartesian unit stresses to the cylindrical  stress space and then extract their 
polar angles. The polar angles will be used in Matlab to sample the CY polynomial for the yield onset.
"""

sunit = FE.load_cases(number_3d=100, number_6d=0)
sunit_cyl = FE.s_cyl(sunit)

neg_idx = [angle for angle in sunit_cyl[:, 1] < 0]
neg_stresses = sunit_cyl[neg_idx, :]
neg_stresses_add = np.array([neg_stresses[:, 0], neg_stresses[:, 1] + 2*np.pi, neg_stresses[:, 2]]).T

sunit_cyl_transformed = []
idx_check = []
for count, stress in enumerate(sunit_cyl):
    if stress[1] < 0:
        stress[1] = stress[1] + 2*np.pi
        idx_check.append(count)
    sunit_cyl_transformed.append(stress)
sunit_cyl_transformed = np.array(sunit_cyl_transformed)

fig = plt.figure(figsize=(9, 9), dpi=400)
ax = fig.add_subplot(projection='polar')
ax.scatter(sunit_cyl_transformed[neg_idx, 1], sunit_cyl_transformed[neg_idx, 0], s=50)
ax.scatter(neg_stresses[:, 1], neg_stresses[:, 0], s=20)
plt.show()
#np.savetxt("angles_cyl_100.csv", sunit_cyl_transformed, delimiter=",")

