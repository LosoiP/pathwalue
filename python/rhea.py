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

from main import (
    # Constants.
    DELIMITER_TSV,
    FILE_CMP_PARENTS,
    FILE_CMP_REACTIONS,
    FILE_EC_REACTIONS,
    FILE_RXN_ECS,
    FILE_RXN_EQUATIONS,
    FILE_RXN_STOICHIOMETRICS,
    RHEA_EC,
    PATH_JSON,
    PATH_RD,
    PATH_RHEA,
    # Functions.
    get_content,
    get_json,
    get_names,
    write_jsons,
    )

PARENTS = get_json(PATH_JSON, FILE_CMP_PARENTS)  # Run chebi.main() first.


def read_ecs(contents, reaction_masters_reactions):
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
    for row in contents:
        ec, rhea, __ = row.split(DELIMITER_TSV)
        master = reaction_masters_reactions.get(rhea, {})
        try:
            __, reactions = master.popitem()
        except KeyError:
            reactions = [rhea]
        ec_reactions.setdefault(ec, set()).update(reactions)
        for reaction in reactions:
            reaction_ecs.setdefault(reaction, set()).add(ec)
    for ec, reactions in ec_reactions.items():
        ec_reactions[ec] = list(reactions)
    for reaction, ecs in reaction_ecs.items():
        reaction_ecs[reaction] = list(ecs)
    return ec_reactions, reaction_ecs


def read_rds(filenames):
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


def add_supplementary_reactions(cmp_rxns, rxn_equats, rxn_stoich):
    cmp_rxns['61548'][0].append('S1')
    cmp_rxns['61548'][1].append('S2')
    cmp_rxns['57584'][0].append('S2')
    cmp_rxns['57584'][1].append('S1')
    cmp_rxns['57579'][0].append('S3')
    cmp_rxns['57579'][1].append('S4')
    cmp_rxns['57634'][0].append('S4')
    cmp_rxns['57634'][1].append('S3')

    rxn_equats['S1'] = 'D-glucopyranose 6-phosphate => aldehydo-D-glucose 6-phosphate'
    rxn_equats['S2'] = 'aldehydo-D-glucose 6-phosphate => D-glucopyranose 6-phosphate'
    rxn_equats['S3'] = 'D-fructose 6-phosphate => beta-D-fructose 6-phosphate'
    rxn_equats['S4'] = 'beta-D-fructose 6-phosphate => D-fructose 6-phosphate'

    rxn_stoich['S1'] = [{'61548': 1}, {'57584': 1}]
    rxn_stoich['S2'] = [{'57584': 1}, {'61548': 1}]
    rxn_stoich['S3'] = [{'57579': 1}, {'57634': 1}]
    rxn_stoich['S4'] = [{'57634': 1}, {'57579': 1}]


def main():
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
    rdnames = get_names(PATH_RD)

    # Obtain data from rd files and get corresponding JSON filenames.
    rd_data = read_rds(rdnames)
    cmp_rxns, rxn_equats, rxn_master_rxn, rxn_stoich = rd_data

    # EC
    content_ecs = get_content(PATH_RHEA, RHEA_EC)
    ec_reactions, reaction_ecs = read_ecs(content_ecs, rxn_master_rxn)

    # Create supplementary reactions.
    add_supplementary_reactions(cmp_rxns, rxn_equats, rxn_stoich)

    # Save data in JSON format.
    data = [cmp_rxns,
            ec_reactions,
            reaction_ecs,
            rxn_equats,
            rxn_stoich,
            ]
    jsonnames = [FILE_CMP_REACTIONS,
                 FILE_EC_REACTIONS,
                 FILE_RXN_ECS,
                 FILE_RXN_EQUATIONS,
                 FILE_RXN_STOICHIOMETRICS,
                 ]
    write_jsons(data, PATH_JSON, jsonnames)

    return data


if __name__ == '__main__':
    # pass
    data = main()