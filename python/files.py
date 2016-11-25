# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 12:57:40 2016

@author: losoip
"""


import json
import os


# File extensions
_EXTENSION_DAT = '.dat'
_EXTENSION_JS = '.js'
_EXTENSION_JSON = '.json'
_EXTENSION_TSV = '.tsv'
_EXTENSION_RD = '.rd'


# ChEBI files
CHEBI_COMPOUNDS = 'compounds' + _EXTENSION_TSV
CHEBI_DATA = 'chemical_data' + _EXTENSION_TSV
CHEBI_RELATIONS = 'relation' + _EXTENSION_TSV
CHEBI_VERTICES = 'vertice' + _EXTENSION_TSV

# IntEnz files
INTENZ_ENZYMES = 'enzyme' + _EXTENSION_DAT

# Rhea files
RHEA_EC = 'ec-rhea-dir' + _EXTENSION_TSV

# JSON files
_PREFIX_EC = 'enz_'
ENZ_NAMES = _PREFIX_EC + 'names' + _EXTENSION_JSON
ENZ_REACTIONS = _PREFIX_EC + 'reactions' + _EXTENSION_JSON

_PREFIX_MOL = 'mol_'
MOL_CHARGES = _PREFIX_MOL + 'charges' + _EXTENSION_JSON
MOL_DEMANDS = _PREFIX_MOL + 'demands' + _EXTENSION_JSON
MOL_FORMULAE = _PREFIX_MOL + 'formulae' + _EXTENSION_JSON
MOL_IGNORED = _PREFIX_MOL + 'ignored' + _EXTENSION_JSON
MOL_MASSES = _PREFIX_MOL + 'masses' + _EXTENSION_JSON
MOL_NAMES = _PREFIX_MOL + 'names' + _EXTENSION_JSON
MOL_PARENTS = _PREFIX_MOL + 'parents' + _EXTENSION_JSON
MOL_PRICES = _PREFIX_MOL + 'prices' + _EXTENSION_JSON
MOL_REACTIONS = _PREFIX_MOL + 'reactions' + _EXTENSION_JSON
MOL_RELATIONS = _PREFIX_MOL + 'relations' + _EXTENSION_JSON
MOL_VALUES = _PREFIX_MOL + 'values' + _EXTENSION_JSON

_PREFIX_RXN = 'rxn_'
RXN_COMPLEXITIES = _PREFIX_RXN + 'complexities' + _EXTENSION_JSON
RXN_ECS = _PREFIX_RXN + 'ecs' + _EXTENSION_JSON
RXN_EQUATIONS = _PREFIX_RXN + 'equations' + _EXTENSION_JSON
RXN_STOICHIOMETRICS = _PREFIX_RXN + 'stoichiometrics' + _EXTENSION_JSON

# JS files
JS_MOL_DEMANDS = _PREFIX_MOL + 'demands' + _EXTENSION_JS
JS_MOL_NAMES = _PREFIX_MOL + 'names' + _EXTENSION_JS
JS_MOL_PRICES = _PREFIX_MOL + 'prices' + _EXTENSION_JS
JS_MOL_REACTIONS = _PREFIX_MOL + 'reactions' + _EXTENSION_JS
JS_MOL_IGNORED = _PREFIX_MOL + 'ignored' + _EXTENSION_JS
JS_ENZ_NAMES = _PREFIX_EC + 'names' + _EXTENSION_JS
JS_ENZ_REACTIONS = _PREFIX_EC + 'reactions' + _EXTENSION_JS
JS_RXN_COMPLEXITIES = _PREFIX_RXN + 'complexities' + _EXTENSION_JS
JS_RXN_ENZYMES = _PREFIX_RXN + 'enzymes' + _EXTENSION_JS
JS_RXN_EQUATIONS = _PREFIX_RXN + 'equations' + _EXTENSION_JS
JS_RXN_STOICHIOMETRICS = _PREFIX_RXN + 'stoichiometrics' + _EXTENSION_JS


def get_content(path, filename):
    """
    Return content of a text file.

    Parameters
    ----------
    path : str
        Directory path to file.
    filename : str
        Name of the file. Name must include extension.

    Returns
    -------
    list
        Contents of the file. List elements correspond to text file
        rows.

    Raises
    ------
    FileNotFoundError
        If the path or file does not exist.
    TypeError
        If path or filename is not str.

    """
    if not isinstance(path, str):
        raise TypeError('`path` must be str')
    elif not isinstance(filename, str):
        raise TypeError('`filename` must be str')
    with open(os.path.join(path, filename)) as file:
        return file.readlines()


def get_json(path, filename):
    """
    Return data object from a JSON formatted file.

    Parameters
    ----------
    path : str
        Directory path to file.
    filename : str
        Name of the file. Name must include extension.

    Returns
    -------
    object
        Object contained in the JSON file.

    """
    if not isinstance(path, str):
        raise TypeError('`path` must be str')
    elif not isinstance(filename, str):
        raise TypeError('`filename` must be str')
    with open(os.path.join(path, filename)) as file:
        return json.load(file)


def write_json(python_object, path, filename):
    """
    Save object data in a JSON formatted file.

    Parameters
    ----------
    python_object : obj
        Object to be saved in the JSON file.
    path : str
        Directory path to file.
    filename : str
        Name of the target JSON file. Filename must not contain path or
        extension.

    Returns
    -------
    None

    """
    if not isinstance(path, str):
        raise TypeError('`path` must be str')
    elif not isinstance(filename, str):
        raise TypeError('`filename` must be str')
    with open(os.path.join(path, filename), 'w') as file:
        json.dump(python_object, file)


def write_jsons(data, path, filenames):
    """
    Save objects in JSON formatted files.

    Parameters
    ----------
    data : list
        Objects to be saved in the files. Object index must correspond to
        filename index.
    path : str
        Directory path to file.
    filenames : list
        Names of the target JSON files. Filename index must correspond
        to object index.

    Returns
    -------
    None

    """
    if not isinstance(data, (list, tuple)):
        raise TypeError('`data` must be list or tuple')
    elif not isinstance(path, str):
        raise TypeError('`path` must be str')
    elif not isinstance(filenames, (list, tuple)):
        raise TypeError('`filenames` must be list or tuple')
    for object_, filename in zip(data, filenames):
        write_json(object_, path, filename)
