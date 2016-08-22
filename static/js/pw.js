'use strict';
// lodash
// jsnetworkx

/**
 * @fileOverview JavaScript for PathWalue-application.
 *
 * @author Pauli Losoi
 *
 * @requires jQuery
 * @requires Select2
 */


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
    _.forOwn(attributes, function(value, key) {
        element[key] = value;
    });
    return element;
}


/**
 *
 */
function evaluateInput(G, n, C, E, context) {
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
    // Determine search and filter parameters.
    if (C.length !== 0) {
        start = C[0];
        goal = _.last(C);
        if (start === 'any') {
            C = C.slice(1);
            if (goal === 'any') {
                ;
            } else {
                targets = compoundReactions[goal][1];
            }
        } else {
            sources = compoundReactions[start][0];
            if (goal === 'any') {
                C = C.slice(0, -1);
            } else {
                targets = compoundReactions[goal][1];
            }
        }
    } else {
        _.forEach(E, function(ec) {
            sources.push.apply(sources, ecReactions[ec]);
        });
        targets = sources;
    }
    // Find pathways.
    _.forEach(sources, function(s) {
        _.forEach(targets, function(t) {
            pws = findPathway(G, s, t);
            filterPws = filterPathways(pws, C, E, start, goal, context);
            pathways.push(_.uniq(_.flatten(filterPws)));  // REMOVING REDUNDANT ARRAY OBJECTS?
        });
    });
    /*
    for source, target in it.product(sources, targets):
        pws = find_pathway(graph, source, target)
        filtered_pws = filter_pathways(
            pws, source=start, target=goal, compounds=compounds,
            enzymes=enzymes, context=context)
        pathways.update(filtered_pws)

    // Evaluate pathways.
    pathways = list(pathways)
    pathway_data = order_pathway_data(pathways, stoichiometrics,
                                      complexities, demands, prices)
    values = [evaluate_pathway(s, c) for s, c in pathway_data]
    return nbest_items(n, values, pathways)
    */
    console.log(pathways)
    return _.sortBy(pathways, function (pw) {return pw[0];}).slice(0, n);
    /*
    ec_reactions = context['ec_reactions']
    compound_reactions = context['compound_reactions']
    complexities = context['complexities']
    demands = context['demands']
    prices = context['prices']
    stoichiometrics = context['stoichiometrics']

    pathways = set()
    start = None
    goal = None
    sources = [None]
    targets = [None]
    # Determine search and filter parameters.
    if compounds:
        start = compounds[0]
        goal = compounds[-1]
        if start == 'any':
            compounds = compounds[1:]
            if goal == 'any':
                pass
            else:
                targets = compound_reactions[goal][1]
        else:
            sources = compound_reactions[start][0]
            if goal == 'any':
                compounds = compounds[:-1]
            else:
                targets = compound_reactions[goal][1]
    else:
        sources.extend(e for ec in enzymes for e in ec_reactions[ec])
        targets = sources
    # Find pathways.
    for source, target in it.product(sources, targets):
        pws = find_pathway(graph, source, target)
        filtered_pws = filter_pathways(
            pws, source=start, target=goal, compounds=compounds,
            enzymes=enzymes, context=context)
        pathways.update(filtered_pws)

    # Evaluate pathways.
    pathways = list(pathways)
    pathway_data = order_pathway_data(pathways, stoichiometrics,
                                      complexities, demands, prices)
    values = [evaluate_pathway(s, c) for s, c in pathway_data]
    return nbest_items(n, values, pathways)
    */
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
    _.forEach(steps, function(step) {
        rxns.push(step[0]);
        substratesAll.push.apply(substratesAll, step[1]);
        productsAll.push.apply(productsAll, step[2]);
    });
    _.forEach(_.difference(substratesAll, productsAll), function(s) {
        subs.push(compounds[s][0] * compounds[s][1]);
    });
    _.forEach(_.difference(productsAll, substratesAll), function(p) {
        pros.push(compounds[p][0] * compounds[p][1]);
    });
    return Math.ceil((_.sum(pros)-_.sum(subs))*(_.sum(rxns)+1)/steps.length);
}


/**
 * Return pathways that meet filtering conditions.
 * @param {array} pathways pathway arrays.
 * @param {array} C compound ChEBI ID strings.
 * @param {array} E enzyme EC number strings.
 * @param {string} s source ChEBI ID.
 * @param {string} t target ChEBI ID.
 * @param {object} context context object.
 *
 * @returns {array} Approved pathways.
 */
function filterPathways(pathways, C, E, s, t, context) {
    var rxnEcs = context.reaction_ecs;
    var S = context.stoichiometrics;
    var compounds;
    var enzymes;
    var approved;
    var substrates;
    var products;
    var prepreC;
    var preC;
    var discard1;
    var discard2;
    pathways = _.filter(pathways, function(pathway, index, array) {
        approved = true;
        compounds = [];
        enzymes = [];
        _.forEach(pathway, function(reaction, i, pw) {
            substrates = _.keys(S[reaction][0]);
            products = _.keys(S[reaction][1]);
            // Check if target is used as substrate.
            if (_.includes(substrates, t)) {
                approved = false;
                return false;
            // Check if source is produced.
            } else if (_.includes(products, s)) {
                approved = false;
                return false;
            // Check for futile cycles.
            } else if (i >= 2) {
                prepreC = _.keys(S[pw[i - 2]][0]);  // substrates
                preC = _.keys(S[pw[i - 1]][1]);  // products
                discard1 = _.intersection(prepreC, substrates);
                discard2 = _.intersection(preC, substrates);
                if (discard1.length !== 0 && discard2.length !== 0) {
                    approved = false;
                    return false;
                }
                prepreC = _.keys(S[pw[i - 2]][1]);  // products
                preC = _.keys(S[pw[i - 1]][0]);  // substrates
                discard1 = _.intersection(prepreC, products);
                discard2 = _.intersection(preC, products);
                if (discard1.length !== 0 && discard2.length !== 0) {
                    approved = false;
                    return false;
                }
            }
            compounds.push(substrates);
            compounds.push(products);
            enzymes.push(rxnEcs[reaction]);
            });
        // Check for compounds and enzymes.
        if (! _.isEqual(_.intersection(C, _.flattenDeep(compounds)), C)) {
            approved = false;
        } else if (! _.isEqual(_.intersection(E, _.flattenDeep(enzymes)), E)) {
            approved = false;
        }
        if (approved) {
            return true;
        }
    });
    return pathways;
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
        if (target !== null) {
            optParameters['target'] = target;
            try {
                pathway = [jsnx.shortestPath(G, optParameters)];
            }
            catch (error) {
                ;
            }
        } else {
            try {
                pathwaysAll = jsnx.shortestPath(G, optParameters);
            }
            catch (error) {
                ;
            }
        }
    } else if (target !== null) {
        optParameters['target'] = target;
        try {
            pathwaysAll = jsnx.shortestPath(G, optParameters);
        }
        catch (error) {
            ;
        }
    }
    if (pathwaysAll !== undefined) {
        return _.values(pathwaysAll._stringValues);
    }
    return pathway;
}


/**
 * Return values from a form of input and 2 select fields.
 * @param {HTMLElement} form the HTML form element.
 *
 * @returns {object} selected values of form. Keys: 'compounds',
   'enzymes' and 'nResults'.
 */
function getInputValues(form) {
    var nodes = form.childNodes;
    var nodeNResults = nodes[0];
    var nodeCompounds = nodes[1];
    var nodeEnzymes = nodes[2];
    var nResults = nodeNResults.value;
    var compounds = getMultiselectValues(nodeCompounds);
    var enzymes = getMultiselectValues(nodeEnzymes);
    var result = {
        compounds: compounds,
        enzymes: enzymes,
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
 * Submit and evaluate input and return output.
 */
function submitSearch() {
    return null;
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
    if (lenCompounds + lenEnzymes === 0) {
        isValid = false;
    } else {
        isValid = true;
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
