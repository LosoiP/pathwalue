# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 13:37:41 2016

@author: losoip
"""

import pytest

from context import files
from context import paths


_INVALID_FILENAME = 'invalid_filename'
_INVALID_FILENAMES = ['invalid_filename_1', 'invalid_filename_2']
_INVALID_PATH = 'invalid_path'
_VALID_PATH = paths._TESTS
_VALID_CTAB = 'read_test.ctab'
_VALID_MOL = 'read_test.mol'
_VALID_RD = 'read_test.rd'
_VALID_RXN = 'read_test.rxn'
_VALID_JSON = 'read_test.json'
_VALID_JSONS = ['read_test_1.json', 'read_test_2.json']

_JSON_OBJECT = {'test_1': 1, 'test_2': 2}


class TestGetContent:

    def test_raise_filenotfounderror_invalid_filename(self):
        with pytest.raises(FileNotFoundError):
            list(files.get_content(_VALID_PATH, _INVALID_FILENAME))

    def test_raise_filenotfounderror_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            list(files.get_content(_INVALID_PATH, _VALID_JSON))

    def test_raise_no_errors_valid_path_valid_filename(self):
        list(files.get_content(_VALID_PATH, _VALID_JSON))

    def test_raise_typeerror_invalid_filename(self):
        with pytest.raises(TypeError):
            list(files.get_content(_VALID_PATH, list(_VALID_JSON)))

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            list(files.get_content(list(_VALID_PATH), _VALID_JSON))

    def test_return_iterable_of_strings(self):
        for row in files.get_content(_VALID_PATH, _VALID_JSON):
            assert isinstance(row, str)

    def test_return_list(self):
        assert isinstance(files.get_content(_VALID_PATH, _VALID_JSON), list)

    def test_return_newlines_not_stripped(self):
        for row in files.get_content(_VALID_PATH, _VALID_JSON, False):
            assert row.endswith('\n')

    def test_return_newlines_stripped(self):
        for row in files.get_content(_VALID_PATH, _VALID_JSON, True):
            assert not row.endswith('\n')


class TestGetContents:

    def test_raise_filenotfounderror_invalid_filenames(self):
        with pytest.raises(FileNotFoundError):
            list(files.get_contents(_VALID_PATH, _INVALID_FILENAMES))

    def test_raise_filenotfounderror_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            list(files.get_contents(_INVALID_PATH, _VALID_JSONS))

    def test_raise_no_errors_valid_path_valid_filenames(self):
        list(files.get_contents(_VALID_PATH, _VALID_JSONS))

    def test_raise_typeerror_invalid_filenames(self):
        with pytest.raises(TypeError):
            list(files.get_contents(_VALID_PATH, str(_VALID_JSONS)))

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            list(files.get_contents(list(_VALID_PATH), _VALID_JSONS))

    def test_yield_lists_of_strings(self):
        all_files = files.get_contents(_VALID_PATH, _VALID_JSONS)
        for file in all_files:
            assert isinstance(file, list)
            for row in file:
                assert isinstance(row, str)

    def test_yield_newlines_not_stripped(self):
        all_files = files.get_content(_VALID_PATH, _VALID_JSON, False)
        for file in all_files:
            for row in file:
                assert row.endswith('\n')

    def test_yield_newlines_stripped(self):
        all_files = files.get_content(_VALID_PATH, _VALID_JSON, True)
        for file in all_files:
            for row in file:
                assert not row.endswith('\n')


class TestGetJson:

    def test_raise_filenotfounderror_invalid_filename(self):
        with pytest.raises(FileNotFoundError):
            files.get_json(_VALID_PATH, _INVALID_FILENAME)

    def test_raise_filenotfounderror_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            files.get_json(_INVALID_PATH, _VALID_JSON)

    def test_raise_no_errors_valid_path_valid_filename(self):
        files.get_json(_VALID_PATH, _VALID_JSON)

    def test_raise_typeerror_invalid_filename(self):
        with pytest.raises(TypeError):
            files.get_json(_VALID_PATH, list(_VALID_JSON))

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            files.get_json(list(_VALID_PATH), _VALID_JSON)

    def test_return_object(self):
        json_object = files.get_json(_VALID_PATH, _VALID_JSON)
        assert isinstance(json_object, object)

    def test_return_correct_object(self):
        json_object = files.get_json(_VALID_PATH, _VALID_JSON)
        assert json_object == _JSON_OBJECT


class TestParseCtab:

    ctab_valid = files.get_content(_VALID_PATH, _VALID_CTAB)

    # TODO def test_raise_mol_error_REASON(self):

    def test_correct_counts_line(self):
        counts_line = files.parse_ctab_counts_line_(self.ctab_valid[0])
        assert counts_line == {
            'n_atoms': 3, 'n_bonds': 2, 'n_atoms_lists': 0, '': None,
            'is_chiral': False,
            'n_stext': 0, 'n_rxn_components': 0, 'n_reactants': 0,
            'n_products': 0, 'n_intermediates': 0, 'n_properties': 999,
            'version': 'V2000',
            }

    def test_correct_atom_block(self):
        atom_block = files.parse_ctab_atom_block_(self.ctab_valid[1:4])
        assert atom_block == [
            '   -0.4125    0.7145    0.0000 H   0  0  0  0  0  0  0  0  0  0  0  0',
            '    0.0000    0.0000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0',
            '   -0.4125   -0.7145    0.0000 H   0  0  0  0  0  0  0  0  0  0  0  0',
            ]

    def test_correct_bond_block(self):
        bond_block = files.parse_ctab_bond_block_(self.ctab_valid[4:6])
        assert bond_block == [
            '  2  1  1  0  0  0  0',
            '  2  3  1  0  0  0  0',
            ]

    def test_correct_atoms_lists(self):
        atoms_lists = files.parse_ctab_atoms_lists_([])
        assert atoms_lists == {}

    def test_correct_stext(self):
        stext = files.parse_ctab_stext_([])
        assert stext == {}

    def test_correct_properties(self):
        properties = files.parse_ctab_properties_(self.ctab_valid[6])
        assert properties == {}

    def test_correct_ctab(self):
        ctab = files.parse_ctab(self.ctab_valid)
        assert ctab == (
            files.parse_ctab_counts_line_(self.ctab_valid[0]),
            files.parse_ctab_atom_block_(self.ctab_valid[1:4]),
            files.parse_ctab_bond_block_(self.ctab_valid[4:6]),
            files.parse_ctab_atoms_lists_([]),
            files.parse_ctab_stext_([]),
            files.parse_ctab_properties_(self.ctab_valid[6]),
            )


class TestParseMol:

    mol_valid = files.get_content(_VALID_PATH, _VALID_MOL)

    # TODO def test_raise_mol_error_REASON(self):

    def test_correct_header(self):
        header, __ = files.parse_mol(self.mol_valid)
        assert header == {'name': 'CHEBI:15377', 'meta': '', 'comment': ''}

    def test_correct_ctab(self):
        __, ctab = files.parse_mol(self.mol_valid)
        assert ctab == files.parse_ctab(self.mol_valid[4:])


class TestParseRd:

    rd_valid = files.get_content(_VALID_PATH, _VALID_RD)

    # TODO def test_raise_rd_error_REASON(self):

    def test_correct_record_data(self):
        rd = files.parse_rd(self.rd_valid)
        assert rd.records[0].data == {
            'masterId': '10748',
            'status': 'approved',
            'qualifiers': set(['MA', 'FO', 'CB']),
            'equation': 'H(+) + hydrogencarbonate => CO2 + H2O',
            }

    def test_correct_record_identifier(self):
        rd = files.parse_rd(self.rd_valid)
        assert rd.records[0].identifier == 'RIREG:10749'

    def test_correct_record_rxn(self):
        rd = files.parse_rd(self.rd_valid)
        assert rd.records[0].rxn == files.parse_rxn(self.rd_valid[3:])

    def test_correct_time(self):
        rd = files.parse_rd(self.rd_valid)
        assert rd.time == '10/22/2016 18:17'

    def test_correct_version(self):
        rd = files.parse_rd(self.rd_valid)
        assert rd.version == '1'


class TestParseRxn:

    rxn_valid = files.get_content(_VALID_PATH, _VALID_RXN)

    # TODO def test_raise_rxn_error_REASON(self):

    def test_correct_header(self):
        header, *__ = files.parse_rxn(self.rxn_valid)
        assert header == {'name': 'Rhea  rhea-util102220161817  10749',
                          'comment': 'RHEA:release=77'}

    def test_correct_reactants_products(self):
        __, n_reactants_products, __ = files.parse_rxn(self.rxn_valid)
        assert n_reactants_products == (2, 2)

    def test_correct_mols(self):
        *__, mols = files.parse_rxn(self.rxn_valid)
        assert mols == [
            files.parse_mol(self.rxn_valid[5:13]),
            files.parse_mol(self.rxn_valid[13:27]),
            files.parse_mol(self.rxn_valid[27:38]),
            files.parse_mol(self.rxn_valid[38:49]),
            ]


class TestParseTsv:

    tsv_valid = [
        'FIELD_1\tFIELD_2\tFIELD_3\n',
        '1-1\t1-2\t1-3\n',
        '2-1\t2-2\t2-3\n',
        ]
    tsv_invalid_data = [
        'FIELD_1\tFIELD_2\tFIELD_3\n',
        '1-1\t1-2\t1-3\n',
        '2-1\t2-2  2-3\n',
        ]

    def test_raise_tsv_error_invalid_data(self):
        with pytest.raises(files.TsvError):
            list(files.parse_tsv(self.tsv_invalid_data))

    def test_raise_tsv_error_invalid_data_header_1_2_3(self):
        with pytest.raises(files.TsvError):
            list(files.parse_tsv(self.tsv_invalid_data, ['H1', 'H2', 'H3']))

    def test_yield_correct_fields(self):
        fields = list(files.parse_tsv(self.tsv_valid))
        correct_fields = [
            {'FIELD_1': '1-1', 'FIELD_2': '1-2', 'FIELD_3': '1-3'},
            {'FIELD_1': '2-1', 'FIELD_2': '2-2', 'FIELD_3': '2-3'},
            ]
        assert fields == correct_fields

    def test_yield_correct_fields_header_1_2_3(self):
        fields = list(files.parse_tsv(self.tsv_valid, ['H1', 'H2', 'H3']))
        correct_fields = [
            {'H1': 'FIELD_1', 'H2': 'FIELD_2', 'H3': 'FIELD_3'},
            {'H1': '1-1', 'H2': '1-2', 'H3': '1-3'},
            {'H1': '2-1', 'H2': '2-2', 'H3': '2-3'},
            ]
        assert fields == correct_fields


class TestWriteJson:

    filename = 'write_test.json'

    def test_output_file_exists(self):
        files.write_json(_JSON_OBJECT, _VALID_PATH, self.filename)
        output = files.get_json(_VALID_PATH, self.filename)
        assert isinstance(output, type(_JSON_OBJECT))

    def test_raise_typeerror_invalid_filename(self):
        with pytest.raises(TypeError):
            files.write_json(_JSON_OBJECT, _VALID_PATH, list(self.filename))

    def test_raise_no_errors_valid_path_valid_filename(self):
        files.write_json(_JSON_OBJECT, _VALID_PATH, self.filename)

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            files.write_json(_JSON_OBJECT, list(_VALID_PATH), self.filename)

    def test_return_none(self):
        output = files.write_json(_JSON_OBJECT, _VALID_PATH, self.filename)
        assert isinstance(output, type(None))


class TestWriteJsons:

    filenames = ['write_test_1.json', 'write_test_2.json']
    data = [_JSON_OBJECT, _JSON_OBJECT]

    def test_output_files_exist(self):
        files.write_jsons(self.data, _VALID_PATH, self.filenames)
        for file, test_object in zip(self.filenames, self.data):
            output = files.get_json(_VALID_PATH, file)
            assert isinstance(output, type(test_object))

    def test_raise_no_errors_valid_data_path_filenames(self):
        files.write_jsons(self.data, _VALID_PATH, self.filenames)

    def test_raise_typeerror_invalid_data_type(self):
        with pytest.raises(TypeError):
            files.write_jsons(str(self.data), _VALID_PATH, self.filenames)

    def test_raise_typeerror_invalid_filenames_type(self):
        with pytest.raises(TypeError):
            files.write_jsons(self.data, _VALID_PATH, str(self.filenames))

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            files.write_jsons(self.data, list(_VALID_PATH), self.filenames)

    def test_return_none(self):
        output = files.write_jsons(self.data, _VALID_PATH, self.filenames)
        assert isinstance(output, type(None))
