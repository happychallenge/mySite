$(function() {

    /* Binding */
    // Create person .js-create-person
    // $("#js-create-person").click(function(){
    //     var btn = $(this);
    //     console.log(btn);
    //     $.ajax({
    //         url: btn.attr("data-url"),
    //         type: 'get',
    //         dataType: 'html',
    //         beforeSend: function() {
    //             $("#modal-person").modal("show");
    //         },
    //         success: function(data) {
    //             $("#modal-person .modal-content").html(data);
    //         }
    //     });
    // });

    $("#modal-person").on("submit", ".js-person-save-form", function(){
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function(data) {
                if (data.form_is_valid) {
                    $("#person-table tbody").html(data.html_person_list);
                    $("#modal-person").modal("hide");
                } else {
                    $("#modal-person .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    });

});
