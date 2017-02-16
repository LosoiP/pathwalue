# -*- coding: utf-8 -*-
# (C) 2017 Tampere University of Technology
# MIT License
# Pauli Losoi
"""
Created on Fri Nov 25 12:57:40 2016

@author: losoip
"""


import os

from exceptions import DirectoryNotFoundError


# Directory names
_DAT = 'dat'
_JS = 'js'
_JSON = 'json'
_RD = 'rd'
_TSV = 'tsv'

# Directory paths
_BASE = os.path.normpath('..')
_DATA = os.path.join(_BASE, 'data')
_TESTS = os.path.join(_BASE, 'tests')

_CHEBI = os.path.join(_DATA, 'chebi')
_INTENZ = os.path.join(_DATA, 'intenz')
_RHEA = os.path.join(_DATA, 'rhea')

CHEBI_TSV = os.path.join(_CHEBI, _TSV)
INTENZ_DAT = os.path.join(_INTENZ, _DAT)
JS = os.path.join(_DATA, _JS)
JSON = os.path.join(_DATA, _JSON)
RHEA_RD = os.path.join(_RHEA, _RD)
RHEA_TSV = os.path.join(_RHEA, _TSV)


def get_names(path):
    """
    Return a list of filenames in a directory.

    Parameters
    ----------
    path : str
        Directory path.

    Returns
    -------
    list
        String names of files in the directory. Names also contain file
        extensions.

    """
    if not isinstance(path, str):
        raise TypeError('`path` must be str')
    # os.walk yields tuple of 3: dirpath, dirnames and filenames.
    try:
        __, __, filenames = os.walk(path).__next__()
    except StopIteration:
        raise DirectoryNotFoundError('directory `{}` not found'.format(path))
    else:
        return filenames
