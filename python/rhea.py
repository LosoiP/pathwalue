# -*- coding: utf-8 -*-
# Original by Tommi Aho
# Modified by Pauli Losoi

"""
Read and process Rhea data to JSON files.

Requires that chebi.main() has been run. (ChEBI parent IDs)

Functions
---------
read_ecs: read and process EC file.
read_rds: read and process rd files.
main: process Rhea data to JSON files.

"""

from collections import Counter

RD_APPROVED = 'approved'
RD_QUALIFIERS_DENIED = ['TR', 'CR']  # transport, class
RD_QUALIFIERS_REQUIRED = ['CB', 'FO', 'MA']  # balanced, formula, mass


def crosslink_master_ids(reaction_masters):
    """
    """
    master_reactions = {}
    for rhea, master in reaction_masters.items():
        master_reactions.setdefault(master, []).append(rhea)
    return master_reactions


def read_ecs(contents, reaction_masters, master_reactions):
    """
    Read Rhea EC number data.

    Parameters
    ----------
    contents : iterable
        EC file rows as strings.
    reaction_masters_reactions: dict
        Rhea ID string keys to dict values that map Rhea ID strings to
        a list of Rhea ID strings.

    Returns
    -------
    tuple
        Rhea EC number data dicts that map EC numbers to Rhea IDs and
        vice-versa.

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
            if status != RD_APPROVED:
                print(', status {}'.format(status), end='')
                approve_reaction = False
            # Check reaction qualifiers.
            qualifiers_raw = record.data['qualifiers']
            qualifiers = qualifiers_raw.strip('[]').replace(' ', '').split(',')
            types_qualifier.update(qualifiers)
            if any(q in qualifiers for q in RD_QUALIFIERS_DENIED):
                print(', forbidden qualifiers {}'.format(qualifiers), end='')
                approve_reaction = False
            elif not all(q in qualifiers for q in RD_QUALIFIERS_REQUIRED):
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
