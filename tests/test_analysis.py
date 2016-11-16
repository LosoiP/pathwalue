# -*- coding: utf-8 -*-
"""
pytest module for analysis.py unit tests.

"""

from context import analysis as an
import networkx as nx
import pytest


ONTOLOGY_GRAPH = nx.DiGraph([('a', 'b')])
GRAPH_TYPES = {
    'a': {'1': 1, '2': 2, '3': 3},
    'b': {'1': 2, '2': 4, '3': 6},
    }
GRAPH_RELATIONS = {
    '1': {'2': 'a', '3': 'b'},
    '2': {'1': 'c', '3': 'a'},
    '3': {'1': 'd', '2': 'c'},
    '4': {'1': 'e', '2': 'f'},
    }
STOICHIOMETRICS = {
    '1': [{'1': 1, '2': 2}, {'3': 3, '4': 4}],
    '2': [{'1': 1, '2': 2}, {'5': 5, '6': 6}],
    '3': [{'3': 3, '4': 4}, {'1': 1, '2': 2}],
    '4': [{'3': 3, '4': 4}, {'5': 5, '6': 6}],
    '5': [{'5': 5, '6': 6}, {'1': 1, '2': 2}],
    '6': [{'5': 5, '6': 6}, {'3': 3, '4': 4}],
    }
COMPLEXITY_CMPS = {
    '1': 1,
    '2': 2,
    '3': 3,
    }


class TestCompareFormulae:

    def test_2_empty_dicts(self):
        with pytest.raises(ValueError):
            an.compare_formulae(({}, {}))

    def test_neither_list_nor_tuple(self):
        with pytest.raises(TypeError):
            an.compare_formulae({'C': 6, 'H': 12, 'O': 6})

    def test_too_few_dicts(self):
        with pytest.raises(ValueError):
            an.compare_formulae([{'C': 6, 'H': 12, 'O': 6}])

    def test_too_many_dicts(self):
        with pytest.raises(ValueError):
            an.compare_formulae([{'C': 6}, {'H': 12}, {'O': 6}])

    def test_2_different_dicts(self):
        assert an.compare_formulae([{'Al': 1, 'Br': 3}, {'Br': 3}]) == 1

    def test_2_identical_dicts(self):
        assert an.compare_formulae(({'H': 2, 'O': 1}, {'H': 2, 'O': 1})) == 0


class TestEvaluateComplexity:

    def test_invalid_id(self):
        with pytest.raises(an.RheaIDError):
            an.evaluate_complexity('a')

    def test_not_str(self):
        with pytest.raises(TypeError):
            an.evaluate_complexity(1)

    def test_correct_output(self):
        output = an.evaluate_complexity('1', STOICHIOMETRICS, COMPLEXITY_CMPS)
        assert output == 2*2 + 1*1


class TestEvaluateCompound:

    def test_invalid_type_demand(self):
        with pytest.raises(TypeError):
            an.evaluate_compound('4167', 3.14)

    def test_invalid_type_price(self):
        with pytest.raises(TypeError):
            an.evaluate_compound(3.14, '4167')

    def test_negative_demand(self):
        with pytest.raises(ValueError):
            an.evaluate_compound(-1.0, 3.14)

    def test_negative_price(self):
        with pytest.raises(ValueError):
            an.evaluate_compound(1, -1)

    def test_numeric_output(self):
        assert isinstance(an.evaluate_compound(1, 1.5), (float, int))


class TestEvaluateOntology:

    def test_correct_output(self):
        G = an.initialize_graph(GRAPH_RELATIONS, GRAPH_TYPES)
        compounds = ['1', '2', '3', '4']
        output = [an.evaluate_ontology(G, c, GRAPH_TYPES) for c in compounds]
        assert output == [18, 15, 9, 0]


class TestInitializeGraph:

    graph = an.initialize_graph(GRAPH_RELATIONS, GRAPH_TYPES)

    def test_correct_edges(self):
        correct = set([('1', '2'), ('1', '3'), ('2', '3')])
        assert set(nx.edges(self.graph)) == correct

    def test_correct_nodes(self):
        correct = set(['1', '2', '3'])
        assert set(nx.nodes(self.graph)) == correct


class TestParseFormula:

    def test_invalid_characters(self):
        with pytest.raises(an.ParseCharacterError):
            an.parse_formula('?')

    def test_not_str(self):
        with pytest.raises(TypeError):
            an.parse_formula(1)

    def test_all_specials_1(self):
        assert an.parse_formula('H2O.2(2H2O.C2H4)10.H2O') \
            == {'C': 40, 'H': 164, 'O': 42}

    def test_all_specials_2(self):
        assert an.parse_formula('2Al(OH)3.(C6H12O6)n') \
            == {'Al': 2, 'C': 6, 'H': 18, 'O': 12}

    def test_all_specials_3(self):
        number = 1 + 2*(1 + 2*(2 + 2*(2*2)))
        assert an.parse_formula('OH.2OH(2OH.2(2OH)2)2') \
            == {'H': number, 'O': number}

    def test_dots_1(self):
        assert an.parse_formula('10H2O.5H2O.H2O') == {'H': 32, 'O': 16}

    def test_dots_2(self):
        assert an.parse_formula('Al2O3.5Al2O3.10Al2O3') == {'Al': 32, 'O': 48}

    def test_empty_str(self):
        assert an.parse_formula('') == {}

    def test_no_numbers_1(self):
        assert an.parse_formula('CHO') == {'C': 1, 'H': 1, 'O': 1}

    def test_no_numbers_2(self):
        assert an.parse_formula('AlBrCr') == {'Al': 1, 'Br': 1, 'Cr': 1}

    def test_no_numbers_3(self):
        assert an.parse_formula('AlCHNa') == {'Al': 1, 'C': 1, 'H': 1, 'Na': 1}

    def test_parentheses_1(self):
        assert an.parse_formula('(Al2O3)10') == {'Al': 20, 'O': 30}

    def test_parentheses_2(self):
        assert an.parse_formula('(C100Br20)n') == {'Br': 20, 'C': 100}

    def test_parentheses_3(self):
        assert an.parse_formula('(SH2(SO4(OH)2)2)2') \
            == {'H': 12, 'O': 24, 'S': 6}
