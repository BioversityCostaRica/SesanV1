$(document).ready(function () {


    $(".Form_Pilar").submit(function (e) {
        var form = this;
        e.preventDefault();

        swal({
                title: "Se eliminara este pilar!",
                text: "Seguro que desea eliminar este pilar?",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "Si, deseo eliminarlo!",
                cancelButtonText: "No, deseo cancelar!",
                closeOnConfirm: false,
                closeOnCancel: false
            },
            function (isConfirm) {
                if (isConfirm) {
                    //"#jqEditTable").off('submit').submit();
                    form.submit();
                } else {
                    swal({
                        title: "Cancelado",
                        text: "No se eliminara este pilar",
                        type: "success"
                    });
                }
            });


    });

    if ($("#msj").val() != "[]") {
        var msj = $("#msj").val().replace("[", "").replace("]", "").split(",");
        swal({
            title: msj[0].slice(1, -1),
            text: msj[1].slice(2, -1),
            type: msj[2].slice(2, -1),
        });
        $("#msj").val("[]");
    }
    var vals;
    var vId;

    function update_text() {


        $("#rang1_" + vId).html("Sin afectacion: " + $('#var_min_' + vId).val() + " - " + vals[0]);
        $("#rang2_" + vId).html("Afectacion Moderada: " + (Number(vals[0]) + 1).toString() + " - " + vals[1]);
        $("#rang3_" + vId).html("Afectacion Alta: " + (Number(vals[1]) + 1).toString() + " - " + vals[2]);
        $("#rang4_" + vId).html("Afectacion muy alta: " + (Number(vals[2]) + 1).toString() + " - " + $('#var_max_' + vId).val());


    }

    function verify_max_min() {
        if ($('#var_max_' + vId).val() != "" && $('#var_min_' + vId).val() != "") {
            if ($('#var_max_' + vId).val() <= $('#var_min_' + vId).val()) {
                $("#incon_msj_" + vId).css({"color": "red"});
                return false;
            }
            else {
                $("#incon_msj_" + vId).css({"color": "white"});
                $("#rang1_" + vId).css({"opacity": "1"});
                $("#rang2_" + vId).css({"opacity": "1"});
                $("#rang3_" + vId).css({"opacity": "1"});
                $("#rang4_" + vId).css({"opacity": "1"});
                return true;
            }
        }
        else {
            $("#incon_msj_" + vId).css({"color": "red"});
            return false
        }
        return false

    }


    var vd = $("#vars_id").val().split(",");


    var left_to_rigth = true;

    var obs = [];

    var current;

    if (vd[0] != "") {
        for (var v = 0; v < vd.length; v++) {

            var vv = vd[v];
            max = 100;
            min = 0;
            var slider = document.getElementById('slider_' + vd[v]);
            obs.push([vd[v], slider]);
            current = slider;
            noUiSlider.create(current, {
                start: [25, 50, 75],
                connect: [true, true, true, true],
                step: 1,
                range: {
                    'min': [min],
                    'max': [max]
                },
                tooltips: false,
                //format: "v",

            });


            var connect = current.querySelectorAll('.noUi-connect');
            var color = ["#11c300", "#ffe132","#ff9936",  "#ff1313"];

            for (var i = 0; i < connect.length; i++) {
                $(connect[i]).css({"background": color[i]});
            }
            $(".noUi-base, .noUi-connects").css({'position': 'initial'});

            current.noUiSlider.on('update', function (values) {
                vals = values;
                update_text();

            });

            $("#rotate_" + vd[v]).click(function () {

                var connect = current.querySelectorAll('.noUi-connect');
                if (!left_to_rigth) {

                    var color = ["#11c300","#ffe132", "#ff9936",  "#ff1313"];
                    left_to_rigth = true;
                }
                else {
                    var color = ["#ff1313","#ff9936", "#ffe132",  "#11c300"];
                    left_to_rigth = false;
                }


                for (var i = 0; i < connect.length; i++) {
                    $(connect[i]).css({"background": color[i]});
                }
                $(".noUi-base, .noUi-connects").css({'position': 'initial'});
            });

            $("#form_vars_" + vd[v]).submit(function (e) {

                if (verify_max_min()) {
                    $("#vd1_" + vId).val($("#v1_" + vId).val());
                    $("#vd2_" + vId).val($("#v2_" + vId).val());
                    $("#vd3_" + vId).val($('#var_min_' + vId).val());
                    $("#vd4_" + vId).val($('#var_max_' + vId).val());

                    var r1, r2, r3, r4;

                    if (left_to_rigth) {
                        r1 = $('#var_min_' + vId).val() + "-" + vals[0];
                        r2 = (Number(vals[0]) + 1).toString() + "-" + vals[1];
                        r3 = (Number(vals[1]) + 1).toString() + "-" + vals[2];
                        r4 = (Number(vals[2]) + 1).toString() + "-" + $('#var_max_' + vId).val();
                    }
                    else {
                        r4 = (Number(vals[0]) - 1).toString() + "-" + $('#var_min_' + vId).val();
                        r3 = (Number(vals[1]) - 1).toString() + "-" + (Number(vals[0])).toString();
                        r2 = (Number(vals[2]) - 1).toString() + "-" + (Number(vals[1])).toString();
                        r1 = $('#var_max_' + vId).val() + "-" + (Number(vals[2])).toString();
                    }

                    $("#vdR_" + vId).val(r1 + "|" + r2 + "|" + r3 + "|" + r4);
                }
                else {
                    $("#incon_msj_" + vd[v]).css({"color": "red"});
                    $("#rang1_" + vd[v]).css({"opacity": "0"});
                    $("#rang2_" + vd[v]).css({"opacity": "0"});
                    $("#rang3_" + vd[v]).css({"opacity": "0"});
                    $("#rang4_" + vd[v]).css({"opacity": "0"});

                    e.preventDefault();
                }


            });


            $('#var_max_' + vd[v]).bind('input', function () {

                if (verify_max_min()) {
                    current.noUiSlider.updateOptions({
                        range: {
                            'min': Number($('#var_min_' + vId).val()),
                            'max': Number($('#var_max_' + vId).val())
                        }
                    });

                    var calc = Number($('#var_max_' + vId).val());
                    calc = (calc / 4);
                    current.noUiSlider.set([calc, calc * 2, calc * 3])

                }
                else {
                    $("#rang1_" + vd[v]).css({"opacity": "0"});
                    $("#rang2_" + vd[v]).css({"opacity": "0"});
                    $("#rang3_" + vd[v]).css({"opacity": "0"});
                    $("#rang4_" + vd[v]).css({"opacity": "0"});
                }
                update_text();

            });

            $('#var_min_' + vd[v]).bind('input', function () {
                if (verify_max_min()) {

                    current.noUiSlider.updateOptions({
                        range: {
                            'min': Number($('#var_min_' + vd[v]).val()),
                            'max': Number($('#var_max_' + vd[v]).val())
                        }
                    });

                    var calc = Number($('#var_max_' + vd[v]).val());
                    calc = (calc / 4);
                    current.noUiSlider.set([calc, calc * 2, calc * 3])

                }
                else {
                    $("#rang1_" + vd[v]).css({"opacity": "0"});
                    $("#rang2_" + vd[v]).css({"opacity": "0"});
                    $("#rang3_" + vd[v]).css({"opacity": "0"});
                    $("#rang4_" + vd[v]).css({"opacity": "0"});
                }
                update_text();
            });
        }

    }


    //var text_val = $('#first').children().eq(1).text();

    $('.modalV').on('shown.bs.modal', function () {


        vId = $(this).children().find("#vId").val();

        $("#rang1_" + vId).css({"opacity": "1"});
        $("#rang2_" + vId).css({"opacity": "1"});
        $("#rang3_" + vId).css({"opacity": "1"});
        $("#rang4_" + vId).css({"opacity": "1"});

        $("#vd1_" + vId).val("");
        $("#vd2_" + vId).val("");
        $("#vd3_" + vId).val("");
        $("#vd4_" + vId).val("");
        $("#vdR_" + vId).val("");
        //$("#var_max_"+ vId).val("");
        //$("#var_min_"+ vId).val("");
        $("#incon_msj_" + vId).css({"color": "white"});

        console.log(obs);
        for (var i = 0; i < obs.length; i++) {
            if (obs[i][0] == vId) {
                current = obs[i][1];
            }
        }


        if (parseInt($("#p_lv1_" + vId).val()) < parseInt($("#p_lv3_" + vId).val())) {
            var color =["#11c300",  "#ffe132","#ff9936", "#ff1313"];
            left_to_rigth = true;
            min = parseInt($("#var_min_" + vId).val());
            max = parseInt($("#var_max_" + vId).val());

            lv1 = parseInt($("#p_lv1_" + vId).val());
            lv2 = parseInt($("#p_lv2_" + vId).val());
            lv3 = parseInt($("#p_lv3_" + vId).val());

        }
        else {
            var color = ["#ff1313",  "#ff9936","#ffe132", "#11c300"];
            left_to_rigth = false;
            min = parseInt($("#var_min_" + vId).val());
            max = parseInt($("#var_max_" + vId).val());

            lv3 = parseInt($("#p_lv1_" + vId).val());
            lv2 = parseInt($("#p_lv2_" + vId).val());
            lv1 = parseInt($("#p_lv3_" + vId).val());

        }



        current.noUiSlider.updateOptions({
            start: [lv1, lv2, lv3],

            range: {
                'min': [min],
                'max': [max]
            }
        });


        var connect = current.querySelectorAll('.noUi-connect');

        for (var i = 0; i < connect.length; i++) {
            $(connect[i]).css({"background": color[i]});
        }
        $(".noUi-base, .noUi-connects").css({'position': 'initial'});


        current.noUiSlider.on('update', function (values) {


                vals = values;


                id = vId;


                var r1, r2, r3, r4;
                min = parseInt($("#var_min_" + id).val());
                max = parseInt($("#var_max_" + id).val());
                if (min < max) {


                    r1 = min.toString() + "-" + vals[0];
                    r2 = (Number(vals[0]) + 1).toString() + "-" + vals[1];
                    r3 = (Number(vals[1]) + 1).toString() + "-" + vals[2];
                    r4 = (Number(vals[2]) + 1).toString() + "-" + max.toString();
                }
                else {

                   r1 = max.toString() + "-" + vals[0];
                    r2 = (Number(vals[0]) + 1).toString() + "-" + vals[1];
                    r3 = (Number(vals[1]) + 1).toString() + "-" + vals[2];
                    r4 = (Number(vals[2]) + 1).toString() + "-" + min.toString();
                }

                $("#rang1_" + id).html("Sin afectacion:" + r1);
                $("#rang2_" + id).html("Afectacion Moderada:" + r2);
                $("#rang3_" + id).html("Afectacion Alta:" + r3);
                $("#rang4_" + id).html("Afectacion muy alta:" + r4);

            });

    });


    //modal_nf

    $('.modal_nf').on('shown.bs.modal', function () {

        var left_to_rigth_fn = true;
        max = 100;
        min = 0;
        var slider = document.getElementById('slider_nf');
        noUiSlider.create(slider, {
            start: [25, 50, 75],
            connect: [true, true, true, true],
            step: 1,
            range: {
                'min': [min],
                'max': [max]
            },
            tooltips: false

        });


        var connect = slider.querySelectorAll('.noUi-connect');
        var color = ["#11c300",  "#ffe132","#ff9936", "#ff1313"];

        for (var i = 0; i < connect.length; i++) {
            $(connect[i]).css({"background": color[i]});
        }
        $(".noUi-base, .noUi-connects").css({'position': 'initial'});
        var vals;
        slider.noUiSlider.on('update', function (values) {
            vals = values;
            $("#rang1_nf").html("Sin afectacion: 0 - " + values[0]);
            $("#rang2_nf").html("Afectacion Moderada: " + (Number(values[0]) + 1).toString() + " - " + values[1]);
            $("#rang3_nf").html("Afectacion Alta: " + (Number(values[1]) + 1).toString() + " - " + values[2]);
            $("#rang4_nf").html("Afectacion muy alta: " + (Number(values[2]) + 1).toString() + " - 100");

            var r1, r2, r3, r4;

            if (left_to_rigth_fn) {
                r1 = "0-" + values[0];
                r2 = (Number(values[0]) + 1).toString() + "-" + values[1];
                r3 = (Number(values[1]) + 1).toString() + "-" + values[2];
                r4 = (Number(values[2]) + 1).toString() + "-100";
            }
            else {
                r4 = (Number(values[0]) - 1).toString() + "-0";
                r3 = (Number(values[1]) - 1).toString() + "-" + (Number(values[0])).toString();
                r2 = (Number(values[2]) - 1).toString() + "-" + (Number(values[1])).toString();
                r1 = "100-" + (Number(values[2])).toString();
            }

            $("#vdR_nf").val(r1 + "|" + r2 + "|" + r3 + "|" + r4);

        });

        $("#rotate_nf").click(function () {
            var values = vals;
            var connect = slider.querySelectorAll('.noUi-connect');
                            console.log("csa");

            if (!left_to_rigth_fn) {

                var color = ["#11c300", "#ffe132", "#ff9936", "#ff1313"];
                left_to_rigth_fn = true;

                r1 = "0-" + values[0];
                r2 = (Number(values[0]) + 1).toString() + "-" + values[1];
                r3 = (Number(values[1]) + 1).toString() + "-" + values[2];
                r4 = (Number(values[2]) + 1).toString() + "-" + $('#var_max_' + vId).val();
            }
            else {
                var color = ["#ff1313", "#ff9936",  "#ffe132","#11c300"];
                left_to_rigth_fn = false;
                r4 = (Number(values[0]) - 1).toString() + "-0";
                r3 = (Number(values[1]) - 1).toString() + "-" + (Number(values[0])).toString();
                r2 = (Number(values[2]) - 1).toString() + "-" + (Number(values[1])).toString();
                r1 = "100-" + (Number(values[2])).toString();

            }
            $("#vdR_nf").val(r1 + "|" + r2 + "|" + r3 + "|" + r4);


            for (var i = 0; i < connect.length; i++) {
                $(connect[i]).css({"background": color[i]});
            }
            $(".noUi-base, .noUi-connects").css({'position': 'initial'});
        });

    });


});

