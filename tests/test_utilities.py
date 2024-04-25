import pytest
from unittest import TestCase
import os

from notebooks.utilities import retrieve_anode_material
from notebooks.xrd_file_parser import file_content, _pattern_match, ras_file_parser


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


class TestXrdFileParser(TestCase):

    RAS_FILE_NAME = "data/xrd_file.ras"

    def setUp(self):
        _file_path = os.path.dirname(__file__)
        self.ras_file_name = os.path.abspath(os.path.join(_file_path, self.RAS_FILE_NAME))

    def test_pattern_match(self):
        content = file_content(self.ras_file_name)

        ras_alpha1_pattern = r"\*HW_XG_WAVE_LENGTH_ALPHA1\s{1}\"(\d\.\d*)\""
        ras_alpha1_starts_with = "*HW_XG_WAVE_LENGTH_ALPHA1"

        for line in content:

            match = _pattern_match(pattern=ras_alpha1_pattern,
                                   line_starts_with=ras_alpha1_starts_with,
                                   line=line)
            if match:
                value_returned = match

        value_expected = "1.540593"

        assert value_expected == value_returned

    def test_ras_file_parser(self):

        metadata_returned = ras_file_parser(self.ras_file_name)

        metadata_expected = {'alpha1': '1.540593',
                             'alpha2': '1.544414',
                             'beta': '1.392250',
                             'data_first_line': 19,
                             }

        for key in metadata_expected.keys():
            assert metadata_returned[key] == metadata_expected[key]
