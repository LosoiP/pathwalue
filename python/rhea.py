# -*- coding: utf-8 -*-
# (C) 2017 Tampere University of Technology
# MIT License
# Original by Tommi Aho
# Modified by Pauli Losoi

"""
Read and process Rhea data to JSON files.

Functions
---------
crosslink_master_ids
    Map master reaction IDs to reaction IDs.
read_ecs
    Read EC number to Rhea ID mapping data.
read_rd_data
    Read rd records.

"""

from collections import Counter

# Rd file contants:
# An rd file is rejected, if it contains denied qualifiers, if it
# doesn't contain required qualifiers or if it isn't approved.
_RD_APPROVED = 'approved'
_RD_QUALIFIERS_DENIED = ['TR', 'CR']  # transport, class
_RD_QUALIFIERS_REQUIRED = ['CB', 'FO', 'MA']  # balanced, formula, mass


def crosslink_master_ids(reaction_masters):
    """
    Map master reaction IDs to reaction IDs.

    EC numbers are mapped to undirected Rhea master reactions. Rhea rd
    files map directed Rhea reaction to undirected master reactions.
    Mapping master reactions to directed reactions allows mapping enzyme
    EC numbers to directed reaction Rhea IDs.

    Parameters
    ----------
    reaction_masters : dict
        Mapping from reaction IDs to master IDs.

    Returns
    -------
    dict
        Mapping from master IDs to reaction IDs.

    """
    master_reactions = {}
    for rhea, master in reaction_masters.items():
        master_reactions.setdefault(master, []).append(rhea)
    return master_reactions


def read_ecs(contents, reaction_masters, master_reactions):
    """
    Read Rhea EC number to Rhea ID mapping data.

    Parameters
    ----------
    contents : iterable of dicts
        EC number string keyed by 'EC' and Rhea ID string keyed by
        'RHEA'.
    reaction_masters : dict
        Mapping from directed reaction Rhea ID strings to undirected
        master reaction Rhea ID strings.
    masters_reactions: dict
        Mapping from undirected master reaction Rhea ID strings to
        directed reaction Rhea ID strings.

    Returns
    -------
    tuple of 2 dicts
        Complementary dicts that map EC numbers to Rhea IDs and vice
        -versa.

        [0] maps EC number strings to Rhea ID strings.

        [1] maps Rhea ID strings to EC number strings.

    """
    ec_reactions, reaction_ecs = {}, {}
    for entry in contents:
        ec = entry['EC']
        rhea = entry['RHEA']
        master = reaction_masters.get(rhea, rhea)
        reactions = master_reactions.get(master, [])
        ec_reactions.setdefault(ec, set()).update(reactions)
        for reaction in reactions:
            reaction_ecs.setdefault(reaction, set()).add(ec)
        print('RHEA: EC {}, reactions {}'.format(ec, reactions))
    for ec, reactions in ec_reactions.items():
        ec_reactions[ec] = list(reactions)
    for reaction, ecs in reaction_ecs.items():
        reaction_ecs[reaction] = list(ecs)
    print('RHEA: {} enzymes found, linked to {} reactions'.format(
        len(ec_reactions), len(reaction_ecs)))
    return ec_reactions, reaction_ecs


def read_rd_data(rds_parsed, chebi_parents):
    """
    Read rd records.

    Parameters
    ----------
    rds_parsed : iterable of files.Rd namedtuples
        Parsed rd files.

    Returns
    -------
    tuple of 4 dicts
        [0] mapping from ChEBI ID strings to 2 lists of Rhea ID strings,
        [0] corresponds to reactions consuming the molecule, [1] to
        reactions producing.

        [1] mapping from Rhea ID strings to reaction equation strings.

        [2] mapping from directed reaction Rhea ID strings to undirected
        master reaction Rhea ID strings.

        [3] mapping from Rhea ID strings to a list of 2 mappings from
        ChEBI ID strings to stoichiometric integers. [0] corresponds to
        consumed molecules and [1] to produced molecules.

    See also
    --------
        files.parse_rd
    """
    mol_rxns, rxn_equats, rxn_masters, rxn_stoich = {}, {}, {}, {}
    n_records = 0
    n_accepted = 0
    types_dtype = Counter()
    types_status = Counter()
    types_qualifier = Counter()
    for rd in rds_parsed:
        for record in rd.records:
            approve_reaction = True
            print('RHEA: {}'.format(record.identifier), end='')
            n_records += 1
            # Save datatypes.
            types_dtype.update(record.data.keys())
            # Check reaction status and qualifiers.
            status = record.data['status']
            types_status[status] += 1
            if status != _RD_APPROVED:
                print(', status {}'.format(status), end='')
                approve_reaction = False
            # Check reaction qualifiers.
            qualifiers_raw = record.data['qualifiers']
            qualifiers = qualifiers_raw.strip('[]').replace(' ', '').split(',')
            types_qualifier.update(qualifiers)
            if any(q in qualifiers for q in _RD_QUALIFIERS_DENIED):
                print(', forbidden qualifiers {}'.format(qualifiers), end='')
                approve_reaction = False
            elif not all(q in qualifiers for q in _RD_QUALIFIERS_REQUIRED):
                print(', inadequate qualifiers {}'.format(qualifiers), end='')
                approve_reaction = False
            # Check that reaction molecules belong to ChEBI.
            rxn = record.rxn
            for mol in rxn.mols:
                if mol.name.partition(':')[0] != 'CHEBI':
                    print(', non-ChEBI $MOL entry {}'.format(mol.name), end='')
                    approve_reaction = False
            # Save reaction data.
            if approve_reaction:
                *__, id_rhea = record.identifier.partition(' ')
                print(', saving reaction {}'.format(id_rhea))
                reactants = Counter()
                for mol in rxn.mols[:rxn.n_reactants]:
                    *__, id_chebi = mol.name.partition(':')
                    chebi = chebi_parents.get(id_chebi, id_chebi)
                    mol_rxns.setdefault(id_chebi, [[], []])[0].append(id_rhea)
                    reactants[chebi] += 1
                products = Counter()
                for mol in rxn.mols[rxn.n_reactants:]:
                    *__, id_chebi = mol.name.partition(':')
                    chebi = chebi_parents.get(id_chebi, id_chebi)
                    mol_rxns.setdefault(id_chebi, [[], []])[1].append(id_rhea)
                    products[chebi] += 1
                rxn_stoich[id_rhea] = [dict(reactants), dict(products)]
                rxn_equats[id_rhea] = record.data['equation']
                rxn_masters[id_rhea] = record.data['masterId']
                n_accepted += 1
            else:
                print()
    for chebi, reactions in mol_rxns.items():
        mol_rxns[chebi] = [list(set(reactions[0])), list(set(reactions[1]))]
    print('RHEA: {} records read, {} accepted'.format(n_records, n_accepted))
    print('RHEA: found statuses {}'.format(types_status))
    print('RHEA: found qualifiers {}'.format(types_qualifier))
    print('RHEA: found $DTYPEs {}'.format(types_dtype))
    return mol_rxns, rxn_equats, rxn_masters, rxn_stoich
