# -*- coding: utf-8 -*-
"""
Evaluate compound demands and prices and reaction complexities.

Functions
---------
compare_formulae: return Euclidian distance between chemical formulae.
evaluate_complexity: return reaction complexity.
evaluate_compound: return compound value.
evaluate_ontology: return ontology-derived value.
initialize_graph: initialize networkx.DiGraph to ontology analysis.
parse_formula: return a dict representation of a chemical formula str.
main: create JSON files for prices, demands and complexities.

Exceptions
----------
ParseCharacterError: error in parsing a chemical formula.

"""


from collections import Counter
from math import sqrt

import networkx as nx
import numpy as np

from exceptions import ReactionIdError


RELATIONS_DEMAND = set(['has_role', 'is_a'])
RELATIONS_PRICE = set(['has_role', 'has_functional_parent',
                       'is_substituent_group_from', 'has_part', 'is_a'])
CHEBIS_DEMAND = {
    '33232': 1,  # application
    # Applications (ChEBI 33232)
    '33286': 2,  # agrochemical
    '75835': 1,  # anti-anaemic agent
    '67079': 1,  # anti-inflammatory agent
    '77964': 1,  # anticaking agent
    '77973': 1,  # antifoaming agent
    '64857': 1,  # cosmetic
    '75358': 1,  # curing agent
    '27780': 1,  # detergent
    '37958': 1,  # dye
    '78152': 1,  # enzyme mimic
    '75324': 1,  # excipient
    '79314': 1,  # flame retardant
    '64047': 1,  # food additive
    '48318': 1,  # fragnance
    '33292': 2,  # fuel
    '77968': 1,  # humectant
    '47867': 1,  # indicator
    '35209': 1,  # label
    '64345': 1,  # MALDI matrix material
    '74152': 1,  # mordant
    '74886': 1,  # neoglycolipid probe
    '25944': 2,  # pesticide
    '79056': 2,  # plasticiser
    '50406': 1,  # probe
    '76414': 1,  # propellant
    '51087': 1,  # protecting group
    '50533': 1,  # protein denaturant
    '73352': 1,  # protein-sequencing agent
    '33893': 2,  # reagent
    '78433': 2,  # refrigerant
    '46787': 2,  # solvent
    '35204': 1,  # tracer
    '52217': 2,  # pharmaceutical
    # Pharmaceuticals (ChEBI 52217)
    '23888': 1,  # drug
    }
CHEBIS_PRICE = {
    # Groups
    '33249': 1,  # organyl group
    '23019': 2,  # carbonyl group
    '46883': 2,  # carboxy group
    '51422': 1,  # organodiyl group
    '79073': 1,  # CHOH group
    '43176': 1,  # hydroxy group
    '50860': 1,  # organic molecular entity
    # Organic molecular entities (ChEBI 50860)
    '18059': 1,  # lipid
    '78840': 2,  # olefinic compound
    '64709': 1,  # organic acid
    '50047': 1,  # organic amino compound
    '33245': 1,  # organic fundamental parent
    '33822': 1,  # organic hydroxy compound
    '33635': 1,  # organic polycyclic compound
    # Lipids (ChEBI 18059)
    '35366': 1,  # fatty acid
    '28868': 1,  # fatty acid anion
    '35748': 1,  # fatty acid ester
    '24026': 1,  # fatty alcohol
    '29348': 1,  # fatty amide
    '35741': 1,  # glycerolipid
    '131727': 1,  # hydroxylipid
    '24913':  1,  # isoprenoid
    # Olefinic compounds (ChEBI 78840)
    '33641': 1,  # olefin
    # Acyclic olefins (ChEBI 33645)
    '32878': 1,  # alkene
    # Organic amino compounds (ChEBI 50047)
    '32952': 1,  # amine
    '33709': 1,  # amino acid
    '22478': 1,  # amino alcohol
    '33869': 1,  # aromatic amine
    # Organic fundamental parents (ChEBI 33245)
    '24632': 1,  # hydrocarbon
    # Organic hydroxy compounds (ChEBI 33822)
    '30879': 1,  # alcohol
    '33823': 1,  # enol
    '33853': 1,  # phenols
    }

COMPLEXITY_COMPOUNDS = {
    # Deoxyribonucleotides
    '61404': 1,  # dATP(4-)
    '57667': 1,  # dADP(3-)
    '58245': 1,  # dAMP(2-)
    '61481': 1,  # dCTP(4-)
    '58593': 1,  # dCDP(3-)
    '57566': 1,  # dCMP(2-)
    '61429': 1,  # dGTP(4-)
    '58595': 1,  # dGDP(4-)
    '57673': 1,  # dGMP(4-)
    '61382': 1,  # dITP(4-)
    '37568': 1,  # dTTP(4-)
    '58369': 1,  # dTDP(3-)
    '63528': 1,  # dTMP(2-)
    '61555': 1,  # dUTP(4-)
    '60471': 1,  # dUDP(3-)
    '246422': 1,  # dUMP(2-)
    # Ribonucleotides
    '30616': 1,  # ATP(4-)
    '456216': 1,  # ADP(3-)
    '456215': 1,  # AMP(2-)
    '37563': 1,  # CTP(4-)
    '58069': 1,  # CDP(3-)
    '60377': 1,  # CMP(2-)
    '37565': 1,  # GTP(4-)
    '58189': 1,  # GDP(3-)
    '58115': 1,  # GMP(2-)
    '61402': 1,  # ITP(4-)
    '58280': 1,  # IDP(3-)
    '58053': 1,  # IMP(2-)
    '46398': 1,  # UTP(4-)
    '58223': 1,  # UDP(3-)
    '57865': 1,  # UMP(2-)
    '61314': 1,  # XTP(4-)
    '59884': 1,  # XDP(3-)
    '57464': 1,  # XMP(2-)
    # Cofactors and -enzymes
    '16509': 1,  # 1,4-benzoquinone
    '57530': 1,  # 1,5-dihydrocoenzyme F420(4-)
    '16810': 1,  # 2-oxoglutarate(2-)
    '175763': 1,  # 2-trans,6-trans-farnesyl diphosphate(3-)
    '28889': 1,  # 5,6,7,8-tetrahydropteridine
    '57454': 1,  # 10-formyltetrahydrofolate(2-)
    '57288': 1,  # acetyl-CoA(4-)
    '58342': 1,  # acyl-CoA(4-)
    '64876': 1,  # bacillthiol(1-)
    '60488': 1,  # cob(I)alamin(1-)
    '16304': 1,  # cob(II)alamin
    '28911': 1,  # cob(III)alamin
    '57287': 1,  # CoA(4-)
    '58319': 1,  # coenzyme M(1-)
    '59920': 1,  # coenzyme F420-1(4-)
    '57922': 1,  # coenzyme gamma-F420-2(5-)
    '58596': 1,  # coenzyme B(3-)
    '59923': 1,  # coenzyme alpha-F420-3(6-)
    '83348': 1,  # chlorophyllide a(2-)
    '71302': 1,  # MoO2-molybdopterin cofactor(2-)
    '71305': 1,  # WO2-molybdopterin cofactor(2-)
    '57692': 1,  # FAD(3-)
    '58307': 1,  # FADH2(2-)
    '33737': 1,  # Fe2S2 di-mu-sulfido-diiron(2+)
    '33738': 1,  # Fe2S2 di-mu-sulfido-diiron(1+)
    '57618': 1,  # FMNH2
    '58210': 1,  # FMN(3-)
    '57925': 1,  # glutathionate(1-)
    '17594': 1,  # hydroquinone
    '57384': 1,  # malonyl-CoA(5-)
    '57540': 1,  # NAD
    '57945': 1,  # NADH
    '58349': 1,  # NADP(3-)
    '57783': 1,  # NADPH(4-)
    '17154': 1,  # nicotinamide
    '16768': 1,  # mycothiol
    '57387': 1,  # oleoyl-CoA(4-)
    '57379': 1,  # palmitoyl-CoA(4-)
    '18067': 1,  # phylloquinone
    '28026': 1,  # plastoquinol-9
    '28377': 1,  # plastoquinone-9
    '59648': 1,  # precursor Z(1-)
    '87467': 1,  # prenyl-FMNH2(2-)
    '17310': 1,  # pyridoxal
    '16709': 1,  # pyridoxine
    '58442': 1,  # pyrroloquinoline quinone(3-)
    '77660': 1,  # pyrroloquinoline quinol(4-)
    '43711': 1,  # (R)-dihydrolipoamide
    '76202': 1,  # riboflavin cyclic 4',5'-phosphate(2-)
    '57856': 1,  # S-adenosyl-L-homocysteine zwitterion
    '59789': 1,  # S-adenosyl-L-methionine zwitterion
    '71177': 1,  # tetrahydromonapterin
    '33723': 1,  # tetra-mu3-suldifo-tetrairon(1+)
    '33722': 1,  # tetra-mu3-suldifo-tetrairon(2+)
    }


class ParseCharacterError(ValueError):
    pass


def compare_formulae(formulae):
    """
    Return distance between chemical formulae.

    Distance between formulae is Euclidian distance in N-dimensional
    space. N is the amount of different chemical elements in formulae
    and the value in a dimension is the stoichiometric number of the
    element in a formula. Value defaults to 0 if the formula doesn't
    contain the element.

    Parameters
    ----------
    formulae : iterable
        Must contain 2 chemical formulae dicts {'element': int, ...}.
        Use `parse_formula` to construct dicts.

    Returns
    -------
    number
        Euclidian distance

        sqrt(sum((n_element_in_formula1 - n_element_in_formula2)**2))

    Raises
    ------
    ValueError
        If both formula dicts are empty or if the number of dicts is
        invalid.
    TypeError
        If `formulae` is not a list or a tuple.

    See also
    --------
    parse_formula

    """
    if not isinstance(formulae, (list, tuple)):
        raise TypeError('Input must be an iterable of 2 dicts.')
    elif len(formulae) != 2:
        raise ValueError('Input does not have 2 dicts.')
    elif not any(formulae):
        raise ValueError('Both formula dicts are empty')
    else:
        elements = {key for formula in formulae for key in formula.keys()}
        element_distances = {}
        for element in elements:
            amounts = [formula.get(element, 0) for formula in formulae]
            element_distances[element] = (amounts[0] - amounts[1])**2
        return sqrt(sum(element_distances.values()))


def evaluate_complexity(reaction, stoichiometrics={}, compounds={}):
    """
    Evaluate complexity factor for reaction step.

    Reaction complexity factor is currently the amount of compounds in
    `compounds` consumed in reaction  multiplied by their respective
    complexity values.

    Parameters
    ----------
    reaction : str
        Reaction Rhea ID.
    stoichiometrics : dict
        Mapping from Rhea ID to a list of two dicts. [0] maps from
        substrate ChEBI IDs to stoichiometric numbers and [1] maps from
        product ChEBI IDs to stoichiometric numbers.
    compounds : dict
        Mapping from ChEBIs ID to complexity values.

    Returns
    -------
    number
        Reaction complexity factor.

    Raises
    ------
    TypeError
        If `reaction` is not a string.
    RheaIDError
        If `reaction` is not recognized as a Rhea ID number.

    """
    if not isinstance(reaction, str):
        raise TypeError('Input must be a reaction Rhea ID string.')
    elif reaction not in stoichiometrics:
        raise ReactionIdError('No reaction found with ID {}.'.format(reaction))
    # Get the amount of consumed cofactors.
    values = {}
    reaction_substrates, __ = stoichiometrics[reaction]
    for chebi, complexity in compounds.items():
        amount = reaction_substrates.count(chebi)
        values[chebi] = amount * complexity

    # Evaluate complexity factor.
    total = sum(values.values())
    if total < 0:
        return 0
    return total


def evaluate_compound(demand, price):
    """
    Evaluate compound.

    Parameters
    ----------
    demand : number
        Compound demand.
    price : number
        Compound price.

    Returns
    -------
    number
        Value of the compound.

    Raises
    ------
    TypeError
        If `demand` or `price` are not numeric.
    ValueError
        If `demand` or `price` is not non-negative.

    """
    if not isinstance(demand, (float, int)):
        raise TypeError('Input demand type must be float or int.')
    elif not isinstance(price, (float, int)):
        raise TypeError('Input price type must be float or int.')
    elif demand < 0 or price < 0:
        raise ValueError('Demand and price must be non-negative.')
    return demand * price


def evaluate_ontology(graph, compound, target_values):
    """
    Evaluate ontology.

    Parameters
    ----------
    graph : networkx.DiGraph object
        Use `initialize_graph` to create `graph`.
    compound : str
        ChEBI ID.
    types : dict
        Mapping from relation strings to dicts that map target ChEBI
        IDs to target value numbers.

    Returns
    -------
    number
        Sum of found target values.

    """
    values = []
    for target, value in target_values.items():
        try:
            if nx.has_path(graph, compound, target):
                values.append(value)
        except nx.NetworkXError:
            continue
    return sum(values)


def initialize_graph(compound_relations, relation_types):
    """
    Initialize a compound-centric graph for ChEBI ontology analysis.

    Parameters
    ----------
    compound_relations : dict
        Mapping from ChEBI ID strings to dicts that map target ChEBI ID
        strings to relation type strings.
    relation_types : iterable
        Relation type_strings to be included in creating edges between
        ChEBI ID string nodes.

    Returns
    -------
    networkx.DiGraph object

    """
    graph = nx.DiGraph()
    for compound, targets in compound_relations.items():
        for target, relation in targets.items():
            if relation in relation_types:
                graph.add_edge(compound, target)
    return graph


def parse_formula(formula):
    """
    Parse str to dict from chemical elements to stoichiometric numbers.

    Handles parentheses and dots within formula. Arbitrary multiplier n
    is treated as 1. Empty string returns an empty dict.

    Parameters
    ----------
    formula : str
        Molecular formula.

    Returns
    -------
    dict
        Mapping from element strings to stoichiometric numbers.

    Raises
    ------
    ParseCharacterError
        If `formula` contains invalid characters.
    TypeError
        If `formula` is not a string.

    """
    def find_multiplier(start):
        nr_multiplier = start
        number_ = []
        while nr_multiplier < len(formula):
            target = formula[nr_multiplier]
            if target.isdigit():
                number_.append(target)
                nr_multiplier += 1
            else:
                break
        try:
            multiplier = int(''.join(number_))
        except ValueError:
            multiplier = 1
        finally:
            return multiplier

    # Check for valid input type.
    if not isinstance(formula, str):
        raise TypeError('Input formula must be a string.')

    nr_character = 0
    element, number = [], []
    elements, numbers = [], []
    element_numbers = Counter()
    # Multipliers
    multipliers = [[find_multiplier(nr_character)], [1]]

    # Parse formula.
    while nr_character < len(formula):
        character = formula[nr_character]
        # Find chemical elements.
        # Chemical elements start with an uppercase character.
        if character.isupper():
            element.append(character)
            # Scan for element-number pair.
            nr_target = nr_character + 1
            while nr_target < len(formula):
                target = formula[nr_target]
                # Terminate scan at a special or an uppercase character.
                if target in '.()' or target.isupper():
                    elements.append(''.join(element))
                    try:
                        numbers.append(
                            np.prod(multipliers) * int(''.join(number)))
                    except ValueError:
                        numbers.append(np.prod(multipliers) * 1)
                    finally:
                        element.clear()
                        number.clear()
                        break
                # Extend element or number.
                elif target.islower():
                    element.append(target)
                elif target.isdigit():
                    number.append(target)
                nr_target += 1
        # Scan for dot multipliers.
        elif character == '.':
            multipliers[0].pop()
            m_dot = find_multiplier(nr_character + 1)
            multipliers[0].append(m_dot)
        # Scan for parentheses multipliers.
        elif character == '(':
            m_dot = find_multiplier(nr_character + 1)
            m_paren = find_multiplier(formula.find(')', nr_character) + 1)
            multipliers[0].append(m_dot)
            multipliers[1].append(m_paren)
        # Reset parentheses multiplier.
        elif character == ')':
            multipliers[0].pop()
            multipliers[1].pop()
        # Invalid character.
        elif not character.islower() and not character.isdigit():
            raise ParseCharacterError(
                'Invalid character: {}'.format(character))

        nr_character += 1

    # Add last element and number.
    if element:
        elements.append(''.join(element))
        try:
            numbers.append(np.prod(multipliers) * int(''.join(number)))
        except ValueError:
            numbers.append(np.prod(multipliers) * 1)

    # Sum numbers to elements, and return.
    for element, number in zip(elements, numbers):
        element_numbers.update({element: number})

    return element_numbers
