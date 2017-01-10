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
    for ec, reactions in ec_reactions.items():
        ec_reactions[ec] = list(reactions)
    for reaction, ecs in reaction_ecs.items():
        reaction_ecs[reaction] = list(ecs)
    return ec_reactions, reaction_ecs


def read_rds_old(filenames):
    """
    Read rd files, and return reaction data and target JSON filenames.

    Parameters
    ----------
    filenames : list
        Names of rd files. Names must contain the file extension.

    Returns
    -------
    tuple
        Dict objects formed from rd files.
        [0] compound ChEBI IDs to consuming and producing reaction Rhea
        ID lists.
        [1] reaction Rhea IDs to reaction equation strings.
        [2] list of dicts of reaction Rhea IDs to dicts of reactant and
        product IDs to stoichiometric numbers.

    """
    # Preallocate data collections.
    chebis_all = set()
    data_equations, data_stoichiometrics = {}, {}
    compound_consumed_by, compound_produced_by = {}, {}
    master_reactions, reaction_masters = {}, {}
    reaction_masters_reactions = {}

    # Process contents file by file.
    for filename in filenames:
        content = get_content(PATH_RD, filename)

        # Reset reaction file variables.
        reaction, equation = '', ''
        chebis = []
        approved = False
        # qualified = False  # Out of use since 20160616.
        nr_row = 0

        # Parse reaction file.
        while nr_row < len(content):
            row = content[nr_row]
            # Recognize data fields.
            if row.startswith('$'):
                columns = row.split()
                marker = columns[0]
                # Find ChEBI IDs.
                if marker == '$MOL':
                    nr_row += 1
                    type_id, chebi = content[nr_row].split(':')
                    if type_id != 'CHEBI':
                        approved = False
                        break
                    parent = PARENTS.get(chebi.rstrip(), chebi.rstrip())
                    chebis.append(parent)
                # Find master ID, status and equation.
                # Qualifiers (out of use at the moment):
                # TR - transport
                # CR - class of reactions
                # CB - chemically balanced
                # MA - ?
                # FO - ?
                elif marker == '$DTYPE':
                    dtype = columns[1].rstrip()
                    nr_row += 1
                    if dtype == 'masterId':
                        __, master = content[nr_row].split()
                    elif dtype == 'status':
                        __, status = content[nr_row].split()
                        if status == 'approved':
                            approved = True
                    elif dtype == 'qualifiers':
                        *__, qualifiers = content[nr_row].partition(' ')
                        if 'TR' in qualifiers:
                            approved = False
                            break
                    elif dtype == 'equation':
                        # Detect how many rows the equation spans.
                        nr_target = nr_row
                        while nr_target < len(content):
                            if content[nr_target]:
                                nr_target += 1
                            else:
                                break
                        # Form the equation string.
                        equation = ''.join(content[nr_row:nr_target])
                        equation = equation.lstrip('$DATUM').strip()
                        equation = equation.replace('\n', '')
                        nr_row = nr_target
                # Find Rhea ID and stoichiometric numbers.
                elif marker == '$RXN':
                    nr_row += 1
                    nr_target = nr_row
                    while nr_target < len(content):
                        target = content[nr_target]
                        if target.startswith('Rhea'):
                            *__, reaction = content[nr_target].split()
                        elif target.startswith('RHEA'):
                            nr_target += 1
                            numbers = content[nr_target].split()
                            n_reactants, n_products = list(map(int, numbers))
                            break
                        elif target.startswith('$'):
                            break
                        nr_target += 1
                    nr_row = nr_target
            nr_row += 1

        # Save approved and qualified reaction data.
        # NOTE Qualifiers are now ignored 16.6.2016
        if approved:
            chebis_all.update(chebis)
            # Calculate stoichiometric numbers.
            reactants = Counter(chebis[:n_reactants])
            products = Counter(chebis[n_reactants:n_reactants + n_products])
            # Assign reaction to reactants.
            for reactant in reactants:
                compound_consumed_by.setdefault(reactant, []).append(reaction)
            # Assign reaction to products.
            for product in products:
                compound_produced_by.setdefault(product, []).append(reaction)
            # Add reaction data to data dicts.
            data_equations[reaction] = equation
            data_stoichiometrics[reaction] = [dict(reactants), dict(products)]
            reaction_masters[reaction] = master
            master_reactions.setdefault(master, []).append(reaction)

    # Map compounds to reactions.
    data_compound_reactions = {}
    for compound in chebis_all:
        consumes = compound_consumed_by.get(compound, [])
        produces = compound_produced_by.get(compound, [])
        data_compound_reactions[compound] = [consumes, produces]

    # Map reactions to masters to reactions.
    for reaction in reaction_masters:
        master = reaction_masters[reaction]
        reactions = master_reactions[master]
        reaction_masters_reactions[reaction] = {master: reactions}

    data = [data_compound_reactions,
            data_equations,
            reaction_masters_reactions,
            data_stoichiometrics,
            ]
    return data


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
                for mol in rxn.mols[:rxn.n_reactants]:
                    *__, id_chebi = mol.name.partition(':')
                    chebi = chebi_parents.get(id_chebi, id_chebi)
                    mol_rxns.setdefault(id_chebi, [[], []])[0].append(id_rhea)
                    rxn_stoich.setdefault(id_rhea, [[], []])[0].append(chebi)
                for mol in rxn.mols[rxn.n_reactants:]:
                    *__, id_chebi = mol.name.partition(':')
                    chebi = chebi_parents.get(id_chebi, id_chebi)
                    mol_rxns.setdefault(id_chebi, [[], []])[1].append(id_rhea)
                    rxn_stoich.setdefault(id_rhea, [[], []])[1].append(chebi)
                rxn_equats[id_rhea] = record.data['equation']
                rxn_masters[id_rhea] = record.data['masterId']
                n_accepted += 1
            else:
                print()
    print('RHEA: {} records read, {} accepted'.format(n_records, n_accepted))
    print('RHEA: found statuses {}'.format(types_status))
    print('RHEA: found qualifiers {}'.format(types_qualifier))
    print('RHEA: found $DTYPEs {}'.format(types_dtype))
    return mol_rxns, rxn_equats, rxn_masters, rxn_stoich
