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


});


