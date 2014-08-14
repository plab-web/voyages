$(document).ready(function() {
    $("tr .checkbox-list-item-0").hover(
        function() {
            /* If len == 2, it's region highlighting */
            if ($(this).children().length == 2){
                $(this).toggleClass("checkbox-list-item-0 checkbox-list-item-0-active");
            }
            /* If len > 0, it's area highlighting */
            else if ($(this).children().eq(2).children().length > 0) {
                $(this).toggleClass("checkbox-list-item-0 checkbox-list-item-0-active");
                $(this).children().eq(2).children().show();
            }
        }, function() {
            if ($(this).children().length == 2){
                $(this).toggleClass("checkbox-list-item-0-active checkbox-list-item-0");
            }
            if ($(this).children().eq(2).children().length > 0) {
                $(this).toggleClass("checkbox-list-item-0-active checkbox-list-item-0");
                $(this).children().eq(2).children().hide();
            }
        }
    );
});

function regionClick(clicked_input){
    var area_parent = $(clicked_input).parents().eq(6);

    if ($(clicked_input).prop('checked')) {
        /* Check if all regions checked, and check area if so */
        var allChecked = true;
        $(area_parent).find("input[name^=region-button-]").each(function( index ){
            if (! $(this).prop("checked")){
                allChecked = false;
                return;
            }
        });
        if (allChecked){
            $(area_parent).find("input[name^=area-button-]").prop("checked", true);
        }
    } else {
        /* Uncheck parent (area) input) */
        $(area_parent).find("input[name^=area-button-]").prop("checked", false);
    }


    return false;
}

function areaClick(clicked_input){
    var area_parent = $(clicked_input).parents().eq(2);
    if ($(clicked_input).prop('checked')){
        /* Check all children */
        $(area_parent).find("input[name^=region-button-]").prop("checked", true);
    } else {
        /* Uncheck all children */
        $(area_parent).find("input[name^=region-button-]").prop("checked", false);
    }

    return false;
}

function allClicked(clicked_button, action){
    var div_parent = $(clicked_button).parents().eq(4);
    if (action == 1){
        $(div_parent).find("input[name^=area-button-]").prop("checked", true);
        $(div_parent).find("input[name^=region-button-]").prop("checked", true);
    } else {
        $(div_parent).find("input[name^=area-button-]").prop("checked", false);
        $(div_parent).find("input[name^=region-button-]").prop("checked", false);
    }

    return false;
}