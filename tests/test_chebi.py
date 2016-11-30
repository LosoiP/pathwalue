# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 13:37:14 2016

@author: losoip
"""

import pytest

from context import chebi


class TestParseChemicalData:

    chemical_data_valid = [
        {'COMPOUND_ID': '10', 'TYPE': 'CHARGE', 'CHEMICAL_DATA': '-1'},
        {'COMPOUND_ID': '10', 'TYPE': 'FORMULA', 'CHEMICAL_DATA': 'H2O'},
        {'COMPOUND_ID': '10', 'TYPE': 'MASS', 'CHEMICAL_DATA': '18.1'},
        {'COMPOUND_ID': '12', 'TYPE': 'MONOISOTOPIC MASS',
         'CHEMICAL_DATA': '18.2'},
        ]
    chemical_data_invalid_type = [
        {'COMPOUND_ID': '10', 'TYPE': '', 'CHEMICAL_DATA': '-1'},
        ]
    compound_parents = {'10': 'P10', '11': 'P11'}

    def test_return_correct_charge(self):
        charges, *__ = chebi.parse_chemical_data(self.chemical_data_valid)
        assert charges['10'] == -1

    def test_return_correct_charge_parents(self):
        charges, *__ = chebi.parse_chemical_data(self.chemical_data_valid,
                                                 self.compound_parents)
        assert charges['P10'] == -1

    def test_return_correct_formula(self):
        __, formulae, __ = chebi.parse_chemical_data(self.chemical_data_valid)
        assert formulae['10'] == 'H2O'

    def test_return_correct_formula_parents(self):
        __, formulae, __ = chebi.parse_chemical_data(self.chemical_data_valid,
                                                     self.compound_parents)
        assert formulae['P10'] == 'H2O'

    def test_return_correct_masses(self):
        *__, masses = chebi.parse_chemical_data(self.chemical_data_valid)
        assert masses == {'10': 18.1, '12': 18.2}

    def test_return_correct_mass_parents(self):
        *__, masses = chebi.parse_chemical_data(self.chemical_data_valid,
                                                self.compound_parents)
        assert masses == {'P10': 18.1, '12': 18.2}

    def test_raise_value_error_invalid_type(self):
        with pytest.raises(ValueError):
            chebi.parse_chemical_data(self.chemical_data_invalid_type)


class TestParseCompounds:

    compounds_valid = [
        {'ID': '10', 'NAME': 'c0', 'PARENT_ID': 'null', 'STATUS': 'C'},
        {'ID': '11', 'NAME': 'null', 'PARENT_ID': '10', 'STATUS': 'C'},
        ]
    compounds_invalid = [
        {'ID': '12', 'NAME': 'null', 'PARENT_ID': 'null', 'STATUS': 'C'},
        ]

    def test_return_correct_compound_names(self):
        __, compound_names = chebi.parse_compounds(self.compounds_valid)
        assert compound_names == {'10': 'c0'}

    def test_return_correct_compound_parents(self):
        compound_parents, __ = chebi.parse_compounds(self.compounds_valid)
        assert compound_parents == {'11': '10'}

    def test_raise_value_error_name_null_parent_null(self):
        with pytest.raises(ValueError):
            chebi.parse_compounds(self.compounds_invalid)


class TestParseRelations:

    relations = [
        {
            'ID': 'R1', 'FINAL_ID': 'V1', 'INIT_ID': 'V2', 'STATUS': 'C',
            'TYPE': 'T1'
            },
        {
            'ID': 'R2', 'FINAL_ID': 'V2', 'INIT_ID': 'V1', 'STATUS': 'E',
            'TYPE': 'T2'
            },
        ]
    vertex_compounds = {'V1': 'C1', 'V2': 'C2'}

    def test_return_correct_compound_names(self):
        compound_relations = chebi.parse_relations(self.relations,
                                                   self.vertex_compounds)
        assert compound_relations == {'C2': {'C1': 'T1'}}


class TestParseVertices:

    vertices = [
        {'ID': 'V1', 'COMPOUND_CHILD_ID': 'C1'},
        {'ID': 'V2', 'COMPOUND_CHILD_ID': 'C2'},
        ]
    compound_parents = {'C1': 'P1'}

    def test_return_correct_vertex_compounds(self):
        vertex_compounds = chebi.parse_vertices(self.vertices)
        assert vertex_compounds == {'V1': 'C1', 'V2': 'C2'}

    def test_return_correct_vertex_compounds_parents(self):
        vertex_compounds = chebi.parse_vertices(self.vertices,
                                                self.compound_parents)
        assert vertex_compounds == {'V1': 'P1', 'V2': 'C2'}
