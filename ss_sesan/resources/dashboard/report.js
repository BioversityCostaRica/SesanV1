/**
 * Created by acoto on 30/11/17.
 */

$(document).ready(function () {

    $('.chosen-select').chosen({width: "100%"});

    $("#linkRep").prop("disabled", true);

    genIMG_64()

});

function genIMG_64() {

    try {

        html2canvas($("#sit_san"), {
            onrendered: function (canvas) {

                var data = canvas.toDataURL("image/png", 0.50);

                $("#pptx_img").val(data);
                $("#linkRep").prop("disabled", false);


            }

        });

        html2canvas($("#calendario"), {
            onrendered: function (canvas) {

                var data = canvas.toDataURL("image/png");

                $("#pptx_img2").val(data);


                //$("#linkRep").prop("disabled",false);


            }

        });


    }
    catch (error) {
        console.log();
    }
    //calendario
}


function printReport() {
    var fecha = $("#rep_date").val();
    var munic = $("#rep_mun").val();

    var pptx = new PptxGenJS();

    //slide 1
    var slide = pptx.addNewSlide();
    slide.addText(
        'Situación de Seguridad Alimentaria y Nutricional\nCOMUSAN ' + munic + ', ' + fecha,
        {x: 0.0, y: 0.0, w: '100%', h: 1.5, align: 'c', font_size: 24, color: '0088CC', fill: 'F1F1F1'}
    );

    var rows = [
        ['Fecha de elaboración del informe', fecha],
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
    slide.addImage({x: 3, y: 0.3, h: 5, w: 3.5, data: $("#pptx_img").val()});


    //slide 3
    var slide3 = pptx.addNewSlide();
    slide3.addImage({x: 1, y: 0.3, h: 5, w: 8, data: $("#pptx_img2").val()});


    pptx.save('report_' + munic + "_" + fecha);
}