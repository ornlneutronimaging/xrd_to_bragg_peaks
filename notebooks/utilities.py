import numpy as np

xrd_lambda_angstroms_dict = {'cu': {'average': 1.54184,
                                    'alpha1': 1.54056,
                                    'alpha2': 1.54439,
                                    'beta': 1.39222,
                                   },
                             'mo': {'average': 0.71073,
                                    'alpha1': 0.7093,
                                    'alpha2': 0.71359,
                                    'beta': 0.63229,
                                   },
                             'ag': {'average': 0.56088,
                                    'alpha1': 0.55942,
                                    'alpha2': 0.56381,
                                    'beta': 0.49708,
                                   },
                             'cr': {'average': 2.291,
                                    'alpha1': 2.2897,
                                    'alpha2': 2.29361,
                                    'beta': 2.08487,
                                   },
                             'fe': {'average': 1.93736,
                                    'alpha1': 1.93604,
                                    'alpha2': 1.93998,
                                    'beta': 1.75661,
                                   },
                             'co': {'average': 1.79026,
                                    'alpha1': 1.78897,
                                    'alpha2': 1.79285,
                                    'beta': 1.62079,
                                   },
                            }


def retrieve_anode_material(alpha1:float =None, alpha2:float =None, beta:float =None, tolerance_error=0.001) -> str:
    """return the anode material from lookup table"""
    
    for material in xrd_lambda_angstroms_dict.keys():
        if alpha1:
            if np.abs(alpha1 - xrd_lambda_angstroms_dict[material]['alpha1']) > tolerance_error:
                continue
        if alpha2:
            if np.abs(alpha2 - xrd_lambda_angstroms_dict[material]['alpha2']) > tolerance_error:
                continue
        if beta:
            if np.abs(beta - xrd_lambda_angstroms_dict[material]['beta']) > tolerance_error:
                continue

        return material

    return None


def from_theta_to_lambda(two_theta=None, units='rad', xrd_lambda_angstroms=None):
    """returns the lambda value of the twoTheta value of a given wavelength (xrd_lambda_angstroms)"""
    if units == 'deg':
        two_theta = np.array([np.deg2rad(_theta) for _theta in two_theta])
    else:
        two_theta = np.array(two_theta)

    d = xrd_lambda_angstroms / (2 * np.sin(two_theta / 2))

    return d
