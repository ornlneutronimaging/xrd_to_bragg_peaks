from unittest import TestCase
import numpy as np

from notebooks.utilities import retrieve_anode_material
from notebooks.utilities import from_theta_to_lambda

PRECISION = 0.0001


class TestRetrieveAnodeMaterial(TestCase):

    def test_simple_case(self):

        alpha1 = 1.54056
        returned_element = retrieve_anode_material(alpha1=alpha1)
        expected_element = 'cu'
        assert expected_element == returned_element

        alpha2 = 0.71359
        returned_element = retrieve_anode_material(alpha2=alpha2)
        expected_element = 'mo'
        assert expected_element == returned_element

        alpha1 = 0.7093
        alpha2 = 0.71359
        returned_element = retrieve_anode_material(alpha1=alpha1, alpha2=alpha2)
        expected_element = 'mo'
        assert expected_element == returned_element

        alpha1 = 0.55942
        alpha2 = 0.56381
        beta = 0.49708
        returned_element = retrieve_anode_material(alpha1=alpha1, alpha2=alpha2, beta=beta)
        expected_element = 'ag'
        assert expected_element == returned_element

        beta = 0.49708
        returned_element = retrieve_anode_material(beta=beta)
        expected_element = 'ag'
        assert expected_element == returned_element

    def test_not_matching_cases(self):

        alpha1 = 1.55
        returned_element = retrieve_anode_material(alpha1=alpha1)
        expected_element = None
        assert expected_element == returned_element

    def test_tolerance_error(self):

        alpha1 = 1.54056
        returned_element = retrieve_anode_material(alpha1=alpha1, tolerance_error=0.0001)
        expected_element = 'cu'
        assert expected_element == returned_element

        alpha1 = 1.5404
        returned_element = retrieve_anode_material(alpha1=alpha1, tolerance_error=0.0001)
        expected_element = None
        assert expected_element == returned_element


class TestFromThetaToLambda(TestCase):

    def test_simple_conversion_with_rad(self):
        two_theta_rad = [np.pi/2., np.pi/3.]
        two_theta_expected = [0.88388, 1.25]
        two_theta_returned = from_theta_to_lambda(two_theta=two_theta_rad,
                                                  units='rad',
                                                  xrd_lambda_angstroms=1.25)

        for _exp, _ret in zip(two_theta_expected, two_theta_returned):
            assert np.abs(_exp - _ret) < PRECISION

    def test_simple_conversion_with_deg(self):
        two_theta_deg = [90, 60]
        two_theta_expected = [0.88388, 1.25]
        two_theta_returned = from_theta_to_lambda(two_theta=two_theta_deg,
                                                  units='deg',
                                                  xrd_lambda_angstroms=1.25)

        for _exp, _ret in zip(two_theta_expected, two_theta_returned):
            assert np.abs(_exp - _ret) < PRECISION
