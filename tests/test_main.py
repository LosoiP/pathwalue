# -*- coding: utf-8 -*-
"""
pytest module for main.py tests.

"""

from collections import OrderedDict

import networkx as nx
import pytest

from context import main as m


STOICHIOMETRICS = {
    '1': [{'1': 1, '2': 1}, {'3': 1, '4': 1}],
    '2': [{'1': 2, '2': 2}, {'5': 2, '6': 2}],
    '3': [{'3': 1, '4': 1}, {'1': 1, '2': 1}],
    '4': [{'3': 3, '4': 3}, {'5': 3, '6': 3}],
    '5': [{'5': 2, '6': 2}, {'1': 2, '2': 2}],
    '6': [{'5': 3, '6': 3}, {'3': 3, '4': 3}],
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
GRAPH = m.initialize_graph(
    STOICHIOMETRICS,
    COMPOUND_REACTIONS,
    set(),
    m._IGNORED_COMPOUNDS,
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
        output = m.determine_intermediates(self.substrates, self.products)
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
        output = m.evaluate_input(
            1, GRAPH, compounds=['1', '3'], context=CONTEXT)
        assert len(output) == 1

    def test_return_2_result_n_2(self):
        output = m.evaluate_input(
            2, GRAPH, compounds=['1', '3'], context=CONTEXT)
        assert len(output) == 2

    # Compounds
    def test_return_correct_pathways_compounds_1_any(self):
        output = m.evaluate_input(
            self.n, GRAPH, compounds=['1', 'any'], context=CONTEXT)
        correct = [('1', ), ('1', '4'), ('2', ), ('2', '6')]
        pathways = [pw for __, pw in output]
        assert sorted(pathways) == sorted(correct)

    def test_return_correct_pathways_compounds_any_1(self):
        output = m.evaluate_input(
            self.n, GRAPH, compounds=['any', '1'], context=CONTEXT)
        correct = [('3', ), ('4', '5'), ('5', ), ('6', '3')]
        pathways = [pw for __, pw in output]
        assert sorted(pathways) == sorted(correct)

    def test_return_correct_pathways_compounds_1_3(self):
        output = m.evaluate_input(
            self.n, GRAPH, compounds=['1', '3'], context=CONTEXT)
        pathways = [pw for __, pw in output]
        correct = [('1', ), ('2', '6')]
        assert sorted(pathways) == sorted(correct)

    def test_return_correct_pathways_compounds_1_3_5(self):
        output = m.evaluate_input(
            self.n, GRAPH, compounds=['1', '3', '5'], context=CONTEXT)
        pathways = [pw for __, pw in output]
        correct = [('1', '4')]
        assert sorted(pathways) == sorted(correct)

    # Enzymes
    def test_return_correct_pathways_enzymes_1(self):
        output = m.evaluate_input(
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
        output = m.evaluate_input(
            self.n, GRAPH, enzymes=['1', '2'], context=CONTEXT)
        correct = [
            ('1', ), ('1', '4'), ('1', '4', '5'),
            ('4', '5', '1'),
            ('5', '1'), ('5', '1', '4'),
            ]
        pathways = [pw for __, pw in output]
        assert sorted(pathways) == sorted(correct)

    def test_return_correct_pathways_enzymes_1_2_3(self):
        output = m.evaluate_input(
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
        output = m.evaluate_input(
            self.n, GRAPH, compounds=['1', 'any'], enzymes=['1'],
            context=CONTEXT)
        correct = [('1', ), ('1', '4'), ('2', ), ('2', '6')]
        pathways = [pw for __, pw in output]
        assert sorted(pathways) == sorted(correct)

    def test_return_correct_pathways_compounds_any_1_enzymes_1(self):
        output = m.evaluate_input(
            self.n, GRAPH, compounds=['any', '1'], enzymes=['1'],
            context=CONTEXT)
        correct = [('3', ), ('6', '3')]
        pathways = [pw for __, pw in output]
        assert sorted(pathways) == sorted(correct)

    def test_return_correct_pathways_compounds_1_3_enzymes_1_2(self):
        output = m.evaluate_input(
            self.n, GRAPH, compounds=['1', '3'], enzymes=['1', '2'],
            context=CONTEXT)
        pathways = [pw for __, pw in output]
        correct = [('1', )]
        assert sorted(pathways) == sorted(correct)

    def test_return_correct_pathways_compounds_1_3_5_enzymes_1_2_3(self):
        output = m.evaluate_input(
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
            m.evaluate_pathway(self.steps_1, list(self.compounds))

    def test_return_correct_value_56_steps_1(self):
        output = m.evaluate_pathway(self.steps_1, self.compounds)
        assert output == 56

    def test_return_correct_value_36_steps_2(self):
        output = m.evaluate_pathway(self.steps_2, self.compounds)
        assert output == 36

    def test_return_correct_value_ceil_16times14per3_steps_3(self):
        output = m.evaluate_pathway(self.steps_3, self.compounds)
        assert output == m.m.ceil(16 * 14 / 3)


class TestFilterPathways:

    pathways = [
        ['1'], ['1', '4'], ['1', '4', '5'],
        ['4'], ['4', '5'], ['4', '5', '1'],
        ['5'], ['5', '1'], ['5', '1', '4'],
        ]

    def test_raise_keyerror_no_optional_arguments(self):
        with pytest.raises(KeyError):
            list(m.filter_pathways(self.pathways))

    def test_yield_no_pathways_filter_all(self):
        correct = []
        output = list(
            m.filter_pathways(self.pathways, compounds=['1', '3', '5'],
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
            m.filter_pathways(self.pathways, compounds=['1'], context=CONTEXT))
        assert output == correct

    def test_yield_correct_pathways_filter_compounds_1_3(self):
        correct = [
            ('1', ), ('1', '4'), ('1', '4', '5'),
            ('4', '5'), ('4', '5', '1'),
            ('5', '1'), ('5', '1', '4'),
            ]
        output = list(
            m.filter_pathways(
                self.pathways, compounds=['1', '3'], context=CONTEXT))
        assert output == correct

    def test_yield_correct_pathways_filter_compounds_1_3_5(self):
        correct = [
            ('1', '4'), ('1', '4', '5'),
            ('4', '5'), ('4', '5', '1'),
            ('5', '1'), ('5', '1', '4'),
            ]
        output = list(
            m.filter_pathways(
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
            m.filter_pathways(self.pathways, enzymes=['1'], context=CONTEXT))
        assert output == correct

    def test_yield_correct_pathways_filter_enzymes_1_3(self):
        correct = [
            ('1', '4'), ('1', '4', '5'),
            ('4', '5', '1'),
            ('5', '1', '4'),
            ]
        output = list(
            m.filter_pathways(
                self.pathways, enzymes=['1', '3'], context=CONTEXT))
        assert output == correct

    def test_yield_correct_pathways_filter_enzymes_1_3_4(self):
        correct = [('1', '4', '5'), ('4', '5', '1'), ('5', '1', '4')]
        output = list(
            m.filter_pathways(
                self.pathways, enzymes=['1', '3', '4'], context=CONTEXT))
        assert output == correct

    # Source
    def test_yield_correct_pathways_filter_source_3(self):
        correct = [('4', ), ('4', '5'), ('5', )]
        output = list(
            m.filter_pathways(self.pathways, source='3', context=CONTEXT))
        assert output == correct

    def test_yield_correct_pathways_filter_source_5(self):
        correct = [('1', ), ('5', ), ('5', '1')]
        output = list(
            m.filter_pathways(self.pathways, source='5', context=CONTEXT))
        assert output == correct

    # Target
    def test_yield_correct_pathways_filter_target_3(self):
        correct = [('1', ), ('5', ), ('5', '1')]
        output = list(
            m.filter_pathways(self.pathways, target='3', context=CONTEXT))
        assert output == correct

    def test_yield_correct_pathways_filter_target_5(self):
        correct = [('1', ), ('1', '4'), ('4', )]
        output = list(
            m.filter_pathways(self.pathways, target='5', context=CONTEXT))
        assert output == correct

    # No filter parameters
    def test_yield_correct_pathways_filter_not_cycle_6_1_3_5(self):
        pathways = [['6', '1', '3', '5']]
        correct = [('6', '1', '3', '5')]
        output = list(m.filter_pathways(pathways, context=CONTEXT))
        assert output == correct

    def test_yield_correct_pathways_filter_cycle_1_3_2(self):
        correct = []
        output = list(m.filter_pathways([['1', '3', '2']], context=CONTEXT))
        assert output == correct

    def test_yield_correct_pathways_filter_cycle_5_1_3(self):
        correct = []
        output = list(m.filter_pathways([['5', '1', '3']], context=CONTEXT))
        assert output == correct

    def test_yield_correct_pathways_filter_cycle_5_1_3_2(self):
        pathways = [['5', '1', '3', '2']]
        correct = []
        output = list(m.filter_pathways(pathways, context=CONTEXT))
        assert output == correct

    def test_yield_all_pathways_no_filters_no_cycles(self):
        output = list(m.filter_pathways(self.pathways, context=CONTEXT))
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
            m.filter_pathways(self.pathways, compounds=['1'], enzymes=['3'],
                              context=CONTEXT))
        assert output == correct

    def test_filter_compounds_1_3_source_5(self):
        correct = [('1', ), ('5', '1')]
        output = list(
            m.filter_pathways(self.pathways, compounds=['1', '3'], source='5',
                              context=CONTEXT))
        assert output == correct

    def test_filter_compounds_1_3_target_3(self):
        correct = [('1', ), ('5', '1')]
        output = list(
            m.filter_pathways(self.pathways, compounds=['1', '3'], target='3',
                              context=CONTEXT))
        assert output == correct

    def test_filter_enzymes_1_source_5(self):
        correct = [('1', ), ('5', '1')]
        output = list(
            m.filter_pathways(
                self.pathways, enzymes=['1'], source='5', context=CONTEXT))
        assert output == correct

    def test_filter_enzymes_1_target_5(self):
        correct = [('1', ), ('1', '4')]
        output = list(
            m.filter_pathways(
                self.pathways, enzymes=['1'], target='5', context=CONTEXT))
        assert output == correct

    def test_filter_source_3_target_5(self):
        correct = [('4', )]
        output = list(
            m.filter_pathways(
                self.pathways, source='3', target='5', context=CONTEXT))
        assert output == correct

    def test_filter_compounds_1_3_enzymes_1_source_1_target_3(self):
        correct = [('1', )]
        output = list(
            m.filter_pathways(self.pathways, compounds=['1', '3'],
                              enzymes=['1'], source='1', target='3',
                              context=CONTEXT))
        assert output == correct


class TestFindPathway:

    graph = m.initialize_graph(STOICHIOMETRICS, COMPOUND_REACTIONS)

    def test_catch_keyerror_invalid_source_id(self):
        list(m.find_pathway(self.graph, source='source', target=None))

    def test_catch_keyerror_invalid_target_id(self):
        list(m.find_pathway(self.graph, source=None, target='target'))

    def test_correct_pathways_in_output_source_1_target_none(self):
        output = list(m.find_pathway(self.graph, source='1', target=None))
        correct = [['1'], ['1', '4'], ['1', '4', '5']]
        assert sorted(output) == sorted(correct)

    def test_correct_pathways_in_output_source_none_target_5(self):
        output = list(m.find_pathway(self.graph, source=None, target='5'))
        correct = [['1', '4', '5'], ['4', '5'], ['5']]
        assert sorted(output) == sorted(correct)

    def test_correct_pathways_in_output_source_1_target_5(self):
        output = list(m.find_pathway(self.graph, source='1', target='5'))
        correct = [['1', '4', '5']]
        assert sorted(output) == sorted(correct)

    def test_correct_pathways_in_output_source_5_target_1(self):
        output = list(m.find_pathway(self.graph, source='5', target='1'))
        correct = [['5', '1']]
        assert sorted(output) == sorted(correct)

    def test_raise_catch_networkxnopath_no_paths_found(self):
        output = list(m.find_pathway(self.graph, source='1', target='6'))
        assert output == []


class TestFormatCompound:

    compound = {'1': 1}
    output = m.format_compound(compound, CONTEXT)

    def test_correct_chebi_in_output(self):
        assert self.output['chebi'] == '1'

    def test_correct_name_in_output(self):
        assert self.output['name'] == 'a'

    def test_correct_number_in_output(self):
        assert self.output['number'] == 1

    def test_dict_not_changed_in_function(self):
        correct = {
            'chebi': '1',
            'number': 1,
            'name': 'a',
            }
        assert m.format_compound(self.compound, CONTEXT) == correct

    def test_empty_data_empty_compound(self):
        assert m.format_compound({}, CONTEXT) == {}

    def test_only_chebi_and_number_in_output_empty_context(self):
        output = m.format_compound({'1': 1})
        assert output == {'chebi': '1', 'name': '', 'number': 1}


class TestFormatOutput:

    results = [
        (5, ['1', '4']),
        (8, ['2', '6']),
        ]
    output = m.format_output(results, CONTEXT)

    def test_correct_values_in_output(self):
        values = set(pw['value'] for pw in self.output)
        assert values == set([5, 8])

    def test_correct_reactions_in_output(self):
        pws = [pw['reactions'] for pw in self.output]
        rheas = set(r['rhea'] for reactions in pws for r in reactions)
        assert rheas == set(['1', '2', '4', '6'])

    def test_correct_substrates_in_output(self):
        pws = [pw['substrates'] for pw in self.output]
        chebis = set(s['chebi'] for substrates in pws for s in substrates)
        assert chebis == set(['1', '2'])

    def test_correct_intermediates_in_output(self):
        pws = [pw['intermediates'] for pw in self.output]
        chebis = set(i['chebi'] for inters in pws for i in inters)
        assert chebis == set(['3', '4', '5', '6'])

    def test_correct_products_in_output(self):
        pws = [pw['products'] for pw in self.output]
        chebis = set(p['chebi'] for products in pws for p in products)
        assert chebis == set(['5', '6', '3', '4'])


class TestFormatPathway:

    value = 1
    reactions = ['1', '2', '4']
    output = m.format_pathway(value, reactions, CONTEXT)
    output_no_context = m.format_pathway(value, reactions)
    output_no_reactions = m.format_pathway(value, [], CONTEXT)

    def test_correct_intermediates_in_output(self):
        intermediates = self.output['intermediates']
        correct = [
            {'chebi': '3', 'name': 'c', 'number': (3, 1)},
            {'chebi': '4', 'name': 'd', 'number': (3, 1)},
            ]
        assert all(i in correct for i in intermediates)
        assert all(c in intermediates for c in correct)

    def test_correct_products_in_output(self):
        products = self.output['products']
        correct = [
            {'chebi': '5', 'name': 'e', 'number': 2},
            {'chebi': '6', 'name': 'f', 'number': 2},
            ]
        assert all(p in correct for p in products)
        assert all(c in products for c in correct)

    def test_no_redundant_products_in_output(self):
        context = CONTEXT
        context['stoichiometrics'] = {
            }
        products = self.output['products']
        for p in products:
            assert products.count(p) == 1

    def test_no_redundant_intermediates_in_output(self):
        intermediates = self.output['intermediates']
        for i in intermediates:
            assert intermediates.count(i) == 1

    def test_no_redundant_substrates_in_output(self):
        substrates = self.output['substrates']
        for s in substrates:
            assert substrates.count(s) == 1

    def test_correct_reactions_in_output(self):
        reactions = self.output['reactions']
        correct = [
            {'rhea': '1',
             'equation': 'eq1',
             'enzymes': {'1': 'aase', '2': 'base'},
             'substrates': {'1': 1, '2': 1},
             'products': {'3': 1, '4': 1},
             },
            {'rhea': '2',
             'equation': 'eq2',
             'enzymes': {'1': 'aase', '3': 'case'},
             'substrates': {'1': 2, '2': 2},
             'products': {'5': 2, '6': 2},
             },
            {'rhea': '4',
             'equation': 'eq4',
             'enzymes': {'2': 'base', '3': 'case'},
             'substrates': {'3': 3, '4': 3},
             'products': {'5': 3, '6': 3},
             },
             ]
        assert reactions == correct

    def test_correct_substrates_in_output(self):
        substrates = self.output['substrates']
        correct = [
            {'chebi': '1', 'name': 'a', 'number': 1},
            {'chebi': '2', 'name': 'b', 'number': 1},
            ]
        print(substrates)
        assert all(s in correct for s in substrates)
        assert all(c in substrates for c in correct)

    def test_correct_value_in_output(self):
        assert self.output['value'] == 1

    def test_empty_intermediates_empty_context(self):
        intermediates = self.output_no_context['intermediates']
        assert not any(v for i in intermediates for v in i.values())

    def test_empty_intermediates_empty_reactions(self):
        intermediates = self.output_no_reactions['intermediates']
        assert not any(v for i in intermediates for v in i.values())

    def test_empty_products_empty_context(self):
        products = self.output_no_context['products']
        assert not any(v for p in products for v in p.values())

    def test_empty_products_empty_reactions(self):
        products = self.output_no_reactions['products']
        assert not any(v for p in products for v in p.values())

    def test_empty_substrates_empty_context(self):
        substrates = self.output_no_context['substrates']
        assert not any(v for s in substrates for v in s.values())

    def test_empty_substrates_empty_reactions(self):
        substrates = self.output_no_reactions['substrates']
        assert not any(v for s in substrates for v in s.values())

    def test_empty_reactions_empty_reactions(self):
        reactions = self.output_no_reactions['reactions']
        assert not any(v for r in reactions for v in r.values())

    def test_reactions_empty_context(self):
        reactions = self.output_no_context['reactions']
        correct = [
            {'rhea': '1', 'equation': '', 'enzymes': {}, 'substrates': {},
             'products': {}},
            {'rhea': '2', 'equation': '', 'enzymes': {}, 'substrates': {},
             'products': {}},
            {'rhea': '4', 'equation': '', 'enzymes': {}, 'substrates': {},
             'products': {}},
            ]
        assert reactions == correct

    def test_value_empty_context(self):
        assert self.output_no_context['value'] == 1

    def test_value_empty_reactions(self):
        assert self.output_no_reactions['value'] == 1


class TestFormatReaction:

    rhea = '1'
    output = m.format_reaction(rhea, CONTEXT)

    def test_correct_enzymes_in_output(self):
        enzymes = self.output['enzymes']
        correct = {'1': 'aase', '2': 'base'}
        assert enzymes == correct

    def test_correct_equation_in_output(self):
        assert self.output['equation'] == 'eq1'

    def test_correct_products_in_output(self):
        products = {'3': 1, '4': 1}
        assert self.output['products'] == products

    def test_correct_rhea_in_output(self):
        assert self.output['rhea'] == '1'

    def test_correct_substrates_in_output(self):
        substrates = {'1': 1, '2': 1}
        assert self.output['substrates'] == substrates

    def test_only_rhea_in_output_empty_context(self):
        output = m.format_reaction(self.rhea)
        correct = {
            'rhea': '1',
            'equation': '',
            'enzymes': {},
            'substrates': {},
            'products': {},
            }
        assert output == correct


class TestInitializeGraph:

    def test_has_correct_edges(self):
        G = m.initialize_graph(STOICHIOMETRICS, COMPOUND_REACTIONS)
        assert set(nx.edges(G)) \
            == set([('1', '4'), ('2', '6'), ('3', '2'),
                    ('4', '5'), ('5', '1'), ('6', '3')])

    def test_has_correct_nodes(self):
        G = m.initialize_graph(STOICHIOMETRICS, COMPOUND_REACTIONS)
        assert set(nx.nodes(G)) == set(['1', '2', '3', '4', '5', '6'])

    def test_ignores_correct_compounds_1(self):
        G = m.initialize_graph(
            STOICHIOMETRICS, COMPOUND_REACTIONS,
            set(), set(('1', '3', '6'))
            )
        assert set(nx.edges(G)) \
            == set([('1', '4'), ('2', '6'), ('3', '2'),
                    ('4', '5'), ('5', '1'), ('6', '3')])
        assert set(nx.nodes(G)) == set(['1', '2', '3', '4', '5', '6'])

    def test_ignores_correct_compounds_2(self):
        G = m.initialize_graph(
            STOICHIOMETRICS, COMPOUND_REACTIONS,
            set(), set(('1', '2'))
            )
        assert set(nx.edges(G)) \
            == set([('1', '4'), ('2', '6'), ('4', '5'), ('6', '3')])
        assert set(nx.nodes(G)) == set(['1', '2', '3', '4', '5', '6'])

    def test_ignores_correct_reactions_1(self):
        G = m.initialize_graph(
            STOICHIOMETRICS, COMPOUND_REACTIONS,
            set('1'), set()
            )
        assert set(nx.edges(G)) \
            == set([('2', '6'), ('3', '2'), ('4', '5'), ('6', '3')])
        assert set(nx.nodes(G)) == set(['2', '3', '4', '5', '6'])

    def test_ignores_correct_reactions_2(self):
        G = m.initialize_graph(
            STOICHIOMETRICS, COMPOUND_REACTIONS,
            set(('1', '2')), set()
            )
        assert set(nx.edges(G)) == set([('4', '5'), ('6', '3')])
        assert set(nx.nodes(G)) == set(['3', '4', '5', '6'])

    def test_returns_default_null_graph(self):
        assert not nx.nodes(m.initialize_graph())


class TestIntersectDict:

    def test_default_return_empty_dict(self):
        output = m.intersect_dict({'1': 1, '2': 2, '3': 3})
        assert output == {}

    def test_intersect_correctly(self):
        output = m.intersect_dict({'1': 1, '2': 2, '3': 3}, set(('1', '2')))
        correct = {'1': 1, '2': 2}
        assert output == correct


class TestNBestItems:

    n = 3
    values = [1, 2, 3, 4, 5, 6]
    items = ['worst', 'worse', 'bad', 'good', 'better', 'best']

    def test_raise_typeerror_n_invalid_type(self):
        with pytest.raises(TypeError):
            m.nbest_items(str(self.n), self.values, self.items)

    def test_raise_typeerror_values_not_numbers(self):
        with pytest.raises(TypeError):
            m.nbest_items(self.n, [str(v) for v in self.values], self.items)

    def test_raise_valueerror_n_less_than_1(self):
        with pytest.raises(ValueError):
            m.nbest_items(0, self.values, self.items)

    def test_return_correct_amount(self):
        output = m.nbest_items(self.n, self.values, self.items)
        assert len(output) == self.n

    def test_return_correct_sorting(self):
        output = m.nbest_items(self.n, self.values, self.items)
        correct = [(6, 'best'), (5, 'better'), (4, 'good')]
        assert output == correct


class TestOrderPathwayData:

    pathways = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ]
    output = list(m.order_pathway_data(
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


class TestGetContent:

    invalid_filename = 'invalid_filename.txt'
    invalid_path = 'invalid_path'
    valid_filename = m.RHEA_EC
    valid_path = m.PATH_RHEA

    def test_output_contains_strings(self):
        output = m.get_content(self.valid_path, self.valid_filename)
        for item in output:
            assert isinstance(item, str)

    def test_output_is_list(self):
        output = m.get_content(self.valid_path, self.valid_filename)
        assert isinstance(output, list)

    def test_raise_filenotfounderror_invalid_filename(self):
        with pytest.raises(FileNotFoundError):
            m.get_content(self.valid_path, self.invalid_filename)

    def test_raise_filenotfounderror_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            m.get_content(self.invalid_path, self.valid_filename)

    def test_raise_no_errors_valid_path_valid_filename(self):
        m.get_content(self.valid_path, self.valid_filename)

    def test_raise_typeerror_invalid_filename(self):
        with pytest.raises(TypeError):
            m.get_content(self.valid_path, list(self.valid_filename))

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            m.get_content(list(self.valid_path), self.valid_filename)


class TestGetJson:

    invalid_filename = 'invalid_filename.txt'
    invalid_path = 'invalid_path'
    valid_filename = m.FILE_CMP_REACTIONS
    valid_path = m.PATH_JSON

    def test_output_is_object(self):
        output = m.get_json(self.valid_path, self.valid_filename)
        assert isinstance(output, object)

    def test_raise_filenotfounderror_invalid_filename(self):
        with pytest.raises(FileNotFoundError):
            m.get_json(self.valid_path, self.invalid_filename)

    def test_raise_filenotfounderror_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            m.get_json(self.invalid_path, self.valid_filename)

    def test_raise_no_errors_valid_path_valid_filename(self):
        m.get_json(self.valid_path, self.valid_filename)

    def test_raise_typeerror_invalid_filename(self):
        with pytest.raises(TypeError):
            m.get_json(self.valid_path, list(self.valid_filename))

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            m.get_json(list(self.valid_path), self.valid_filename)


class TestGetNames:

    invalid_path = 'invalid_path'
    valid_path = m.PATH_JSON

    def test_output_contains_strings(self):
        output = m.get_names(self.valid_path)
        for item in output:
            assert isinstance(item, str)

    def test_output_is_list(self):
        output = m.get_names(self.valid_path)
        assert isinstance(output, list)

    def test_raise_directorynotfounderror_invalid_path(self):
        with pytest.raises(m.DirectoryNotFoundError):
            m.get_names(self.invalid_path)

    def test_raise_no_errors_valid_path(self):
        m.get_names(self.valid_path)

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            m.get_names(list(self.invalid_path))


class TestWriteJson:

    filename = 'test1.txt'
    path = m.PATH_JSON
    data_object = {}

    def test_output_file_exists(self):
        m.write_json(self.data_object, self.path, self.filename)
        output = m.get_json(self.path, self.filename)
        assert isinstance(output, type(self.data_object))

    def test_raise_typeerror_invalid_filename(self):
        with pytest.raises(TypeError):
            m.write_json(self.data_object, self.path, list(self.filename))

    def test_raise_no_errors_valid_path_valid_filename(self):
        m.write_json(self.data_object, self.path, self.filename)

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            m.write_json(self.data_object, list(self.path), self.filename)

    def test_return_none(self):
        output = m.write_json(self.data_object, self.path, self.filename)
        assert isinstance(output, type(None))


class TestWriteJsons:

    filenames = ['test1.txt', 'test2.txt']
    path = m.PATH_JSON
    data = [{}, {}]

    def test_output_files_exist(self):
        m.write_jsons(self.data, self.path, self.filenames)
        for file, test_object in zip(self.filenames, self.data):
            output = m.get_json(self.path, file)
            assert isinstance(output, type(test_object))

    def test_raise_no_errors_valid_data_path_filenames(self):
        m.write_jsons(self.data, self.path, self.filenames)

    def test_raise_typeerror_invalid_data_type(self):
        with pytest.raises(TypeError):
            m.write_jsons(str(self.data), self.path, self.filenames)

    def test_raise_typeerror_invalid_filenames_type(self):
        with pytest.raises(TypeError):
            m.write_jsons(self.data, self.path, str(self.filenames))

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            m.write_jsons(self.data, list(self.path), self.filenames)

    def test_return_none(self):
        output = m.write_jsons(self.data, self.path, self.filenames)
        assert isinstance(output, type(None))
