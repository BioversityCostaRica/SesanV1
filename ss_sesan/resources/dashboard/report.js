/**
 * Created by acoto on 30/11/17.
 */

$(document).ready(function () {






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

     var map_name = $('#map_name').val().replace(" ", "_");

     var kmlLayer = new google.maps.KmlLayer({
     url: "http://192.155.81.175/kml/" + map_name + ".kml",
     map: map1,
     preserveViewport: true
     });

    genIMG_64()

});

function genIMG_64() {

    html2canvas($("#alert_img")[0], {
        onrendered: function (canvas) {
            var data = canvas.toDataURL("image/png");
            $("#pptx_img").val(data);

        }

    });


}


function printReport() {
        var fecha = "Enero 2018";
    var munic = "Alotenango";

    var pptx = new PptxGenJS();

    //slide 1
    var slide = pptx.addNewSlide();
    slide.addText(
        'Situacion de seguridad Alimentaria y Nutricional\nCOMUSAN' + munic + ', ' + fecha,
        {x: 0.0, y: 0.0, w: '100%', h: 1.5, align: 'c', font_size: 24, color: '0088CC', fill: 'F1F1F1'}
    );

    var rows = [
        ['Fecha de elaboracion del informe', fecha],
        ['Fuente de informacion: ', 'COMUSAN de ' + munic],
        ['Responsable del informe ', 'Oficina Municipal de SAN / SESAN']
    ];
    var tabOpts = {x: 0.5, y: 2.0, w: 9.0};
    var celOpts = {
        fill: 'dfefff', font_size: 24, color: '6f9fc9', rowH: 1.0,
        valign: 'm', align: 'c', border: {pt: '1', color: 'FFFFFF'}
    };
    slide.addTable(rows, tabOpts, celOpts);

    //slide 2
    var slide = pptx.addNewSlide();

    slide.addText(
        'Situacion SAN ' + munic + '\nFecha de emision del informe: ' + fecha + '\nComision Nacional de Seguridad Alimentaria',
        {x: 0.0, y: 0.0, w: '50%', h: 1.5, align: 'c', font_size: 18, color: '0088CC', fill: 'F1F1F1'}
    );

    /*slide.addText(
        'Situacion SAN del municipio',
        {x: 5, y: 0.0, w: '50%', h: 0.5, align: 'c', font_size: 14, color: '000000'}
    );*/

    slide.addImage({x: 5, y: 0.2, w: 3, h: 2.5, data:$("#pptx_img").val()});
    pptx.save('Demo-Simple');
}