# -*- coding: utf-8 -*-
"""
Define functions, constants and exceptions for PathWalue application.

PEP 257:
The docstring of a script (a stand-alone program) should be usable as
its "usage" message, printed when the script is invoked with incorrect
or missing arguments (or perhaps with a "-h" option, for "help"). Such
a docstring should document the script's function and command line
syntax, environment variables, and files. Usage messages can be fairly
elaborate (several screens full) and should be sufficient for a new
user to use the command properly, as well as a complete quick reference
to all options and arguments for the sophisticated user.

The docstring for a module should generally list the classes,
exceptions and functions (and any other objects) that are exported by
the module, with a one-line summary of each. (These summaries generally
give less detail than the summary line in the object's docstring.) The
docstring for a package (i.e., the docstring of the package's
__init__.py module) should also list the modules and subpackages
exported by the package.

The docstring for a function or method should summarize its behavior
and document its arguments, return value(s), side effects, exceptions
raised, and restrictions on when it can be called (all if applicable).
Optional arguments should be indicated. It should be documented whether
keyword arguments are part of the interface.

The docstring for a class should summarize its behavior and list the
public methods and instance variables. If the class is intended to be
subclassed, and has an additional interface for subclasses, this
interface should be listed separately (in the docstring). The class
constructor should be documented in the docstring for its __init__
method. Individual methods should be documented by their own docstring.

If a class subclasses another class and its behavior is mostly
inherited from that class, its docstring should mention this and
summarize the differences. Use the verb "override" to indicate that a
subclass method replaces a superclass method and does not call the
superclass method; use the verb "extend" to indicate that a subclass
method calls the superclass method (in addition to its own behavior).

"""


import chebi
import files
import paths


def initialize_chebi():
    """
    Convert ChEBI tsv files to JSON files for analysis.

    Parameters
    ----------
    None

    Returns
    -------
    list
        Dicts of data.

    """

    # Obtain compound data.
    contents_compound = files.get_content(paths.CHEBI_TSV, files.CHEBI_COMPOUNDS)
    compound_data = read_compounds(contents_compound)
    compound_parents, compound_names = compound_data

    # Obtain chemical data.
    contents_chemical = files.get_content(paths.CHEBI_TSV, files.CHEBI_DATA)
    chemical_data = read_chemical_data(contents_chemical, compound_parents)
    compound_charges, compound_formulae, compound_masses = chemical_data

    # Obtain vertex data.
    contents_vertex = files.get_content(paths.CHEBI_TSV, files.CHEBI_VERTICES)
    vertex_compounds = read_vertices(contents_vertex, compound_parents)

    # Obtain relation data.
    contents_relation = files.get_content(paths.CHEBI_TSV, files.CHEBI_RELATIONS)
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
        files.MOL_CHARGES,
        files.MOL_NAMES,
        files.MOL_PARENTS,
        files.MOL_RELATIONS,
        files.MOL_FORMULAE,
        files.MOL_MASSES,
        ]

    # Save data in JSON format.
    files.write_jsons(data_all, paths.JSON, jsonnames_all)
    return data_all


if __name__ == '__main__':
    pass
