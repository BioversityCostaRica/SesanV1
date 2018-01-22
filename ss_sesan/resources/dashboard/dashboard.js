$(document).ready(function () {

    //-------------------------

    genMap();


    //-------------------------
    $('.footable').footable();
    $("span.pie").peity("pie");
    //code for registry.jinja2

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


    $('.chosen-select').chosen({width: "100%"});

    $('#password2').on('keyup', function () {
        if ($('#password').val() == $('#password2').val()) {
            $('#message').html('Correcto').css('color', 'green');
        } else
            $('#message').html('Las contraseñas no coinciden').css('color', 'red');
    });

    $('#munic_list').on('change', function () {
        $('#m_munic').html('').css('color', 'red');
    });
    $('#inst_list').on('change', function () {
        $('#m_inst').html('').css('color', 'red');
    });


    $("#submit").submit(function (e) {

        //console.log(document.activeElement.id); // name of submit button
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


    try {

        var pltData = $("#pltData1").val().split("-");
        var pltData2 = $("#pltData2").val().split("-");
        var doughnutData = {
            labels: ["Lluvia", "No lluvia"],
            datasets: [{
                data: [(100 / parseInt(pltData[0])) * parseInt(pltData[1]), 100 - (100 / parseInt(pltData[0]) ) * parseInt(pltData[1])],
                backgroundColor: ["#9CC3DA", "#dedede"]
            }]
        };


        var doughnutOptions = {
            responsive: false,
            legend: {
                display: false
            },
            tooltips: {
                enabled: false
            }

        };
        var ctx4 = document.getElementById("doughnutChart2").getContext("2d");
        new Chart(ctx4, {type: 'doughnut', data: doughnutData, options: doughnutOptions});

        var doughnutData = {
            labels: ["% de Ninos", " "],
            datasets: [{
                data: [parseInt(pltData2[0]), parseInt(pltData2[1])],
                backgroundColor: ["#9CC3DA", "#dedede"]
            }]
        };


        var doughnutOptions = {
            responsive: false,
            legend: {
                display: false
            },
            tooltips: {
                enabled: false
            }
        };


        var ctx4 = document.getElementById("doughnutChart").getContext("2d");
        new Chart(ctx4, {type: 'doughnut', data: doughnutData, options: doughnutOptions});

    }
    catch (err) {

    }


});


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
    expand();

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

    collapse();
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
    map1.controls[google.maps.ControlPosition.RIGHT_TOP].push(legend)

    var map_points = $('#map_points').val();

    map_points2 = JSON.parse("[" + map_points.replace(/'/g, '"') + "]");



    var kmlLayer = new google.maps.KmlLayer({
        url: "www.spc.noaa.gov/products/outlook/SPC_outlooks.kml",
        map: map1,
        preserveViewport: true
    });
    kmlLayer.setMap(map1);


    var lat = [];
    var lon = [];


    for (i = 0; i < map_points2[0].length; i++) {
        var marker = new google.maps.Marker({
            position: {lat: map_points2[0][i].vals[0][2], lng: map_points2[0][i].vals[0][3]},

            map: map1,
            title: map_points2[0][i].vals[0][1],
            //label: { text: map_points2[0][i].vals[0][1] },

            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 8.5,
                fillColor: map_points2[0][i].vals[0][4],
                fillOpacity: 0.4,
                strokeWeight: 0.4
            },
            //icon: 'https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=0ahUKEwjN6OaB79rYAhWDyVMKHeehAwMQjBwIBA&url=https%3A%2F%2Fwww.pr7.it%2Fwp-content%2Fuploads%2F2013%2F04%2Fpr7-green-point.png&psig=AOvVaw26MJGpQogf07H2wF4a7xiV&ust=1516136566665061'
        });

        if (!lat.includes(map_points2[0][i].vals[0][2])) {
            lat.push(map_points2[0][i].vals[0][2])
        }

        if (!lon.includes(map_points2[0][i].vals[0][3])) {
            lon.push(map_points2[0][i].vals[0][3])
        }
    }

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
    map1.controls[google.maps.ControlPosition.RIGHT_TOP].push(legend)
}