'use strict';
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
var PATHWAYS = [
    ['1'], ['1', '4'], ['1', '4', '5'],
    ['4'], ['4', '5'], ['4', '5', '1'],
    ['5'], ['5', '1'], ['5', '1', '4'],
];



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

QUnit.module('testCreateHTMLElement');
QUnit.test('testPElement', function(assert) {
    var attributes = {
        text: 'text',
    };
    var element = createHTMLElement(document, 'P', attributes);
    assert.strictEqual(element.tagName, 'P', 'correct tagName: P')
    assert.strictEqual(element.text, 'text', 'correct text: text');
});
QUnit.test('testOptionElement', function(assert) {
    var attributes = {
        selected: true,
        value: 'value',
    };
    var element = createHTMLElement(document, 'OPTION', attributes);
    assert.strictEqual(element.tagName, 'OPTION', 'correct tagName: OPTION');
    assert.strictEqual(element.selected, true, 'correct selected: true');
    assert.strictEqual(element.value, 'value', 'correct value: value');
});



QUnit.module('testDetermineIntermediates');


QUnit.module('testEvaluateInput');
QUnit.test('testValidateInputFields', function(assert) {
    var cEmptyEEmptyInvalid = validateInputCE([], []);
    var cEmptyEValid = validateInputCE([], ['1', '2']);
    var cValidEEmpty = validateInputCE(['1', '2'], []);
    var cValidEValid = validateInputCE(['1', '2'], ['1', '2']);
    var nInvalid0 = validateInputN(0);
    var nInvalid21 = validateInputN(21);
    var nValid10 = validateInputN(10);
    assert.strictEqual(nInvalid0, false, 'false for invalid input n = 0');
    assert.strictEqual(nInvalid21, false, 'false for invalid input n = 21');
    assert.strictEqual(nValid10, true, 'true for valid input n = 10');
    assert.strictEqual(cEmptyEEmptyInvalid, false, 'false for invalid input empty C empty E');
    assert.strictEqual(cEmptyEValid, true, 'true for valid input empty C');
    assert.strictEqual(cValidEEmpty, true, 'true for valid input empty E');
    assert.strictEqual(cValidEValid, true, 'true for valid input C and E');
});
QUnit.test('testReturnCorrectAmountResults', function(assert) {
    var GRAPH = initializeGraph(STOICHIOMETRICS, COMPOUND_REACTIONS);
    var results1 = evaluateInput(GRAPH, 1, ['1', '3'], [], CONTEXT);
    var results2 = evaluateInput(GRAPH, 2, ['1', '3'], [], CONTEXT);
    assert.strictEqual(results1.length, 1, 'return 1 result');
    assert.strictEqual(results2.length, 2, 'return 2 results');
});
QUnit.test('testReturnCorrectCompoundResults', function(assert) {
    var GRAPH = initializeGraph(STOICHIOMETRICS, COMPOUND_REACTIONS);
    var resultsC1Any = evaluateInput(GRAPH, 100, ['1', 'any'], [], CONTEXT);
    var resultsCAny1 = evaluateInput(GRAPH, 100, ['any', '1'], [], CONTEXT);
    var resultsC13 = evaluateInput(GRAPH, 100, ['1', '3'], [], CONTEXT);
    var resultsC135 = evaluateInput(GRAPH, 100, ['1', '3', '5'], [], CONTEXT);
    var C1Any = [['1'], ['1', '4'], ['2'], ['2', '6']];
    var CAny1 = [['3'], ['4', '5'], ['5'], ['6', '3']];
    var C13 = [['1'], ['2', '6']];
    var C135 = [['1', '4']];
    assert.deepEqual(resultsC1Any[1], C1Any, 'C1Any');
    assert.deepEqual(resultsCAny1[1], CAny1, 'CAny1');
    assert.deepEqual(resultsC13[1], C13, 'C13');
    assert.deepEqual(resultsC135[1], C135, 'C135');
});
QUnit.test('testReturnCorrectEnzymeResults', function(assert) {
    var GRAPH = initializeGraph(STOICHIOMETRICS, COMPOUND_REACTIONS);
    var resultsE1 = evaluateInput(GRAPH, 100, [], ['1'], CONTEXT);
    var resultsE12 = evaluateInput(GRAPH, 100, [], ['1', '2'], CONTEXT);
    var resultsE123 = evaluateInput(GRAPH, 100, [], ['1', '2', '3'], CONTEXT);
    var E1 = [
        ['1'], ['1', '4'], ['1', '4', '5'],
        ['2'], ['2', '6'], ['2', '6', '3'],
        ['3'], ['3', '2'], ['3', '2', '6'],
        ['4', '5', '1'],
        ['5', '1'],
        ['6', '3'], ['6', '3', '2'],
    ];
    var E12 = [
        ['1', ], ['1', '4'], ['1', '4', '5'],
        ['4', '5', '1'],
        ['5', '1'], ['5', '1', '4'],
    ];
    var E123 = [
        ['1', '4'], ['1', '4', '5'],
        ['4', '5', '1'],
        ['5', '1', '4'],
    ];
    assert.deepEqual(resultsE1[1], E1, 'E1');
    assert.deepEqual(resultsE12[1], E12, 'E12');
    assert.deepEqual(resultsE123[1], E123, 'E123');
});
QUnit.test('testReturnCorrectCombinationResults', function(assert) {
    var GRAPH = initializeGraph(STOICHIOMETRICS, COMPOUND_REACTIONS);
    var resultsC1AnyE1 = evaluateInput(GRAPH, 100, ['1', 'any'], ['1'], CONTEXT);
    var resultsCAny1E1 = evaluateInput(GRAPH, 100, ['any', '1'], ['1'], CONTEXT);
    var resultsC13E12 = evaluateInput(GRAPH, 100, ['1', '3'], ['1', '2'], CONTEXT);
    var resultsC135E123 = evaluateInput(GRAPH, 100, ['1', '3', '5'], ['1', '2', '3'], CONTEXT);
    var C1AnyE1 = [['1'], ['1', '4'], ['2'], ['2', '6']];
    var CAny1E1 = [['3'], ['6', '3']];
    var C13E12 = [['1']];
    var C135E123 = [['1', '4']];
    assert.deepEqual(resultsC1AnyE1[1], C1AnyE1, 'C1any E1');
    assert.deepEqual(resultsCAny1E1[1], CAny1E1, 'Cany1 E1');
    assert.deepEqual(resultsC13E12[1], C13E12, 'C13 E12');
    assert.deepEqual(resultsC135E123[1], C135E123, 'C135 E123');
});


QUnit.module('testEvaluatePathway');
QUnit.test('testCorrectResults', function(assert) {
    var steps1 = [[6, ['5', '6'], ['3', '4']]];
    var steps2 = [
        [2, ['1', '2'], ['5', '6']],
        [6, ['5', '6'], ['3', '4']],
    ];
    var steps3 = [
        [4, ['3', '4'], ['5', '6']],
        [6, ['5', '6'], ['3', '4']],
        [3, ['3', '4'], ['1', '2']],
    ];
    var compounds = {
        '1': [1, 6], '2': [2, 5], '3': [3, 4],
        '4': [4, 3], '5': [5, 2], '6': [1, 6],
    };
    var value1 = evaluatePathway(steps1, compounds);
    var value2 = evaluatePathway(steps2, compounds);
    var value3 = evaluatePathway(steps3, compounds);
    assert.strictEqual(value1, 56, 'steps 1 -> 56');
    assert.strictEqual(value2, 36, 'steps 2 -> 36');
    assert.strictEqual(value3, Math.ceil(16*14/3), 'steps 3 -> ceil(16*14/3)');
});


QUnit.module('testFilterPathway');
QUnit.test('testFilterAll', function(assert) {
    var pws = filterPathways(PATHWAYS, ['1', '3', '5'], ['1', '2', '3', '4'],
        '1', '3', CONTEXT);
    assert.deepEqual(pws, [], 'filter all pathways');
});
QUnit.test('testFilterCompounds', function(assert) {
    var pws1 = filterPathways(PATHWAYS, ['1'], [], '', '', CONTEXT);
    var pws13 = filterPathways(PATHWAYS, ['1', '3'], [], '', '', CONTEXT);
    var pws135 = filterPathways(PATHWAYS, ['1', '3', '5'], [], '', '', CONTEXT);
    var filtered1 = [
        ['1'], ['1', '4'], ['1', '4', '5'],
        ['4', '5'], ['4', '5', '1'],
        ['5'], ['5', '1'], ['5', '1', '4'],
    ];
    var filtered13 = [
        ['1'], ['1', '4'], ['1', '4', '5'],
        ['4', '5'], ['4', '5', '1'],
        ['5', '1'], ['5', '1', '4'],
    ];
    var filtered135 = [
        ['1', '4'], ['1', '4', '5'],
        ['4', '5'], ['4', '5', '1'],
        ['5', '1'], ['5', '1', '4'],
    ];
    assert.deepEqual(pws1, filtered1, 'filter correct compounds 1');
    assert.deepEqual(pws13, filtered13, 'filter correct compounds 1 and 3');
    assert.deepEqual(pws135, filtered135, 'filter correct compounds 1, 3 and 5');
});
QUnit.test('testFilterEnzymes', function(assert) {
    var pws1 = filterPathways(PATHWAYS, [], ['1'], '', '', CONTEXT);
    var pws13 = filterPathways(PATHWAYS, [], ['1', '3'], '', '', CONTEXT);
    var pws135 = filterPathways(PATHWAYS, [], ['1', '3', '4'], '', '', CONTEXT);
    var filtered1 = [
        ['1'], ['1', '4'], ['1', '4', '5'],
        ['4', '5', '1'],
        ['5', '1'], ['5', '1', '4'],
    ];
    var filtered13 = [
        ['1', '4'], ['1', '4', '5'],
        ['4', '5', '1'],
        ['5', '1', '4'],
    ];
    var filtered135 = [['1', '4', '5'], ['4', '5', '1'], ['5', '1', '4']];
    assert.deepEqual(pws1, filtered1, 'filter correct enzymes 1');
    assert.deepEqual(pws13, filtered13, 'filter correct enzymes 1 and 3');
    assert.deepEqual(pws135, filtered135, 'filter correct enzymes 1, 3 and 5');
});
QUnit.test('testSources', function(assert) {
    var pws3 = filterPathways(PATHWAYS, [], [], '3', '', CONTEXT);
    var pws5 = filterPathways(PATHWAYS, [], [], '5', '', CONTEXT);
    var filtered3 = [['4'], ['4', '5'], ['5']];
    var filtered5 = [['1'], ['5'], ['5', '1']];
    assert.deepEqual(pws3, filtered3, 'filter correct source 3');
    assert.deepEqual(pws5, filtered5, 'filter correct source 5');
});
QUnit.test('testTargets', function(assert) {
    var pws3 = filterPathways(PATHWAYS, [], [], '', '3', CONTEXT);
    var pws5 = filterPathways(PATHWAYS, [], [], '', '5', CONTEXT);
    var filtered3 = [['1'], ['5'], ['5', '1']];
    var filtered5 = [['1'], ['1', '4'], ['4']];
    assert.deepEqual(pws3, filtered3, 'filter correct target 3');
    assert.deepEqual(pws5, filtered5, 'filter correct target 5');
});
QUnit.test('testNoFilters', function(assert) {
    var pws = filterPathways(PATHWAYS, [], [], '', '', CONTEXT);
    var pws132 = filterPathways([['1', '3', '2']], [], [], '', '', CONTEXT);
    var pws513 = filterPathways([['5', '1', '3']], [], [], '', '', CONTEXT);
    var pws5132 = filterPathways([['5', '1', '3', '2']], [], [], '', '', CONTEXT);
    var pws6135 = filterPathways([['6', '1', '3', '5']], [], [], '', '', CONTEXT);
    assert.deepEqual(pws, PATHWAYS, "don't filter pathways");
    assert.deepEqual(pws132, [], 'filter cycle 1, 3, 2');
    assert.deepEqual(pws513, [], 'filter cycle 5, 1, 3');
    assert.deepEqual(pws5132, [], 'filter cycle 5, 1, 3, 2');
    assert.deepEqual(pws6135, [['6', '1', '3', '5']], "don't filter 6, 1, 3, 5");
});
QUnit.test('testPairedFilters', function(assert) {
    var pwsC1E3 = filterPathways(PATHWAYS, ['1'], ['3'], '', '', CONTEXT);
    var pwsC13S5 = filterPathways(PATHWAYS, ['1', '3'], [], '5', '', CONTEXT);
    var pwsC13T3 = filterPathways(PATHWAYS, ['1', '3'], [], '', '3', CONTEXT);
    var pwsE1S5 = filterPathways(PATHWAYS, [], ['1'], '5', '', CONTEXT);
    var pwsE1T5 = filterPathways(PATHWAYS, [], ['1'], '', '5', CONTEXT);
    var pwsS3T5 = filterPathways(PATHWAYS, [], [], '3', '5', CONTEXT);
    var pwsC13E1S1T3 = filterPathways(PATHWAYS, ['1', '3'], ['1'], '1', '3', CONTEXT);
    var filteredC1E3 = [
        ['1', '4'], ['1', '4', '5'],
        ['4', '5'], ['4', '5', '1'],
        ['5', '1', '4'],
        ];
    var filteredC13S5 = [['1'], ['5', '1']];
    var filteredC13T3 = [['1'], ['5', '1']];
    var filteredE1S5 = [['1'], ['5', '1']];
    var filteredE1T5 = [['1'], ['1', '4']];
    var filteredS3T5 = [['4']];
    var filteredC13E1S1T3 = [['1']];
    assert.deepEqual(pwsC1E3, filteredC1E3, 'filter correct C1 E3');
    assert.deepEqual(pwsC13S5, filteredC13S5, 'filter correct C13 S5');
    assert.deepEqual(pwsC13T3, filteredC13T3, 'filter correct C13 T3');
    assert.deepEqual(pwsE1S5, filteredE1S5, 'filter correct E1 S5');
    assert.deepEqual(pwsE1T5, filteredE1T5, 'filter correct E1 T5');
    assert.deepEqual(pwsS3T5, filteredS3T5, 'filter correct S3 T5');
    assert.deepEqual(pwsC13E1S1T3, filteredC13E1S1T3, 'filter correct C13 E1 S1 T3');
});


QUnit.module('testFindPathway');
QUnit.test('testCatchErrors', function(assert) {
    var G = initializeGraph(STOICHIOMETRICS, COMPOUND_REACTIONS)
    assert.notOk(findPathway(G, 'source', null), 'return undefined')
    assert.notOk(findPathway(G, null, 'target'), 'return undefined')
    assert.notOk(findPathway(G, '1', '6'), 'return undefined')
});
QUnit.test('testFindCorrectPathways', function(assert) {
    var G = initializeGraph(STOICHIOMETRICS, COMPOUND_REACTIONS)
    var source1Target5 = [['1', '4', '5']];
    var source1TargetNull = [['1'], ['1', '4'], ['1', '4', '5']];
    var source5Target1 = [['5', '1']];
    var sourceNullTarget5 = [['1', '4', '5'], ['4', '5'], ['5']];
    var pws1To5 = findPathway(G, '1', '5');
    var pws1ToNull = findPathway(G, '1', null);
    var pws5To1 = findPathway(G, '5', '1');
    var pwsNullTo5 = findPathway(G, null, '5');
    assert.deepEqual(pws1To5, source1Target5, 'correct pathways S1T5');
    assert.deepEqual(pws1ToNull, source1TargetNull, 'correct pathways S1Tnull');
    assert.deepEqual(pws5To1, source5Target1, 'correct pathways S5T1');
    assert.deepEqual(pwsNullTo5, sourceNullTarget5, 'correct pathways SnullT5');
});


QUnit.module('testFormatCompound');


QUnit.module('testFormatPathway');


QUnit.module('testFormatOutput');


QUnit.module('testFormatReaction');


QUnit.module('testGetInputValues');
QUnit.test('testGetCorrectValues', function(assert) {
    var form = createInputForm();
    var values = getInputValues(form);
    var correct = {
        nResults: '10',
        compounds: ['c1', 'c2'],
        enzymes: ['e1', 'e2'],
    };
    assert.deepEqual(values, correct, 'return correct values: n10, Cc1c2 Ee1e2');
});


QUnit.module('testGetMultiselectValues');


QUnit.module('testInitializeGraph');
QUnit.test('testCorrectOutputs', function(assert) {
    var G = initializeGraph(STOICHIOMETRICS, COMPOUND_REACTIONS);
    var correctNodes = ['1', '2', '3', '4', '5', '6'];
    var correctEdges = [
        ['1', '4'], ['2', '6'], ['3', '2'],
        ['4', '5'], ['5', '1'], ['6', '3']
    ];
    assert.deepEqual(G.nodes(), correctNodes, 'correct nodes');
    assert.deepEqual(G.edges(), correctEdges, 'correct edges');
});
QUnit.test('testCorrectIgnores', function(assert) {
    var I1 = ['1', '3', '6'];
    var I2 = ['1', '2'];
    var G1 = initializeGraph(STOICHIOMETRICS, COMPOUND_REACTIONS, I1);
    var G2 = initializeGraph(STOICHIOMETRICS, COMPOUND_REACTIONS, I2);
    var correctNodes1 = ['1', '2', '3', '4', '5', '6'];
    var correctNodes2 = ['1', '2', '3', '4', '5', '6'];
    var correctEdges1 = [
        ['1', '4'], ['2', '6'], ['3', '2'],
        ['4', '5'], ['5', '1'], ['6', '3']
    ];
    var correctEdges2 = [['1', '4'], ['2', '6'], ['4', '5'], ['6', '3']];
    assert.deepEqual(G1.nodes(), correctNodes1, 'correct nodes I136');
    assert.deepEqual(G1.edges(), correctEdges1, 'correct edges I136');
    assert.deepEqual(G2.nodes(), correctNodes2, 'correct nodes I12');
    assert.deepEqual(G2.edges(), correctEdges2, 'correct edges I12');
});


QUnit.module('testIntersectDict');


QUnit.module('testNBestItems');


QUnit.module('testOrderPathwayData');
