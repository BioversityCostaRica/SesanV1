
/**
 * Created by acoto on 26/07/18.
 */

$(document).ready(function () {


    var vals;
    var vId;

    /*function update_text() {


     $("#rang1_" + vId).html("Sin afectacion: " + $('#var_min_' + vId).val() + " - " + vals[0]);
     $("#rang2_" + vId).html("Afectacion Moderada: " + (Number(vals[0]) + 1).toString() + " - " + vals[1]);
     $("#rang3_" + vId).html("Afectacion Alta: " + (Number(vals[1]) + 1).toString() + " - " + vals[2]);
     $("#rang4_" + vId).html("Afectacion muy alta: " + (Number(vals[2]) + 1).toString() + " - " + $('#var_max_' + vId).val());


     }*/

    //https://refreshless.com/nouislider/examples/#section-keyboard

    var vd = $("#varsR_id").val().split(",");
    obs = [];
    var current;
    /*if (vd[0] != "[]") {
     for (var v = 0; v < vd.length; v++) {

     var slider = document.getElementById('sliderR_' + vd[v]);
     obs.push([vd[v], slider]);

     if (parseInt($("#lv1_" + vd[v]).val()) < parseInt($("#lv3_" + vd[v]).val())) {
     var color = ["#11c300", "#ffe132", "#ff9936", "#ff1313"];
     left_to_rigth = true;
     min = parseInt($("#minR_" + vd[v]).val());
     max = parseInt($("#maxR_" + vd[v]).val());

     lv1 = parseInt($("#lv1_" + vd[v]).val());
     lv2 = parseInt($("#lv2_" + vd[v]).val());
     lv3 = parseInt($("#lv3_" + vd[v]).val());

     }
     else {
     var color = ["#ff1313", "#ff9936", "#ffe132", "#11c300"];
     left_to_rigth = false;
     max = parseInt($("#minR_" + vd[v]).val());
     min = parseInt($("#maxR_" + vd[v]).val());

     lv3 = parseInt($("#lv1_" + vd[v]).val());
     lv2 = parseInt($("#lv2_" + vd[v]).val());
     lv1 = parseInt($("#lv3_" + vd[v]).val());

     }


     current = slider;
     noUiSlider.create(current, {
     start: [lv1, lv2, lv3],
     connect: [true, true, true, true],
     step: 1,
     range: {
     'min': [min],
     'max': [max]
     },
     tooltips: false,
     keyboardSupport:true,
     //behaviour: vd[v],


     });
     //https://refreshless.com/nouislider/slider-options/#section-keyboard-support
     //https://refreshless.com/nouislider/examples/#section-keypress






     var connect = current.querySelectorAll('.noUi-connect');

     for (var i = 0; i < connect.length; i++) {
     $(connect[i]).css({"background": color[i]});
     }
     $(".noUi-base, .noUi-connects").css({'position': 'initial'});


     //----------------------------------------


     /!*var handle = current.querySelector('.noUi-handle');



     handle.addEventListener('keydown', function (e) {
     console.log(handle);
     console.log(e.which);

     var value =current.noUiSlider.get();
     console.log(value);
     console.log(e);
     console.log($(this).get());
     console.log("*-*-*-*");



     if (e.which === 37) {
     current.noUiSlider.set(value - 1);
     }

     if (e.which === 39) {
     current.noUiSlider.set(value + 1);
     }
     });*!/





     //--------------------------------------------



     current.noUiSlider.on('update', function (values,handle) {
     //inputs[handle].value = values[handle];

     vals = values;


     id = $(this)[0].target.id;
     id = id.split("_")[1];


     var r1, r2, r3, r4;
     min = parseInt($("#minR_" + id).val());
     max = parseInt($("#maxR_" + id).val());
     if (min < max) {

     $("#mun_ran_" + id).val(min.toString() + ";");


     r1 = min.toString() + "-" + vals[0];
     r2 = (Number(vals[0]) + 1).toString() + "-" + vals[1];
     r3 = (Number(vals[1]) + 1).toString() + "-" + vals[2];
     r4 = (Number(vals[2]) + 1).toString() + "-" + max.toString();

     $("#mun_ran_" + id).val(r1 + ";" + r2 + ";" + r3 + ";" + r4 + ";LR");
     $("#rangR1_" + id).html("Sin afectacion:" + r1);
     $("#rangR2_" + id).html("Afectacion Moderada:" + r2);
     $("#rangR3_" + id).html("Afectacion Alta:" + r3);
     $("#rangR4_" + id).html("Afectacion muy alta:" + r4);

     }
     else {
     r1 = max.toString() + "-" + (Number(vals[0]) - 1);
     r2 = (Number(vals[0]) ).toString() + "-" + (Number(vals[1]) - 1).toString();
     r3 = (Number(vals[1]) ).toString() + "-" + (Number(vals[2]) - 1).toString();
     r4 = (Number(vals[2])).toString() + "-" + min.toString();

     $("#mun_ran_" + id).val(r1 + ";" + r2 + ";" + r3 + ";" + r4 + ";RL");
     $("#rangR1_" + id).html("Afectacion muy alta:" + r1);
     $("#rangR2_" + id).html("Afectacion Alta:" + r2);
     $("#rangR3_" + id).html("Afectacion Moderada:" + r3);
     $("#rangR4_" + id).html("Sin afectacion:" + r4);


     }


     });

     }

     }*/

    var vd = $("#varsR_id").val().split(",");


    $("#saveall").click(function () {


        for (var v = 0; v < vd.length; v++) {

            for (var i = 0; i < 8; i++) {
                inputV=$("#val_" + vd[v] + "_" + i.toString());
                if (inputV.valid() == false) {
                    swal({
                        title: "Error",
                        text: "Hay inconsistencias en sus datos",
                        type: "error",
                    });
                    return
                }
                else{

                    console.log("todo bien");
                }
            }


        }


        for (var v = 0; v < vd.length; v++) {

         $.ajax({
         type: "POST",
         url: "ranges",
         data: $('#submitrange_'+vd[v]).serialize()// serializes the form's elements.

         });
         }

         swal({
         title: "Correcto",
         text: "Rangos guardados correctamente",
         type: "success",
         });



        //document.getElementById(".submitrange").submit();


    });


});
