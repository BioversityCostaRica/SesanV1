$(document).ready(function () {
    function getFiles() {
        var pdata ={"getFiles": "1", "date": $("#cur_date").val()};
        if ($("#munic_list").val()!= undefined){
            if ($("#munic_list").val()== "") {
                pdata = {"getFiles": "1", "date": $("#cur_date").val()}
            }
            else{
                pdata = {"getFiles": $("#munic_list").val(), "date": $("#cur_date").val()}
            }
        };


        $.ajax({
            type: "POST",
            url: "uploadfiles",
            data: pdata,
            dataType: 'json',
            statusCode: {
                201: function (data, textStatus, jqXHR) {

                    $("#fil").remove();

                    var container = $('#container');
                    var table = $('<table id="fil" class="table table-hover header-fixed">');
                    table.append('<thead><th>Nombre</th><th class="text-center"></th></thead>');
                    var tr = $('<tbody>');
                    for (i = 0; i < data["ff"].length; i++) {
                        row = data["ff"][i].split("/").slice(-1)[0];
                        //durl=/downfiles/{parent}/{user}/{file}

                        //durl=/downfiles/{parent}/{user}/{file}

                        var origin = window.location.origin;

                        if (pdata["getFiles"] != "1"){
                            dir = origin + /downfiles/ + $("#parent").val() + "/user/" + data["login"] + "/attach/" + $("#cur_date").val() + "/" + row;
                            del = origin + /downfiles/ + $("#parent").val() + "/user/" + data["login"] + "/attach/" + $("#cur_date").val() + "/" + row + "_delfile";

                        }
                        else{
                            dir = origin + /downfiles/ + $("#parent").val() + "/user/" + $("#uname").val() + "/attach/" + $("#cur_date").val() + "/" + row;
                        del = origin + /downfiles/ + $("#parent").val() + "/user/" + $("#uname").val() + "/attach/" + $("#cur_date").val() + "/" + row + "_delfile";

                        }



                        row = '<a href="' + dir + '">' + row + '</a>';

                        tr.append('<tr><td>' + row + '</td><td class="text-center"><a class="btn btn-danger btn-circle" href="' + del + '" ><i class="fa fa-times"></i></a><td></tr>');


                    }
                    table.append(tr);
                    container.append(table);
                    $("#file_name").html("");


                },

            },

        });

    };

    route = window.location.toString().split("/")[3];

    if (route == "dashboard") {
        getFiles();
    }


    $("#file_name").on('DOMSubtreeModified', function () {

        if ($(this).html() != "") {


            let photo = document.getElementById("filefull").files[0];

            let formData = new FormData();
            //formData.append("file", $(this).html());
            formData.append("userfile", photo)
            formData.append("date", $("#cur_date").val());

            // formData.append("user", JSON.stringify(user));   // you can add also some json data to formData like e.g. user = {name:'john', age:34}

            let xhr = new XMLHttpRequest();
            xhr.open("POST", 'uploadfiles');
            xhr.onreadystatechange = function () {
                if (xhr.readyState > 3 && xhr.status == 201) {
                    getFiles();
                }
                ;
            };
            xhr.send(formData);


        }


    });


    //---Wizard---------------------


    if ($("#cur_date").val() != undefined) {

        var expires = new Date();
        expires.setTime(expires.getTime() + (1 * 24 * 60 * 60 * 1000));
        document.cookie = "cur_date" + '=' + $("#cur_date").val() + ';expires=' + expires.toUTCString();

    }

    if ($("#msj").val() != "[]") {
        var msj = $("#msj").val().replace("[", "").replace("]", "").split(",");
        swal({
            title: msj[0].slice(1, -1),
            text: msj[1].slice(2, -1),
            type: msj[2].slice(2, -1),
        });
        $("#msj").val("[]");
    }


    //alert(document.cookie);

    $('.file-box').each(function () {
        animationHover(this, 'pulse');
    });

    var vars = []

    $("#newV_0").click(function () {
        if (!$("#newT_0").val()) {
            alert("texto en blanco")
        }
        else {
            if (vars.indexOf($("#newT_0").val()) >= 0) {
                alert("ya existe esa variable")
            }
            else {
                vars.push($("#newT_0").val());
                console.log("agregar var");

            }

        }

    });


    function get_wizard_data() {
        //console.log("*-*-*-*");
        var jsonP = {};
        jsonP["pilarName"] = $("#pilarName").val();
        jsonP["coef_pond"] = $("#coef_pond").val();
        jsonP["desc"] = $("#desc").val();
        jsonP["rang"] = $("#vdR_nf").val();

        jsonP["ind"] = {};

        var ind = $("#ind_tags").val();

        ind = ind.split(",");
        for (i = 0; i < ind.length; i++) {
            id = ind[i].replace(/ /g, "_");
            jsonP.ind[id] = {};
            jsonP.ind[id]["name"] = ind[i];
            jsonP.ind[id]["vars"] = [];
            var vars = $(".var_" + id).val();
            vars = vars.split(",");
            for (j = 0; j < vars.length; j++) {
                jsonP.ind[id]["vars"].push(vars[j])
            }

        }

        $("#jsondata").val(JSON.stringify(jsonP));

        //console.log(JSON.stringify(jsonP));


    }

    function tag_methods() {
        $('.tagsinput').tagsinput({
            tagClass: 'label label-primary',
        });


//$(".bootstrap-tagsinput").css({"width": "100% !important"});
        $("bootstrap-tagsinput input").css({"border": "0px"});
        $("bootstrap-tagsinput input").css({"width": "100%"});
        $(".bootstrap-tagsinput").css({"min-width": "326px"});
//set_white_tag();

        $('.tagsinput').on('beforeItemAdd', function (event) {
            set_white_tag();
            set_normal_message();
        });

        $('.tagsinput').on('beforeItemRemove', function (event) {
            var vals = $(".tagsinput").val();
            vals = vals.split(",");
            if (vals.length == 1 && vals[0] == "") {
                set_red_tag();
            }
        });

        $('.tagsinput').on('itemRemoved', function (event) {

            id = event.item.replace(/ /g, "_");

            $("#id-" + id).remove();
            $("#tab-" + id).remove();

        });
    }


    function set_white_tag() {
        $(".wizard .content .body .bootstrap-tagsinput input").css({
            "background": "#fbfffd",
            "border": "0px solid #FFFFFF",
            "color": "#000000"
        });
        $(".wizard .content .body .bootstrap-tagsinput").css({
            "background": "#fbfffd",
            "border": "1px solid #fbc2c4;",
            "color": "#fbfffd"
        });

    }

    function set_red_tag() {

        $(".wizard .content .body input").css({
            "background": "rgb(251, 227, 228)",
            "border": "1px solid #fbc2c4;",
            "color": "#8a1f11"
        });
        $(".wizard .content .body .bootstrap-tagsinput").css({
            "background": "rgb(251, 227, 228)",
            "border": "1px solid #fbc2c4;",
            "color": "#8a1f11"
        });

    }

    function isInArray(value, array) {
        return array.indexOf(value) > -1;
    }

    var final_vals = [];
    var final_vals_class = []


    function table(tit, i, id) {
        var table = 'Variables para el indicador ' + tit + '<BR><input class="tagsinput form-control var_' + id + '" type="text" value=""/>';
        return table
    }


    function load_tabs() {
        var vals = $(".tagsinput").val();
        vals = vals.split(",");


        for (i = 0; i < vals.length; i++) {

            if (!isInArray(vals[i], final_vals)) {

                id = vals[i].replace(/ /g, "_");

                /*if (i == 0) {
                 li = "<li class='active' id='id_" + id + "'><a data-toggle='tab' href='#tab-" + id + "'>" + vals[i] + "</a></li>";
                 cont = "<div id='tab-" + id + "' class='tab-pane active'><div class='panel-body'><strong>Donec quam felis"+vals[i]+"</strong></div></div>"


                 }
                 else {*/
                li = "<li class='' id='id-" + id + "'><a data-toggle='tab' class='var_tabs' id='h_" + id + "' href='#tab-" + id + "'>" + vals[i] + "</a></li>";
                cont = "<div id='tab-" + id + "' class='tab-pane'><div class='panel-body'><strong>" + table(vals[i], i, id) + "</strong></div></div>";

                /* }*/

                $("#tab_list").append(li);
                $("#tab_cont").append(cont);
                final_vals.push(vals[i]);
                final_vals_class.push(id)


            }


        }

    }

    function set_red_message(href_id) {
        $("#h_" + href_id).css({"color": "#8a1f11",})
    }

    function set_normal_message() {
        $(".var_tabs").css({"color": "#A7B1C2",})
    }


    $(".formwiz").steps({
        bodyTag: "fieldset",
        onStepChanging: function (event, currentIndex, newIndex) {
            //set_white_tag();
            // Always allow going backward even if the current step contains invalid fields!
            if (currentIndex > newIndex) {
                return true;
            }


            var form = $(this);

            // Clean up if user went backward before
            if (currentIndex < newIndex) {
                // To remove error styles
                $(".body:eq(" + newIndex + ") label.error", form).remove();
                $(".body:eq(" + newIndex + ") .error", form).removeClass("error");
            }

            // Disable validation on fields that are disabled or hidden.
            form.validate().settings.ignore = ":disabled,:hidden";
            if (currentIndex == 1) {
                var vals = $(".tagsinput").val();
                vals = vals.split(",");

                if (vals.length >= 1 && vals[0] != "") {
                    set_white_tag();
                }
                else {
                    set_red_tag();
                    return false;
                }

            }
            if (currentIndex == 2) {
                set_normal_message();
                for (i = 0; i < final_vals_class.length; i++) {

                    var vals = $(".var_" + final_vals_class[i]).val();
                    if (vals != null) {
                        vals = vals.split(",");
                        if (vals.length >= 1 && vals[0] != "") {
                            set_white_tag();
                        }
                        else {
                            set_red_message(final_vals_class[i]);
                            return false;
                        }
                    }

                }


            }


            // Start validation; Prevent going forward if false
            return form.valid();
        },
        onStepChanged: function (event, currentIndex, priorIndex) {

            if (currentIndex === 2) {
                load_tabs();
                tag_methods();
                set_white_tag();


            }
            if (currentIndex === 1) {
                set_white_tag();
            }


        },
        onFinishing: function (event, currentIndex) {
            var form = $(this);

            // Disable validation on fields that are disabled.
            // At this point it's recommended to do an overall check (mean ignoring only disabled fields)
            form.validate().settings.ignore = ":disabled";

            // Start validation; Prevent form submission if false
            return form.valid();
        }
        ,
        onFinished: function (event, currentIndex) {
            var form = $(this);

            // Submit form input
            get_wizard_data();
            form.submit();
        }
    }).validate({
        errorPlacement: function (error, element) {
            element.before(error);
        },
        rules: {
            confirm: {
                equalTo: "#password"
            }
        }
    });

    tag_methods();


//$(".tagsinput").tagsinput('items')


//-----------------------


//-------------------------
    try {
        genMap();
    }
    catch (err) {
    }


//-------------------------
    $('.footable').footable();
    $("span.pie").peity("pie");
//code for registry.jinja2

    try {

        $.fn.datepicker.dates.es = {
            days: ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
            daysShort: ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"],
            daysMin: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa"],
            months: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
            monthsShort: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
            today: "Hoy",
            monthsTitle: "Meses",
            clear: "Borrar",
            weekStart: 1,
            format: "dd/mm/yyyy"
        }

        $('#dateP').datepicker({
            minViewMode: 1,
            keyboardNavigation: false,
            forceParse: false,
            forceParse: false,
            autoclose: true,
            todayHighlight: true,
            format: 'MM yyyy',
            //monthsShort:["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"],
            language: "es"

        });

        $('#dateP').datepicker().on("changeDate", function (e) {

            //$('#dateP').datepicker('update')
            //alert($("#dateP").val())
            $('#newMonth').submit();
            // `e` here contains the extra attributes
        });
    }
    catch (err) {

    }


    $('.chosen-select').chosen({width: "100%"});

    $('#password2').on('keyup', function () {
        if ($('#password').val() == $('#password2').val()) {
            $('#message').html('Correcto').css('color', 'green');
        } else
            $('#message').html('Las contraseñas no coinciden').css('color', 'red');
    });


    $('#password2_').on('keyup', function () {
        if ($('#password_').val() == $('#password2_').val()) {
            $('#message_').html('Correcto').css('color', 'green');
        } else
            $('#message_').html('Las contraseñas no coinciden').css('color', 'red');
    });


    $('#munic_list').on('change', function () {
        $('#m_munic').html('').css('color', 'red');
    });
    $('#inst_list').on('change', function () {
        $('#m_inst').html('').css('color', 'red');
    });


    $("#submit").submit(function (e) {
        if ($('#munic_list option:selected').val() == '') {
            $('#m_munic').html('Seleccione un municipio').css('color', 'red');
            e.preventDefault();
        }
        if ($('#inst_list option:selected').val() == '') {
            $('#m_inst').html('Seleccione una institucion').css('color', 'red');
            e.preventDefault();
        }
        if ($('#password').val() != $('#password2').val()) {
            $('#message').html('Las contraseñas deben coincidir').css('color', 'red');
            e.preventDefault();
        }

    });

    $("#submit_pass").submit(function (e) {

        if ($('#password_').val() != $('#password2_').val()) {
            $('#message_').html('Las contraseñas deben coincidir').css('color', 'red');
            e.preventDefault();
        }

    });


    try {

        var pltData = $("#pltData1").val().split("-");
        var pltData2 = $("#pltData2").val().split("-");
        var doughnutData = {
            labels: ["% Dias: " + (100 / parseInt(pltData[0])) * parseInt(pltData[1]).toString()],
            datasets: [{
                data: [(100 / parseInt(pltData[0])) * parseInt(pltData[1]), 100 - (100 / parseInt(pltData[0]) ) * parseInt(pltData[1])],
                backgroundColor: ["#1AB394", "#dedede"]
            }]
        };


        var doughnutOptions = {
            responsive: true,
            legend: {
                display: true
            },
            tooltips: {
                enabled: false
            }

        };
        var ctx4 = document.getElementById("doughnutChart2").getContext("2d");
        new Chart(ctx4, {type: 'doughnut', data: doughnutData, options: doughnutOptions});

        var doughnutData = {
            labels: ["% Afectacion: " + parseInt(pltData2[0]).toString()],
            datasets: [{
                data: [parseInt(pltData2[0]), parseInt(pltData2[1])],
                backgroundColor: ["#1AB394", "#dedede"]
            }]
        };


        var doughnutOptions = {
            responsive: true,
            legend: {
                display: true
            },
            tooltips: {
                enabled: false
            }
        };


        var ctx4 = document.getElementById("doughnutChart").getContext("2d");
        new Chart(ctx4, {type: 'doughnut', data: doughnutData, options: doughnutOptions});
        //$("#doughnutChart").hide();
    }
    catch (err) {

    }


})
;


function expand() {
    $('.footable').trigger('footable_expand_all');

    $('.footable').bind('footable_breakpoint', function () {
        $('.footable').trigger('footable_expand_all');
    });

}

function collapse() {
    var rows = $('.footable tr');
    for (i = 0; i < rows.length; i++) {
        if ($(rows[i]).hasClass("footable-detail-show")) {
            $(rows[i]).trigger('footable_toggle_row');
        }

    }
}

function expandFoo() {

    if ($("#collapse").html().indexOf("Mostrar") >= 0) {
        expand();
        $("#collapse").html("Ocultar todo");

    }

    else if ($("#collapse").html().indexOf("Ocultar") >= 0) {
        collapse();

        $("#collapse").html("Mostrar todo");

    }


}

function showPDF() {

    $("#formXLS").submit();

    /*expand();

     var doc = new jsPDF();
     doc.setProperties({
     title: "Reporte SESAN",
     subject: "Bioversity International",
     author: 'Bioversity International',
     creator: 'Copyright Bioversity International © 2017'
     });
     doc.text($("#title").html(), 10, 20);
     doc.text(" ", 10, 25);

     doc.addHTML($('#summary'), -30, 44, {
     'background': '#fff',
     pagesplit: true,
     'width': 1000,
     }, function () {
     doc.save('report.pdf');
     });

     collapse();*/
}

function genMap() {
    var mapOptions1 = {
        zoomControl: true,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: false,
        rotateControl: false,
        fullscreenControl: false,
        draggable: true,
        zoom: 11,
        center: new google.maps.LatLng(15.1554019, -90.3945255),
        // Style for Google Maps
        styles: [{
            "featureType": "administrative",
            "elementType": "all",
            "stylers": [{"saturation": "-100"}]
        }, {
            "featureType": "administrative.country",
            "elementType": "labels",
            "stylers": [{"visibility": "on"}]
        }, {
            "featureType": "administrative.province",
            "elementType": "all",
            "stylers": [{"visibility": "off"}]
        }, {
            "featureType": "administrative.province",
            "elementType": "labels",
            "stylers": [{"visibility": "on"}]
        }, {
            "featureType": "administrative.locality",
            "elementType": "labels",
            "stylers": [{"visibility": "on"}, {"hue": "#ff0000"}]
        }, {
            "featureType": "landscape",
            "elementType": "all",
            "stylers": [{"saturation": -100}, {"lightness": 65}, {"visibility": "on"}]
        }, {
            "featureType": "poi",
            "elementType": "all",
            "stylers": [{"saturation": -100}, {"lightness": "50"}, {"visibility": "simplified"}]
        }, {
            "featureType": "road",
            "elementType": "all",
            "stylers": [{"saturation": "-100"}]
        }, {
            "featureType": "road.highway",
            "elementType": "all",
            "stylers": [{"visibility": "simplified"}]
        }, {
            "featureType": "road.arterial",
            "elementType": "all",
            "stylers": [{"lightness": "30"}]
        }, {
            "featureType": "road.local",
            "elementType": "all",
            "stylers": [{"lightness": "40"}]
        }, {
            "featureType": "transit",
            "elementType": "all",
            "stylers": [{"saturation": -100}, {"visibility": "simplified"}]
        }, {
            "featureType": "water",
            "elementType": "geometry",
            "stylers": [{"hue": "#ffff00"}, {"lightness": -25}, {"saturation": -97}]
        }, {"featureType": "water", "elementType": "labels", "stylers": [{"lightness": -25}, {"saturation": -100}]}]
    };

    var mapElement1 = document.getElementById('map1');

    var map1 = new google.maps.Map(mapElement1, mapOptions1);

    var legend = document.getElementById('legend');
    //map1.controls[google.maps.ControlPosition.RIGHT_TOP].push(legend);

    var map_points = $('#map_points').val();
    map_points2 = map_points.replace("[[", "").replace("]]", "").split("], [");
    //map_points2 = map_points.split("], [");
    //map_points2 = JSON.parse("[" + map_points.replace(/'/g, '"') + "]");



     var lat = [];
     var lon = [];


     for (i = 0; i < map_points2.length; i++) {
     var row = map_points2[i].split(",");

     var marker = new google.maps.Marker({

     position: {
     lat: parseFloat(row[2].toString().replace(" ", "")),
     lng: parseFloat(row[3].toString().replace(" ", ""))
     },

     map: map1,
     title: row[1].split("'").join(""),
     //label: { text: map_points2[0][i].vals[0][1] },

     icon: {
     path: google.maps.SymbolPath.CIRCLE,
     scale: 8.5,
     fillColor: row[4].split("'").join(""),
     fillOpacity: 0.4,
     strokeWeight: 0.4
     },
     //icon: 'https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=0ahUKEwjN6OaB79rYAhWDyVMKHeehAwMQjBwIBA&url=https%3A%2F%2Fwww.pr7.it%2Fwp-content%2Fuploads%2F2013%2F04%2Fpr7-green-point.png&psig=AOvVaw26MJGpQogf07H2wF4a7xiV&ust=1516136566665061'
     });

     if (!lat.includes(parseFloat(row[2].toString().replace(" ", "")))) {
     lat.push(parseFloat(row[2].toString().replace(" ", "")))
     }

     if (!lon.includes(parseFloat(row[3].toString().replace(" ", "")))) {
     lon.push(parseFloat(row[3].toString().replace(" ", "")))
     }
     }
     ;


     var total = 0;
     for (var i in lat) {
     total += lat[i];
     }
     ;
     lat = total / lat.length;
     total = 0;
     for (var i in lon) {
     total += lon[i];
     }
     ;
     lon = total / lon.length;
     map1.setCenter({lat: lat, lng: lon});

     var legend = document.getElementById('legend');
     map1.controls[google.maps.ControlPosition.RIGHT_TOP].push(legend);


    var map_name = $('#map_name').val();
    console.log("http://190.111.0.168/kml/" + map_name + ".kml");
    var kmlLayer = new google.maps.KmlLayer({
        //url: "http://"+window.location.host+"/kml/" + map_name + ".kml",
        url: "http://190.111.0.168/kml/" + map_name + ".kml",
        map: map1,
        preserveViewport: false
    });

    //kmlLayer.setMap(map1);


}


