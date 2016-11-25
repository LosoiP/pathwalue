# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 13:37:14 2016

@author: losoip
"""

import pytest

from context import chebi


class TestReadChemicalData:

    def test_return_correct_charge(self):
        assert False

    def test_return_correct_formula(self):
        assert False

    def test_return_correct_mass(self):
        assert False


class TestReadCompounds:
    pass


class TestReadRelations:
    pass


class TestReadVertices:
    pass


class TestReadTsv:

    tsv_valid = [
        'FIELD_1\tFIELD_2\tFIELD_3\n',
        '1-1\t1-2\t1-3\n',
        '2-1\t2-2\t2-3\n',
        ]

    def test_yield_correct_fields(self):
        fields = list(chebi._read_tsv(self.tsv_valid))
        correct_fields = [
            {'FIELD_1': '1-1', 'FIELD_2': '1-2', 'FIELD_3': '1-3'},
            {'FIELD_1': '2-1', 'FIELD_2': '2-2', 'FIELD_3': '2-3'},
            ]
        assert fields == correct_fields
