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


    var vd = $("#varsR_id").val().split(",");
    obs = [];
    var current;
    if (vd[0] != "[]") {
        for (var v = 0; v < vd.length; v++) {

            var slider = document.getElementById('sliderR_' + vd[v]);
            obs.push([vd[v], slider]);

            if (parseInt($("#lv1_" + vd[v]).val()) < parseInt($("#lv3_" + vd[v]).val())) {
                var color = ["#11c300", "#ff9936", "#ffe132", "#ff1313"];
                left_to_rigth = true;
                min = parseInt($("#minR_" + vd[v]).val());
                max = parseInt($("#maxR_" + vd[v]).val());

                lv1 = parseInt($("#lv1_" + vd[v]).val());
                lv2 = parseInt($("#lv2_" + vd[v]).val());
                lv3 = parseInt($("#lv3_" + vd[v]).val());

            }
            else {
                var color = ["#ff1313", "#ffe132", "#ff9936", "#11c300"];
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
                //behaviour: vd[v],


            });

            var connect = current.querySelectorAll('.noUi-connect');

            for (var i = 0; i < connect.length; i++) {
                $(connect[i]).css({"background": color[i]});
            }
            $(".noUi-base, .noUi-connects").css({'position': 'initial'});

            current.noUiSlider.on('update', function (values) {



                vals = values;


                id = $(this)[0].target.id;
                id = id.split("_")[1];




                var r1, r2, r3, r4;
                min = parseInt($("#minR_" + id).val());
                    max = parseInt($("#maxR_" + id).val());
                if (min < max) {

                    $("#mun_ran_"+id).val(min.toString() +";");


                    r1 = min.toString() + "-" + vals[0];
                    r2 = (Number(vals[0]) + 1).toString() + "-" + vals[1];
                    r3 = (Number(vals[1]) + 1).toString() + "-" + vals[2];
                    r4 = (Number(vals[2]) + 1).toString() + "-" + max.toString();

                    $("#mun_ran_"+id).val(r1 +";"+r2 +";"+r3 +";"+r4 +";LR");

                }
                else {

                   r1 = max.toString() + "-" + vals[0];
                    r2 = (Number(vals[0]) + 1).toString() + "-" + vals[1];
                    r3 = (Number(vals[1]) + 1).toString() + "-" + vals[2];
                    r4 = (Number(vals[2]) + 1).toString() + "-" + min.toString();

                    $("#mun_ran_"+id).val(r1 +";"+r2 +";"+r3 +";"+r4 +";RL");
                }


                $("#rangR1_" + id).html("Sin afectacion:" + r1);
                $("#rangR2_" + id).html("Afectacion Moderada:" + r2);
                $("#rangR3_" + id).html("Afectacion Alta:" + r3);
                $("#rangR4_" + id).html("Afectacion muy alta:" + r4);

            });

        }

    }


});
