function beforeInsert(table,data)
{

  var i1 = data.getIndexByColumnName("start_time_survey_1");
  var i2 = data.getIndexByColumnName("end_time_survey_26");

  //var sig1 = data.getIndexByColumnName("img_sig_rep");
  //var sig2 = data.getIndexByColumnName("img_sig_tec");

  var d_id = data.getIndexByColumnName("device_id_3");
  


  //var uuid = data.getIndexByColumnName("uuid");
  if (i1 >= 0 && i2 >= 0 )
  {
    date=data.itemValue(i1);
    date=date.split("T").join(" ").split(".")[0];
    data.setItemValue(i1,date);

    date=data.itemValue(i2);
    date=date.split("T").join(" ").split(".")[0];
    data.setItemValue(i2,date);


    //sig=data.itemValue(sig1);
    //data.setItemValue(sig1,"n_path/"+sig);

    //sig=data.itemValue(sig2);
    //data.setItemValue(sig2,"n_path/"+sig);

    d_id2 = data.itemValue(d_id);
    data.setItemValue(d_id,"n_path-"+d_id2);

    //mun = data.itemValue(mun);
    //id = mon+mun;

    //data.setItemValue(uuid, id );


  }

}

