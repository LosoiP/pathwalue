# -*- coding: utf-8 -*-
# (C) 2017 Tampere University of Technology
# MIT License
# Pauli Losoi
"""
Created on Fri Nov 25 13:38:10 2016

@author: losoip
"""

from collections import OrderedDict

import networkx as nx
import pytest

from context import pw
from context import chebi


STOICHIOMETRICS = {
    '1': [['1', '2', '2'], ['3', '3', '3', '4', '4', '4', '4']],
    '2': [['1', '2', '2'], ['5', '5', '6']],
    '3': [['3', '3', '3', '4', '4', '4', '4'], ['1', '2', '2']],
    '4': [['3', '3', '3', '4', '4', '4', '4'], ['5', '5', '6']],
    '5': [['5', '5', '6'], ['1', '2', '2']],
    '6': [['5', '5', '6'], ['3', '3', '3', '4', '4', '4', '4']],
    }
COMPLEXITIES = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    }
COMPOUND_REACTIONS = {
    '1': [['1', '2'], ['3', '5']],
    '2': [['1', '2'], ['3', '5']],
    '3': [['3', '4'], ['1', '6']],
    '4': [['3', '4'], ['1', '6']],
    '5': [['5', '6'], ['2', '4']],
    '6': [['5', '6'], ['2', '4']],
    }
DEMANDS = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    }
PRICES = {
    '1': 6,
    '2': 5,
    '3': 4,
    '4': 3,
    '5': 2,
    '6': 1,
    }
COMPOUNDS = {
    '1': 'a',
    '2': 'b',
    '3': 'c',
    '4': 'd',
    '5': 'e',
    '6': 'f',
    }
ENZYMES = {
    '1': 'aase',
    '2': 'base',
    '3': 'case',
    '4': 'dase',
    }
EQUATIONS = {
    '1': 'eq1',
    '2': 'eq2',
    '3': 'eq3',
    '4': 'eq4',
    '5': 'eq5',
    '6': 'eq6',
    }
REACTION_ECS = {
    '1': ['1', '2'],
    '2': ['1', '3'],
    '3': ['1', '4'],
    '4': ['2', '3'],
    '5': ['2', '4'],
    '6': ['3', '4'],
    }
EC_REACTIONS = {
    '1': ['1', '2', '3'],
    '2': ['1', '4', '5'],
    '3': ['2', '4', '6'],
    '4': ['3', '5', '6'],
    }
CONTEXT = {
    'stoichiometrics': STOICHIOMETRICS,
    'complexities': COMPLEXITIES,
    'compound_reactions': COMPOUND_REACTIONS,
    'demands': DEMANDS,
    'prices': PRICES,
    'compounds': COMPOUNDS,
    'enzymes': ENZYMES,
    'equations': EQUATIONS,
    'reaction_ecs': REACTION_ECS,
    'ec_reactions': EC_REACTIONS,
    }
GRAPH = pw.initialize_graph(
    STOICHIOMETRICS,
    COMPOUND_REACTIONS,
    set(),
    chebi.IGNORED_COMPOUNDS,
    )


class TestDetermineIntermediates:

    substrates = [
        {'chebi': '10', 'number': 1, 'name': 'a'},
        {'chebi': '20', 'number': 2, 'name': 'b'},
        {'chebi': '20', 'number': 2, 'name': 'b'},
        {'chebi': '30', 'number': 3, 'name': 'c'},
        ]
    products = [
        {'chebi': '20', 'number': 2, 'name': 'b'},
        {'chebi': '30', 'number': 3, 'name': 'c'},
        {'chebi': '30', 'number': 3, 'name': 'c'},
        {'chebi': '40', 'number': 4, 'name': 'd'},
        ]

    def test_determine_correct_intermediates(self):
        output = pw.determine_intermediates(self.substrates, self.products)
        correct = {'20': (4, 2), '30': (3, 6)}
        assert output == correct


class TestEvaluateInput:

    n = 100
    pathways_all = [
        ('1', ), ('1', '4'), ('1', '4', '5'),
        ('2', ), ('2', '6'), ('2', '6', '3'),
        ('3', ), ('3', '2'), ('3', '2', '6'),
        ('4', ), ('4', '5'), ('4', '5', '1'),
        ('5', ), ('5', '1'), ('5', '1', '4'),
        ('6', ), ('6', '3'), ('6', '3', '2'),
        ]

    def test_return_1_result_n_1(self):
        output = pw.evaluate_input(
            1, GRAPH, compounds=['1', '3'], context=CONTEXT)
        assert len(output) == 1

    def test_return_2_result_n_2(self):
        output = pw.evaluate_input(
            2, GRAPH, compounds=['1', '3'], context=CONTEXT)
        assert len(output) == 2

    # Compounds
    def test_return_correct_pathways_compounds_1_any(self):
        output = pw.evaluate_input(
            self.n, GRAPH, compounds=['1', 'any'], context=CONTEXT)
        correct = [('1', ), ('1', '4'), ('2', ), ('2', '6')]
        pathways = [pw for __, pw in output]
        assert sorted(pathways) == sorted(correct)

    def test_return_correct_pathways_compounds_any_1(self):
        output = pw.evaluate_input(
            self.n, GRAPH, compounds=['any', '1'], context=CONTEXT)
        correct = [('3', ), ('4', '5'), ('5', ), ('6', '3')]
        pathways = [pw for __, pw in output]
        assert sorted(pathways) == sorted(correct)

    def test_return_correct_pathways_compounds_1_3(self):
        output = pw.evaluate_input(
            self.n, GRAPH, compounds=['1', '3'], context=CONTEXT)
        pathways = [pw for __, pw in output]
        correct = [('1', ), ('2', '6')]
        assert sorted(pathways) == sorted(correct)

    def test_return_correct_pathways_compounds_1_3_5(self):
        output = pw.evaluate_input(
            self.n, GRAPH, compounds=['1', '3', '5'], context=CONTEXT)
        pathways = [pw for __, pw in output]
        correct = [('1', '4')]
        assert sorted(pathways) == sorted(correct)

    # Enzymes
    def test_return_correct_pathways_enzymes_1(self):
        output = pw.evaluate_input(
            self.n, GRAPH, enzymes=['1'], context=CONTEXT)
        correct = [
            ('1', ), ('1', '4'), ('1', '4', '5'),
            ('2', ), ('2', '6'), ('2', '6', '3'),
            ('3', ), ('3', '2'), ('3', '2', '6'),
            ('4', '5', '1'),
            ('5', '1'),
            ('6', '3'), ('6', '3', '2'),
            ]
        pathways = [pw for __, pw in output]
        assert sorted(pathways) == sorted(correct)

    def test_return_correct_pathways_enzymes_1_2(self):
        output = pw.evaluate_input(
            self.n, GRAPH, enzymes=['1', '2'], context=CONTEXT)
        correct = [
            ('1', ), ('1', '4'), ('1', '4', '5'),
            ('4', '5', '1'),
            ('5', '1'), ('5', '1', '4'),
            ]
        pathways = [pw for __, pw in output]
        assert sorted(pathways) == sorted(correct)

    def test_return_correct_pathways_enzymes_1_2_3(self):
        output = pw.evaluate_input(
            self.n, GRAPH, enzymes=['1', '2', '3'], context=CONTEXT)
        correct = [
            ('1', '4'), ('1', '4', '5'),
            ('4', '5', '1'),
            ('5', '1', '4'),
            ]
        pathways = [pw for __, pw in output]
        assert sorted(pathways) == sorted(correct)

    # Combinations
    def test_return_correct_pathways_compounds_1_any_enzymes_1(self):
        output = pw.evaluate_input(
            self.n, GRAPH, compounds=['1', 'any'], enzymes=['1'],
            context=CONTEXT)
        correct = [('1', ), ('1', '4'), ('2', ), ('2', '6')]
        pathways = [pw for __, pw in output]
        assert sorted(pathways) == sorted(correct)

    def test_return_correct_pathways_compounds_any_1_enzymes_1(self):
        output = pw.evaluate_input(
            self.n, GRAPH, compounds=['any', '1'], enzymes=['1'],
            context=CONTEXT)
        correct = [('3', ), ('6', '3')]
        pathways = [pw for __, pw in output]
        assert sorted(pathways) == sorted(correct)

    def test_return_correct_pathways_compounds_1_3_enzymes_1_2(self):
        output = pw.evaluate_input(
            self.n, GRAPH, compounds=['1', '3'], enzymes=['1', '2'],
            context=CONTEXT)
        pathways = [pw for __, pw in output]
        correct = [('1', )]
        assert sorted(pathways) == sorted(correct)

    def test_return_correct_pathways_compounds_1_3_5_enzymes_1_2_3(self):
        output = pw.evaluate_input(
            self.n, GRAPH, compounds=['1', '3', '5'], enzymes=['1', '2', '3'],
            context=CONTEXT)
        pathways = [pw for __, pw in output]
        correct = [('1', '4')]
        assert sorted(pathways) == sorted(correct)


class TestEvaluatePathway:

    steps_1 = OrderedDict([
        ('6', [6, {'5': 5, '6': 6}, {'3': 3, '4': 4}]),
        ])
    steps_2 = OrderedDict([
        ('2', [2, {'1': 1, '2': 2}, {'5': 5, '6': 6}]),
        ('6', [6, {'5': 5, '6': 6}, {'3': 3, '4': 4}]),
        ])
    steps_3 = OrderedDict([
        ('4', [4, {'3': 3, '4': 4}, {'5': 5, '6': 6}]),
        ('6', [6, {'5': 5, '6': 6}, {'3': 3, '4': 4}]),
        ('3', [3, {'3': 3, '4': 4}, {'1': 1, '2': 2}]),
        ])
    compounds = {
        '1': (1, 6), '2': (2, 5), '3': (3, 4),
        '4': (4, 3), '5': (5, 2), '6': (1, 6),
        }

    def test_raise_typeerror_compounds_not_dict(self):
        with pytest.raises(TypeError):
            pw.evaluate_pathway(self.steps_1, list(self.compounds))

    def test_return_correct_value_56_steps_1(self):
        output = pw.evaluate_pathway(self.steps_1, self.compounds)
        assert output == 56

    def test_return_correct_value_36_steps_2(self):
        output = pw.evaluate_pathway(self.steps_2, self.compounds)
        assert output == 36

    def test_return_correct_value_ceil_16times14per3_steps_3(self):
        output = pw.evaluate_pathway(self.steps_3, self.compounds)
        assert output == pw.m.ceil(16 * 14 / 3)


class TestFilterPathways:

    pathways = [
        ['1'], ['1', '4'], ['1', '4', '5'],
        ['4'], ['4', '5'], ['4', '5', '1'],
        ['5'], ['5', '1'], ['5', '1', '4'],
        ]

    def test_raise_keyerror_no_optional_arguments(self):
        with pytest.raises(KeyError):
            list(pw.filter_pathways(self.pathways))

    def test_yield_no_pathways_filter_all(self):
        correct = []
        output = list(
            pw.filter_pathways(self.pathways, compounds=['1', '3', '5'],
                              enzymes=['1', '2', '3', '4'], source='1',
                              target='3', context=CONTEXT))
        assert output == correct

    # Compounds
    def test_yield_correct_pathways_filter_compounds_1(self):
        correct = [
            ('1', ), ('1', '4'), ('1', '4', '5'),
            ('4', '5'), ('4', '5', '1'),
            ('5', ), ('5', '1'), ('5', '1', '4'),
            ]
        output = list(
            pw.filter_pathways(self.pathways, compounds=['1'], context=CONTEXT))
        assert output == correct

    def test_yield_correct_pathways_filter_compounds_1_3(self):
        correct = [
            ('1', ), ('1', '4'), ('1', '4', '5'),
            ('4', '5'), ('4', '5', '1'),
            ('5', '1'), ('5', '1', '4'),
            ]
        output = list(
            pw.filter_pathways(
                self.pathways, compounds=['1', '3'], context=CONTEXT))
        assert output == correct

    def test_yield_correct_pathways_filter_compounds_1_3_5(self):
        correct = [
            ('1', '4'), ('1', '4', '5'),
            ('4', '5'), ('4', '5', '1'),
            ('5', '1'), ('5', '1', '4'),
            ]
        output = list(
            pw.filter_pathways(
                self.pathways, compounds=['1', '3', '5'], context=CONTEXT))
        assert output == correct

    # Enzymes
    def test_yield_correct_pathways_filter_enzymes_1(self):
        correct = [
            ('1', ), ('1', '4'), ('1', '4', '5'),
            ('4', '5', '1'),
            ('5', '1'), ('5', '1', '4'),
            ]
        output = list(
            pw.filter_pathways(self.pathways, enzymes=['1'], context=CONTEXT))
        assert output == correct

    def test_yield_correct_pathways_filter_enzymes_1_3(self):
        correct = [
            ('1', '4'), ('1', '4', '5'),
            ('4', '5', '1'),
            ('5', '1', '4'),
            ]
        output = list(
            pw.filter_pathways(
                self.pathways, enzymes=['1', '3'], context=CONTEXT))
        assert output == correct

    def test_yield_correct_pathways_filter_enzymes_1_3_4(self):
        correct = [('1', '4', '5'), ('4', '5', '1'), ('5', '1', '4')]
        output = list(
            pw.filter_pathways(
                self.pathways, enzymes=['1', '3', '4'], context=CONTEXT))
        assert output == correct

    # Source
    def test_yield_correct_pathways_filter_source_3(self):
        correct = [('4', ), ('4', '5'), ('5', )]
        output = list(
            pw.filter_pathways(self.pathways, source='3', context=CONTEXT))
        assert output == correct

    def test_yield_correct_pathways_filter_source_5(self):
        correct = [('1', ), ('5', ), ('5', '1')]
        output = list(
            pw.filter_pathways(self.pathways, source='5', context=CONTEXT))
        assert output == correct

    # Target
    def test_yield_correct_pathways_filter_target_3(self):
        correct = [('1', ), ('5', ), ('5', '1')]
        output = list(
            pw.filter_pathways(self.pathways, target='3', context=CONTEXT))
        assert output == correct

    def test_yield_correct_pathways_filter_target_5(self):
        correct = [('1', ), ('1', '4'), ('4', )]
        output = list(
            pw.filter_pathways(self.pathways, target='5', context=CONTEXT))
        assert output == correct

    # No filter parameters
    def test_yield_correct_pathways_filter_not_cycle_6_1_3_5(self):
        pathways = [['6', '1', '3', '5']]
        correct = [('6', '1', '3', '5')]
        output = list(pw.filter_pathways(pathways, context=CONTEXT))
        assert output == correct

    def test_yield_correct_pathways_filter_cycle_1_3_2(self):
        correct = []
        output = list(pw.filter_pathways([['1', '3', '2']], context=CONTEXT))
        assert output == correct

    def test_yield_correct_pathways_filter_cycle_5_1_3(self):
        correct = []
        output = list(pw.filter_pathways([['5', '1', '3']], context=CONTEXT))
        assert output == correct

    def test_yield_correct_pathways_filter_cycle_5_1_3_2(self):
        pathways = [['5', '1', '3', '2']]
        correct = []
        output = list(pw.filter_pathways(pathways, context=CONTEXT))
        assert output == correct

    def test_yield_all_pathways_no_filters_no_cycles(self):
        output = list(pw.filter_pathways(self.pathways, context=CONTEXT))
        correct = list(tuple(pw) for pw in self.pathways)
        assert output == correct

    # Paired filters
    def test_filter_compounds_1_enzymes_3(self):
        correct = [
            ('1', '4'), ('1', '4', '5'),
            ('4', '5'), ('4', '5', '1'),
            ('5', '1', '4'),
            ]
        output = list(
            pw.filter_pathways(self.pathways, compounds=['1'], enzymes=['3'],
                              context=CONTEXT))
        assert output == correct

    def test_filter_compounds_1_3_source_5(self):
        correct = [('1', ), ('5', '1')]
        output = list(
            pw.filter_pathways(self.pathways, compounds=['1', '3'], source='5',
                              context=CONTEXT))
        assert output == correct

    def test_filter_compounds_1_3_target_3(self):
        correct = [('1', ), ('5', '1')]
        output = list(
            pw.filter_pathways(self.pathways, compounds=['1', '3'], target='3',
                              context=CONTEXT))
        assert output == correct

    def test_filter_enzymes_1_source_5(self):
        correct = [('1', ), ('5', '1')]
        output = list(
            pw.filter_pathways(
                self.pathways, enzymes=['1'], source='5', context=CONTEXT))
        assert output == correct

    def test_filter_enzymes_1_target_5(self):
        correct = [('1', ), ('1', '4')]
        output = list(
            pw.filter_pathways(
                self.pathways, enzymes=['1'], target='5', context=CONTEXT))
        assert output == correct

    def test_filter_source_3_target_5(self):
        correct = [('4', )]
        output = list(
            pw.filter_pathways(
                self.pathways, source='3', target='5', context=CONTEXT))
        assert output == correct

    def test_filter_compounds_1_3_enzymes_1_source_1_target_3(self):
        correct = [('1', )]
        output = list(
            pw.filter_pathways(self.pathways, compounds=['1', '3'],
                              enzymes=['1'], source='1', target='3',
                              context=CONTEXT))
        assert output == correct


class TestFindPathway:

    graph = pw.initialize_graph(STOICHIOMETRICS, COMPOUND_REACTIONS)

    def test_catch_keyerror_invalid_source_id(self):
        list(pw.find_pathway(self.graph, source='source', target=None))

    def test_catch_keyerror_invalid_target_id(self):
        list(pw.find_pathway(self.graph, source=None, target='target'))

    def test_correct_pathways_in_output_source_1_target_none(self):
        output = list(pw.find_pathway(self.graph, source='1', target=None))
        correct = [['1'], ['1', '4'], ['1', '4', '5']]
        assert sorted(output) == sorted(correct)

    def test_correct_pathways_in_output_source_none_target_5(self):
        output = list(pw.find_pathway(self.graph, source=None, target='5'))
        correct = [['1', '4', '5'], ['4', '5'], ['5']]
        assert sorted(output) == sorted(correct)

    def test_correct_pathways_in_output_source_1_target_5(self):
        output = list(pw.find_pathway(self.graph, source='1', target='5'))
        correct = [['1', '4', '5']]
        assert sorted(output) == sorted(correct)

    def test_correct_pathways_in_output_source_5_target_1(self):
        output = list(pw.find_pathway(self.graph, source='5', target='1'))
        correct = [['5', '1']]
        assert sorted(output) == sorted(correct)

    def test_raise_catch_networkxnopath_no_paths_found(self):
        output = list(pw.find_pathway(self.graph, source='1', target='6'))
        assert output == []


class TestInitializeGraph:

    def test_has_correct_edges(self):
        G = pw.initialize_graph(STOICHIOMETRICS, COMPOUND_REACTIONS)
        assert set(nx.edges(G)) \
            == set([('1', '4'), ('2', '6'), ('3', '2'),
                    ('4', '5'), ('5', '1'), ('6', '3')])

    def test_has_correct_nodes(self):
        G = pw.initialize_graph(STOICHIOMETRICS, COMPOUND_REACTIONS)
        assert set(nx.nodes(G)) == set(['1', '2', '3', '4', '5', '6'])

    def test_ignores_correct_compounds_1(self):
        G = pw.initialize_graph(
            STOICHIOMETRICS, COMPOUND_REACTIONS,
            set(), set(('1', '3', '6'))
            )
        assert set(nx.edges(G)) \
            == set([('1', '4'), ('2', '6'), ('3', '2'),
                    ('4', '5'), ('5', '1'), ('6', '3')])
        assert set(nx.nodes(G)) == set(['1', '2', '3', '4', '5', '6'])

    def test_ignores_correct_compounds_2(self):
        G = pw.initialize_graph(
            STOICHIOMETRICS, COMPOUND_REACTIONS,
            set(), set(('1', '2'))
            )
        assert set(nx.edges(G)) \
            == set([('1', '4'), ('2', '6'), ('4', '5'), ('6', '3')])
        assert set(nx.nodes(G)) == set(['1', '2', '3', '4', '5', '6'])

    def test_ignores_correct_reactions_1(self):
        G = pw.initialize_graph(
            STOICHIOMETRICS, COMPOUND_REACTIONS,
            set('1'), set()
            )
        assert set(nx.edges(G)) \
            == set([('2', '6'), ('3', '2'), ('4', '5'), ('6', '3')])
        assert set(nx.nodes(G)) == set(['2', '3', '4', '5', '6'])

    def test_ignores_correct_reactions_2(self):
        G = pw.initialize_graph(
            STOICHIOMETRICS, COMPOUND_REACTIONS,
            set(('1', '2')), set()
            )
        assert set(nx.edges(G)) == set([('4', '5'), ('6', '3')])
        assert set(nx.nodes(G)) == set(['3', '4', '5', '6'])

    def test_returns_default_null_graph(self):
        assert not nx.nodes(pw.initialize_graph())


class TestIntersectDict:

    def test_default_return_empty_dict(self):
        output = pw.intersect_dict({'1': 1, '2': 2, '3': 3})
        assert output == {}

    def test_intersect_correctly(self):
        output = pw.intersect_dict({'1': 1, '2': 2, '3': 3}, set(('1', '2')))
        correct = {'1': 1, '2': 2}
        assert output == correct


class TestNBestItems:

    n = 3
    values = [1, 2, 3, 4, 5, 6]
    items = ['worst', 'worse', 'bad', 'good', 'better', 'best']

    def test_raise_typeerror_n_invalid_type(self):
        with pytest.raises(TypeError):
            pw.nbest_items(str(self.n), self.values, self.items)

    def test_raise_typeerror_values_not_numbers(self):
        with pytest.raises(TypeError):
            pw.nbest_items(self.n, [str(v) for v in self.values], self.items)

    def test_raise_valueerror_n_less_than_1(self):
        with pytest.raises(ValueError):
            pw.nbest_items(0, self.values, self.items)

    def test_return_correct_amount(self):
        output = pw.nbest_items(self.n, self.values, self.items)
        assert len(output) == self.n

    def test_return_correct_sorting(self):
        output = pw.nbest_items(self.n, self.values, self.items)
        correct = [(6, 'best'), (5, 'better'), (4, 'good')]
        assert output == correct


class TestOrderPathwayData:

    pathways = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ]
    output = list(pw.order_pathway_data(
        pathways, STOICHIOMETRICS, COMPLEXITIES, DEMANDS, PRICES))

    def test_yield_correct_compounds(self):
        compounds = [c for __, c in self.output]
        assert compounds == [
            {'1': (1, 6), '2': (2, 5), '3': (3, 4),
             '4': (4, 3), '5': (5, 2), '6': (6, 1),
             },
            {'1': (1, 6), '2': (2, 5), '3': (3, 4),
             '4': (4, 3), '5': (5, 2), '6': (6, 1),
             },
            ]

    def test_yield_correct_steps(self):
        steps = [s for s, __ in self.output]
        assert steps == [
            OrderedDict([
                ('1', [1, {'1': 1, '2': 1}, {'3': 1, '4': 1}]),
                ('2', [2, {'1': 2, '2': 2}, {'5': 2, '6': 2}]),
                ('3', [3, {'3': 1, '4': 1}, {'1': 1, '2': 1}]),
                ]),
            OrderedDict([
                ('4', [4, {'3': 3, '4': 3}, {'5': 3, '6': 3}]),
                ('5', [5, {'5': 2, '6': 2}, {'1': 2, '2': 2}]),
                ('6', [6, {'5': 3, '6': 3}, {'3': 3, '4': 3}]),
                ]),
            ]
