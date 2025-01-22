import numpy as np
from matplotlib import pyplot as plt
import json
import pandas as pd

def intersect(s_eq, e_eq, plot=True):
    """
    Calculates the elastic line from hom. stress and equiv. strain and determines intersection with stress-strain curve.
    Parameters
    ----------
    s_eq : array-like
        Array of equivalent stresses
    e_eq : array-like
        Array of equivalent total strains
    plot : bool, default=False
        whether the stress-strain curve + intersection should be plotted

    Returns
    -------
    x : double
        value of equivalent strain at which elastic line intersects stress strain curve
    y : double
        value of equivalent stress at which elastic line intersects stress strain curve
    top : int
        index in s_eq and e_eq that is just above the intersection point
    bot : int
        index in s_eq and e_eq that is just below the intersection point
    """
    # Set up intersecting line with m at 0.002 strain
    m_1 = 0.0
    for j in range(10, 21, 5):
        m_1 += s_eq[j] / e_eq[j]
    m_1 /= 3
    c_1 = s_eq[15] - m_1 * (e_eq[15] + 0.002)

    # find intersection interval
    s_eq = np.array(s_eq)
    e_eq = np.array(e_eq)
    s_l = m_1 * e_eq + c_1

    diff = s_eq - s_l
    try:
        top = np.where(diff < 0)[0][0]
    except IndexError:
        print(
            "Plastic strain is too low. The line with slope E=%6.2f MPa is not intersecting the stress-strain curve.\n"
            "To solve this issue, increase load and rerun simulation." % m_1)
        raise
    bot = top - 1

    # define line in this interval
    m_2 = (s_eq[top] - s_eq[bot]) / (e_eq[top] - e_eq[bot])
    c_2 = s_eq[top] - m_2 * e_eq[top]

    # find intersetion point
    x = (c_2 - c_1) / (m_1 - m_2)
    y = m_1 * x + c_1

    if plot:
        fig = plt.figure(figsize=(10, 6), dpi=200)
        ax = fig.add_subplot()
        ax.plot(e_eq, s_eq, label='CPFEM', marker='x')
        ax.plot(e_eq, s_l, marker='.', color='k')
        ax.plot(x, y, marker='x', color='r')
        ax.legend(loc="lower right")
        ax.set_title('Stress-Strain Curve', pad=20)
        ax.set_ylim(0, np.max(s_eq))
        plt.xlabel('$E_{vM}$')
        plt.ylabel('$S_{vM}$ [MPa]')

    return x, y, top, bot


def calc_yield_point(result_file, plot=False, write_strains=False):
    """
    Function that calculates the homogenized yield onset at 0.2 % equivalent plastic strain from a result dict object.
    Parameters
    ----------
    result_file : dict
        Dictionary containing the homogenized CP results
    plot : bool, default=False
        whether the stress-strain curve + intersection should be plotted

    Returns
    -------
    syld : array-like
        homogenized yield onset at 0.2 % plastic strain
    """
    # Assumes a the 'Results' dict of Data_Base.json
    s_eq = result_file['S']
    e_eq = result_file['E']
    stresses = pd.DataFrame(result_file, columns=['S11', 'S22', 'S33', 'S32', 'S13', 'S12'])
    strains_pl = pd.DataFrame(result_file, columns = ['Ep11', 'Ep22', 'Ep33', 'Ep32', 'Ep13', 'Ep12'])

    # Interpolate between equivalent stresses and scale up
    try:
        x, y, top, bot = intersect(s_eq, e_eq, plot=plot)
    except IndexError:
        raise
    if s_eq[top] - s_eq[bot] <= 1e-5:
        print('WARNING: stress difference too small for interpolation of {res}'.format(res=result_file))
        print(y-s_eq[bot])
        s_yld = stresses.iloc[bot].values
        # print(stresses.iloc[bot].values)
        # print('openp seq: {}'.format(s_eq[bot]))
        # print('pylab seq: {}'.format(FE.seq_J2(stresses.iloc[bot].values)))
    else:
        if not write_strains:
            s_yld = stresses.iloc[bot].values + (stresses.iloc[top].values - stresses.iloc[bot].values) * \
                    (y - s_eq[bot]) / (s_eq[top] - s_eq[bot])
        else:
            s_yld = strains_pl.iloc[bot].values + (strains_pl.iloc[top].values - strains_pl.iloc[bot].values) * \
                    (y - s_eq[bot]) / (s_eq[top] - s_eq[bot])
    return s_yld