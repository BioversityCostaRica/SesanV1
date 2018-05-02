function beforeInsert(table,data)
{

    var i1 = data.getIndexByColumnName("start_time_survey_1");
    var i2 = data.getIndexByColumnName("end_time_survey_26");

    var dOs = data.getIndexByColumnName("date_fecha_informe_6"); 
    var mun = data.getIndexByColumnName("seo_muni_5"); 
    var uuid = data.getIndexByColumnName("uuid");
    if (i1 >= 0 && i2 >= 0 )
    {
    	date=data.itemValue(i1);
    	date=date.split("T").join(" ").split(".")[0];
      	data.setItemValue(i1,date);

    	date=data.itemValue(i2);
    	date=date.split("T").join(" ").split(".")[0];
      	data.setItemValue(i2,date);

      	mon = data.itemValue(dOs);
      	mon = mon.split("-");
      	mon = [mon[1],mon[0]].join("");

      	mun = data.itemValue(mun);
      	id = mon+mun;

      	data.setItemValue(uuid, id );


    }

}

