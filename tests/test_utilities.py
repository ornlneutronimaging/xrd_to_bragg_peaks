from unittest import TestCase
import numpy as np
import pytest
import os

from notebooks.utilities import retrieve_anode_material
from notebooks.utilities import from_theta_to_d
from notebooks.utilities import find_peaks_above_threshold
from notebooks.xrd_file_parser import xrd_file_parser

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

    def test_passing_no_input(self):
        alpha1 = None
        alpha2 = None
        beta = None
        expected_element = None
        returned_element = retrieve_anode_material(alpha1=alpha1, alpha2=alpha2, beta=beta)
        assert expected_element == returned_element

    def test_not_passing_any_input(self):
        expected_element = None
        returned_element = retrieve_anode_material()
        assert expected_element == returned_element


class TestFromThetaTod(TestCase):

    def test_simple_conversion_with_rad(self):
        two_theta_rad = [np.pi/2., np.pi/3.]
        two_theta_expected = [0.88388, 1.25]
        two_theta_returned = from_theta_to_d(two_theta=two_theta_rad,
                                             units='rad',
                                             xrd_lambda_angstroms=1.25)

        for _exp, _ret in zip(two_theta_expected, two_theta_returned):
            assert np.abs(_exp - _ret) < PRECISION

    def test_simple_conversion_with_deg(self):
        two_theta_deg = [90, 60]
        two_theta_expected = [0.88388, 1.25]
        two_theta_returned = from_theta_to_d(two_theta=two_theta_deg,
                                             units='deg',
                                             xrd_lambda_angstroms=1.25)

        for _exp, _ret in zip(two_theta_expected, two_theta_returned):
            assert np.abs(_exp - _ret) < PRECISION


class TestFindPeaks(TestCase):

    TXT_FILE_NAME = "data/xrd_file_full.txt"

    def setUp(self):
        _file_path = os.path.dirname(__file__)
        self.txt_file_name = os.path.abspath(os.path.join(_file_path, self.TXT_FILE_NAME))

    def test_xaxis_and_yaxis_can_not_be_none(self):
        xaxis = None
        yaxis = np.array([1, 2, 3, 4])

        with pytest.raises(AttributeError):
            xaxis, yaxis = find_peaks_above_threshold(xaxis=xaxis,
                                                      yaxis=yaxis)

        xaxis = np.array([1, 2, 3, 4])
        yaxis = None

        with pytest.raises(AttributeError):
            xaxis, yaxis = find_peaks_above_threshold(xaxis=xaxis,
                                                      yaxis=yaxis)

        xaxis = None
        yaxis = None
        with pytest.raises(AttributeError):
            xaxis, yaxis = find_peaks_above_threshold(xaxis=xaxis,
                                                      yaxis=yaxis)

    def test_retrieve_peaks(self):
        metadata_dict = xrd_file_parser(self.txt_file_name)
        yaxis = metadata_dict['data']['intensity']
        xaxis = metadata_dict['data']['2theta']

        peaks_dict = find_peaks_above_threshold(xaxis=xaxis,
                                                yaxis=yaxis)

        yaxis_peaks_returned = peaks_dict['yaxis'][0:3]
        xaxis_peaks_returned = peaks_dict['xaxis'][0:3]

        yaxis_peaks_expected = np.array([24976.1222, 87214.3515, 79633.2479])
        xaxis_peaks_expected = np.array([7.2524, 11.9614, 17.6904])

        for _y_exp, _y_ret in zip(yaxis_peaks_expected, yaxis_peaks_returned):
            assert _y_exp == _y_ret

        for _x_exp, _x_ret in zip(xaxis_peaks_expected, xaxis_peaks_returned):
            assert _x_exp == _x_ret
