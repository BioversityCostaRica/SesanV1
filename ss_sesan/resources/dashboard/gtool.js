/**
 * Created by acoto on 09/07/18.
 */
$(document).ready(function () {


    if ($("#msj").val() != "[]") {
        var msj = $("#msj").val().replace("[", "").replace("]", "").split(",");
        swal({
            title: msj[0].slice(1, -1),
            text: msj[1].slice(2, -1),
            type: msj[2].slice(2, -1),
        });
        $("#msj").val("[]");
    }

    var json = $.parseJSON($("#filldata").val());

    $('#dset').on('change', function (e) {
        opt = $('#dset').val();
        $('#dset2').empty()
        if (opt == "SAN") {
            var option = new Option("SAN", "SAN");
            $('#dset2').append($(option));

        }
        if (opt == "Pilares") {
            for (i = 0; i < json.pilar.length; i++) {
                var option = new Option(json.pilar[i][1], json.pilar[i][0]);
                $('#dset2').append($(option));

            }
        }
        if (opt == "Indicadores") {
            for (i = 0; i < json.ind.length; i++) {
                var option = new Option(json.ind[i][1], json.ind[i][0]);
                $('#dset2').append($(option));

            }
        }
        if (opt == "Variables") {
            for (i = 0; i < json.var.length; i++) {
                var option = new Option(json.var[i][1], json.var[i][0]);
                $('#dset2').append($(option));

            }
        }


        $("#dset2").trigger("chosen:updated");
        $("#getData4Analize").val($('#dset2').val() + "*$%" + $('#dset').val());


    });
    $('#dset2').on('change', function (e) {

        $("#getData4Analize").val($('#dset2').val() + "*$%" + $('#dset').val());

    });

    if ($("#data4plot").val() != "[]" && $("#data4plot").val() != "") {
        data = $("#data4plot").val();

        //data = "[['Date', 'Disponibilidad', 'Acceso', 'Utilizaci Biologica'], ['2018-05-01', None, None, 50.0], ['2018-06-01', 9.43, 18.18, 0.0]]";
        data = data.replace("[[", "").replace("]]", "").split("], [");

        if (data.length > 1) {
            dataTable = new google.visualization.DataTable();
            var numRows = data.length;
            var numCols = data[0].length;


            for (i = 0; i < data.length; i++) {


                d = data[i].split("'").join("");
                d = d.split(", ");

                if (i == 0) {
                    for (j = 0; j < d.length; j++) {
                        if (j == 0) {
                            dataTable.addColumn('string', d[j]);
                        }
                        else {
                            dataTable.addColumn('number', d[j]);
                        }
                    }
                }
                else {
                    d.forEach(function (item, k) {
                        if (k > 0) {
                            if (item == "None") {
                                d[k] = null
                            }
                            else {
                                d[k] = parseFloat(d[k])
                            }
                        }
                    });
                    dataTable.addRow(d);

                }


            }
            drawChart(dataTable);


        }
        else {
            swal({
                title: "No existe información",
                text: "No se encontraron datos disponibles para este gráfico",
                type: "warning"
            });
        }


        //

    }

    //var wrapper = null;
    //var chartEditor = null;
    //var data = null;


    function drawChart(dataTable) {
        var data = dataTable;

        var wrapper = new google.visualization.ChartWrapper({
            chartType: 'LineChart',
            dataTable: data,
            title: 'Datos disponibles',
            legend: {position: 'bottom'},
            container: document.getElementById('chart')
        });

        wrapper.draw();

        var chartEditor = new google.visualization.ChartEditor();

        google.visualization.events.addListener(chartEditor, 'ok', function redrawChart() {

            wrapper2 = chartEditor.getChartWrapper();
            wrapper2.setOption('height', "100%");
            wrapper2.setOption('width', "500px");
            wrapper2.draw(document.getElementById('chart'));
        });
        $("#editchart").click(function (e) {
            chartEditor.openDialog(wrapper);
            $(".google-visualization-charteditor-dialog").css({"width": "auto"});
            // $(".charts-flat-menu-button .google-visualization-clickeditor-bubble .charts-flat-menu-button-indicator .").css({"width": "auto !important"});
        });

        $("#downplot").click(function (e) {
            var imgUri = wrapper.getChart().getImageURI();
            var link = document.createElement("a");
            link.download = "_data.png";
            link.href = imgUri;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);


        });

        $("#downdata").click(function (e) {
            var dataT = wrapper.getDataTable();
            var csv_out = dataTableToCSV(dataT);
            var blob = new Blob([csv_out], {type: 'text/csv;charset=utf-8'});
            var url = window.URL || window.webkitURL;
            var link = document.createElementNS("http://www.w3.org/1999/xhtml", "a");
            link.href = url.createObjectURL(blob);
            link.download ="_data.csv";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);


        });
        function dataTableToCSV(dataTable_arg) {
            var dt_cols = dataTable_arg.getNumberOfColumns();
            var dt_rows = dataTable_arg.getNumberOfRows();
            //dt_cols=4;
            var csv_cols = [];
            var csv_out;

            // Iterate columns
            for (var i=0; i<dt_cols; i++) {
                // Replace any commas in column labels
                csv_cols.push(dataTable_arg.getColumnLabel(i).replace(/,/g,""));
            }
            // Create column row of CSV

            csv_out = csv_cols.join(",")+"\r\n";
            // Iterate rows
            for (i=0; i<dt_rows; i++) {
                var raw_col = [];
                for (var j=0; j<dt_cols; j++) {
                    xxx=dataTable_arg.getFormattedValue(i, j, 'label');

                    if (xxx.indexOf(':') == -1){
                        raw_col.push(xxx.replace(',', '.'));
                    }

                }
                // Add row to CSV text
                csv_out += raw_col.join(",")+"\r\n";
            }

            return csv_out;
        }


    }


});


