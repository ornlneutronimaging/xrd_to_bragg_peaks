import os
import re

xrd_patterns = {'ras': {'alpha1': r"\*HW_XG_WAVE_LENGTH_ALPHA1\s{1}\"(\d\.\d*)\"",
                        'alpha2': r"\*HW_XG_WAVE_LENGTH_ALPHA2\s{1}\"(\d\.\d*)\"",
                        'beta': r"\*HW_XG_WAVE_LENGTH_BETA\s{1}\"(\d\.\d*)\"",
                        },
                'asc': {'alpha1': None,
                        'alpha2': None,
                        'beta': None,
                        },
                }

xrd_starts_with = {'ras': {'alpha1': "*HW_XG_WAVE_LENGTH_ALPHA1",
                           'alpha2': "*HW_XG_WAVE_LENGTH_ALPHA2",
                           'beta': "*HW_XG_WAVE_LENGTH_BETA",
                           'data_start': "*RAS_INT_START",
                           },
                   'asc': {'alpha1': None,
                           'alpha2': None,
                           'beta': None,
                           'data_start': None,
                           },
                   }


def file_content(file_name):
    with open(file_name, 'r', errors='replace') as f:
        content = f.readlines()

    return content


def xrd_file_parser(xrd_file_name):
    if not os.path.exists(xrd_file_name):
        return None

    name, extension = os.path.splitext(xrd_file_name)

    if extension == '.ras':
        return ras_file_parser(xrd_file_name)

    return None


def _pattern_match(pattern=None, line_starts_with=None, line=None):
    if line.startswith(line_starts_with):
        m = re.match(pattern, line)
        if m:
            return m.group(1)
    return None


def ras_file_parser(xrd_file_name):
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

    return metadata
