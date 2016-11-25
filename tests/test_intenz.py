# -*- coding: utf-8 -*-
"""
pytest module for intenz.py unit tests.

"""

from context import intenz


SAMPLES = '''
ID   1.14.17.3
DE   Peptidylglycine monooxygenase.
AN   PAM.
AN   Peptidyl alpha-amidating enzyme.
AN   Peptidylglycine 2-hydroxylase.
AN   Peptidylglycine alpha-amidating monooxygenase.
CA   Peptidylglycine + ascorbate + O(2) = peptidyl(2-hydroxyglycine) +
CA   dehydroascorbate + H(2)O.
CF   Copper.
CC   -!- Peptidylglycines with a neutral amino acid residue in the penultimate
CC       position are the best substrates for the enzyme.
CC   -!- The product is unstable and dismutates to glyoxylate and the
CC       corresponding desglycine peptide amide, a reaction catalyzed by
CC       EC 4.3.2.5.
CC   -!- Involved in the final step of biosynthesis of alpha-melanotropin and
CC       related biologically active peptides.
PR   PROSITE; PDOC00080;
DR   P08478, AMD1_XENLA ;  P12890, AMD2_XENLA ;  P83388, AMDL_CAEEL ;
DR   P10731, AMD_BOVIN  ;  P19021, AMD_HUMAN  ;  P97467, AMD_MOUSE  ;
DR   P14925, AMD_RAT    ;  Q95XM2, PHM_CAEEL  ;  O01404, PHM_DROME  ;
//

ID   2.3.1.43
DE   Phosphatidylcholine--sterol O-acyltransferase
DE   test.
AN   LCAT.
AN   Lecithin--cholesterol acyltransferase.
AN   Phospholipid--cholesterol acyltransferase.
CA   Phosphatidylcholine + a sterol = 1-acylglycerophosphocholine +
CA   a sterol ester.
CC   -!- Palmitoyl, oleoyl, and linoleoyl can be transferred; a number of
CC       sterols, including cholesterol, can act as acceptors.
CC   -!- The bacterial enzyme also catalyzes the reactions of EC 3.1.1.4 and
CC       EC 3.1.1.5.
PR   PROSITE; PDOC00110;
DR   P10480, GCAT_AERHY ;  P53760, LCAT_CHICK ;  O35573, LCAT_ELIQU ;
DR   P04180, LCAT_HUMAN ;  O35724, LCAT_MICMN ;  P16301, LCAT_MOUSE ;
DR   O35502, LCAT_MYOGA ;  Q08758, LCAT_PAPAN ;  P30930, LCAT_PIG   ;
DR   P53761, LCAT_RABIT ;  P18424, LCAT_RAT   ;  O35840, LCAT_TATKG ;
//
'''.split('\n')


class TestGetEnzymes:

    def test_yield_correct_output(self):
        output = list(ie.get_enzymes([s + '\n' for s in SAMPLES]))
        correct = [
            {'ec': '1.14.17.3',
             'name': 'Peptidylglycine monooxygenase'
             },
            {'ec': '2.3.1.43',
             'name': 'Phosphatidylcholine--sterol O-acyltransferase test'
             },
            ]
        assert output == correct


class TestMergeDicts:

    samples = [
        {'key1': 'value11', 'key2': 'value12', 'key3': 'value13'},
        {'key1': 'value21', 'key2': 'value22', 'key3': 'value23'},
        {'key1': 'value31', 'key2': 'value32', 'key4': 'value34'},
        ]

    def test_return_empty_dict_for_empty_iterable(self):
        assert ie.merge_dicts([], 'key1', 'key2') == {}

    def test_return_empty_dict_for_invalid_key(self):
        assert ie.merge_dicts(self.samples, '', 'key1') == {}

    def test_return_empty_values_for_invalid_value_key(self):
        output = ie.merge_dicts(self.samples, 'key1', '')
        assert not any(value for value in output.values())

    def test_return_correct_key_value_pairs(self):
        output = ie.merge_dicts(self.samples, 'key1', 'key2')
        correct = {
            'value11': 'value12',
            'value21': 'value22',
            'value31': 'value32',
            }
        assert output == correct

    def test_return_correct_key_value_pairs_input_iter(self):
        output = ie.merge_dicts(iter(self.samples), 'key1', 'key2')
        correct = {
            'value11': 'value12',
            'value21': 'value22',
            'value31': 'value32',
            }
        assert output == correct

    def test_return_correct_key_none_pairs(self):
        output = ie.merge_dicts(self.samples, 'key1', 'key3')
        correct = {
            'value11': 'value13',
            'value21': 'value23',
            }
        assert output == correct
