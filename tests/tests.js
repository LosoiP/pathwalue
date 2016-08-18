/**
 * @fileOverview QUnit tests for PathWalue-application.
 *
 * @author Pauli Losoi
 *
 * @requires jQuery
 * @requires Select2
 * @requires QUnit
 */



// -------------------
// Test data constants
// -------------------

var STOICHIOMETRICS = {
    '1': [{'1': 1, '2': 1}, {'3': 1, '4': 1}],
    '2': [{'1': 2, '2': 2}, {'5': 2, '6': 2}],
    '3': [{'3': 1, '4': 1}, {'1': 1, '2': 1}],
    '4': [{'3': 3, '4': 3}, {'5': 3, '6': 3}],
    '5': [{'5': 2, '6': 2}, {'1': 2, '2': 2}],
    '6': [{'5': 3, '6': 3}, {'3': 3, '4': 3}],
};
var COMPLEXITIES = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
};
var COMPOUND_REACTIONS = {
    '1': [['1', '2'], ['3', '5']],
    '2': [['1', '2'], ['3', '5']],
    '3': [['3', '4'], ['1', '6']],
    '4': [['3', '4'], ['1', '6']],
    '5': [['5', '6'], ['2', '4']],
    '6': [['5', '6'], ['2', '4']],
};
var DEMANDS = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
};
var PRICES = {
    '1': 6,
    '2': 5,
    '3': 4,
    '4': 3,
    '5': 2,
    '6': 1,
};
var COMPOUNDS = {
    '1': 'a',
    '2': 'b',
    '3': 'c',
    '4': 'd',
    '5': 'e',
    '6': 'f',
};
var ENZYMES = {
    '1': 'aase',
    '2': 'base',
    '3': 'case',
    '4': 'dase',
};
var EQUATIONS = {
    '1': 'eq1',
    '2': 'eq2',
    '3': 'eq3',
    '4': 'eq4',
    '5': 'eq5',
    '6': 'eq6',
};
var REACTION_ECS = {
    '1': ['1', '2'],
    '2': ['1', '3'],
    '3': ['1', '4'],
    '4': ['2', '3'],
    '5': ['2', '4'],
    '6': ['3', '4'],
};
var EC_REACTIONS = {
    '1': ['1', '2', '3'],
    '2': ['1', '4', '5'],
    '3': ['2', '4', '6'],
    '4': ['3', '5', '6'],
};
var CONTEXT = {
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
};



// ------------------------------
// Test data initialize functions
// ------------------------------

function createInputForm() {
    var form = document.createElement('FORM');
    var nResults = document.createElement('INPUT');
    var compounds = createMultiselect(document, 'c');
    var enzymes = createMultiselect(document, 'e');
    nResults.type = 'number';
    nResults.value = '10';
    form.appendChild(nResults);
    form.appendChild(compounds);
    form.appendChild(enzymes);
    return form
}


function createMultiselect(documentObject, elementName) {
    var multiselect = documentObject.createElement('SELECT');
    var option1 = documentObject.createElement('OPTION');
    var option2 = documentObject.createElement('OPTION');
    multiselect.multiple = 'multiple';
    option1.value = elementName + '1';
    option2.value = elementName + '2';
    option1.selected = true;
    option2.selected = true;
    multiselect.appendChild(option1);
    multiselect.appendChild(option2);
    return multiselect
}



// --------------------------
// Test modules and functions
// --------------------------

QUnit.module('TestDetermineIntermediates');


QUnit.module('TestEvaluateInput');
QUnit.test('TestValidateInputFields', function(assert) {
    var cEmptyEEmptyInvalid = validateInputCE([], []);
    var cEmptyEValid = validateInputCE([], ['1', '2']);
    var cValidEEmpty = validateInputCE(['1', '2'], []);
    var cValidEValid = validateInputCE(['1', '2'], ['1', '2']);
    var nInvalid0 = validateInputN(0);
    var nInvalid21 = validateInputN(21);
    var nValid10 = validateInputN(10);
    assert.strictEqual(nInvalid0, false, 'false for invalid input');
    assert.strictEqual(nInvalid21, false), 'false for invalid input';
    assert.strictEqual(nValid10, true, 'true for valid input');
    assert.strictEqual(cEmptyEEmptyInvalid, false, 'false for invalid input');
    assert.strictEqual(cEmptyEValid, true, 'true for valid input');
    assert.strictEqual(cValidEEmpty, true, 'true for valid input');
    assert.strictEqual(cValidEValid, true, 'true for valid input');
});


QUnit.module('TestEvaluatePathway');


QUnit.module('TestFilterPathway');


QUnit.module('TestFindPathway');


QUnit.module('TestFormatCompound');


QUnit.module('TestFormatPathway');


QUnit.module('TestFormatOutput');


QUnit.module('TestFormatReaction');


QUnit.module('TestGetInputValues');
QUnit.test('TestGetCorrectValues', function(assert) {
    var form = createInputForm();
    var values = getInputValues(form);
    var correct = {
        'nResults': '10',
        'compounds': ['c1', 'c2'],
        'enzymes': ['e1', 'e2'],
    };
    assert.deepEqual(values, correct, 'return correct values');
});


QUnit.module('TestGetMultiselectValues');


QUnit.module('TestInitializeGraph');


QUnit.module('TestIntersectDict');


QUnit.module('TestNBestItems');


QUnit.module('TestOrderPathwayData');
