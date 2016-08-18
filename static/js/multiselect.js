$(document).ready(
    function() {
        $(".select2Multi").select2().on(
            'select2:select',
            function(e) {
                $selectedElement = $(e.params.data.element);
                $selectedElementOptgroup = $selectedElement.parent("optgroup");
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