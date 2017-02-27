README: PathWalue
Author: Pauli Losoi (pauli.losoi@tut.fi)
License: MIT license, see LICENSE.txt for details.
(C) 2017 Tampere University of Technology


NOTE: Code base is under revision.
Outline and purpose of the code stays the same, but implementation details are subject to change.

The html documents index.html and details.html are used at the web-site
http://www.tut.fi/pathw/ along with the directory static/. PathWalue
directory structure is detailed below.


Full Table of Contents of repository (31.1.2017):

.gitignore
FILTERED_CHEBIS.txt
LICENSE.txt
MARKET_CHEBIS.txt
REACTION_CHEBIS.txt
README.txt
details.html
index.html
python/
    __init__.py
    chebi.py
    exceptions.py
    files.py
    intenz.py
    main.py
    market.py
    paths.py
    pw.py
    rhea.py
static/
    css/
        pw.css
    js/
        pw.js
        pwsetup.js
tests/
    context.py
    read_test.ctab
    read_test.json
    read_test.mol
    read_test.rd
    read_test.rxn
    test_chebi.py
    test_files.py
    test_intenz.py
    test_main.py
    test_market.py
    test_paths.py
    test_pw.py
    test_rhea.py
    tests.html
    tests.js


PathWalue directory structure (27.2.2017):
Note, some of the files aren't in this repository.

details.html  # Detailed description page.
index.html  # Main page of the application.
static/  # Directory for non-html files served.
    css/
        external/  # 3rd party css files.
            select2.min.css
        pw.css  # Cascading Style Sheet for PathWalue.
    js/
        data/  # Js files comprising the data used by PathWalue.
            cmp_demands.js
            cmp_prices.js
            cmp_names.js
            cmp_reactions.js
            ec_names.js
            ec_reactions.js
            rxn_complexities.js
            rxn_ecs.js
            rxn_equations.js
            rxn_stoichiometrics.js
            ignored_chebis.js
        external/  # 3rd party js files.
            jquery-3.1.0.min.js
            select2.min.js
            lodash.min.js
            jsnetworkx.js
        pw.js  # PathWalue js functions.
        pwsetup.js  # PathWalue setup js.
    png/
        logo.png  # TUT logo.

