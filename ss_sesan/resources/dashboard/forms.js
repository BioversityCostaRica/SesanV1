$(document).ready(function () {

    if ($("#msj").val() != "[]") {
        var msj = $("#msj").val().replace("[", "").replace("]", "").split(",");
        swal({
            title: msj[0].slice(1, -1),
            text: msj[1].slice(2, -1),
            type: msj[2].slice(2, -1),
        });
        $("#msj").val("[]");
    }




    $('.dual_select').bootstrapDualListbox({
        selectorMinimalHeight: 75,
        filterTextClear: "Mostrar todo",
        showFilterInputs: false,
        infoText: "Disponiles: {0}",
        infoTextEmpty: ""
    });


    $('#multiple').change(function() {

      if ($(this).prop('checked')) {
            $("#val_multi").val("multiple");
        }
        else {
            $("#val_multi").val("one");
        }
    });



    $("#form_newForm").submit(function (e) {


        if ($("#f_name").val() != "" && $('#dl1').val().length > 0) {
            $("#fn").val($("#f_name").val() + "++" + $('#dl1').val() + "++" + $('#dl2').val())
        }

        else {
            if ($("#f_name").val() == "") {
                $("#alertF").css({"opacity": "1"});
            }
            if ($('#dl1').val().length == 0) {
                $("#alertF2").css({"opacity": "1"});
            }


            e.preventDefault();
        }
    });


    //$("#submitF").one('submit', function (e) {

    $(".sub_f").submit(function (e) {

        var form = this;
        e.preventDefault();


        swal({
                title: "Se eliminara este formulario!",
                text: "Seguro que desea eliminar este formulario?",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Si, deseo eliminarlos!",
                cancelButtonText: "No, deseo cancelar!",
                closeOnConfirm: false,
                closeOnCancel: false,
                html: false
            },
            function (isConfirm) {
                if (isConfirm) {

                    //$("#submitF").off('submit').submit();
                    //console.log(x);
                    form.submit();
                    //$($x).off('submit').submit();

                } else {

                    swal({
                        title: "Cancelado",
                        text: "No se eliminara este formulario",
                        type: "success"
                    });
                }
            });
    });

    //form_fu
    $(".form_fu").submit(function (e) {
        $("#fu_" + $(this).attr("id")).val($('#fu_l_' + $(this).attr("id")).val() + "*" + $(this).attr("id"))
    });


    $('#f_name').bind('input', function () {
        if ($("#f_name").val() != "") {
            $("#alertF").css({"opacity": "0"});
        }
        else {
            $("#alertF").css({"opacity": "1"});

        }
    });
    $('#dl1').on('change', function () {
        if ($("#dl1").val().length > 0) {
            $("#alertF2").css({"opacity": "0"});
        }
        else {
            $("#alertF2").css({"opacity": "1"});

        }
    });
});


