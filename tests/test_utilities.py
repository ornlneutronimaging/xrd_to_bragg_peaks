import pytest
from unittest import TestCase
import os

from notebooks.utilities import retrieve_anode_material
from notebooks.xrd_file_parser import file_content, _pattern_match, ras_file_parser, asc_file_parser, xrd_file_parser


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


class TestXrdRasFileParser(TestCase):

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

        data_expected = {'2theta': [20, 20.01, 20.02, 20.03, 20.04, 20.05, 20.06],
                         'intensity': [165., 187., 159., 160., 153., 203., 168.],
                         'error': [1., 1., 1., 1., 1., 1., 1.]}

        for key in metadata_expected.keys():
            assert metadata_returned[key] == metadata_expected[key]

        data_returned = metadata_returned['data']

        for key in data_returned.keys():
            for _exp, _return in zip(data_returned[key], data_expected[key]):
                assert _exp == _return


class TestXrdAscFileParser(TestCase):

    ASC_FILE_NAME = "data/xrd_file.asc"
    RAS_FILE_NAME = "data/xrd_file.ras"

    def setUp(self):
        _file_path = os.path.dirname(__file__)
        self.asc_file_name = os.path.abspath(os.path.join(_file_path, self.ASC_FILE_NAME))

    def test_asc_pattern_match(self):
        content = file_content(self.asc_file_name)

        alpha1_pattern = r"\*WAVE_LENGTH1\s*\=\s*(\d\.\d*)"
        alpha1_starts_with = "*WAVE_LENGTH1"

        for line in content:

            match = _pattern_match(pattern=alpha1_pattern,
                                   line_starts_with=alpha1_starts_with,
                                   line=line)
            if match:
                value_returned = match

        value_expected = "1.54059"

        assert value_expected == value_returned

    def test_asc_file_parser(self):

        metadata_returned = asc_file_parser(self.asc_file_name)

        metadata_expected = {'alpha1': '1.54059',
                             'alpha2': '1.54441',
                             'data_first_line': 28,
                             }
        for key in metadata_expected.keys():
            assert metadata_returned[key] == metadata_expected[key]

        twotheta_expected = {'start': '20',
                             'stop': '120',
                             'step': '0.01',
                             }
        for key in twotheta_expected.keys():
            assert metadata_returned['2theta'][key] == twotheta_expected[key]

        data_expected = [165, 187, 159, 160, 153, 203, 168, 161, 153, 167, 159, 175]
        data_returned = metadata_returned['data']

        for _exp, _ret in zip(data_expected, data_returned):
            assert _exp == _ret


class TestXrdFileParser(TestCase):
    """testing using the base method that will call the respective xrd extension file dependent methods"""

    ASC_FILE_NAME = "data/xrd_file.asc"
    RAS_FILE_NAME = "data/xrd_file.ras"

    def setUp(self):
        _file_path = os.path.dirname(__file__)
        self.asc_file_name = os.path.abspath(os.path.join(_file_path, self.ASC_FILE_NAME))
        self.ras_file_name = os.path.abspath(os.path.join(_file_path, self.RAS_FILE_NAME))

    def test_ras_file_parser(self):

        metadata_returned = xrd_file_parser(self.ras_file_name)

        metadata_expected = {'alpha1': '1.540593',
                             'alpha2': '1.544414',
                             'beta': '1.392250',
                             'data_first_line': 19,
                             }

        data_expected = {'2theta': [20, 20.01, 20.02, 20.03, 20.04, 20.05, 20.06],
                         'intensity': [165., 187., 159., 160., 153., 203., 168.],
                         'error': [1., 1., 1., 1., 1., 1., 1.]}

        for key in metadata_expected.keys():
            assert metadata_returned[key] == metadata_expected[key]

        data_returned = metadata_returned['data']

        for key in data_returned.keys():
            for _exp, _return in zip(data_returned[key], data_expected[key]):
                assert _exp == _return

    def test_asc_file_parser(self):

        metadata_returned = xrd_file_parser(self.asc_file_name)

        metadata_expected = {'alpha1': '1.54059',
                             'alpha2': '1.54441',
                             'data_first_line': 28,
                             }
        for key in metadata_expected.keys():
            assert metadata_returned[key] == metadata_expected[key]

        twotheta_expected = {'start': '20',
                             'stop': '120',
                             'step': '0.01',
                             }
        for key in twotheta_expected.keys():
            assert metadata_returned['2theta'][key] == twotheta_expected[key]

        data_expected = [165, 187, 159, 160, 153, 203, 168, 161, 153, 167, 159, 175]
        data_returned = metadata_returned['data']

        for _exp, _ret in zip(data_expected, data_returned):
            assert _exp == _ret
