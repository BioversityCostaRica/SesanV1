$(document).ready(function () {
    $('.footable').footable();
    $("span.pie").peity("pie");
    //code for registry.jinja2

    $.fn.datepicker.dates.es={days:["Domingo","Lunes","Martes","Miércoles","Jueves","Viernes","Sábado"],daysShort:["Dom","Lun","Mar","Mié","Jue","Vie","Sáb"],daysMin:["Do","Lu","Ma","Mi","Ju","Vi","Sa"],months:["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"],monthsShort:["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"],today:"Hoy",monthsTitle:"Meses",clear:"Borrar",weekStart:1,format:"dd/mm/yyyy"}

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

    $('#dateP').datepicker().on("changeDate", function(e) {

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
         if ($('#password').val() != $('#password2').val()){
            $('#message').html('Las contraseñas deben coincidir').css('color', 'red');
            e.preventDefault();
         }

    });


    var data1 = [
        [0, 4], [1, 8], [2, 5], [3, 10], [4, 4], [5, 16], [6, 5], [7, 11], [8, 6], [9, 11], [10, 30], [11, 10], [12, 13], [13, 4], [14, 3], [15, 3], [16, 6]
    ];
    var data2 = [
        [0, 1], [1, 0], [2, 2], [3, 0], [4, 1], [5, 3], [6, 1], [7, 5], [8, 2], [9, 3], [10, 2], [11, 1], [12, 0], [13, 2], [14, 8], [15, 0], [16, 0]
    ];
    $("#flot-dashboard-chart").length && $.plot($("#flot-dashboard-chart"), [
            data1, data2
        ],
        {
            series: {
                lines: {
                    show: false,
                    fill: true
                },
                splines: {
                    show: true,
                    tension: 0.4,
                    lineWidth: 1,
                    fill: 0.4
                },
                points: {
                    radius: 0,
                    show: true
                },
                shadowSize: 2
            },
            grid: {
                hoverable: true,
                clickable: true,
                tickColor: "#d5d5d5",
                borderWidth: 1,
                color: '#d5d5d5'
            },
            colors: ["#1ab394", "#1C84C6"],
            xaxis: {},
            yaxis: {
                ticks: 4
            },
            tooltip: false
        }
    );

              var doughnutData = {
                labels: ["App","Software","Laptop" ],
                datasets: [{
                    data: [300,50,100],
                    backgroundColor: ["#a3e1d4","#dedede","#9CC3DA"]
                }]
            } ;


            var doughnutOptions = {
                responsive: false,
                legend: {
                    display: false
                }
            };


            var ctx4 = document.getElementById("doughnutChart").getContext("2d");
            new Chart(ctx4, {type: 'doughnut', data: doughnutData, options:doughnutOptions});

            var doughnutData = {
                labels: ["App","Software","Laptop" ],
                datasets: [{
                    data: [70,27,85],
                    backgroundColor: ["#a3e1d4","#dedede","#9CC3DA"]
                }]
            } ;


            var doughnutOptions = {
                responsive: false,
                legend: {
                    display: false
                }
            };


            var ctx4 = document.getElementById("doughnutChart2").getContext("2d");
            new Chart(ctx4, {type: 'doughnut', data: doughnutData, options:doughnutOptions});

});



