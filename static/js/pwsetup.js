'use strict';
// (C) 2017 Tampere University of Technology
// MIT License
// Pauli Losoi
/**
 * @file JavaScript for PathWalue-application.
 *
 * @requites jQuery
 * @requires Lodash
 *
 * @requires pw.js
 */

(function (PW, $, _) {
    $(document).ready(
        function () {
            PW.GRAPH = PW.initializeGraph(
                PW.DATA.stoichiometrics, PW.DATA.compound_reactions, PW.DATA.IGNORED_COMPOUNDS);
            PW.initializeForm(
                _.keys(PW.DATA.compound_reactions), PW.DATA.compounds,
                _.keys(PW.DATA.ec_reactions), PW.DATA.enzymes);

            $(".select2Multi").select2().on(
                'select2:select',
                function(e) {
                    var $selectedElement = $(e.params.data.element);
                    var $selectedElementOptgroup = $selectedElement.parent("optgroup");
                    if ($selectedElementOptgroup.length > 0) {
                        $selectedElement.data(
                            "select2-originaloptgroup",
                            $selectedElementOptgroup
                        );
                    }
                    $selectedElement.detach().appendTo($(e.target));
                    $(e.target).trigger('change');  // Update UI.
                }
            )
        }
    );
})(PW, $, _);
