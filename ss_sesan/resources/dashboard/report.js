/**
 * Created by acoto on 30/11/17.
 */

$(document).ready(function () {


    /*document.getElementById("linkRep").onclick = function () {
     //document.getElementById("formRep").submit();
     $("#formRep").submit();
     console.log("*-*-")
     };*/

    $('#formRep').submit(function (e) {
        //$("#rep_vals").val(genReportImg());
        //console.log(genReportImg());

        e.preventDefault();
        var comp = ["sit_san", "map_d"];
        //var imgB64 = [];
        for (i = 0; i < comp.length; i++) {
            html2canvas($("#" + comp[i])[0], {
                useCORS: true,
                allowTaint:true,
                onrendered: function (canvas) {
                    var data = canvas.toDataURL();
                    var img = document.createElement('img');
                    img.src = 'data:image/png;base64,' + data;
                    //imgB64.push(img.src);
                    $("#rep_vals").val($('#rep_vals').val() + "$*$" + img.src);
                    console.log(typeof (img.src))
                }

            });
        }
        $(this).submit();
        /*$(this).append($.map(params, function (param) {
         return $('<input>', {
         type: 'hidden',
         name: param.name,
         value: param.value
         })
         }))*/
    });


    var map_points = $('#map_points').val();

    map_points2 = JSON.parse("[" + map_points.replace(/'/g, '"') + "]");


    var mapOptions1 = {
        zoomControl: true,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: false,
        rotateControl: false,
        fullscreenControl: false,
        draggable: true,
        zoom: 11,
        //center: new google.maps.LatLng(15.1554019, -90.3945255),
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


    var lat = [];
    var lon = [];

    var legend = document.getElementById('legend');
    map1.controls[google.maps.ControlPosition.RIGHT_TOP].push(legend)


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


});



