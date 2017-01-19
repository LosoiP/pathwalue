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


from collections import namedtuple

import chebi
import files
import market
import paths
import pw
import rhea


def compare_pathways(pathways_raw, reactions_ref, context):
    """
    """
    Pathway = namedtuple('Pathway', ['path', 'score', 's_s', 's_p', 's_mol',
                                     's_rxn'])
    pathways = []
    substrates_ref = set()
    products_ref = set()
    for reaction in reactions_ref:
        substrates_ref.update(context['stoichiometrics'][reaction][0])
        products_ref.update(context['stoichiometrics'][reaction][1])
    compounds_ref = substrates_ref | products_ref
    for score, reactions in pathways_raw:
        substrates = set()
        products = set()
        for reaction in reactions:
            substrates.update(context['stoichiometrics'][reaction][0])
            products.update(context['stoichiometrics'][reaction][1])
        compounds = substrates | products
        intersect_c = compounds & compounds_ref
        intersect_s = substrates & substrates_ref
        intersect_p = products & products_ref
        intersect_r = set(reactions) & set(reactions_ref)
        union_c = compounds | compounds_ref
        union_s = substrates | substrates_ref
        union_p = products | products_ref
        union_r = set(reactions) | set(reactions_ref)
        s_s = len(intersect_s) / len(union_s)
        s_p = len(intersect_p) / len(union_p)
        s_m = len(intersect_c) / len(union_c)
        s_r = len(intersect_r) / len(union_r)
        pathway = Pathway(reactions, score, s_s, s_p, s_m, s_r)
        pathways.append(pathway)
    return pathways


def initialize_chebi():
    """
    Convert ChEBI tsv files to JSON files.

    Parameters
    ----------
    None

    Returns
    -------
    list
        Dicts of data.

    """
    # Obtain compound data.
    raw_compounds = files.get_content(paths.CHEBI_TSV, files.CHEBI_COMPOUNDS)
    tsv_compounds = files.parse_tsv(raw_compounds)
    compound_data = chebi.parse_compounds(tsv_compounds)
    compound_parents, compound_names = compound_data

    # Obtain chemical data.
    raw_chemical = files.get_content(paths.CHEBI_TSV, files.CHEBI_DATA)
    tsv_chemical = files.parse_tsv(raw_chemical)
    chemical_data = chebi.parse_chemical_data(tsv_chemical, compound_parents)
    compound_charges, compound_formulae, compound_masses = chemical_data

    # Obtain vertex data.
    raw_vertex = files.get_content(paths.CHEBI_TSV, files.CHEBI_VERTICES)
    tsv_vertex = files.parse_tsv(raw_vertex)
    vertex_compounds = chebi.parse_vertices(tsv_vertex, compound_parents)

    # Obtain relation data.
    raw_relation = files.get_content(paths.CHEBI_TSV, files.CHEBI_RELATIONS)
    tsv_relation = files.parse_tsv(raw_relation)
    compound_relations = chebi.parse_relations(tsv_relation, vertex_compounds)

    # Collect data and assign corresponding JSON filenames.
    # List indices must match each other.
    data = [
        compound_charges,
        compound_names,
        compound_parents,
        compound_relations,
        compound_formulae,
        compound_masses,
        ]
    jsonnames = [
        files.MOL_CHARGES,
        files.MOL_NAMES,
        files.MOL_PARENTS,
        files.MOL_RELATIONS,
        files.MOL_FORMULAE,
        files.MOL_MASSES,
        ]

    # Save data in JSON format.
    files.write_jsons(data, paths.JSON, jsonnames)
    return data


def initialize_market():
    """
    Run analysis to evaluate demands, prices and complexities.

    Parameters
    ----------
    None

    Returns
    -------
    list
        Dicts of data.

    """
    compound_reactions = files.get_json(paths.JSON, files.MOL_REACTIONS)
    compound_relations = files.get_json(paths.JSON, files.MOL_RELATIONS)
    stoichiometrics = files.get_json(paths.JSON, files.RXN_STOICHIOMETRICS)
    complexity_compounds = market.COMPLEXITY_COMPOUNDS

    graph_d = market.initialize_graph(compound_relations,
                                      market.RELATIONS_DEMAND)
    graph_p = market.initialize_graph(compound_relations,
                                      market.RELATIONS_PRICE)
    # Collect and save data to JSON files.
    demand, price, complexity = {}, {}, {}
    ignored = 0
    for compound in compound_reactions:
        print('MARKET: CHEBI {}'.format(compound), end='')
        if compound in chebi.IGNORED_COMPOUNDS:
            print(', ignored')
            demand[compound] = 0
            price[compound] = 0
            ignored += 1
        else:
            demand[compound] = market.evaluate_ontology(graph_d, compound,
                                                        market.CHEBIS_DEMAND)
            price[compound] = market.evaluate_ontology(graph_p, compound,
                                                       market.CHEBIS_PRICE)
            print(', demand {}, price {}'.format(demand[compound],
                                                 price[compound]))
    for reaction in stoichiometrics:
        complexity[reaction] = market.evaluate_complexity(reaction,
                                                          stoichiometrics,
                                                          complexity_compounds)
        print('MARKET: RHEA {}, complexity {}'.format(reaction,
                                                      complexity[reaction]))
    print('MARKET: {}/{} compounds, {} reactions'.format(
        len(compound_reactions) - ignored, len(compound_reactions),
        len(stoichiometrics)))
    data = [
        complexity,
        demand,
        price,
        ]
    jsonnames = [
        files.RXN_COMPLEXITIES,
        files.MOL_DEMANDS,
        files.MOL_PRICES,
        ]
    files.write_jsons(data, paths.JSON, jsonnames)
    return data


def initialize_rhea(chebi_parents={}):
    """
    Convert Rhea rd files to JSON formatted files for analysis.

    Parameters
    ----------
    None

    Returns
    -------
    list
        Rhea data in dicts.

    """
    # Obtain rd filenames.
    rd_filenames = paths.get_names(paths.RHEA_RD)

    # Extract data from rd files.
    rds_raw = files.get_contents(paths.RHEA_RD, rd_filenames)
    rds_parsed = (files.parse_rd(rd) for rd in rds_raw)
    data_rhea = rhea.read_rd_data(rds_parsed, chebi_parents)
    mol_rxns, rxn_equats, rxn_master, rxn_stoich = data_rhea
    master_rxn = rhea.crosslink_master_ids(rxn_master)

    # Extract data from tsv file.
    ecs_raw = files.get_content(paths.RHEA_TSV, files.RHEA_EC)
    ecs_tsv = files.parse_tsv(ecs_raw, ['EC', 'RHEA', 'DIRECTION'])
    ec_reactions, reaction_ecs = rhea.read_ecs(ecs_tsv, rxn_master, master_rxn)

    # Save data in JSON format.
    data = [mol_rxns,
            ec_reactions,
            reaction_ecs,
            rxn_equats,
            rxn_stoich,
            ]
    jsonnames = [files.MOL_REACTIONS,
                 files.ENZ_REACTIONS,
                 files.RXN_ECS,
                 files.RXN_EQUATIONS,
                 files.RXN_STOICHIOMETRICS,
                 ]
    files.write_jsons(data, paths.JSON, jsonnames)

    return data


def main():
    """
    """
    # Define context.
    context = {
        'ec_reactions': files.get_json(paths.JSON, files.ENZ_REACTIONS),
        'compound_reactions': files.get_json(paths.JSON, files.MOL_REACTIONS),
        'complexities': files.get_json(paths.JSON, files.RXN_COMPLEXITIES),
        'demands': files.get_json(paths.JSON, files.MOL_DEMANDS),
        'equations': files.get_json(paths.JSON, files.RXN_EQUATIONS),
        'ignored': chebi.IGNORED_COMPOUNDS,
        'prices': files.get_json(paths.JSON, files.MOL_PRICES),
        'reaction_ecs': files.get_json(paths.JSON, files.RXN_ECS),
        'stoichiometrics': files.get_json(paths.JSON,
                                          files.RXN_STOICHIOMETRICS),
        }
    S = context['stoichiometrics']
    mol_rxns = context['compound_reactions']
    G = pw.initialize_graph(S, mol_rxns, set(), chebi.IGNORED_COMPOUNDS)

    # Define reference pathways.
    ref_eth = ['45485', '25292']
    ref_iso = ['10189', '15991', '17066', '16342', '23733', '23285', '13370']

    # Obtain results.
    start = 100
    stop = 101
    Cs_eth = [
        [],
        ['any', '16236'],
        ['15361', 'any'],
        ['15361', '16236'],
#        ['any', '15343', '16236'],
#        ['15361', '15343', 'any'],
#        ['15361', '15343', '16236'],
        ]
    Es_eth = [
        [],
#        ['4.1.1.1'],
#        ['1.1.1.1'],
#        ['4.1.1.1', '1.1.1.1'],
        ]
    Cs_iso = [
        [],
        ['any', '35194'],
        ['57286', 'any'],
        ['57286', '35194'],
#        ['any', '43074', '35194'],
#        ['any', '57623', '35194'],
#        ['any', '58146', '57557', '35194'],
#        ['57286', '57623', 'any'],
#        ['57286', '43074', 'any'],
#        ['57286', '58146', '57557', 'any'],
#        ['57286', '43074', '36464', '58146', '57557', '128769', '57623', '35194'],
        ]
    Es_iso = [
        [],
#        ['2.3.3.10'],
#        ['4.2.3.27'],
#        ['2.3.3.10', '4.2.3.27'],
#        ['2.3.3.10', '5.3.3.2', '4.2.3.27'],
#        ['2.3.3.10', '4.1.1.33', '5.3.3.2', '4.2.3.27'],
#        ['2.3.3.10', '2.7.4.2', '4.1.1.33', '5.3.3.2', '4.2.3.27'],
#        ['2.3.3.10', '2.7.1.36', '2.7.4.2', '4.1.1.33', '5.3.3.2', '4.2.3.27'],
#        ['2.3.3.10', '1.1.1.34', '2.7.1.36', '2.7.4.2', '4.1.1.33', '5.3.3.2', '4.2.3.27'],
#        ['2.3.3.10', '1.1.1.34', '4.2.3.27'],
#        ['2.3.3.10', '1.1.1.34', '2.7.1.36', '4.2.3.27'],
#        ['2.3.3.10', '1.1.1.34', '2.7.1.36', '2.7.4.2', '4.2.3.27'],
#        ['2.3.3.10', '1.1.1.34', '2.7.1.36', '2.7.4.2', '4.1.1.33', '4.2.3.27'],
#        ['2.3.3.10', '1.1.1.34', '2.7.1.36', '2.7.4.2', '4.1.1.33', '5.3.3.2', '4.2.3.27'],
        ]
    results_eth = run_analysis(G, start, stop, Cs_eth, Es_eth, ref_eth,
                               context)
    results_iso = run_analysis(G, start, stop, Cs_iso, Es_iso, ref_iso,
                               context)

    return show_results([results_eth, results_iso], ['ETH', 'ISO'], context)


def run_analysis(G, n_start, n_stop, Cs, Es, reference, context):
    """
    """
    Parameters = namedtuple('Parameters', ['n', 'C', 'E'])
    Result = namedtuple('Result', ['pathways', 'parameters'])
    results = []
    for n in range(n_start, n_stop):
        for C in Cs:
            for E in Es:
                parameters = Parameters(n, C, E)
                raw = pw.evaluate_input(n, G, C, E, context)
                # Compare to reference and save results.
                pathways = compare_pathways(raw, reference, context)
                results.append(Result(pathways, parameters))
    return results


def show_results(results, names, context):
    """
    """
    pw_entries = ['score', 's_s', 's_p', 's_mol', 's_rxn']
    results_best = []
    with open('results_all.txt', mode='w') as file:
        for result, name in zip(results, names):
            for pathways, parameters in result:
                print(name, parameters)
                print(name, parameters, file=file)
                s_mols = []
                s_rxns = []
                n = len(pathways)
                for pathway in pathways:
                    print(pathway)
                    print(pathway, file=file)
                    s_mols.append(pathway.s_mol)
                    s_rxns.append(pathway.s_rxn)
                    for rxn in pathway.path:
                        print(rxn, context['equations'][rxn])
                        print(rxn, context['equations'][rxn], file=file)
                    for value, key in zip(pathway[1:], pw_entries):
                        print(key, value)
                        print(key, value, file=file)
                    print()
                    print(file=file)
                if n > 0:
                    mean_mols = sum(s_mols) / n
                    mean_rxns = sum(s_rxns) / n
                    print(name, 'Result:', mean_mols, file=file)
                    print(name, 'Result:', mean_rxns, file=file)
                    if mean_mols > 0.5 or mean_rxns > 0.5:
                        results_best.append([parameters, pathways, name,
                                             mean_mols, mean_rxns])
                print()
                print(file=file)
    with open('results.txt', mode='w') as file:
        for parameters, pathways, name, mean_mols, mean_rxns in results_best:
            if len(pathways) == 0:
                continue
            print(name, parameters, file=file)
            print(name, mean_mols, mean_rxns, file=file)
            print(file=file)
            for pathway in pathways:
                print(pathway, file=file)
                for rxn in pathway.path:
                    print(rxn, context['equations'][rxn], file=file)
                for value, key in zip(pathway[1:], pw_entries):
                    print(key, value, file=file)
                print(file=file)
            print(file=file)
    return results_best
