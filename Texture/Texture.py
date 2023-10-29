import numpy as np
from cubic_ortho_wrapped_tfunction import governor as gsh_governor

"""
This is a first  try to integrate texture functionality into the framework.
However, the creation of texture files is performed in Abaqus! It is though doubtful if this class is required here.
"""


class Texture(object):
    def __init__(self, orientations=None, name='Texture'):
        self.orientations = orientations
        self.name = name
        self.fourier_base, fourier_idx = gsh_governor()
        self.fourier_idx = np.array(fourier_idx)
        self.fourier_coefficients = None #self.calc_fourier_coefficients()

    @classmethod
    def from_file(cls, ori_file, name="Texture", skip_header=0, delimiter=',', convention='Bunge', unit='rad'):
        orientations = np.genfromtxt(ori_file, delimiter=delimiter, skip_header=skip_header)
        if unit == 'deg' or unit == 'degree':
            print("Converting orientations from degree to radians!")
            orientations = np.deg2rad(orientations)
        if convention != 'Bunge':
            raise ValueError("{} is not a valid convetion. Only 'Bunge' angle convetion implemented so far."
                             .format(convention))
        texture = cls(orientations=orientations, name=name)
        return texture

    @classmethod
    def from_alphas(cls, alphas, name="Texture", truncation=12,
                    file_texturehull="boundary_cubic-orthorhombic_3deg.csv"):
        texture = cls(name=name)
        ori_hull = np.genfromtxt(file_texturehull, delimiter=',')
        print(ori_hull.shape)
        n_coeff = len(texture.fourier_idx[texture.fourier_idx[:, 0] <= truncation])
        n_alpha = len(alphas)

        # Set up matrix of single crystal Fourier coefficients (convex hull)
        A = np.zeros((n_coeff, n_alpha))
        for idx_coeff in range(n_coeff):
            scaling = 1
            # scaling = (2 * fourier_idx[idx_coeff, 0] + 1)
            A[idx_coeff, :] = scaling * np.conjugate(
                texture.fourier_base[idx_coeff](ori_hull[:, 0], ori_hull[:, 1], ori_hull[:, 2]))

        # Calculate the fourier coefficients of the polycrystalline texture
        f = A @ np.array(alphas)
        texture.fourier_coefficients = f
        return texture

