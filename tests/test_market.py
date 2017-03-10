# -*- coding: utf-8 -*-
# (C) 2017 Tampere University of Technology
# MIT License
# Pauli Losoi
"""
Test market module.

"""

from context import market
import networkx as nx
import pytest


ONTOLOGY_GRAPH = nx.DiGraph([('a', 'b')])
GRAPH_TYPES = set(['a', 'b'])
GRAPH_CHEBIS = {'1': 1, '2': 2, '3': 3}
GRAPH_RELATIONS = {
    '1': {'2': 'a', '3': 'b'},
    '2': {'1': 'c', '3': 'a'},
    '3': {'1': 'd', '2': 'c'},
    '4': {'1': 'e', '2': 'f'},
    }
STOICHIOMETRICS = {
    '1': [['1', '2', '2'], ['3', '3', '3', '4', '4', '4', '4']],
    '2': [['1', '2', '2'], ['5', '5', '6']],
    '3': [['3', '3', '3', '4', '4', '4', '4'], ['1', '2', '2']],
    '4': [['3', '3', '3', '4', '4', '4', '4'], ['5', '5', '6']],
    '5': [['5', '5', '6'], ['1', '2', '2']],
    '6': [['5', '5', '6'], ['3', '3', '3', '4', '4', '4', '4']],
    }
COMPLEXITY_CMPS = {
    '1': 1,
    '2': 2,
    '3': 3,
    }


class TestEvaluateCompound:

    def test_invalid_type_demand(self):
        with pytest.raises(TypeError):
            market.evaluate_compound('4167', 3.14)

    def test_invalid_type_price(self):
        with pytest.raises(TypeError):
            market.evaluate_compound(3.14, '4167')

    def test_negative_demand(self):
        with pytest.raises(ValueError):
            market.evaluate_compound(-1.0, 3.14)

    def test_negative_price(self):
        with pytest.raises(ValueError):
            market.evaluate_compound(1, -1)

    def test_numeric_output(self):
        assert isinstance(market.evaluate_compound(1, 1.5), (float, int))


class TestEvaluateOntology:

    def test_correct_output(self):
        G = market.initialize_graph(GRAPH_RELATIONS, GRAPH_TYPES)
        compounds = ['1', '2', '3', '4']
        output = [market.evaluate_ontology(G, c, GRAPH_CHEBIS) for c in compounds]
        assert output == [6, 5, 3, 0]


class TestInitializeGraph:

    graph = market.initialize_graph(GRAPH_RELATIONS, GRAPH_TYPES)

    def test_correct_edges(self):
        correct = set([('1', '2'), ('1', '3'), ('2', '3')])
        assert set(nx.edges(self.graph)) == correct

    def test_correct_nodes(self):
        correct = set(['1', '2', '3'])
        assert set(nx.nodes(self.graph)) == correct

