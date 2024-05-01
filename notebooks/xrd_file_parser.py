import os
import re
import pandas as pd
import numpy as np

xrd_patterns = {'ras': {'alpha1': r"\*HW_XG_WAVE_LENGTH_ALPHA1\s{1}\"(\d\.\d*)\"",
                        'alpha2': r"\*HW_XG_WAVE_LENGTH_ALPHA2\s{1}\"(\d\.\d*)\"",
                        'beta': r"\*HW_XG_WAVE_LENGTH_BETA\s{1}\"(\d\.\d*)\"",
                        },
                'asc': {'alpha1': r"\*WAVE_LENGTH1\s*\=\s*(\d\.\d*)",
                        'alpha2': r"\*WAVE_LENGTH2\s*\=\s*(\d\.\d*)",
                        '2theta': {'start': r"\*START\s*\=\s*(\d*)",
                                   'stop': r"\*STOP\s*\=\s*(\d*)",
                                   'step': r"\*STEP\s*\=\s*(\d*\.\d*)"},
                        },
                }

xrd_starts_with = {'ras': {'alpha1': "*HW_XG_WAVE_LENGTH_ALPHA1",
                           'alpha2': "*HW_XG_WAVE_LENGTH_ALPHA2",
                           'beta': "*HW_XG_WAVE_LENGTH_BETA",
                           'data_start': "*RAS_INT_START",
                           },
                   'asc': {'alpha1': "*WAVE_LENGTH1",
                           'alpha2': "*WAVE_LENGTH2",
                           'data_start': "*INDEX",
                           '2theta': {'start': "*START",
                                      'stop': "*STOP",
                                      'step': "*STEP"}
                           },
                   }


class XrdFileType:
    ras = '.ras'
    asc = '.asc'
    txt = '.txt'


def file_content(file_name):
    with open(file_name, 'r', errors='replace') as f:
        content = f.readlines()

    return content


def xrd_file_parser(xrd_file_name=None, xrd_file_content=None, xrd_file_type=XrdFileType.ras):
    if (not os.path.exists(xrd_file_name)) and (xrd_file_content is None):
        return None

    if xrd_file_name:
        name, extension = os.path.splitext(xrd_file_name)
    else:
        extension = xrd_file_type

    if extension == XrdFileType.ras:
        return ras_file_parser(xrd_file_name, xrd_file_content)
    elif extension == XrdFileType.asc:
        return asc_file_parser(xrd_file_name, xrd_file_content)
    elif extension == XrdFileType.txt:
        return txt_file_parser(xrd_file_name, xrd_file_content)

    return None


def _pattern_match(pattern=None, line_starts_with=None, line=None):
    if line.startswith(line_starts_with):
        m = re.match(pattern, line)
        if m:
            return m.group(1)
    return None


def asc_file_parser(xrd_file_name=None, xrd_file_content=None):
    """retrieve the following metadata from the ASC file"""
    metadata = {'alpha1': None,
                'alpha2': None,
                '2theta': {'start': None,
                           'stop': None,
                           'step': None,
                           },
                'data': None,
                'data_first_line': 0,
                }
    if xrd_file_name is None:
        if xrd_file_content is None:
            raise AttributeError("Provide either xrd_file_name or xrd_file_content")

        else:
            content = xrd_file_content

    else:
        content = file_content(xrd_file_name)

    first_data_row = 0
    for line in content:

        for _key in ['alpha1', 'alpha2']:
            match = _pattern_match(line=line,
                                   pattern=xrd_patterns['asc'][_key],
                                   line_starts_with=xrd_starts_with['asc'][_key])

            if match:
                metadata[_key] = match
                break

        for _key in xrd_patterns['asc']['2theta'].keys():

            match = _pattern_match(line=line,
                                   pattern=xrd_patterns['asc']['2theta'][_key],
                                   line_starts_with=xrd_starts_with['asc']['2theta'][_key])
            if match:
                metadata['2theta'][_key] = match
                break

        first_data_row += 1

        if line.startswith(xrd_starts_with['asc']['data_start']):
            first_data_row += 1
            metadata['data_first_line'] = first_data_row
            break

    # retrieve data
    full_data = []

    content = content[first_data_row:-3]
    for _row in content:
        _row_array = _row.split(",")
        for _element in _row_array:
            full_data.append(int(_element.strip()))

    metadata['data'] = np.transpose(full_data)

    return metadata


def ras_file_parser(xrd_file_name=None, xrd_file_content=None):
    """retrieve the following metadata from the RAS file"""
    metadata = {'alpha1': None,
                'alpha2': None,
                'beta': None,
                'data': None,
                'data_first_line': 0,
                }

    content = file_content(xrd_file_name)

    for line in content:

        for key in xrd_patterns['ras'].keys():

            match = _pattern_match(line=line,
                                   pattern=xrd_patterns['ras'][key],
                                   line_starts_with=xrd_starts_with['ras'][key])
            if match:
                metadata[key] = match
                break

        metadata['data_first_line'] += 1

        if line.startswith(xrd_starts_with['ras']['data_start']):
            break

    # loading data now
    data = pd.read_csv(xrd_file_name,
                       names=['2theta', 'intensity', 'error'],
                       skiprows=metadata['data_first_line'],
                       sep=" ",
                       encoding='latin1')
    data = data[:-2]
    metadata['data'] = {'2theta': np.array(data['2theta']),
                        'intensity': np.array(data['intensity']),
                        'error': np.array(data['error'])}

    return metadata


def txt_file_parser(xrd_file_name=None, xrd_file_content=None):
    if xrd_file_name is None:
        if xrd_file_content is None:
            raise AttributeError("Provide either xrd_file_name or xrd_file_content")

        data = pd.read_csv(xrd_file_content, names=['2theta', 'intensity'], skiprows=1, sep='\t')

    else:
        data = pd.read_csv(xrd_file_name, names=['2theta', 'intensity'], skiprows=1, sep='\t')

    return {'data': {'2theta': np.array(data['2theta']),
                     'intensity': np.array(data['intensity']),
                     },
            }
