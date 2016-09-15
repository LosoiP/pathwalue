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

var RHEA_CHEBIS = {
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
var CHEBI_RHEAS = {
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
var RHEA_ECS = {
    '1': ['1', '2'],
    '2': ['1', '3'],
    '3': ['1', '4'],
    '4': ['2', '3'],
    '5': ['2', '4'],
    '6': ['3', '4'],
};
var EC_RHEAS = {
    '1': ['1', '2', '3'],
    '2': ['1', '4', '5'],
    '3': ['2', '4', '6'],
    '4': ['3', '5', '6'],
};
var DATA = {
    'stoichiometrics': RHEA_CHEBIS,
    'complexities': COMPLEXITIES,
    'compound_reactions': CHEBI_RHEAS,
    'demands': DEMANDS,
    'prices': PRICES,
    'compounds': COMPOUNDS,
    'enzymes': ENZYMES,
    'equations': EQUATIONS,
    'reaction_ecs': RHEA_ECS,
    'ec_reactions': EC_RHEAS,
};



// ------------------------------
// Test data initialize functions
// ------------------------------

function createInputForm() {
    var form = document.createElement('FORM');
    var attrOption = {value:10, text:'10', selected:true};
    var option = createHTMLElement(document, 'OPTION', attrOption);
    var nResults = createHTMLElement(document, 'SELECT');
    var compounds = createMultiselect(document, 'c');
    var enzymes = createMultiselect(document, 'e');
    var filterLinks = createMultiselect(document, 'fl');
    nResults.appendChild(option);
    form.appendChild(nResults);
    form.appendChild(compounds);
    form.appendChild(enzymes);
    form.appendChild(filterLinks);
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


function createPathways() {
    return [
        ['1'], ['1', '4'], ['1', '4', '5'],
        ['4'], ['4', '5'], ['4', '5', '1'],
        ['5'], ['5', '1'], ['5', '1', '4'],
    ];
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


QUnit.module('testEvaluateInput');
QUnit.test('testValidateInputFields', function(assert) {
    var cEmptyEEmptyInvalid = validateInputCE([], []);
    var cEmptyEValid = validateInputCE([], ['1', '2']);
    var cValidEEmpty = validateInputCE(['1', '2'], []);
    var cValidEValid = validateInputCE(['1', '2'], ['1', '2']);
    var nInvalid0 = validateInputN(0);
    var nInvalid21 = validateInputN(21);
    var nValid10 = validateInputN(10);
    assert.strictEqual(nInvalid0, false, 'false, n = 0');
    assert.strictEqual(nInvalid21, false, 'false, n = 21');
    assert.strictEqual(nValid10, true, 'true, n = 10');
    assert.strictEqual(cEmptyEEmptyInvalid, false, 'false, empty C empty E');
    assert.strictEqual(cEmptyEValid, true, 'true, empty C');
    assert.strictEqual(cValidEEmpty, true, 'true, empty E');
    assert.strictEqual(cValidEValid, true, 'true, valid C and E');
});
QUnit.test('testReturnCorrectAmountResults', function(assert) {
    var G = initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS);
    var results1 = evaluateInput(G, 1, ['1', 'any'], [], [], DATA);
    var results2 = evaluateInput(G, 2, ['1', 'any'], [], [], DATA);
    assert.strictEqual(results1.length, 1, 'return 1 result');
    assert.strictEqual(results2.length, 2, 'return 2 results');
});
QUnit.test('testReturnCorrectOrdering', function(assert) {
    var G = initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS);
    var results = _.unzip(evaluateInput(G, 100, ['1', 'any'], [], [], DATA))[0];
    assert.ok(results[0] >= results[1] >= results[2] >= results[3], 'correct ordering');
});
QUnit.test('testReturnCorrectCompoundResults', function(assert) {
    var G = initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS);
    var resultsC1Any = evaluateInput(G, 100, ['1', 'any'], [], [], DATA);
    var resultsCAny1 = evaluateInput(G, 100, ['any', '1'], [], [], DATA);
    var resultsC13 = evaluateInput(G, 100, ['1', '3'], [], [], DATA);
    var resultsC135 = evaluateInput(G, 100, ['1', '3', '5'], [], [], DATA);
    var C1Any = [['1'], ['1', '4'], ['2'], ['2', '6']];
    var CAny1 = [['3'], ['4', '5'], ['5'], ['6', '3']];
    var C13 = [['1'], ['2', '6']];
    var C135 = [['1', '4']];
    assert.deepEqual(_.unzip(resultsC1Any)[1].sort(), C1Any, 'C1Any');
    assert.deepEqual(_.unzip(resultsCAny1)[1].sort(), CAny1, 'CAny1');
    assert.deepEqual(_.unzip(resultsC13)[1].sort(), C13, 'C13');
    assert.deepEqual(_.unzip(resultsC135)[1].sort(), C135, 'C135');
});
QUnit.test('testReturnCorrectEnzymeResults', function(assert) {
    var G = initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS);
    var resultsE1 = evaluateInput(G, 100, [], ['1'], [], DATA);
    var resultsE12 = evaluateInput(G, 100, [], ['1', '2'], [], DATA);
    var resultsE123 = evaluateInput(G, 100, [], ['1', '2', '3'], [], DATA);
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
    assert.deepEqual(_.unzip(resultsE1)[1].sort(), E1, 'E1');
    assert.deepEqual(_.unzip(resultsE12)[1].sort(), E12, 'E12');
    assert.deepEqual(_.unzip(resultsE123)[1].sort(), E123, 'E123');
});
QUnit.test('testReturnCorrectCombinationResults', function(assert) {
    var G = initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS);
    var resultsC1AnyE1 = evaluateInput(G, 100, ['1', 'any'], ['1'], [], DATA);
    var resultsCAny1E1 = evaluateInput(G, 100, ['any', '1'], ['1'], [], DATA);
    var resultsC13E12 = evaluateInput(G, 100, ['1', '3'], ['1', '2'], [], DATA);
    var resultsC135E123 = evaluateInput(G, 100, ['1', '3', '5'], ['1', '2', '3'], [], DATA);
    var resultsC5E12 = evaluateInput(G, 100, ['5'], ['1', '2'], [], DATA);
    var C1AnyE1 = [['1'], ['1', '4'], ['2'], ['2', '6']];
    var CAny1E1 = [['3'], ['6', '3']];
    var C13E12 = [['1']];
    var C135E123 = [['1', '4']];
    var C5E12 = [
        ['1', '4'], ['1', '4', '5'], ['4', '5', '1'],
        ['5', '1'], ['5', '1', '4'],];
    assert.deepEqual(_.unzip(resultsC1AnyE1)[1].sort(), C1AnyE1, 'C1any E1');
    assert.deepEqual(_.unzip(resultsCAny1E1)[1].sort(), CAny1E1, 'Cany1 E1');
    assert.deepEqual(_.unzip(resultsC13E12)[1].sort(), C13E12, 'C13 E12');
    assert.deepEqual(_.unzip(resultsC135E123)[1].sort(), C135E123, 'C135 E123');
    assert.deepEqual(_.unzip(resultsC5E12)[1].sort(), C5E12, 'C5 E12');
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
    var pws = filterPathways(createPathways(), ['1', '3', '5'], ['1', '2', '3', '4'],
        '1', '3', [], DATA);
    assert.deepEqual(pws, [], 'filter all pathways');
});
QUnit.test('testFilterCompounds', function(assert) {
    var pws1 = filterPathways(createPathways(), ['1'], [], '', '', [], DATA);
    var pws13 = filterPathways(createPathways(), ['1', '3'], [], '', '', [], DATA);
    var pws135 = filterPathways(createPathways(), ['1', '3', '5'], [], '', '', [], DATA);
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
    var pws1 = filterPathways(createPathways(), [], ['1'], '', '', [], DATA);
    var pws13 = filterPathways(createPathways(), [], ['1', '3'], '', '', [], DATA);
    var pws135 = filterPathways(createPathways(), [], ['1', '3', '4'], '', '', [], DATA);
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
    var pws3 = filterPathways(createPathways(), [], [], '3', '', [], DATA);
    var pws5 = filterPathways(createPathways(), [], [], '5', '', [], DATA);
    var filtered3 = [['4'], ['4', '5'], ['5']];
    var filtered5 = [['1'], ['5'], ['5', '1']];
    assert.deepEqual(pws3, filtered3, 'filter correct source 3');
    assert.deepEqual(pws5, filtered5, 'filter correct source 5');
});
QUnit.test('testTargets', function(assert) {
    var pws3 = filterPathways(createPathways(), [], [], '', '3', [], DATA);
    var pws5 = filterPathways(createPathways(), [], [], '', '5', [], DATA);
    var filtered3 = [['1'], ['5'], ['5', '1']];
    var filtered5 = [['1'], ['1', '4'], ['4']];
    assert.deepEqual(pws3, filtered3, 'filter correct target 3');
    assert.deepEqual(pws5, filtered5, 'filter correct target 5');
});
QUnit.test('testNoFilters', function(assert) {
    var pws = filterPathways(createPathways(), [], [], '', '', [], DATA);
    var pws132 = filterPathways([['1', '3', '2']], [], [], '', '', [], DATA);
    var pws513 = filterPathways([['5', '1', '3']], [], [], '', '', [], DATA);
    var pws5132 = filterPathways([['5', '1', '3', '2']], [], [], '', '', [], DATA);
    var pws6135 = filterPathways([['6', '1', '3', '5']], [], [], '', '', [], DATA);
    assert.deepEqual(pws, createPathways(), "don't filter pathways");
    assert.deepEqual(pws132, [], 'filter cycle 1, 3, 2');
    assert.deepEqual(pws513, [], 'filter cycle 5, 1, 3');
    assert.deepEqual(pws5132, [], 'filter cycle 5, 1, 3, 2');
    assert.deepEqual(pws6135, [['6', '1', '3', '5']], "don't filter 6, 1, 3, 5");
});
QUnit.test('testPairedFilters', function(assert) {
    var pwsC1E3 = filterPathways(createPathways(), ['1'], ['3'], '', '', [], DATA);
    var pwsC13S5 = filterPathways(createPathways(), ['1', '3'], [], '5', '', [], DATA);
    var pwsC13T3 = filterPathways(createPathways(), ['1', '3'], [], '', '3', [], DATA);
    var pwsE1S5 = filterPathways(createPathways(), [], ['1'], '5', '', [], DATA);
    var pwsE1T5 = filterPathways(createPathways(), [], ['1'], '', '5', [], DATA);
    var pwsS3T5 = filterPathways(createPathways(), [], [], '3', '5', [], DATA);
    var pwsC13E1S1T3 = filterPathways(createPathways(), ['1', '3'], ['1'], '1', '3', [], DATA);
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
    var G = initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS)
    assert.notOk(findPathway(G, 'source', null), 'source to null, return undefined');
    assert.notOk(findPathway(G, null, 'target'), 'return undefined');
    assert.notOk(findPathway(G, '1', '6'), 'return undefined');
    assert.notOk(findPathway(G, null, null), 'return undefined');
});
QUnit.test('testFindCorrectPathways', function(assert) {
    var G = initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS)
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
QUnit.test('testCorrectResults', function(assert) {
    var compoundElement = formatCompound(document, '1', DATA);
    var text = compoundElement.innerHTML;
    var correct = 'ChEBI:1 a';
    assert.deepEqual(text, correct, "return element with innerHTML 'ChEBI:1 a'");
});


QUnit.module('testFormatList');
QUnit.test('testCorrectCompoundResults', function(assert) {
    var listElement = formatList(document, 'OL', 'title', ['1', '2'], formatCompound, DATA);
    var html = listElement.innerHTML;
    var correct = 'title<ol><li>ChEBI:1 a</li><li>ChEBI:2 b</li></ol>';
    assert.ok(_.includes(html, 'title'), "include 'title'");
    assert.ok(_.includes(html, '<ol>'), "include '<ol>'");
    assert.ok(_.includes(html, '</ol>'), "include '</ol>'");
    assert.ok(_.includes(html, '<li>'), "include '<li>'");
    assert.ok(_.includes(html, '</li>'), "include '</li>'");
    assert.ok(_.includes(html, 'ChEBI:1 a'), "include 'ChEBI:1 a'");
    assert.ok(_.includes(html, 'ChEBI:2 b'), "include 'ChEBI:2 b'");
    assert.deepEqual(html, correct, 'return element with correct innerHTLM');
});


QUnit.module('testFormatPathway');
QUnit.test('testCorrectCompoundResults', function(assert) {
    var listElement = formatPathway(document, [1, ['1', '4']], DATA);
    var html = listElement.innerHTML;
    // var correct = 'title<ol><li>ChEBI:1 a</li><li>ChEBI:2 b</li></ol>';
    assert.ok(_.includes(html, 'Total reaction:'), "include 'Total reaction:'");
    assert.ok(_.includes(html, '<b>'), "include '<b>'");
    assert.ok(_.includes(html, '</b>'), "include '</b>'");
    assert.ok(_.includes(html, _.escape('a + b => e + f')), 'include total reaction');
    assert.ok(_.includes(html, '<li>'), "include '<li>'");
    assert.ok(_.includes(html, '</li>'), "include '</li>'");
    assert.ok(_.includes(html, 'Score: 1'), "include 'Score: 1'");
    assert.ok(_.includes(html, '<ul>'), "include '<ul>'");
    assert.ok(_.includes(html, '</ul>'), "include '</ul>'");
    assert.ok(_.includes(html, '<ol>'), "include '<ol>'");
    assert.ok(_.includes(html, '</ol>'), "include '</ol>'");
    assert.ok(_.includes(html, '<br>'), "include '<br>'");
    assert.ok(_.includes(html, 'Substrates:'), "include 'Substrates:'");
    assert.ok(_.includes(html, 'Intermediates:'), "include 'Intermediates:'");
    assert.ok(_.includes(html, 'Products:'), "include 'Products:'");
    assert.ok(_.includes(html, 'Reaction steps:'), "include 'Reaction steps:'");
    // assert.deepEqual(html, correct, 'return element with correct innerHTLM');
});

QUnit.module('testFormatOutput');
QUnit.test('testReturnInvalidParameterMessage', function(assert) {
    var listElement = formatOutput(document, undefined, DATA);
    var html = listElement.innerHTML;
    var correct = 'Invalid search parameters. Please enter either at least 2 compounds or at least 1 enzyme.';
    assert.deepEqual(html, correct, 'return element with correct innerHTLM');
});
QUnit.test('testReturnNoPathways', function(assert) {
    var listElement = formatOutput(document, [], DATA);
    var html = listElement.innerHTML;
    var correct = 'No pathways were found.';
    assert.deepEqual(html, correct, 'return element with correct innerHTLM');
});
QUnit.test('testReturnOutput', function(assert) {
    var listElement = formatOutput(document, [[1, ['1', '4']], [2, ['2', '6']]], DATA);
    var html = listElement.innerHTML;
    assert.ok(_.includes(html, 'Total reaction:'), "include 'Total reaction:'");
    assert.ok(_.includes(html, '<b>'), "include '<b>'");
    assert.ok(_.includes(html, '</b>'), "include '</b>'");
    assert.ok(_.includes(html, _.escape('a + b => e + f')), 'include total reaction');
    assert.ok(_.includes(html, _.escape('a + b => c + d')), 'include total reaction');
    assert.ok(_.includes(html, '<li>'), "include '<li>'");
    assert.ok(_.includes(html, '</li>'), "include '</li>'");
    assert.ok(_.includes(html, 'Score: 1'), "include 'Score: 1'");
    assert.ok(_.includes(html, 'Score: 2'), "include 'Score: 2'");
    assert.ok(_.includes(html, '<ul>'), "include '<ul>'");
    assert.ok(_.includes(html, '</ul>'), "include '</ul>'");
    assert.ok(_.includes(html, '<ol>'), "include '<ol>'");
    assert.ok(_.includes(html, '</ol>'), "include '</ol>'");
    assert.ok(_.includes(html, '<br>'), "include '<br>'");
    assert.ok(_.includes(html, 'Substrates:'), "include 'Substrates:'");
    assert.ok(_.includes(html, 'Intermediates:'), "include 'Intermediates:'");
    assert.ok(_.includes(html, 'Products:'), "include 'Products:'");
    assert.ok(_.includes(html, 'Reaction steps:'), "include 'Reaction steps:'");
});


QUnit.module('testFormatReaction');
QUnit.test('testReturnCorrectResults', function(assert) {
    var listElement = formatReaction(document, '1', DATA);
    var html = listElement.innerHTML;
    assert.ok(_.includes(html, '<dl>'), "include '<dl>'");
    assert.ok(_.includes(html, '</dl>'), "include '</dl>'");
    assert.ok(_.includes(html, '<dt>'), "include '<dt>'");
    assert.ok(_.includes(html, '</dt>'), "include '</dt>'");
    assert.ok(_.includes(html, '<dd>'), "include '<dd>'");
    assert.ok(_.includes(html, '</dd>'), "include '</dd>'");
    assert.ok(_.includes(html, '<b>'), "include '<b>'");
    assert.ok(_.includes(html, '</b>'), "include '</b>'");
    assert.ok(_.includes(html, 'Rhea:1'), "include 'Rhea:1'");
    assert.ok(_.includes(html, 'EC:1 aase'), "include 'EC:1 aase'");
    assert.ok(_.includes(html, 'EC:2 base'), "include 'EC:2 base'");
    assert.ok(_.includes(html, 'Substrate ChEBI:1 a'), "include 'Substrate ChEBI:1 a'");
    assert.ok(_.includes(html, 'Substrate ChEBI:2 b'), "include 'Substrate ChEBI:2 b'");
    assert.ok(_.includes(html, 'Product ChEBI:3 c'), "include 'Product ChEBI:3 c'");
    assert.ok(_.includes(html, 'Product ChEBI:4 d'), "include 'Product ChEBI:4 d'");
});


QUnit.module('testGetInputValues');
QUnit.test('testGetCorrectValues', function(assert) {
    var form = createInputForm();
    var values = getInputValues(form);
    var correct = {
        nResults: 10,
        compounds: ['c1', 'c2'],
        enzymes: ['e1', 'e2'],
        filterLinks: ['fl1', 'fl2']
    };
    assert.deepEqual(values, correct, 'return correct values: n10, Cc1c2 Ee1e2, FLfl1fl2');
});


QUnit.module('testGetMultiselectValues');
QUnit.test('testGetCorrectValues', function(assert) {
    var multiselect = createMultiselect(document, 'e');
    var values = getMultiselectValues(multiselect);
    var correct = ['e1', 'e2'];
    assert.deepEqual(values, correct, "return ['e1', 'e2']");
});



QUnit.module('testInitializeGraph');
QUnit.test('testCorrectOutputs', function(assert) {
    var G = initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS);
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
    var G1 = initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS, I1);
    var G2 = initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS, I2);
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


QUnit.module('testOrderPathwayData');
QUnit.test('testReturnCorrectData', function(assert) {
    var pathways = [['1', '2', '3'], ['4', '5', '6']];
    var output = orderPathwayData(
        pathways, RHEA_CHEBIS, COMPLEXITIES, DEMANDS, PRICES);
    var steps = [
        [
            [1, ['1', '2'], ['3', '4']],
            [2, ['1', '2'], ['5', '6']],
            [3, ['3', '4'], ['1', '2']]
        ],
        [
            [4, ['3', '4'], ['5', '6']],
            [5, ['5', '6'], ['1', '2']],
            [6, ['5', '6'], ['3', '4']]
        ],
    ];
    var compounds = [
        {
            '1': [1, 6], '2': [2, 5], '3': [3, 4],
            '4': [4, 3], '5': [5, 2], '6': [6, 1],
        },
        {
            '1': [1, 6], '2': [2, 5], '3': [3, 4],
            '4': [4, 3], '5': [5, 2], '6': [6, 1],
        },
    ];
    assert.deepEqual(output[0], steps, 'correct step data');
    assert.deepEqual(output[1], compounds, 'correct compound data');
});
