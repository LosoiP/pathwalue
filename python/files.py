# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 12:57:40 2016

@author: losoip
"""


import json
import os

from exceptions import TSVFieldError


# Delimiters
_DELIMITER_TSV = '\t'

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


def get_contents(path, filenames):
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
    elif not isinstance(filenames, list):
        raise TypeError('`filenames` must be list')
    for filename in filenames:
        with open(os.path.join(path, filename)) as file:
            yield file.readlines()


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


def parse_ctab_counts_line_(ctab):
    """
    """
    counts_line = {}
    indices = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 39]
    keys = ['n_atoms', 'n_bonds', 'n_atoms_lists', '', 'is_chiral', 'n_stext',
            'n_rxn_components', 'n_reactants', 'n_products',
            'n_intermediates', 'n_properties', 'version']
    for key, index_lag, index_lead in zip(keys, indices[:-1], indices[1:]):
        value = ctab[index_lag:index_lead].strip()
        if key.startswith('n_'):
            try:
                value = int(value)
            except ValueError:
                value = 0
        elif key.startswith('is_'):
            try:
                value = bool(int(value))
            except ValueError:
                value = False
        elif key:
            pass
        else:
            value = None
        counts_line[key] = value
    return counts_line


def parse_ctab_atom_block_(contents):
    """
    """
    atom_block = []
    for row in contents:
        atom_block.append(row.rstrip('\n'))
    return atom_block


def parse_ctab_bond_block_(contents):
    """
    """
    bond_block = []
    for row in contents:
        bond_block.append(row.rstrip('\n'))
    return bond_block


def parse_ctab_atoms_lists_(contents):
    """
    """
    return {}


def parse_ctab_stext_(contents):
    """
    """
    return {}


def parse_ctab_properties_(contents):
    """
    """
    return {}


def parse_ctab(contents):
    """
    """
    counts_line = parse_ctab_counts_line_(contents[0])
    n_atoms = counts_line['n_atoms']
    n_bonds = counts_line['n_bonds']
    n_properties = counts_line['n_properties']
    first = 1
    last = first + n_atoms

    atoms = parse_ctab_atom_block_(contents[first:last])

    first, last = last, last + n_bonds
    bonds = parse_ctab_bond_block_(contents[first:last])

    atoms_lists = parse_ctab_atoms_lists_([])

    stext = parse_ctab_stext_([])

    first, last = last, last + n_properties
    properties = parse_ctab_properties_(contents[first:last])
    return counts_line, atoms, bonds, atoms_lists, stext, properties


def parse_mol(contents):
    """
    """


def parse_rd(contents):
    """
    """


def parse_rxn(contents):
    """
    """


def parse_tsv(contents, fields_header=[]):
    """
    """

    start_index = 0
    if not fields_header:
        fields_header = contents[0].strip().split(_DELIMITER_TSV)
        start_index = 1
    for index_row, row in enumerate(contents[start_index:]):
        fields_row = row.strip().split(_DELIMITER_TSV)
        if len(fields_header) != len(fields_row):
            raise TSVFieldError(
                "row {}: {} fields found, {} expected".format(
                    index_row, len(fields_row), len(fields_header)))
        else:
            yield dict(zip(fields_header, fields_row))


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
