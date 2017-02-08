'use strict';
/**
 * @fileOverview JavaScript for PathWalue-application.
 *
 * @author Pauli Losoi
 *
 * @requires Lodash
 * @requires jQuery
 * @requires JSNetworkX
 * @requires Select2
 */

var PW = (function (PW, $, jsnx, _, select2) {


/**
 * Return a new HTML element with attributes.
 * @param {HTMLElement} documentObject the document.
 * @param {string} tagName the HTML element tag name.
 * @param {object} attributes the attributes to the HTML element.
 *
 * @returns {HTMLElement} HTML element.
 */
function createHTMLElement(documentObject, tagName, attributes) {
    var element = documentObject.createElement(tagName);
    _.forOwn(attributes, function (value, key) {
        element[key] = value;
    });
    return element;
}


/**
 * Search and return best scoring pathways.
 * @param {jsnx.DiGraph} G
 * @param {number} n
 * @param {array} C
 * @param {array} E
 * @param {object} context
 *
 * @returns {array}
 */
function evaluateInput(G, n, C, E, Fl, context) {
    var pathways = [];
    var ecReactions = context['ec_reactions'];
    var compoundReactions = context['compound_reactions'];
    var complexities = context['complexities'];
    var demands = context['demands'];
    var prices = context['prices'];
    var stoichiometrics = context['stoichiometrics'];
    var start = null;
    var goal = null;
    var sources = [null];
    var targets = [null];
    var pws;
    var filterPws;
    var pathway;
    var data;
    var values = [];
    var i;
    var iLen;
    var lenSources;
    var lenTargets;
    var maxSources;
    var maxTargets;
    var maxPw;
    var maxFilter;
    //var a = 1000;
    //var b = 1000;
    //var c = 5;
    var filter = {compounds: C, enzymes: E, source: '', target: '', links: Fl};
    // Determine search and filter parameters.
    if (C.length > 1) {
        start = C[0];
        goal = _.last(C);
        if (start === 'any') {
            C = C.slice(1);  // affects filter
            start = null;
            if (goal === 'any') {  // too wide to implement
                return [];
            } else {
                targets = compoundReactions[goal][1];
            }
        } else {
            sources = compoundReactions[start][0];
            if (goal === 'any') {
                C = C.slice(0, -1);  // affects filter
                goal = null;
            } else {
                targets = compoundReactions[goal][1];
            }
        }
        filter.source = start;
        filter.target = goal;
    } else {
        if (E.length > 1) {
            sources = [];
        }
        _.forEach(E, function(ec) {
            sources.push.apply(sources, ecReactions[ec]);
        });
        sources = _.uniqWith(sources, _.isEqual);
        targets = sources;
    }
    // Find pathways.
    // Constrain search to optimize performance.
    /*
    lenSources = sources.length;
    lenTargets = targets.length;
    maxSources = Math.ceil(Math.sqrt(a * lenSources / lenTargets));
    maxTargets = Math.ceil(Math.sqrt(a * lenTargets / lenSources));
    if (maxSources > 50) {
        maxSources = 50;
    }
    if (maxTargets > 50) {
        maxTargets > 50;
    }
    if (lenSources > maxSources) {
        lenSources = maxSources;
    }
    if (lenTargets > maxTargets) {
        lenTargets = maxTargets;
    }
    maxPw = Math.ceil(b / (lenSources * lenTargets));
    maxFilter = n + Math.ceil(maxPw / c);
    */
    // Store shortest path from each source to each target in pathways.
    /*
    _.forEach(sources.slice(0, maxSources), function (s, i) {
        _.forEach(targets.slice(0, maxTargets), function (t, j) {
            pws = _.take(findPathway(G, s, t), maxPw);
            filterPws = _.take(
                filterPathways(pws, filter, context), maxFilter);
            pathways.push.apply(pathways, filterPws);
        });
    });
    */
    _.forEach(sources, function (s) {
        _.forEach(targets, function (t) {
            pws = findPathway(G, s, t);
            filterPws = filterPathways(pws, filter, context);
            pathways.push.apply(pathways, filterPws);
        });
    });
    // Evaluate pathways.
    pathways = _.uniqWith(pathways, function (a, b) {
        if (a.length === b.length) {
            for (i = 0, iLen = a.length; i < iLen; i++) {
                if (a[i] !== b[i]) {
                    return false
                }
            }
            return true
        } else {
            return false;
        }
    });
    // Fetch data for evaluate function.
    data = orderPathwayData(
        pathways, stoichiometrics, complexities, demands, prices);
    _.forEach(_.zip(data[0], data[1]), function (SC) {
        values.push(evaluatePathway(SC[0], SC[1]));
    });
    return _.sortBy(_.zip(values, pathways), function (pw) {return - pw[0];}).slice(0, n);
}


/**
 * Return pathway value.
 * @param {array} steps
 * @param {object} compounds
 *
 * @returns {number}
 */
function evaluatePathway(steps, compounds) {
    var rxns = [];
    var pros = [];
    var subs = [];
    var substratesAll = [];
    var productsAll = [];
    var substrates = _.head(steps)[1];
    var products = _.last(steps)[2];
    var s = 1;
    var p = 1;
    var r = 1;
    var c = 1;
    var n = steps.length;
    _.forEach(steps, function(step) {
        rxns.push(step[0]);
        substratesAll.push.apply(substratesAll, step[1]);
        productsAll.push.apply(productsAll, step[2]);
    });
    _.forEach(substrates, function(s) {
        try {
            subs.push(compounds[s][0] * compounds[s][1]);
        }
        catch (error) {
            ;
        }
    });
    _.forEach(products, function(p) {
        try {
            pros.push(compounds[p][0] * compounds[p][1]);
        }
        catch (error) {
            ;
        }
    });
    // Evaluate similarity of all substrates and products.
    s = _.intersection(substratesAll, productsAll).length / _.union(substratesAll, productsAll).length;
    p = _.sum(pros);
    r = _.sum(subs);
    c = _.sum(rxns);
    return Math.ceil(10*Math.sqrt(s)*(p-r)/((c+1)*Math.pow(n,2)));
}


/**
 * Return pathways that meet filtering conditions.
 * @param {array} pathways pathway arrays.
 * @param {object} filter filter object.
 * @param {object} context context object.
 *
 * @returns {array} Approved pathways.
 */
function filterPathways(pathways, filter, context) {
    var rxnEcs = context.reaction_ecs;
    var S = context.stoichiometrics;
    var I = context.IGNORED_COMPOUNDS;
    var C = filter.compounds;
    var E = filter.enzymes;
    var s = filter.source;
    var t = filter.target;
    var Fl = filter.links;
    var compounds;
    var enzymes;
    var approved;
    var substrates;
    var products;
    var prepreC;
    var preC;
    var discard1;
    var discard2;
    var intersectProsSubs;
    var intersectFilterSubs;
    var intersectAll;
    return _.remove(pathways, function(pathway) {
        approved = true;
        compounds = ['any'];
        enzymes = [];
        _.forEach(pathway, function(reaction, i, pw) {
            substrates = _.keys(S[reaction][0]);
            products = _.keys(S[reaction][1]);
            // Check if target is consumed.
            if (_.includes(substrates, t)) {
                approved = false;
                return false;
            // Check if source is produced.
            } else if (_.includes(products, s)) {
                approved = false;
                return false;
            // Check for forbidden links.
            } else if (i >= 1) {
                preC = _.keys(S[pw[i - 1]][1]);  // products
                intersectProsSubs = _.intersection(preC, substrates);
                intersectFilterSubs = _.intersection(Fl, substrates);
                intersectAll = _.intersection(preC, intersectFilterSubs);
                if (intersectAll.length >= intersectProsSubs.length) {
                    approved = false;
                    return false;
                }
                // Check for repetitive consuming and producing.
                // Ignore ignored chebis though.
                if (i >= 2) {
                    prepreC = _.keys(S[pw[i - 2]][0]);  // substrates
                    discard1 = _.intersection(_.difference(prepreC, I), substrates);
                    discard2 = _.intersection(_.difference(preC, I), substrates);  // products
                    if (discard1.length !== 0 && discard2.length !== 0) {
                        approved = false;
                        return false;
                    }
                    prepreC = _.keys(S[pw[i - 2]][1]);  // products
                    preC = _.keys(S[pw[i - 1]][0]);  // substrates
                    discard1 = _.intersection(_.difference(prepreC, I), products);
                    discard2 = _.intersection(_.difference(preC, I), products);
                    if (discard1.length !== 0 && discard2.length !== 0) {
                        approved = false;
                        return false;
                    }
                }
            }
            compounds.push(substrates);
            compounds.push(products);
            enzymes.push(rxnEcs[reaction]);
            });
        if (!approved) {
            return false;
        }
        // Check for compounds and enzymes.
        if (_.intersection(C, _.flattenDeep(compounds)).length !== C.length) {
            return false;
        }
        enzymes = _.intersection(E, _.flattenDeep(enzymes));
        if (enzymes.length !== E.length) {
            return false;
        }
        return true;
    });
}


/**
 * Return pathways from source to target.
 * @param {object} G jsnx.DiGraph object
 * @param {string} source pathway source Rhea ID.
 * @param {string} target pathway target Rhea ID.
 *
 * @returns {array} Rhea ID arrays.
 */
function findPathway(G, source, target) {
    var pathway;
    var pathwaysAll;
    var optParameters = {};
    if (source !== null) {
        optParameters['source'] = source;
        if (target !== null) {  // source to target
            optParameters['target'] = target;
            try {
                pathway = [jsnx.shortestPath(G, optParameters)];
            }
            catch (error) {
                ;
            }
        } else {  // source to all targets
            try {
                pathwaysAll = jsnx.shortestPath(G, optParameters);
            }
            catch (error) {
                ;
            }
        }
    } else if (target !== null) {  // all sources to target
        optParameters['target'] = target;
        try {
            pathwaysAll = jsnx.shortestPath(G, optParameters);
        }
        catch (error) {
            ;
        }
    } 
    // all sources to all targets not implemented
    if (pathwaysAll !== undefined) {
        return _.values(pathwaysAll._stringValues);
    } else {
    return pathway;
    }
}


/**
 * Format a compound entry in results.
 */
function formatCompound(document, chebi, context) {
    var liMain = formatIntermediates(document, chebi, context);
    var price = context.prices[chebi];
    var demand = context.demands[chebi];
    var value = price * demand;
    liMain.innerHTML += ', <small>' + value.toString() + ' (' + price.toString() + ' &sdot; ' + demand.toString() + ')</small>';
    return liMain;
}


/**
 * Format a compound entry in results.
 */
function formatIntermediates(document, chebi, context) {
    var liMain = createHTMLElement(document, 'LI');
    liMain.innerHTML = 'ChEBI:' + chebi + ' ' + context.compounds[chebi];
    return liMain;
}


/**
 * Format a list tag.
 */
function formatList(document, listTag, title, container, f, context) {
    var liMain = createHTMLElement(document, 'LI');
    var list = createHTMLElement(document, listTag);
    liMain.innerHTML = title;
    _.forEach(container, function(c) {
        list.appendChild(f(document, c, context));
    });
    liMain.appendChild(list);
    return liMain;
}


/**
 * Format output for showing results.
 */
function formatOutput(document, results, context) {
    var ol = createHTMLElement(document, 'OL');
    if (results === undefined) {
        ol.innerHTML = 'Invalid search parameters. Please enter either at '
            + 'least 2 compounds or at least 1 enzyme.';
    } else if (results.length === 0) {
        ol.innerHTML = 'No pathways were found.';
    } else {
        _.forEach(results, function(pw) {
            ol.appendChild(formatPathway(document, pw, context));
        });
    }
    return ol;
}


/**
 * Format a pathway entry in results.
 */
function formatPathway(document, pathway, context) {
    var li;
    var ul;
    var ol;
    var liMain = createHTMLElement(document, 'LI');
    var ulMain = createHTMLElement(document, 'UL');
    var S = [];
    var I;
    var P = [];
    var namesS;
    var namesP;
    var totalReaction = 'totalReaction';
    var pwPoints = pathway[0];
    var substratePoints = 0;
    var productPoints = 0;
    var reactionPoints = 0;
    // Group compounds to S, I and P.
    _.forEach(pathway[1], function(rhea) {
        S.push.apply(S, _.keys(context.stoichiometrics[rhea][0]));
    });
    _.forEach(pathway[1], function(rhea) {
        P.push.apply(P, _.keys(context.stoichiometrics[rhea][1]));
    });
    I = _.uniq(_.intersection(S, P));
    S = _.uniq(_.difference(S, I));
    P = _.uniq(_.difference(P, I));
    // Total reaction
    namesS = _.map(S, function(chebi) {return context.compounds[chebi];});
    namesP = _.map(P, function(chebi) {return context.compounds[chebi];});
    totalReaction = namesS.join(' + ') + ' => ' + namesP.join(' + ');
    liMain.innerHTML = 'Total reaction: <b>' + totalReaction + '</b>';
    // Assign points.
    _.forEach(S, function (chebi) {
        substratePoints += context.prices[chebi] * context.demands[chebi];
    });
    _.forEach(P, function (chebi) {
        productPoints += context.prices[chebi] * context.demands[chebi];
    });
    _.forEach(pathway[1], function (rhea) {
        reactionPoints += context.complexities[rhea];
    });
    li = createHTMLElement(document, 'LI');
    li.innerHTML = 'Score: ' + pwPoints.toString() + ', <small>(' + productPoints.toString() + ' &minus; ' + substratePoints.toString() + ') &sdot; (' + reactionPoints.toString() + ' + 1) &frasl; ' + pathway[1].length.toString() + '</small>';
    ulMain.appendChild(li);
    // Substrates
    li = formatList(document, 'UL', 'Substrates: <small>' + substratePoints.toString() + '</small>', S, formatCompound, context);
    ulMain.appendChild(li);
    // Intermediates
    li = formatList(document, 'UL', 'Intermediates:', I, formatIntermediates,
            context);
    ulMain.appendChild(li);
    // Products
    li = formatList(document, 'UL', 'Products: <small>' + productPoints.toString() + '</small>', P, formatCompound, context);
    ulMain.appendChild(li);
    // Reaction steps
    li = formatList(document, 'OL', 'Reaction steps: <small>(' + reactionPoints.toString() + ' + 1) &frasl; ' + pathway[1].length + '</small>', pathway[1],
            formatReaction, context);
    ulMain.appendChild(li);
    
    liMain.appendChild(ulMain);
    liMain.innerHTML += '<br>'
    return liMain;
}


/**
 * Format a reaction entry in results.
 */
function formatReaction(document, rhea, data) {
    var liMain = createHTMLElement(document, 'LI');
    var dl = createHTMLElement(document, 'DL');
    var dt = createHTMLElement(document, 'DT');
    var dd = createHTMLElement(document, 'DD');
    var enzymes = data.reaction_ecs[rhea];
    var substrates = _.keys(data.stoichiometrics[rhea][0]);
    var products = _.keys(data.stoichiometrics[rhea][1]);
    dt.innerHTML = '<b>' + data.equations[rhea] + '</b>';
    dl.appendChild(dt);
    dd.innerHTML = 'Rhea:' + rhea;
    dl.appendChild(dd);
    _.forEach(enzymes, function(ec) {
        dd = createHTMLElement(document, 'DD');
        dd.innerHTML = 'EC:' + ec + ' ' + data.enzymes[ec];
        dl.appendChild(dd);
    });
    _.forEach(substrates, function(c) {  // c = chebi
        dd = createHTMLElement(document, 'DD');
        dd.innerHTML = 'Substrate ChEBI:' + c + ' ' + data.compounds[c];
        dl.appendChild(dd);
    });
    _.forEach(products, function(chebi) {
        dd = createHTMLElement(document, 'DD');
        dd.innerHTML = 'Product ChEBI:' + chebi + ' ' + data.compounds[chebi];
        dl.appendChild(dd);
    });
    liMain.appendChild(dl)
    return liMain;
}


/**
 * Return values from a form of input and 2 select fields.
 * @param {HTMLElement} form the HTML form element.
 *
 * @returns {object} selected values of form. Keys: 'compounds',
   'enzymes' and 'nResults'.
 */
function getInputValues(form) {
    var selectNodes = form.getElementsByTagName('SELECT');
    var nodeNResults = selectNodes[0];
    var nodeCompounds = selectNodes[1];
    var nodeEnzymes = selectNodes[2];
    var nodeFilterLinks = selectNodes[3];
    var nResults = Number(getMultiselectValues(nodeNResults));
    var compounds = getMultiselectValues(nodeCompounds);
    var enzymes = getMultiselectValues(nodeEnzymes);
    var filterLinks = getMultiselectValues(nodeFilterLinks);
    var result = {
        compounds: compounds,
        enzymes: enzymes,
        filterLinks: filterLinks,
        nResults: nResults,
    };
    return result;
}


/**
 * Return all selected values of a select element.
 * @param {HTMLElement} select the HTML select element.
 *
 * @returns {array} selected values of the select element.
 */
function getMultiselectValues(select) {
    var result = [];
    var options = select && select.options;
    var option;
    for (var i = 0, iLen = options.length; i < iLen; i++) {
        option = options[i];
        if (option.selected) {
            result.push(option.value);
        }
    }
    return result;
}


/**
 * Return an initialized jsnx.DiGraph.
 * @param {object} S stoichiometrics object.
 * @param {object} C compounds object.
 * @param {object} I ignored compounds array.
 *
 * @returns {object} jsnx.DiGraph.
 */
function initializeGraph(S, C, I) {
    var G = new jsnx.DiGraph();
    _.forOwn(S, function(rxnCompounds, reaction) {
        _.forOwn(rxnCompounds[1], function(empty, product) {
            // Check that the product is not an ignore compound.
            if (!_.includes(I, product)) {
                _.forEach(C[product][0], function(consumerRxn) {
                    // Check that target is not opposite of source.
                    if (!_.isEqual(S[consumerRxn][1], rxnCompounds[0])) {
                        G.addEdge(reaction, consumerRxn);
                    }
                });
            }
        });
    });
    return G;
}


/**
 * Initialize HTML form at Input section.
 */
function initializeForm(rheaChebis, chebiNames, rheaEcs, ecNames) {
    var compounds = [{id: 'any', text: 'any ChEBI'}];
    var enzymes = [];
    var nResults = [];
    var i = 1;
    var iLen = 20;
    for (; i <= iLen; i++) {
        nResults.push({id:i, text:i});
    }
    _.forEach(rheaChebis, function(chebi) {
        compounds.push({id: chebi, text: chebi + ' ' + chebiNames[chebi]});
    });
    _.forEach(rheaEcs, function(ec) {
        enzymes.push({id: ec, text: ec + ' ' + ecNames[ec]});
    });
    $('#idNResults').select2({
        data: nResults,
    });
    $('#idSelectCompounds').select2({
        data: compounds,
    });
    $('#idSelectEnzymes').select2({
        data: enzymes,
    });
    $('#idSelectFilterLinks').select2({
        data: compounds,
    });
    return;
}




/**
 * Return data for pathway evaluation.
 * @param {array} pathways
 * @param {object} S
 * @param {object} C
 * @param {object} D
 * @param {object} P
 *
 * @returns {array}
 */
function orderPathwayData(pathways, S, C, D, P) {
    var steps = [];
    var stepsPw;
    var compounds = [];
    var compoundsPw;
    var reaction = [];
    var substrates = [];
    var products = [];
    var subs;
    var pros;
    _.forEach(pathways, function(pw) {
        stepsPw = [];
        compoundsPw = {};
        _.forEach(pw, function (rxn) {
            substrates = _.keys(S[rxn][0]);
            products = _.keys(S[rxn][1]);
            _.forEach(substrates, function(s) {
                compoundsPw[s] = [D[s], P[s]];
            });
            _.forEach(products, function(p) {
                compoundsPw[p] = [D[p], P[p]];
            });
            stepsPw.push([C[rxn], substrates, products]);
        });
        steps.push(stepsPw);
        compounds.push(compoundsPw);
    });
    return [steps, compounds];
}


/**
 * Submit and evaluate input and return output.
 */
function submitSearch() {
    var outputSlot = document.getElementById('outputDiv');
    var form = document.getElementById('inputForm');
    var tmp = document.createElement('div');
    var input = getInputValues(form);
    var results;
    var lenChildren = outputSlot.childNodes.length;
    var nIsValid = validateInputN(input.nResults);
    var cEIsValid = validateInputCE(input.compounds, input.enzymes);
    if (validateInputN(nIsValid) && cEIsValid) {
        results = evaluateInput(
            PW.GRAPH, input.nResults, input.compounds, input.enzymes,
            input.filterLinks, PW.DATA);
    }
    tmp.appendChild(formatOutput(document, results, PW.DATA));
    outputSlot.innerHTML = tmp.innerHTML;
    return;
};


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
    if (lenCompounds >= 2) {
        isValid = true;
    } else if (lenEnzymes >= 1) {
        isValid = true;
    } else {
        isValid = false;
    }
    return isValid;
}


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
    return isValid;
}

// Export.
PW.createHTMLElement = createHTMLElement;
PW.evaluateInput = evaluateInput;
PW.evaluatePathway = evaluatePathway;
PW.filterPathways = filterPathways;
PW.findPathway = findPathway;
PW.formatCompound = formatCompound;
PW.formatIntermediates = formatIntermediates;
PW.formatList = formatList;
PW.formatOutput = formatOutput;
PW.formatPathway = formatPathway;
PW.formatReaction = formatReaction;
PW.getInputValues = getInputValues;
PW.getMultiselectValues = getMultiselectValues;
PW.initializeGraph = initializeGraph;
PW.initializeForm = initializeForm;
PW.orderPathwayData = orderPathwayData;
PW.submitSearch = submitSearch;
PW.validateInputCE = validateInputCE;
PW.validateInputN = validateInputN;
return PW;
})(PW || {}, $, jsnx, _);
