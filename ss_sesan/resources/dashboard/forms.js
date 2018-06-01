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


    var fd = $("#forms_id").val().split(",");
    if (fd[0] != "") {

        for (var f = 0; f < fd.length; f++) {
            console.log("#submit_" + fd[f]);
            var ff = fd[f]
            $("#submit_" + fd[f]).submit(function (e) {

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
                        closeOnCancel: false
                    },
                    function (isConfirm) {
                        if (isConfirm) {
                            //"#jqEditTable").off('submit').submit();
                            $("#submit_" + ff).off('submit').submit();
                        } else {
                            swal({
                                title: "Cancelado",
                                text: "No se eliminara este formulario",
                                type: "success"
                            });
                        }
                    });
            });
        }

    }


    $('#f_name').bind('input', function () {
        if ($("#f_name").val() != "") {
            $("#alertF").css({"opacity": "0"});
        }
        else {
            $("#alertF").css({"opacity": "1"});

        }
    });
    $('#dl1').on('change', function () {
        console.log("chas");
        if ($("#dl1").val().length > 0) {
            $("#alertF2").css({"opacity": "0"});
        }
        else {
            $("#alertF2").css({"opacity": "1"});

        }
    });
});


