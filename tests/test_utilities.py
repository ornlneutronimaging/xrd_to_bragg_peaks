from unittest import TestCase

from notebooks.utilities import retrieve_anode_material
from notebooks.utilities import from_theta_to_lambda


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

    def test_simple_conversion(self):
        pass