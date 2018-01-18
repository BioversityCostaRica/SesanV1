$(document).ready(function () {
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



