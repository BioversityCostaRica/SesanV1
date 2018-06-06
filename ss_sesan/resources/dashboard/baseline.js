/**
 * Created by acoto on 15/12/17.
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


    $("#form_lb").submit(function (e) {
        //e.preventDefault();
        var data = [];
        $('#table_new_lb tr').each(function () {
            var mun_id = $("#id_mun_sel").val();
            var id_lb = $($(this).find("td").eq(0).html()).attr("t_id");
            var new_lb = $(this).find("input").val();
            data.push([id_lb, mun_id, new_lb, "*"]);

        });
        $("#mun_sel_data").val(data);
        //console.log("*-*-")
        //$("#form_lb").off('submit_lb').submit()
        //
    });
//submit_update

    $("#update_data").click(function (e) {

        var data = [];
        var count = 0;
        $('#table_lb tr').each(function () {
            if ($(this).find("input").val() != "") {
                count++;
            }
        });
        console.log(count);
        if (count == 0) {
            swal({
                title: "No hay ningun cambio valido en esta linea base",
                text: "No se encontro ninguna actualizacion en estos valores, si desea actualizar alguno cambie el valor en los cuadros de texto. Recuerde que solo se permite el registro de nunmeros en este seccion",
                type: "warning",
            });
            e.preventDefault();

        }
        else {
            //$('#form_lb_m').validate();
            $('#table_lb tr').each(function () {
                console.log();
                var mun_id = $("#id_mun_sel").val();
                var id_lb = $($(this).find("td").eq(0).html()).attr("t_id");
                if ($(this).find("input").val() != "") {
                    var new_lb = $(this).find("input").val();
                    data.push([id_lb, mun_id, new_lb, "*"]);
                }



            });
            $("#mun_sel_data2").val(data);
        }


        //$("#form_lb").off('submit_lb').submit()
        //
    });

    $("#form_lb_m").submit(function (e) {

        if ($(document.activeElement).val() == "delete") {
            e.preventDefault();

            swal({
                    title: "Se eliminaran estos datos!",
                    text: "Seguro que desea eliminar la informacion para este municipio?",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "Si, deseo eliminarla!",
                    cancelButtonText: "No, deseo cancelar!",
                    closeOnConfirm: false,
                    closeOnCancel: false
                },
                function (isConfirm) {
                    if (isConfirm) {
                        //"#jqEditTable").off('submit').submit();
                        $("#form_lb_m").off('submit').submit()
                    } else {
                        swal({
                            title: "Cancelado",
                            text: "No se eliminara esta informacion",
                            type: "success"
                        });
                    }
                });
            //e.preventDefault();
        }

    });


});