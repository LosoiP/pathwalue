# -*- coding: utf-8 -*-
# (C) 2017 Tampere University of Technology
# MIT License
# Pauli Losoi
"""
Evaluate compound demands and prices.

Constants
---------
RELATIONS_DEMAND
    Set of ChEBI relation ID strings used in evaluating demand.
RELATIONS_PRICE
    Set of ChEBI relation ID strings used in evaluating price.
CHEBIS_DEMAND
    Mapping from CHEBI ID strings to demand integer values.
CHEBIS_PRICE
    Mapping from CHEBI ID strings to price integer values.

Functions
---------
evaluate_compound
    Return compound value.
evaluate_ontology
    Return ontology-derived value.
initialize_graph
    Initialize networkx.DiGraph to ontology analysis.

"""


from collections import Counter
from math import sqrt

import networkx as nx
import numpy as np

from exceptions import ReactionIdError


RELATIONS_DEMAND = set([
    # 'has_functional_parent',
    # 'has_parent_hydride',
    # 'has_part',
    'has_role',
    'is_a',
    'is_conjugate_acid_of',
    'is_conjugate_base_of',
    'is_enantiomer_of',
    # 'is_substituent_group_from',
    'is_tautomer_of',
    ])
RELATIONS_PRICE = set([
    # 'has_functional_parent',
    # 'has_parent_hydride',
    'has_part',
    'has_role',
    'is_a',
    'is_conjugate_acid_of',
    'is_conjugate_base_of',
    'is_enantiomer_of',
    'is_substituent_group_from',
    'is_tautomer_of',
    ])
CHEBIS_DEMAND = {
    '50906': 1,  # role
    # Roles (ChEBI 50906)
    '33232': 5,  # application
    '24432': 1,  # biological role
    '51086': 1,  # chemical role
    # Applications (ChEBI 33232)
    '33286': 1,  # agrochemical
    '67079': 1,  # anti-inflammatory agent
    '77964': 1,  # anticaking agent
    '77973': 1,  # antifoaming agent
    '64857': 5,  # cosmetic
    '75358': 1,  # curing agent
    '27780': 1,  # detergent
    '37958': 1,  # dye
    '64047': 1,  # food additive
    '48318': 5,  # fragnance
    '33292': 5,  # fuel
    '77968': 1,  # humectant
    '47867': 1,  # indicator
    '35209': 1,  # label
    '64345': 1,  # MALDI matrix material
    '25944': 1,  # pesticide
    '79056': 1,  # plasticiser
    '50406': 1,  # probe
    '76414': 1,  # propellant
    '33893': 3,  # reagent
    '78433': 1,  # refrigerant
    '46787': 3,  # solvent
    '35204': 1,  # tracer
    '52217': 3,  # pharmaceutical
    # Biological roles (ChEBI 24432)
    '52210': 3,  # pharmacological role
    '50188': 1,  # provitamin
    '50913': 1,  # fixative
    '50846': 1,  # immunomodulator
    '52206': 1,  # biochemical role
    '24850': 1,  # insect attractant
    '73190': 1,  # antimutagen
    '35222': 1,  # inhibitor
    '35703': 1,  # xenobiotic
    # Chemical roles (ChEBI 51086)
    '37527': 1,  # acid
    '22695': 1,  # base
    '74236': 3,  # polymerisation monomer
    '62803': 3,  # fuel additive
    '63046': 1,  # emulsifier
    '22586': 1,  # antioxidant
    '63490': 1,  # explosive
    '46787': 3,  # solvent
    '35225': 1,  # buffer
    '35223': 1,  # catalyst
    '52215': 1,  # photochemical role
    }
CHEBIS_PRICE = {
    # Groups
    '33249': 1,  # organyl group
    '23019': 1,  # carbonyl group
    '46883': 1,  # carboxy group
    '51422': 1,  # organodiyl group
    '79073': 1,  # CHOH group
    '43176': 1,  # hydroxy group
    '50860': 1,  # organic molecular entity
    # Organic molecular entities (ChEBI 50860)
    '18059': 1,  # lipid
    '78840': 1,  # olefinic compound
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
    # Organic fundamental parents (ChEBI 33245)
    '24632': 2,  # hydrocarbon
    # Organic hydroxy compounds (ChEBI 33822)
    '30879': 2,  # alcohol
    '33823': 1,  # enol
    '33853': 1,  # phenols
    # Metabolites
    '75763': 1,  # eukaryotic metabolite
    '76924': 1,  # plant metabolite
    }


class ParseCharacterError(ValueError):
    pass


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
        If demand or price are not numeric.
    ValueError
        If demand or price is not non-negative.

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
    graph : networkx.DiGraph
        Use initialize_graph to create graph.
    compound : string
        ChEBI ID.
    types : dict
        Mapping from ChEBI IDs to value numbers.

    Returns
    -------
    int
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
        hEBI ID string nodes.

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

