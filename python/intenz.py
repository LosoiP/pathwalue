# -*- coding: utf-8 -*-
# (C) 2017 Tampere University of Technology
# MIT License
# Pauli Losoi
"""
Read and process IntEnz data file.

Functions
---------
get_enzymes
    find EC numbers and enzyme names
merge_dicts
    process a list of dicts to a dict.

Todo
----
Move merge_dicts to a more appropriate module.

"""


def get_enzymes(content):
    """
    Find enzyme names and EC numbers in contents.

    Parameters
    ----------
    content : iterable
        enzyme.dat file content strings.

    Yields
    ------
    dict
        Mapping from EC number strings to enzyme name strings.

    """
    ec = ''
    name = []
    for row in content:
        if row.startswith('ID'):
            ec = row[5:].rstrip()
        elif row.startswith('DE'):
            name.append(row[5:].rstrip().rstrip('.'))
        elif row.startswith('//'):
            if name:
                yield {'ec': ec, 'name': ' '.join(name)}
                name.clear()


def merge_dicts(dicts, kkey, vkey):
    """
    Map kkey value to vkey value from dicts in dicts.

    Parameters
    ----------
    dicts : iterable
        Dicts.
    kkey : hashable
        The key to fetch values from dicts to be used as keys.
    vkey : hashable
        The key to fetch values from dicts to be used as values.

    Returns
    -------
    dict
        A new dict that maps kkey values from dicts to vkey values from
        dicts.

    """
    return {d.get(kkey): d.get(vkey) for d in dicts if kkey in d and vkey in d}
