# -*- coding: utf-8 -*-
"""
Read and process IntEnz data to JSON files.

Functions
---------
get_enzymes: find EC numbers and enzyme names
merge_dicts: process a list of dicts to a dict.
main: process IntEnz data to JSON files.

"""


from main import (
    FILE_EC_NAMES,
    INTENZ,
    PATH_INTENZ,
    PATH_JSON,
    get_content,
    write_json,
    )


def get_enzymes(content):
    """
    Find enzyme names names and EC numbers in content.

    Parameters
    ----------
    content : iterable
        Content strs.

    Yields
    ------
    dict
        Mapping from EC number str to enzyme name str.

    """
    ec = ''
    name = []
    for row in content:
        if row.startswith('ID'):
            ec = row[5:].rstrip()
        elif row.startswith('DE'):
            name.append(row[5:].rstrip().rstrip('.'))
        elif row.startswith('//'):
            yield {'ec': ec, 'name': ' '.join(name)}
            name.clear()


def merge_dicts(dicts, kkey, vkey):
    """
    Map `kkey` value to `vkey` value from dicts in `dicts`.

    Parameters
    ----------
    dicts : iterable
        Dicts.
    kkey : hashable
        The key to fetch values from `dicts` to be used as keys.
    vkey : hashable
        The key to fetch values from `dicts` to be used as values.

    Returns
    -------
    dict
        A new dict that maps `kkey` values from `dicts` to `vkey`
        values from `dicts`.

    """
    return {d.get(kkey): d.get(vkey) for d in dicts if kkey in d and vkey in d}


def main():
    """
    Read and process IntEnz enzyme.dat file to JSON files.

    Parameters
    ----------
    None

    Returns
    -------
    list
        Dicts of IntEnz data.

    """
    content = get_content(PATH_INTENZ, INTENZ)
    ec_names = merge_dicts(get_enzymes(content), 'ec', 'name')
    write_json(ec_names, PATH_JSON, FILE_EC_NAMES)
    data = [
        ec_names,
        ]
    return data


if __name__ == '__main__':
    data = main()
