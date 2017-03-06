'use strict';
// (C) 2017 Tampere University of Technology
// MIT License
// Pauli Losoi
/**
 * @file QUnit tests for PathWalue-application.
 *
 * @requires Lodash
 * @requires jQuery
 * @requires JSNetworkX
 * @requires Select2
 * @requires QUnit
 *
 * @requires pw.js
 */


// -------------------
// Test data constants
// -------------------

// Base triplets 1, 4, 5 and 2, 3, 6.
// 2 links to 7 and 7 to 3.
// 4 links to 7 and vice versa.
// 8 links to  9.
var RHEA_CHEBIS = {
    '1': [{'1': 1, '2': 1}, {'3': 1, '4': 1}],
    '2': [{'1': 2, '2': 2}, {'5': 2, '6': 2}],
    '3': [{'3': 1, '4': 1}, {'1': 1, '2': 1}],
    '4': [{'3': 3, '4': 3}, {'5': 3, '6': 3}],
    '5': [{'5': 2, '6': 2}, {'1': 2, '2': 2}],
    '6': [{'5': 3, '6': 3}, {'3': 3, '4': 3}],
    '7': [{'5': 4, '6': 4}, {'3': 4, '4': 4}],
    '8': [{'7': 4}, {'8': 4}],
    '9': [{'8': 4}, {'9': 4}],
};
var CHEBI_RHEAS = {
    '1': [['1', '2'], ['3', '5']],
    '2': [['1', '2'], ['3', '5']],
    '3': [['3', '4'], ['1', '6', '7']],
    '4': [['3', '4'], ['1', '6', '7']],
    '5': [['5', '6', '7'], ['2', '4']],
    '6': [['5', '6', '7'], ['2', '4']],
    '7': [['8'], []],
    '8': [['9'], ['8']],
    '9': [[], ['9']],
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

/**
 * @function createFilter
 * @summary Create a filter object for pw.filterPathways.
 *
 * @param {array} conditions - Name, condition -pairs.
 *
 * @returns {object} Filter object.
 */
function createFilter(conditions) {
    var filter = {compounds: [], enzymes: [], source: '', target: '',
                  links: []};
    _.forEach(conditions, function(condition) {
        filter[condition[0]] = condition[1];
    });
    return filter;
}


/**
 * @function createInputForm
 * @summary Creates a temporary HTML form.
 *
 * @returns {HTML form}
 */
function createInputForm() {
    var form = document.createElement('FORM');
    var attrOption = {value:10, text:'10', selected:true};
    var option = PW.createHTMLElement(document, 'OPTION', attrOption);
    var nResults = PW.createHTMLElement(document, 'SELECT');
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


/**
 * @function createMultiselect
 * @summary Creates a HTML multiselect element.
 *
 * @param {HTML document} documentObject - The document.
 * @param {string} elementName - Name of the element.
 *
 * @returns {HTML select}
 */
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


/**
 * @function createPathways
 * @summary Returns the set of test pathways.
 *
 * @returns {array} Arrays of test pathways.
 */
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
QUnit.test('testPElement', function (assert) {
    var attributes = {text: 'text'};

    var element = PW.createHTMLElement(document, 'P', attributes);

    assert.strictEqual(element.tagName, 'P', 'correct tagName: P')
    assert.strictEqual(element.text, 'text', 'correct text: text');
});
QUnit.test('testOptionElement', function (assert) {
    var attributes = {selected: true, value: 'value'};

    var element = PW.createHTMLElement(document, 'OPTION', attributes);

    assert.strictEqual(element.tagName, 'OPTION', 'correct tagName: OPTION');
    assert.strictEqual(element.selected, true, 'correct selected: true');
    assert.strictEqual(element.value, 'value', 'correct value: value');
});


// TODO add filter field to tests.
QUnit.module('testValidateInputFields');
QUnit.test('testValidateInputFields', function (assert) {
    var cEmptyEEmptyInvalid = PW.validateInputCE([], []);
    var cEmptyEValid = PW.validateInputCE([], ['1', '2']);
    var cValidEEmpty = PW.validateInputCE(['1', '2'], []);
    var cValidEValid = PW.validateInputCE(['1', '2'], ['1', '2']);
    var nInvalid0 = PW.validateInputN(0);
    var nInvalid21 = PW.validateInputN(21);
    var nValid10 = PW.validateInputN(10);

    assert.strictEqual(nInvalid0, false, 'false, n = 0');
    assert.strictEqual(nInvalid21, false, 'false, n = 21');
    assert.strictEqual(nValid10, true, 'true, n = 10');
    assert.strictEqual(cEmptyEEmptyInvalid, false, 'false, empty C empty E');
    assert.strictEqual(cEmptyEValid, true, 'true, empty C');
    assert.strictEqual(cValidEEmpty, true, 'true, empty E');
    assert.strictEqual(cValidEValid, true, 'true, valid C and E');
});
QUnit.module('testEvaluateInput');
QUnit.test('testReturnCorrectAmountResults', function (assert) {
    var G = PW.initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS);

    var results1 = PW.evaluateInput(G, 1, ['1', 'any'], [], [], DATA);
    var results2 = PW.evaluateInput(G, 2, ['1', 'any'], [], [], DATA);

    assert.strictEqual(results1.length, 1, 'n = 1, return 1 result');
    assert.strictEqual(results2.length, 2, 'n = 2, return 2 results');
});
QUnit.test('testReturnCorrectOrdering', function (assert) {
    var G = PW.initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS);

    var results = _.unzip(PW.evaluateInput(G, 90, ['1', 'any'], [], [], DATA))[0];

    assert.ok(results[0] >= results[1] >= results[2] >= results[3],
              'order results from highest score to lowest');
});
QUnit.test('testReturnCorrectCompoundResults', function (assert) {
    var G = PW.initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS);

    var resultsC1Any = PW.evaluateInput(G, 100, ['1', 'any'], [], [], DATA);
    var resultsCAny1 = PW.evaluateInput(G, 100, ['any', '1'], [], [], DATA);
    var resultsC13 = PW.evaluateInput(G, 100, ['1', '3'], [], [], DATA);
    var resultsC135 = PW.evaluateInput(G, 100, ['1', '3', '5'], [], [], DATA);

    var C1Any = [['1'], ['1', '4'], ['2'], ['2', '6'], ['2', '7']];
    var CAny1 = [['3'], ['4', '5'], ['5'], ['6', '3'], ['7', '3']];
    var C13 = [['1'], ['2', '6'], ['2', '7']];
    var C135 = [['1', '4']];
    assert.deepEqual(_.unzip(resultsC1Any)[1].sort(), C1Any,
                     'Compounds: 1, any');
    assert.deepEqual(_.unzip(resultsCAny1)[1].sort(), CAny1,
                     'Compounds: any, 1');
    assert.deepEqual(_.unzip(resultsC13)[1].sort(), C13, 'Compounds: 1, 3');
    assert.deepEqual(_.unzip(resultsC135)[1].sort(), C135,
                     'Compounds: 1, 3, 5');
});
QUnit.test('testReturnCorrectEnzymeResults', function (assert) {
    var G = PW.initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS);

    var resultsE1 = PW.evaluateInput(G, 100, [], ['1'], [], DATA);
    var resultsE12 = PW.evaluateInput(G, 100, [], ['1', '2'], [], DATA);
    var resultsE123 = PW.evaluateInput(G, 100, [], ['1', '2', '3'], [], DATA);

    var E1 = [
        ['1'], ['1', '4'], ['1', '4', '5'],
        ['2'], ['2', '6'], ['2', '6', '3'], ['2', '7'],
        ['3'], ['3', '2'], ['3', '2', '6'], ['3', '2', '7'],
        ['4', '5', '1'],
        ['5', '1'],
        ['6', '3'], ['6', '3', '2'],
        ['7', '3'], ['7', '3', '2'],
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
    assert.deepEqual(_.unzip(resultsE1)[1].sort(), E1, 'Enzymes: 1');
    assert.deepEqual(_.unzip(resultsE12)[1].sort(), E12, 'Enzymes: 1, 2');
    assert.deepEqual(_.unzip(resultsE123)[1].sort(), E123, 'Enzymes: 1, 2, 3');
});
QUnit.test('testReturnCorrectCombinationResults', function (assert) {
    var G = PW.initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS);

    var resultsC1AnyE1 = PW.evaluateInput(G, 100, ['1', 'any'], ['1'], [], DATA);
    var resultsCAny1E1 = PW.evaluateInput(G, 100, ['any', '1'], ['1'], [], DATA);
    var resultsC13E12 = PW.evaluateInput(G, 100, ['1', '3'], ['1', '2'], [],
                                      DATA);
    var resultsC135E123 = PW.evaluateInput(G, 100, ['1', '3', '5'],
                                        ['1', '2', '3'], [], DATA);
    var resultsC5E12 = PW.evaluateInput(G, 100, ['5'], ['1', '2'], [], DATA);

    var C1AnyE1 = [['1'], ['1', '4'], ['2'], ['2', '6'], ['2', '7']];
    var CAny1E1 = [['3'], ['6', '3'], ['7', '3']];
    var C13E12 = [['1']];
    var C135E123 = [['1', '4']];
    var C5E12 = [
        ['1', '4'], ['1', '4', '5'], ['4', '5', '1'],
        ['5', '1'], ['5', '1', '4'],
    ];
    assert.deepEqual(_.unzip(resultsC1AnyE1)[1].sort(), C1AnyE1,
                     'Compounds: 1, any; Enzymes: 1');
    assert.deepEqual(_.unzip(resultsCAny1E1)[1].sort(), CAny1E1,
                     'Compounds: any, 1; Enzymes: 1');
    assert.deepEqual(_.unzip(resultsC13E12)[1].sort(), C13E12,
                     'Compounds: 1, 3; Enzymes: 1, 2');
    assert.deepEqual(_.unzip(resultsC135E123)[1].sort(), C135E123,
                     'Compounds: 1, 3, 5; Enzymes: 1, 2, 3');
    assert.deepEqual(_.unzip(resultsC5E12)[1].sort(), C5E12,
                     'Compounds: 5; Enzymes: 1, 2');
});


QUnit.module('testEvaluatePathway');
QUnit.test('testCorrectResults', function (assert) {
    var pathway1 = ['6'];
    var pathway2 = ['2', '6'];
    var pathway3 = ['4', '6', '3'];

    var value1 = PW.evaluatePathway(pathway1, DATA);
    var value2 = PW.evaluatePathway(pathway2, DATA);
    var value3 = PW.evaluatePathway(pathway3, DATA);
    var evaluateFunction = function(s, p, r, n) {
        return Math.ceil(10*Math.sqrt(s)*(p-r)/Math.pow(n,2));
    };
    var correctValue1 = evaluateFunction(0, 24, 16, 1);
    var correctValue2 = evaluateFunction(1/3, 24, 16, 2);
    var correctValue3 = evaluateFunction(2/3, 16, 24, 3);

    assert.strictEqual(value1, correctValue1,
        'steps 1 -> ceil(10 * sqrt(0) * (25 - 3) / 1^2');
    assert.strictEqual(value2, correctValue2,
        'steps 2 -> ceil(10 * sqrt(1/3) * (25 - 61) / 2^2');
    assert.strictEqual(value3, correctValue3,
        'steps 3 -> ceil(10 * sqrt(2/3) * (61 - 25) / 3^2');
});


QUnit.module('testFilterPathway');
QUnit.test('testFilterAll', function (assert) {
    var filter = createFilter([
        ['compounds', ['1', '3', '5']],
        ['enzymes', ['1', '2', '3', '4']],
        ['source', '1'],
        ['target', '3']
    ]);

    var pws = PW.filterPathways(createPathways(), filter, DATA);

    assert.deepEqual(pws, [], 'filter all pathways');
});
QUnit.test('testFilterCompounds', function (assert) {
    var pws1 = PW.filterPathways(createPathways(),
            createFilter([['compounds', ['1']]]), DATA);
    var pws13 = PW.filterPathways(createPathways(),
            createFilter([['compounds', ['1', '3']]]), DATA);
    var pws135 = PW.filterPathways(createPathways(),
            createFilter([['compounds', ['1', '3', '5']]]), DATA);

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
    assert.deepEqual(pws1, filtered1, 'Compounds: 1');
    assert.deepEqual(pws13, filtered13, 'Compounds: 1, 3');
    assert.deepEqual(pws135, filtered135, 'Compounds: 1, 3; 5');
});
QUnit.test('testFilterEnzymes', function (assert) {
    var pws1 = PW.filterPathways(createPathways(),
            createFilter([['enzymes', ['1']]]), DATA);
    var pws13 = PW.filterPathways(createPathways(),
            createFilter([['enzymes', ['1', '3']]]), DATA);
    var pws134 = PW.filterPathways(createPathways(),
            createFilter([['enzymes', ['1', '3', '4']]]), DATA);

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
    var filtered134 = [['1', '4', '5'], ['4', '5', '1'], ['5', '1', '4']];
    assert.deepEqual(pws1, filtered1, 'Enzymes: 1');
    assert.deepEqual(pws13, filtered13, 'Enzymes: 1, 3');
    assert.deepEqual(pws134, filtered134, 'Enzymes: 1, 3, 4');
});
QUnit.test('testFilterLinks', function (assert) {
    var pws1 = PW.filterPathways(createPathways(),
            createFilter([['links', ['1']]]), DATA);
    var pws12 = PW.filterPathways(createPathways(),
            createFilter([['links', ['1', '2']]]), DATA);
    var pws13 = PW.filterPathways(createPathways(),
            createFilter([['links', ['1', '3']]]), DATA);
    var pws1234 = PW.filterPathways(createPathways(),
            createFilter([['links', ['1', '2', '3', '4']]]), DATA);
    var pws135 = PW.filterPathways(createPathways(),
            createFilter([['links', ['1', '3', '5']]]), DATA);
    var pws123456 = PW.filterPathways(createPathways(),
            createFilter([['links', ['1', '2', '3', '4', '5', '6']]]), DATA);

    var filtered1 = createPathways();
    var filtered12 = [
        ['1'], ['1', '4'], ['1', '4', '5'],
        ['4'], ['4', '5'],
        ['5'],
    ];
    var filtered13 = createPathways();
    var filtered1234 = [['1'], ['4'], ['4', '5'], ['5']];
    var filtered135 = createPathways();
    var filtered123456 = [['1'], ['4'], ['5']];
    assert.deepEqual(pws1, filtered1, 'Links: 1');
    assert.deepEqual(pws12, filtered12, 'Links: 1, 2');
    assert.deepEqual(pws13, filtered13, 'Links: 1, 3');
    assert.deepEqual(pws1234, filtered1234, 'Links: 1, 2, 3, 4');
    assert.deepEqual(pws135, filtered135, 'Links: 1, 3, 5');
    assert.deepEqual(pws123456, filtered123456, 'Links: 1, 2, 3, 4, 5, 6');
});
QUnit.test('testSources', function (assert) {
    var pws3 = PW.filterPathways(createPathways(),
            createFilter([['source', '3']]), DATA);
    var pws5 = PW.filterPathways(createPathways(),
            createFilter([['source', '5']]), DATA);

    var filtered3 = [['4'], ['4', '5'], ['5']];
    var filtered5 = [['1'], ['5'], ['5', '1']];
    assert.deepEqual(pws3, filtered3, 'Source: 3');
    assert.deepEqual(pws5, filtered5, 'Source: 5');
});
QUnit.test('testTargets', function (assert) {
    var pws3 = PW.filterPathways(createPathways(),
            createFilter([['target', '3']]), DATA);
    var pws5 = PW.filterPathways(createPathways(),
            createFilter([['target', '5']]), DATA);

    var filtered3 = [['1'], ['5'], ['5', '1']];
    var filtered5 = [['1'], ['1', '4'], ['4']];
    assert.deepEqual(pws3, filtered3, 'Target: 3');
    assert.deepEqual(pws5, filtered5, 'Target: 5');
});
QUnit.test('testNoFilters', function (assert) {
    var pws = PW.filterPathways(createPathways(), createFilter(), DATA);
    var pws132 = PW.filterPathways([['1', '3', '2']], createFilter(), DATA);
    var pws513 = PW.filterPathways([['5', '1', '3']], createFilter(), DATA);
    var pws5132 = PW.filterPathways([['5', '1', '3', '2']], createFilter(), DATA);
    var pws6327 = PW.filterPathways([['6', '3', '2', '7']], createFilter(), DATA);

    assert.deepEqual(pws, createPathways(), "don't filter pathways");
    assert.deepEqual(pws132, [], 'filter cycle 1, 3, 2');
    assert.deepEqual(pws513, [], 'filter cycle 5, 1, 3');
    assert.deepEqual(pws5132, [], 'filter cycle 5, 1, 3, 2');
    assert.deepEqual(pws6327, [['6', '3', '2', '7']],
                     "don't filter 6, 3, 2, 7");
});
QUnit.test('testPairedFilters', function (assert) {
    var pwsC1E3 = PW.filterPathways(createPathways(),
            createFilter([['compounds', ['1']], ['enzymes', ['3']]]), DATA);

    var pwsC1L12 = PW.filterPathways(createPathways(),
            createFilter([['compounds', ['1']], ['links', ['1', '2']]]), DATA);

    var pwsC13S5 = PW.filterPathways(createPathways(),
            createFilter([['compounds', ['1', '3']], ['source', '5']]), DATA);

    var pwsC13T3 = PW.filterPathways(createPathways(),
            createFilter([['compounds', ['1', '3']], ['target', '3']]), DATA);

    var pwsE1L12 = PW.filterPathways(createPathways(),
            createFilter([['enzymes', ['1']], ['links', ['1', '2']]]), DATA);

    var pwsE1S5 = PW.filterPathways(createPathways(),
            createFilter([['enzymes', ['1']], ['source', '5']]), DATA);

    var pwsE1T5 = PW.filterPathways(createPathways(),
            createFilter([['enzymes', ['1']], ['target', '5']]), DATA);

    var pwsS3L56 = PW.filterPathways(createPathways(),
            createFilter([['source', '3'], ['links', ['5', '6']]]), DATA);

    var pwsS3T5 = PW.filterPathways(createPathways(),
            createFilter([['source', '3'], ['target', '5']]), DATA);

    var pwsT5L34 = PW.filterPathways(createPathways(),
            createFilter([['target', '5'], ['links', ['3', '4']]]), DATA);

    var pwsC13E1S1T3L12 = PW.filterPathways(createPathways(),
            createFilter([['compounds', ['1', '3']], ['enzymes', ['1']],
                ['links', ['1', '2']], ['source', '1'], ['target', '3']]), DATA);

    var filteredC1E3 = [
        ['1', '4'], ['1', '4', '5'],
        ['4', '5'], ['4', '5', '1'],
        ['5', '1', '4'],
        ];
    var filteredC1L12 = [['1'], ['1', '4'], ['1', '4', '5'], ['4', '5'],
                         ['5']];
    var filteredC13S5 = [['1'], ['5', '1']];
    var filteredC13T3 = [['1'], ['5', '1']];
    var filteredE1L12 = [['1'], ['1', '4'], ['1', '4', '5']];
    var filteredE1S5 = [['1'], ['5', '1']];
    var filteredE1T5 = [['1'], ['1', '4']];
    var filteredS3L56 = [['4'], ['5']];
    var filteredS3T5 = [['4']];
    var filteredT5L34 = [['1'], ['4']];
    var filteredC13E1S1T3L12 = [['1']];
    assert.deepEqual(pwsC1E3, filteredC1E3, 'Compounds: 1; Enzymes: 3');
    assert.deepEqual(pwsC1L12, filteredC1L12, 'Compounds: 1; Links: 1, 2');
    assert.deepEqual(pwsC13S5, filteredC13S5, 'Compounds: 1, 3; Source: 5');
    assert.deepEqual(pwsC13T3, filteredC13T3, 'Compounds: 1, 3; Target: 3');
    assert.deepEqual(pwsE1L12, filteredE1L12, 'Enzymes: 1; Links: 1, 2');
    assert.deepEqual(pwsE1S5, filteredE1S5, 'Enzymes: 1; Source: 5');
    assert.deepEqual(pwsE1T5, filteredE1T5, 'Enzymes: 1; Target: 5');
    assert.deepEqual(pwsS3L56, filteredS3L56, 'Source: 3; Links: 5, 6');
    assert.deepEqual(pwsS3T5, filteredS3T5, 'Source: 3; Target: 5');
    assert.deepEqual(pwsT5L34, filteredT5L34, 'Target: 5; Links: 3, 4');
    assert.deepEqual(pwsC13E1S1T3L12, filteredC13E1S1T3L12,
        'Compounds: 1, 3; Enzymes: 1; Source: 1; Target: 3; Links: 1, 2');
});


QUnit.module('testFindPathway');
QUnit.test('testCatchErrors', function (assert) {
    var G = PW.initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS)

    assert.notOk(PW.findPathway(G, 'source', null), 'source to null, undefined');
    assert.notOk(PW.findPathway(G, null, 'target'), 'null to target, undefined');
    assert.notOk(PW.findPathway(G, '1', '8'), '1 to 8, undefined');
    assert.notOk(PW.findPathway(G, null, null), 'null to null, undefined');
});
QUnit.test('testFindCorrectPathways', function (assert) {
    var G = PW.initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS)

    var pws1To5 = PW.findPathway(G, '1', '5');
    var pws1ToNull = PW.findPathway(G, '1', null);
    var pws5To1 = PW.findPathway(G, '5', '1');
    var pwsNullTo5 = PW.findPathway(G, null, '5');

    var source1Target5 = [['1', '4', '5']];
    var source1TargetNull = [
        ['1'], ['1', '4'], ['1', '4', '5'], ['1', '4', '7'],
        ['1', '4', '7', '3'], ['1', '4', '7', '3', '2'],
        ['1', '4', '7', '3', '2', '6'],
    ];
    var source5Target1 = [['5', '1']];
    var sourceNullTarget5 = [
        ['1', '4', '5'], ['2', '7', '4', '5'], ['3', '2', '7', '4', '5'],
        ['4', '5'], ['5'], ['6', '3', '2', '7', '4', '5'], ['7', '4', '5'],
    ];
    assert.deepEqual(pws1To5.sort(), source1Target5, '1 to 5');
    assert.deepEqual(pws1ToNull.sort(), source1TargetNull, '1 to null');
    assert.deepEqual(pws5To1.sort(), source5Target1, '5 to 1');
    assert.deepEqual(pwsNullTo5.sort(), sourceNullTarget5, 'null to 5');
});


QUnit.module('testFormatCompound');
QUnit.test('testCorrectResults', function (assert) {
    var text = PW.formatCompound(document, '1', DATA).innerHTML;

    var correct = 'ChEBI:1 a, ';
    assert.ok(_.includes(text, correct), "element innerHTML has 'ChEBI:1 a'");
});


QUnit.module('testFormatIntermediates');
QUnit.test('testCorrectResults', function (assert) {
    var text = PW.formatIntermediates(document, '1', DATA).innerHTML;

    var correct = 'ChEBI:1 a';
    assert.deepEqual(text, correct, "element innerHTML 'ChEBI:1 a'");
});


QUnit.module('testFormatList');
QUnit.test('testCorrectIntermediatesResults', function (assert) {
    var html = PW.formatList(document, 'OL', 'title', ['1', '2'],
            PW.formatIntermediates, DATA).innerHTML;

    var correct = 'title<ol><li>ChEBI:1 a</li><li>ChEBI:2 b</li></ol>';
    assert.ok(_.includes(html, 'title'), "include 'title'");
    assert.ok(_.includes(html, '<ol>'), "include '<ol>'");
    assert.ok(_.includes(html, '</ol>'), "include '</ol>'");
    assert.ok(_.includes(html, '<li>'), "include '<li>'");
    assert.ok(_.includes(html, '</li>'), "include '</li>'");
    assert.ok(_.includes(html, 'ChEBI:1 a'), "include 'ChEBI:1 a'");
    assert.ok(_.includes(html, 'ChEBI:2 b'), "include 'ChEBI:2 b'");
    assert.deepEqual(html, correct, 'correct innerHTLM');
});


QUnit.module('testFormatPathway');
QUnit.test('testCorrectCompoundResults', function (assert) {
    var html = PW.formatPathway(document, [1, ['1', '4']], DATA).innerHTML;

    assert.ok(_.includes(html, 'Total reaction:'),
              "include 'Total reaction:'");
    assert.ok(_.includes(html, '<b>'), "include '<b>'");
    assert.ok(_.includes(html, '</b>'), "include '</b>'");
    assert.ok(_.includes(html, _.escape('a + b => e + f')),
              'include total reaction');
    assert.ok(_.includes(html, '<li>'), "include '<li>'");
    assert.ok(_.includes(html, '</li>'), "include '</li>'");
    assert.ok(_.includes(html, 'Score: 1, <small>('),
              "include 'Score: 1, <small>('");
    assert.ok(_.includes(html, '<ul>'), "include '<ul>'");
    assert.ok(_.includes(html, '</ul>'), "include '</ul>'");
    assert.ok(_.includes(html, '<ol>'), "include '<ol>'");
    assert.ok(_.includes(html, '</ol>'), "include '</ol>'");
    assert.ok(_.includes(html, '<br>'), "include '<br>'");
    assert.ok(_.includes(html, 'Substrates:'), "include 'Substrates:'");
    assert.ok(_.includes(html, 'Intermediates:'), "include 'Intermediates:'");
    assert.ok(_.includes(html, 'Products:'), "include 'Products:'");
    assert.ok(_.includes(html, 'Reaction steps:'),
              "include 'Reaction steps:'");
});


QUnit.module('testFormatOutput');
QUnit.test('testReturnInvalidParameterMessage', function (assert) {
    var html = PW.formatOutput(document, undefined, DATA).innerHTML;

    var correct = 'Invalid search parameters. Please enter either at least 2 '
        + 'compounds or at least 1 enzyme.';
    assert.deepEqual(html, correct, 'return element with correct innerHTLM');
});
QUnit.test('testReturnNoPathways', function (assert) {
    var html = PW.formatOutput(document, [], DATA).innerHTML;

    var correct = 'No pathways were found.';
    assert.deepEqual(html, correct, 'return element with correct innerHTLM');
});
QUnit.test('testReturnOutput', function (assert) {
    var html = PW.formatOutput(document, [[1, ['1', '4']], [2, ['2', '6']]],
            DATA).innerHTML;

    assert.ok(_.includes(html, 'Total reaction:'), "include 'Total reaction:'");
    assert.ok(_.includes(html, '<b>'), "include '<b>'");
    assert.ok(_.includes(html, '</b>'), "include '</b>'");
    assert.ok(_.includes(html, _.escape('a + b => e + f')),
              'include total reaction 1');
    assert.ok(_.includes(html, _.escape('a + b => c + d')),
              'include total reaction 2');
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
    assert.ok(_.includes(html, 'Reaction steps:'),
              "include 'Reaction steps:'");
});


QUnit.module('testFormatReaction');
QUnit.test('testReturnCorrectResults', function (assert) {
    var html = PW.formatReaction(document, '1', DATA).innerHTML;

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
    assert.ok(_.includes(html, 'Substrate ChEBI:1 a'),
              "include 'Substrate ChEBI:1 a'");
    assert.ok(_.includes(html, 'Substrate ChEBI:2 b'),
              "include 'Substrate ChEBI:2 b'");
    assert.ok(_.includes(html, 'Product ChEBI:3 c'),
              "include 'Product ChEBI:3 c'");
    assert.ok(_.includes(html, 'Product ChEBI:4 d'),
              "include 'Product ChEBI:4 d'");
});


QUnit.module('testGetInputValues');
QUnit.test('testGetCorrectValues', function (assert) {
    var form = createInputForm();
    var values = PW.getInputValues(form);

    var correct = {
        nResults: 10,
        compounds: ['c1', 'c2'],
        enzymes: ['e1', 'e2'],
        filterLinks: ['fl1', 'fl2']
    };
    assert.deepEqual(values, correct,
        'return correct values: n10, Cc1c2 Ee1e2, FLfl1fl2');
});


QUnit.module('testGetMultiselectValues');
QUnit.test('testGetCorrectValues', function (assert) {
    var multiselect = createMultiselect(document, 'e');
    var values = PW.getMultiselectValues(multiselect);

    var correct = ['e1', 'e2'];
    assert.deepEqual(values, correct, "return ['e1', 'e2']");
});



QUnit.module('testInitializeGraph');
QUnit.test('testCorrectOutputs', function (assert) {
    var G = PW.initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS);

    var correctNodes = ['1', '2', '3', '4', '5', '6', '7', '8', '9'];
    var correctEdges = [
        ['1', '4'], ['2', '6'], ['2', '7'], ['3', '2'], ['4', '5'],
        ['4', '7'], ['5', '1'], ['6', '3'], ['7', '3'], ['7', '4'], ['8', '9'],
    ];
    assert.deepEqual(G.nodes(), correctNodes, 'correct nodes');
    assert.deepEqual(G.edges(), correctEdges, 'correct edges');
});
QUnit.test('testCorrectIgnores', function (assert) {
    var I1 = ['1', '3', '6'];
    var I2 = ['1', '2'];

    var G1 = PW.initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS, I1);
    var G2 = PW.initializeGraph(RHEA_CHEBIS, CHEBI_RHEAS, I2);

    var correctNodes1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9'];
    var correctNodes2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9'];
    var correctEdges1 = [
        ['1', '4'], ['2', '6'], ['2', '7'], ['3', '2'], ['4', '5'], ['4', '7'],
        ['5', '1'], ['6', '3'], ['7', '3'], ['7', '4'], ['8', '9'],
    ];
    var correctEdges2 = [
        ['1', '4'], ['2', '6'], ['2', '7'], ['4', '5'], ['4', '7'],
        ['6', '3'], ['7', '3'], ['7', '4'], ['8', '9'],
    ];
    assert.deepEqual(G1.nodes(), correctNodes1, 'correct nodes I136');
    assert.deepEqual(G1.edges(), correctEdges1, 'correct edges I136');
    assert.deepEqual(G2.nodes(), correctNodes2, 'correct nodes I12');
    assert.deepEqual(G2.edges(), correctEdges2, 'correct edges I12');
});

