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
                html: false
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


    $(".submitM").submit(function (e) {

        var form = this;
        e.preventDefault();


        swal({
                title: "Se eliminara esta direccion!",
                text: "Seguro que desea eliminar esta direccion de correo electronico?",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Si, deseo eliminarlo!",
                cancelButtonText: "No, deseo cancelar!",
                closeOnConfirm: false,
                closeOnCancel: false,
                html: false
            },
            function (isConfirm) {
                if (isConfirm) {
                    form.submit();

                } else {

                    swal({
                        title: "Cancelado",
                        text: "No se eliminara este correo",
                        type: "success"
                    });
                }
            });
    });


    $('#depto_list').on('change', function (e) {

        var mun = $("#depto_list").val();
        $('#munic_list').empty();


        $.each($(".mlist"), function (key, value) {

            if ($(this).attr("coded") == mun.toString()) {

                if ($(this).attr("sel") != "") {
                    var option = new Option($(this).attr("value"), $(this).attr("codem"), "selected");

                }
                else {
                    var option = new Option($(this).attr("value"), $(this).attr("codem"));
                }

                $('#munic_list').append($(option));

            }
        });
        $("#munic_list").trigger("chosen:updated");


    });

    var mun = $("#depto_list").val();
    if (mun != "") {
        $.each($(".mlist"), function (key, value) {


            if ($(this).attr("coded") == mun.toString()) {

                if ($(this).attr("sel") != "") {
                    var option = new Option($(this).attr("value"), $(this).attr("codem"));
                    $(option).attr("selected", "selected");
                }
                else {
                    var option = new Option($(this).attr("value"), $(this).attr("codem"));
                }

                $('#munic_list').append($(option));

            }
        });
        $("#munic_list").trigger("chosen:updated");
    }


    function isNumeric(value) {
        return /^\d+$/.test(value);
    }

    $('#user_name').on('input', function () {
        var value = $(this).val();
        if (isNumeric(value)) {
            $(this).val("");
        }
        else {
            var value_without_space = value.replace('-', '').replace('~', '').replace(" ", "").replace("_", "").replace(/[^a-z0-9]/gi, '')
            $(this).val(value_without_space);
        }
    });

    $('#chb_del_mon').change(function() {
        if($(this).is(":checked")) {
            $("#m_l").show();
        }
        else{
            $("#m_l").hide();
        }
    });



    $('#modalUsers').on('shown.bs.modal', function () {


        $(".toggle").css({"min-width": "20% !important","width": "20% !important"});
        $("#chb_del_mon").css({"min-width": "20% !important","width": "20% !important"});

        console.log("ccsa");

    });


    //chb_del_mon

});


