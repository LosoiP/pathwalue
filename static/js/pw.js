/**
 * @fileOverview JavaScript for PathWalue-application.
 *
 * @author Pauli Losoi
 *
 * @requires jQuery
 * @requires Select2
 */


/**
 * Submit and evaluate input and return output.
 */
function submitSearch() {
    return null
};


/**
 * Return values from a form of input and 2 select fields.
 * @param {HTMLElement} form the HTML form element.
 *
 * @returns {object} selected values of form. Keys: 'compounds',
   'enzymes' and 'nResults'.
 */
function getInputValues(form) {
    var nodes = form.childNodes
    var nodeNResults = nodes[0];
    var nodeCompounds = nodes[1];
    var nodeEnzymes = nodes[2];
    var nResults = nodeNResults.value;
    var compounds = getMultiSelectValues(nodeCompounds);
    var enzymes = getMultiSelectValues(nodeEnzymes);
    var result = {
        'compounds': compounds,
        'enzymes': enzymes,
        'nResults': nResults,
        };
    return result
};


/**
 * Return all selected values of a select element.
 * @param {HTMLElement} select the HTML select element.
 *
 * @returns {array} selected values of the select element.
 */
function getMultiSelectValues(select) {
    var result = [];
    var options = select && select.options;
    var option;
    var i = 0;
    var iLen = options.length;
    for (i, iLen; i < iLen; i++) {
        option = options[i];
        if (option.selected) {
            result.push(option.value);
        }
    }
    return result;
}


/**
 * Return a boolean of the validity of two fields.
 * @param {array} compounds array of chosen compounds.
 * @param {array} enzymes array of chosen enzymes.
 *
 * @returns {boolean} false if both compounds and enzymes are empty
    arrays. Returns true otherwise.
 */
function validateInputCE(compounds, enzymes) {
    var isValid;
    var lenCompounds = compounds.length;
    var lenEnzymes = enzymes.length;
    if (lenCompounds + lenEnzymes === 0) {
        isValid = false;
    } else {
        isValid = true;
    }
    return isValid
};


/**
 * Return a boolean of the validity of the numeric field.
 * @param {number} n the number in the field.
 *
 * @returns {boolean} true if 1 < n < 20. Returns false otherwise.
 */
function validateInputN(n) {
    var isValid;
    if (isNaN(n) || n < 1 || n > 20) {
        isValid = false;
    } else {
        isValid = true;
    }
    return isValid
};

