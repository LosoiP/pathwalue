# -*- coding: utf-8 -*-
# (C) 2017 Tampere University of Technology
# MIT License
# Pauli Losoi
"""

Functions
---------
determine_intermediates
    Determine intermediates from reactants and products.
evaluate_input
    Evaluate user input.
evaluate_pathway
    Evaluate pathway score.
filter_pathways
    Filter pathways.
find_pathway
    Find pathway.
intersect_dict
    Reduce dict to have only keys present in another iterable.
initialize_graph
    Initialize networkx.DiGraph for pathway analysis.
nbest_items
    Return n highest scored items.
"""


import collections as cl
import itertools as it
import heapq as hq  # find n max values from a list
import math as m

import networkx as nx


def determine_intermediates(substrates, products):
    """
    Return pathway intermediates.

    Parameters
    ----------
    substrates, products : dict
        Must contain keys chebi and number.

    Returns
    -------
    dict
        ChEBI ID string to tuple of 2 numeric values. First value is
        the amount of occurrences in substrates and the second in
        products.

    """
    substrate_iter = ([s['chebi']] * s['number'] for s in substrates)
    product_iter = ([p['chebi']] * p['number'] for p in products)
    counter_s = cl.Counter(it.chain.from_iterable(substrate_iter))
    counter_p = cl.Counter(it.chain.from_iterable(product_iter))
    intermediate_set = set(counter_s) & set(counter_p)
    intermediates = {i: (counter_s[i], counter_p[i]) for i in intermediate_set}
    return intermediates


def evaluate_input(n, graph, compounds=[], enzymes=[], context={}):
    """
    Evaluate user input.

    Parameters
    ----------
    n : int
        The amount of results to be returned. Must be at least 1.
    graph : networkx.DiGraph
        Rhea reaction ID string nodes and compound edges.
    compounds : list or tuple
        ChEBI ID strings. Order matters.
    enzymes : list or tuple
        EC number strings. Order doesn't matter.
    context : dict
        Mappings from ID strings to data. Must have keys ec_reactions,
        compound_reactions, complexities, demands, prices,
        reactions_ecs, stoichiometrics.

    Returns
    -------
    list
        Tuples of score, pathway -pairs.

    Raises
    ------
    TypeError
        If `n` is not integer.

    """
    if not isinstance(n, int):
        raise TypeError('`n` not int')

    ec_reactions = context['ec_reactions']
    compound_reactions = context['compound_reactions']
    complexities = context['complexities']
    demands = context['demands']
    prices = context['prices']
    stoichiometrics = context['stoichiometrics']

    pathways = set()
    start = None
    goal = None
    sources = [None]
    targets = [None]
    # Determine search and filter parameters.
    if compounds:
        start = compounds[0]
        goal = compounds[-1]
        if start == 'any':
            compounds = compounds[1:]
            if goal == 'any':
                pass
            else:
                targets = compound_reactions[goal][1]
        else:
            sources = compound_reactions[start][0]
            if goal == 'any':
                compounds = compounds[:-1]
            else:
                targets = compound_reactions[goal][1]
    else:
        sources.extend(e for ec in enzymes for e in ec_reactions[ec])
        targets = sources
    # Find pathways.
    for source, target in it.product(sources, targets):
        pws = find_pathway(graph, source, target)
        filtered_pws = filter_pathways(
            pws, source=start, target=goal, compounds=compounds,
            enzymes=enzymes, context=context)
        pathways.update(filtered_pws)

    # Evaluate pathways.
    pathways = list(pathways)
    pathway_data = order_pathway_data(pathways, stoichiometrics,
                                      complexities, demands, prices)
    values = [evaluate_pathway(s, c) for s, c in pathway_data]
    return nbest_items(n, values, pathways)


def evaluate_pathway(steps, compounds):
    """
    Evaluate pathway.

    Evaluates the pathway by calculating values of start and goal
    compounds and intermediate reaction steps. Start and goal compounds
    are determined by the reaction steps.

    Parameters
    ----------
    steps : collections.OrderedDict
        Keys are Rhea ID strings and values are dicts of substrate and
        product ChEBI ID-stoichiometric number -pairs. Order matches
        the order of reaction steps.
    compounds : dict
        Keys are ChEBI ID strings and value are tuples of compound
        demands and prices.

    Returns
    -------
    number
        Pathway's value.

    """
    values_reactions = (data[0] for data in steps.values())
    substrates_all = set(s for step in steps.values() for s in step[1])
    products_all = set(p for step in steps.values() for p in step[2])
    steps_list = list(steps.values())
    substrates = steps_list[0][1]
    products = steps_list[-1][2]
    values_reactants = (compounds[s][1] * compounds[s][0] for s in substrates)
    values_products = (compounds[p][1] * compounds[p][0] for p in products)
    amount_reactions = len(steps)

    # Evaluate similarity of reactants and products.
    s = len(substrates_all & products_all) / len(substrates_all | products_all)
    # Evaluate total value of products and reactants.
    p = sum(values_products)
    r = sum(values_reactants)
    # Evaluate pathway's total complexity factor.
    c = sum(values_reactions)
    # Evaluate and return pathway's value.
    value = m.ceil(10 * m.sqrt(s) * (p - r) / ((c + 1) * amount_reactions**2))
    return value


def filter_pathways(
        pathways,
        source=None,
        target=None,
        compounds=[],
        enzymes=[],
        context={},
        ):
    """
    Yield pathways that meet filtering conditions.

    The effect of filterig parameters is explained below. Filters
    automatically pathways, that repeatedly consumes and produces a
    compound, that is not ignored (see chebi.IGNORED_COMPOUNDS).

    Parameters
    ----------
    pathways : iterable
        Lists of Rhea ID strings.
    source : string
        ChEBI ID of pathway's source compound. Filters pathways that
        have reactions producing source.
    target : string
        ChEBI ID of pathway's target compound. Filters pathways that
        have reactions consuming target.
    compounds : iterable
        CheBI ID strings. Filters pathways that don't have all
        compounds.
    enzymes : iterable
        EC number strings. Filters pathways that don't have all enzymes.
    context : dict
        Key reaction_ecs maps to a dict of Rhea ID string keys to EC
        number string list values.
        Key stoichiometrics maps to a dict of Rhea ID string keys to
        a list of dicts of substrates and products.

    Yields
    ------
    tuple
        Pathway reaction tuples that meet the filtering conditions of
        given arguments.

    """
    reaction_ecs = context['reaction_ecs']
    stoichiometrics = context['stoichiometrics']
    ignored = context.get('ignored', set())
    for pathway in pathways:
        compounds_pw = set(['any'])
        enzymes_pw = set()
        for i, reaction in enumerate(pathway):
            substrates = set(stoichiometrics[reaction][0])
            products = set(stoichiometrics[reaction][1])
            if target in substrates:
                break
            elif source in products:
                break
            elif i >= 2:
                prepre_s = set(stoichiometrics[pathway[i - 2]][0])
                pre_p = set(stoichiometrics[pathway[i - 1]][1])
                discard_substrates_1 = substrates & (prepre_s - ignored)
                discard_substrates_2 = substrates & (pre_p - ignored)
                if discard_substrates_1 and discard_substrates_2:
                    break
                prepre_p = set(stoichiometrics[pathway[i - 2]][1])
                pre_s = set(stoichiometrics[pathway[i - 1]][0])
                discard_products_1 = products & (prepre_p - ignored)
                discard_products_2 = products & (pre_s - ignored)
                if discard_products_1 and discard_products_2:
                    break
            compounds_pw.update(substrates)
            compounds_pw.update(products)
            try:
                enzymes_pw.update(reaction_ecs[reaction])
            except KeyError:
                pass
        else:
            if not set(enzymes) <= enzymes_pw:
                continue
            elif not set(compounds) <= compounds_pw:
                continue
            yield tuple(pathway)


def find_pathway(graph, source=None, target=None):
    """
    Yield pathway lists.

    Parameters
    ----------
    graph : networkx graph object
        Rhea reaction ID nodes.
    reactions : iterable of 1 or 2
        Reaction graph node IDs to search pathways for.

    Yields
    ------
    list
        Pathways from source to target reaction nodes.

    See also
    --------
    initialize_graph

    """
    if target is None:
        if source is None:
            pass
        else:
            try:
                paths = nx.single_source_shortest_path(graph, source).values()
            except KeyError:
                pass
            else:
                for path in paths:
                    yield path
    elif source is None:
        with nx.utils.reversed(graph):
            try:
                paths = nx.single_source_shortest_path(graph, target)
            except KeyError:
                paths = []
        for target in paths:
            yield list(reversed(paths[target]))
    else:
        try:
            yield nx.bidirectional_shortest_path(graph, source, target)
        except nx.NetworkXNoPath:
            pass


def intersect_dict(target, filter_to={}):
    """
    Return dict without keys that aren't present in the iterable.

    Parameters
    ----------
    target : dict
        key: value -pairs.
    filter_to : iterable
        Keys that are to be kept in target.

    Returns
    -------
    dict
        Target dict without keys that aren't present in filter_to.

    """
    for key in target.copy():
        if key not in filter_to:
            target.pop(key)
    return target


def initialize_graph(
        reaction_stoichiometrics={},
        compound_reactions={},
        reactions_ignored=set(),
        compounds_ignored=set(),
        ):
    """
    Initialize graph to find pathways.

    Connects reactions 1 and 2 by an edge (1, 2), if reaction 1
    produces a compound that is consumed by reaction 2. A reaction
    is not connected to its opposite direction node under any
    circumstances. See chebi.IGNORED_COMPOUNDS for a list of compounds,
    that won't connect reactions in the graph.

    Parameters
    ----------
    reaction_stoichiometrics : dict
        Rhea ID string keys, substrate and product dict values.
    compounds_reactions : dict
        ChEBI ID string keys, consumer and producer list values.
    reactions_ignored : set
        Rhea ID strings.
    compounds_ignored : set
        ChEBI ID strings.

    Returns
    -------
    nx.DiGraph object

    See also
    --------
    chebi.IGNORED_COMPOUNDS

    """
    graph = nx.DiGraph()
    # Create edges.
    for reaction in set(reaction_stoichiometrics) - reactions_ignored:
        substrates, products = reaction_stoichiometrics[reaction]
        for product in set(products) - compounds_ignored:
            consumers, __ = compound_reactions[product]
            weight = len(consumers)
            for consumer in set(consumers) - reactions_ignored:
                # Ignore opposite direction of reaction.
                __, consumer_products = reaction_stoichiometrics[consumer]
                if consumer_products == substrates:
                    continue
                graph.add_edge(reaction, consumer, weight=weight)
    return graph


def nbest_items(n, values, items):
    """
    Return n best items.

    Parameters
    ----------
    n : int
        The amount of best value-item -pairs to be returned.
    values : iterable
        Values of items in items. Indices must match.
    items : iterable
        Items to be compared by values in values. Indices must match.

    Returns
    -------
    list
        tuples of value-item -pairs in descending value-order.

    Raises
    ------
    TypeError
        If n or items in values are non-numeric.
    ValueError
        If n is less than 1.

    """
    if not isinstance(n, (float, int)):
        raise TypeError('n non-numeric')
    elif n < 1:
        raise ValueError('n less than 1')
    elif not all((isinstance(value, (float, int)) for value in values)):
        raise TypeError('nonnumerical item in values')
    maxes = hq.nlargest(n, values)
    indices_max = [ix for ix, value in enumerate(values) if value in maxes]
    items_max = [items[index_max] for index_max in indices_max]
    values_max = [values[index_max] for index_max in indices_max]
    return sorted(list(zip(values_max, items_max)), reverse=True)[:n]

