# -*- coding: utf-8 -*-
"""
Read and process ChEBI data to JSON files.

Functions
---------
read_chemical_data: process chemical.tsv
read_compounds: process compounds.tsv
read_relations: process relations.tsv
read_vertices: process vertices.tsv
main: process ChEBI data to JSON files.

"""


from main import (
    # Constants.
    DELIMITER_TSV,
    CHEBI_COMPOUNDS,
    CHEBI_DATA,
    CHEBI_RELATIONS,
    CHEBI_VERTICES,
    FILE_CMP_CHARGES,
    FILE_CMP_FORMULAE,
    FILE_CMP_MASSES,
    FILE_CMP_NAMES,
    FILE_CMP_PARENTS,
    FILE_CMP_RELATIONS,
    PATH_CHEBI,
    PATH_JSON,
    # Functions.
    get_content,
    write_jsons,
    )


def read_chemical_data(contents, compound_parents):
    """
    Read content and return chemical data as dicts.

    Parameters
    ---------
    contents : list
        List of chemical data file row strings.

    compound_parents : dict
        Mapping from compound IDs to parent IDs.

    Returns
    -------
    tuple
        Dicts formed from contents.
        [0] compound IDs to compound charges.
        [1] compound IDs to compound formulae.
        [2] compound IDs to compound masses.

    """
    charges, formulae, masses = {}, {}, {}
    # Process content row by row.
    for row in contents[1:]:
        __, compound, __, type_, data = row.split(DELIMITER_TSV)
        # Map compound ID to parent ID.
        parent = compound_parents.get(compound, compound)
        # Sort data.
        if type_ == 'CHARGE':
            charges[parent] = int(data.strip())
        elif type_ == 'FORMULA':
            formulae[parent] = data.strip()
        elif type_ == 'MASS':
            masses[parent] = float(data.strip())
    return charges, formulae, masses


def read_compounds(contents):
    """
    Read content and return compound data as dicts of str.

    Parameters
    ----------
    contents : list
        List of compound data file row strings.

    Returns
    -------
    tuple
        Dicts formed from contents:
        [0] compound IDs to parent IDs.
        [1] compound IDs to compound names.

   """

    compound_names, compound_parents = {}, {}
    # Process content row by row, but skip header.
    for row in contents[1:]:
        id_, status, __, __, parent, name, *__ = row.split(DELIMITER_TSV)
        # Statuses:
        # C: checked
        # E: preliminary entry
        # O: obsolete
        # S: submitted
        if parent != 'null':
            compound_parents[id_] = parent
        if name != 'null':
            compound_names[id_] = name
    return compound_parents, compound_names


def read_relations(contents, vertex_compounds):
    """
    Read content and return relation data as dict of dict of str.

    Parameters
    ----------
    contents : list
        List of relation data file row strings.

    vertex_compounds : dict
        Mapping from vertex IDs to compound IDs.

    Returns
    -------
    dict
        Mapping from start compound IDs to mappings from goal compound
        IDs to relation type strings.

    """

    compound_relations = {}
    # Process content row by row, but skip header.
    for row in contents[1:]:
        id_, type_, final, initial, status = row.split(DELIMITER_TSV)
        # Include only manually curated relation data.
        if status.strip() == 'C':
            # Map `goal` and `start` to compound IDs.
            start = vertex_compounds[initial]
            goal = vertex_compounds[final]
            # Map relation start to mapping from goal to type.
            try:
                compound_relations[start][goal] = type_
            except KeyError:
                compound_relations[start] = {goal: type_}
    return compound_relations


def read_vertices(content, compound_parents):
    """
    Read content and return vertex data as dict of str.

    Parameters
    ----------
    content : list
        List of vertex data file row strings.

    compound_parents : dict
        Mapping from compound IDs to parents IDs.

    Returns
    -------
    dict
        Mapping from vertex IDs to compound IDs.

    """

    vertex_compounds = {}
    # Process content row by row, but skip header.
    for row in content[1:]:
        id_, compound, *__ = row.split(DELIMITER_TSV)
        # Map compound IDs to parent IDs.
        parent = compound_parents.get(compound, compound)
        vertex_compounds[id_] = parent
    return vertex_compounds


def main():
    """
    Convert ChEBI tsv files to JSON formatted files for analysis.

    Parameters
    ----------
    None

    Returns
    -------
    list
        Dicts of data.

    """

    # Obtain compound data.
    contents_compound = get_content(PATH_CHEBI, CHEBI_COMPOUNDS)
    compound_data = read_compounds(contents_compound)
    compound_parents, compound_names = compound_data

    # Obtain chemical data.
    contents_chemical = get_content(PATH_CHEBI, CHEBI_DATA)
    chemical_data = read_chemical_data(contents_chemical, compound_parents)
    compound_charges, compound_formulae, compound_masses = chemical_data

    # Obtain vertex data.
    contents_vertex = get_content(PATH_CHEBI, CHEBI_VERTICES)
    vertex_compounds = read_vertices(contents_vertex, compound_parents)

    # Obtain relation data.
    contents_relation = get_content(PATH_CHEBI, CHEBI_RELATIONS)
    compound_relations = read_relations(contents_relation, vertex_compounds)

    # Collect data and assign corresponding JSON filenames.
    # List indices must match each other.
    data_all = [
        compound_charges,
        compound_names,
        compound_parents,
        compound_relations,
        compound_formulae,
        compound_masses,
        ]
    jsonnames_all = [
        FILE_CMP_CHARGES,
        FILE_CMP_NAMES,
        FILE_CMP_PARENTS,
        FILE_CMP_RELATIONS,
        FILE_CMP_FORMULAE,
        FILE_CMP_MASSES,
        ]

    # Save data in JSON format.
    write_jsons(data_all, PATH_JSON, jsonnames_all)
    return data_all


if __name__ == '__main__':
    # pass
    data = main()
