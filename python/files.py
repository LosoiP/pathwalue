# -*- coding: utf-8 -*-
# (C) 2017 Tampere University of Technology
# MIT License
# Pauli Losoi
"""
Define functions and constants for PathWalue files.

collections.namedtuple is used in saving parsed database file data for
further use. Constants are the filenames for the database files of
PathWalue. Functions defined in this module read, process and write
files.

Classes
-------
Mol
    collections.namedtuple for mol data.
Rd
    collections.namedtuple for rd data.
RdRecord
    collections.namedtuple for rd records.
Rxn
    collections.namedtuple for rxn data.
Tsv
    collections.namedtuple for tsv data.

Functions
---------
get_content
    Return content list of a text file.
get_contents
    Yield content lists of text files.
get_json
    Return object from a JSON file.
parse_ctab
    Parse a ctab entry. NOT IMPLEMENTED
parse_mol
    Parse a mol entry.
parse_rd
    Parse an rd entry.
parse_rxn
    Parse an rxn entry.
parse_tsv
    Parse a tsv entry.
write_json
    Write an object into a JSON file.
write_jsons
    Write objects into JSON files.

Constants
---------
CHEBI_COMPOUNDS
CHEBI_DATA
CHEBI_RELATIONS
CHEBI_VERTICES
INTENZ_ENZYMES
RHEA_EC
ENZ_NAMES
ENZ_REACTIONS
MOL_CHARGES
MOL_DEMANDS
MOL_FORMULAE
MOL_IGNORED
MOL_MASSES
MOL_NAMES
MOL_PARENTS
MOL_PRICES
MOL_REACTIONS
MOL_RELATIONS
MOL_VALUES
RXN_ECS
RXN_EQUATIONS
RXN_STOICHIOMETRICS
JS_MOL_NAMES
JS_MOL_PRICES
JS_MOL_REACTIONS
JS_MOL_IGNORED
JS_ENZ_NAMES
JS_ENZ_REACTIONS
JS_RXN_ENZYMES
JS_RXN_EQUATIONS
JS_RXN_STOICHIOMETRICS

See also
--------
Description of Several Chemical Structure File Formats Used by Computer
Programs by Arthur Dalby, James G. Nourse et al. in Journal of Chemical
Information and Computer Sciences (1992) 32:244-255

"""


import json
import os


from collections import namedtuple
from exceptions import (
    CtabError,
    MolError,
    RdError,
    RxnError,
    TsvError,
    )


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
JS_RXN_ENZYMES = _PREFIX_RXN + 'enzymes' + _EXTENSION_JS
JS_RXN_EQUATIONS = _PREFIX_RXN + 'equations' + _EXTENSION_JS
JS_RXN_STOICHIOMETRICS = _PREFIX_RXN + 'stoichiometrics' + _EXTENSION_JS


# File formats.
# Ctab = namedtuple('CTAB', ['counts_line', 'atom_block', 'bond_block'])
Mol = namedtuple('MOL', ['name', 'meta', 'comment', 'ctab'])
Rd = namedtuple('RD', ['version', 'time', 'records'])
RdRecord = namedtuple('RDRecord', ['identifier', 'rxn', 'data'])
Rxn = namedtuple('RXN', ['name', 'comment', 'n_reactants', 'n_products',
                         'mols'])
Tsv = namedtuple('TSV', ['fields', 'data'])


def get_content(path, filename, strip_newlines=True):
    """
    Return content list of a text file.

    Parameters
    ----------
    path : string
        Directory path to file.
    filename : string
        Name of the file. Name must include extension.
    strip_newlines : bool
        If true (default), strip newlines '\\n'.

    Returns
    ------
    list
        Contents of the file. Elements correspond to text file rows.

    Raises
    ------
    FileNotFoundError
        If the path or file does not exist.
    TypeError
        If path or filename is not string.

    """
    if not isinstance(path, str):
        raise TypeError('`path` must be str')
    elif not isinstance(filename, str):
        raise TypeError('`filename` must be str')
    contents = []
    with open(os.path.join(path, filename)) as file:
        for line in file:
            if strip_newlines:
                contents.append(line.rstrip('\n'))
            else:
                contents.append(line)
        return contents


def get_contents(path, filenames, strip_newlines=True):
    """
    Yield content lists of text files.

    Parameters
    ----------
    path : string
        Directory path to file.
    filename : list of strings
        Names of the files. Names must include extension.
    strip_newlines : bool
        If true, strip newlines '\\n'.

    Yields
    ------
    list
        File contents.

    Raises
    ------
    FileNotFoundError
        If the path or a file does not exist.
    TypeError
        If filenames is not a list.

    """
    if not isinstance(path, str):
        raise TypeError('`path` must be str')
    elif not isinstance(filenames, list):
        raise TypeError('`filenames` must be list')
    for filename in filenames:
        yield get_content(path, filename, strip_newlines)


def get_json(path, filename):
    """
    Return data object from a JSON file.

    Parameters
    ----------
    path : string
        Directory path to file.
    filename : string
        Name of the file. Name must include extension.

    Returns
    -------
    object
        Object contained in the JSON file.

    See also
    --------
    write_json, write_jsons

    """
    if not isinstance(path, str):
        raise TypeError('`path` must be str')
    elif not isinstance(filename, str):
        raise TypeError('`filename` must be str')
    with open(os.path.join(path, filename)) as file:
        return json.load(file)


def _parse_ctab_counts_line(ctab):
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


def _parse_ctab_atom_block(contents):
    """
    """
    atom_block = []
    for row in contents:
        atom_block.append(row.rstrip('\n'))
    return atom_block


def _parse_ctab_bond_block(contents):
    """
    """
    bond_block = []
    for row in contents:
        bond_block.append(row.rstrip('\n'))
    return bond_block


def _parse_ctab_atoms_lists(contents):
    """
    """
    return {}


def _parse_ctab_stext(contents):
    """
    """
    return {}


def _parse_ctab_properties(contents):
    """
    """
    return {}


def parse_ctab(contents):
    """
    """
    counts_line = _parse_ctab_counts_line(contents[0])
    n_atoms = counts_line['n_atoms']
    n_bonds = counts_line['n_bonds']
    n_properties = counts_line['n_properties']
    first = 1
    last = first + n_atoms

    atoms = _parse_ctab_atom_block(contents[first:last])

    first, last = last, last + n_bonds
    bonds = _parse_ctab_bond_block(contents[first:last])

    atoms_lists = _parse_ctab_atoms_lists([])

    stext = _parse_ctab_stext([])

    first, last = last, last + n_properties
    properties = _parse_ctab_properties(contents[first:last])
    return counts_line, atoms, bonds, atoms_lists, stext, properties


def parse_mol(contents, ctab_parse=False):
    """
    Parse a mol entry.

    Parameters
    ----------
    contents : list
        Mol entry contents.
    ctab_parse : boolean
        If false (default), leave ctab portion of entry unparsed.

    Returns
    -------
    collections.namedtuple
        Properties: name, meta, comment and ctab.

    """
    if contents[0] != '$MOL':
        raise MolError
    name = contents[1]
    meta = contents[2]
    comment = contents[3]
    if ctab_parse:
        ctab = parse_ctab(contents[4:])
    else:
        ctab = ()
    return Mol(name, meta, comment, ctab)


def parse_rd(contents):
    """
    Parse an rd entry.

    Parameters
    ----------
    contents : list
        Rd file contents.

    Returns
    -------
    collections.namedtuple
        Properties: version, time, records

    Raises
    ------
    RdError
        If rd file contents have invalid formatting.
    """
    # Check file validity.
    if len(contents) < 2:
        raise RdError('RD file too short: less than 2 lines found')
    elif contents[0] != '$RDFILE 1':
        raise RdError('identifier "$RDFILE 1" not found at begin')
    elif not contents[1].startswith('$DATM '):
        raise RdError('Time stamp "$DATM " not found at begin')
    # Parse RD file.
    *__, time = contents[1].partition(' ')
    records = []
    intervals_record = []
    # Detect records.
    for i, row in enumerate(contents):
        if row.startswith('$RFMT'):
            intervals_record.append(i)
    intervals_record.append(i + 1)  # i + 1 == len(contents)
    # Parse records.
    for i, j in zip(intervals_record[:-1], intervals_record[1:]):
        records.append(_parse_rd_record(contents[i:j]))
    return Rd(version='1', time=time, records=records)


def _parse_rd_record(contents):
    """
    """
    # Check record validity.
    if not contents[0].startswith('$RFMT'):
        raise RdError('identifier $RFMT expected at begin, {} found'.format(
            contents[0]))
    # Detect data.
    intervals_dtype = []
    for i, row in enumerate(contents):
        if row.startswith('$DTYPE'):
            intervals_dtype.append(i)
    intervals_dtype.append(i + 1)  # i + 1 == len(contents)
    # Parse record.
    *__, identifier = contents[0].partition(' ')
    rxn = parse_rxn(contents[1:intervals_dtype[0]])
    data = {}
    for i, j in zip(intervals_dtype[:-1], intervals_dtype[1:]):
        *__, dtype = contents[i].partition(' ')
        *__, datum = contents[1+i].partition(' ')
        datum_multiline = ' '.join(contents[2+i:j])
        if datum_multiline:
            data[dtype] = ' '.join([datum, datum_multiline])
        else:
            data[dtype] = datum
    return RdRecord(identifier=identifier, rxn=rxn, data=data)


def parse_rxn(contents):
    """
    Parse rxn entry.

    Parameters
    ----------
    contents : list
        Rxn entry contents.

    Returns
    -------
    collections.namedtuple
        properties: name, comment, n_reactants, n_products, mols

    Raises
    ------
    RxnError
        If rxn entry contents have invalid formatting.

    """
    if len(contents) < 5:
        raise RxnError(
            'RXN file too short: expected minimum of 5, {} found'.format(
                len(contents)))
    elif contents[0] != '$RXN':
        raise RxnError('identifier $RXN expected at begin, {} found'.format(
            contents[0]))
    name = contents[2]
    comment = contents[3]
    n_reactants = int(contents[4][0:3])
    n_products = int(contents[4][3:6])
    mols = []
    # Detect mols.
    intervals_mol = []
    for i, row in enumerate(contents):
        if row == '$MOL':
            intervals_mol.append(i)
    intervals_mol.append(i + 1)
    for i, j in zip(intervals_mol[:-1], intervals_mol[1:]):
        mols.append(parse_mol(contents[i:j]))
    # Check validity.
    if len(mols) != n_reactants + n_products:
        raise RxnError('{} $MOL entries expected, {} found'.format(
            n_reactants + n_products, len(mols)))
    return Rxn(name, comment, n_reactants, n_products, mols)


def parse_tsv(contents, fields_header=[]):
    """
    Parse tsv file.

    Parameters
    ----------
    contents : list
        Tsv file contents.
    fields_header : iterable of hashables
        Keys used in yielded dicts. Default [], in which case the
        file is assumed to provide field headers at first row.

    Yields
    ------
    dict
        Tsv field value string keyed by field headers provided either in
        the file or by the user in fields_header.
    """
    start_index = 0
    if not fields_header:
        fields_header = contents[0].strip().split(_DELIMITER_TSV)
        start_index = 1
    for index_row, row in enumerate(contents[start_index:]):
        fields_row = row.strip().split(_DELIMITER_TSV)
        if len(fields_header) != len(fields_row):
            raise TsvError(
                "row {}: {} fields found, {} expected".format(
                    index_row, len(fields_row), len(fields_header)))
        else:
            yield dict(zip(fields_header, fields_row))


def write_json(python_object, path, filename):
    """
    Save object data in a JSON file.

    Parameters
    ----------
    python_object : object
        Object to be saved in the JSON file.
    path : string
        Directory path to file.
    filename : string
        Name of the target JSON file. Filename must not contain path.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If path or filename is not string.

    """
    if not isinstance(path, str):
        raise TypeError('`path` must be str')
    elif not isinstance(filename, str):
        raise TypeError('`filename` must be str')
    with open(os.path.join(path, filename), 'w') as file:
        json.dump(python_object, file)


def write_jsons(data, path, filenames):
    """
    Save objects in JSON files.

    Parameters
    ----------
    data : list
        Objects to be saved in the files. Object index must correspond to
        filename index.
    path : string
        Directory path to file.
    filenames : list
        Names of the target JSON files. Filename index must correspond
        to object index.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If data or filenames is neither list nor tuple, or if path is
        not string.

    """
    if not isinstance(data, (list, tuple)):
        raise TypeError('`data` must be list or tuple')
    elif not isinstance(path, str):
        raise TypeError('`path` must be str')
    elif not isinstance(filenames, (list, tuple)):
        raise TypeError('`filenames` must be list or tuple')
    for object_, filename in zip(data, filenames):
        write_json(object_, path, filename)

