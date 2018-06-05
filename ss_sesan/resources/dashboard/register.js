/**
 * Created by acoto on 27/10/17.
 */

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

    $(".submitU").submit(function (e) {

        var form = this;
        e.preventDefault();


        swal({
                title: "Se eliminara este usuario!",
                text: "Seguro que desea eliminar este usuario?",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Si, deseo eliminarlo!",
                cancelButtonText: "No, deseo cancelar!",
                closeOnConfirm: false,
                closeOnCancel: false,
                html:false
            },
            function (isConfirm) {
                if (isConfirm) {

                    //$("#submitF").off('submit').submit();

                    form.submit();
                    //$($x).off('submit').submit();

                } else {

                    swal({
                        title: "Cancelado",
                        text: "No se eliminara este usuario",
                        type: "success"
                    });
                }
            });
    });


});


