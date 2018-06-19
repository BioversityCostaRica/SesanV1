from ..models import DBSession, Institucione, Munic, User, VariablesInd, Pilare, Indicadore, Grupo, RangosPilare, \
    LineasBase, CentrosUrbano, CoefPond, FormsByUser, Form
from sqlalchemy import func
from datetime import datetime as t
from ..encdecdata import encodeData
import transaction
from datetime import datetime
import os, json, base64
from pprint import pprint
from hashlib import md5
from calendar import monthrange
from zope.sqlalchemy import mark_changed
from glob import glob
import socket
from pyramid.response import FileResponse
from qrtools import QR  # apt-get install libzbar-dev, pip install zbar, pip install qrtools
from ..encdecdata import decodeData
import xlsxwriter
import shutil
from sqlalchemy import or_


def getPob4Map(id_cu, alert):
    mySession = DBSession()

    result = mySession.query(CentrosUrbano).filter(CentrosUrbano.id_cu == id_cu).first()
    data = []
    if result:
        data.append(
            [str(result.categoria).title(), str(result.cu_name).title(), float(result.Y), float(result.X), alert])

    mySession.close()

    return data


def dataReport(self, month, year):
    mySession = DBSession()

    prec_uname = ""
    des_uname = ""
    mides_uname = ""

    valEqui = []
    coefPon = []
    unames = []

    ###



    mySession = DBSession()
    data = {}

    my_forms = mySession.query(FormsByUser.idforms).filter(FormsByUser.id_user == self.user.login)
    res = []
    myDB = []
    if not my_forms is None:
        for row in my_forms:
            my_Pilars = mySession.query(Form).filter(Form.form_id == row.idforms).all()
            if not my_Pilars is None:
                for mp in my_Pilars:
                    myDB.append(mp.form_db)
                    mp = mp.pilar_id.split(",")
                    for m in mp:
                        res.append(m)

    res = list(set(res))
    myDB = list(set(myDB))

    resI = []
    for idP in res:
        my_Ind = mySession.query(Indicadore).filter(Indicadore.Id_pilares == int(idP)).all()
        if not my_Ind is None:
            for mI in my_Ind:
                resI.append(mI.id_indicadores)

    variables = mySession.query(VariablesInd).filter(VariablesInd.id_indicadores.in_(resI)).all()
    indicadores = []
    pilares = []

    ###



    for var in variables:
        if int(var.id_indicadores) not in indicadores:
            indicadores.append(int(var.id_indicadores))

    for db in myDB:

        result = mySession.execute(
            "SELECT COUNT(*) FROM %s.maintable WHERE MONTH(date_fecha_informe_6) = %s and YEAR (date_fecha_informe_6) = %s and surveyid like binary '%s' ;" % (
                db, month, year, "% " + self.user.login + "_%")).scalar()

        pilares_ind_db = mySession.query(Form.pilar_id).filter(Form.form_db == db).first()
        pilares_ind_db = pilares_ind_db[0].split(",")

        if int(result) != 0:

            for i in indicadores:
                i_pi = mySession.query(Indicadore.Id_pilares).filter_by(id_indicadores=i).first()
                if str(int(i_pi[0])) in pilares_ind_db:
                    p_name = mySession.query(Pilare.name_pilares, Pilare.id_pilares).filter_by(
                        id_pilares=int(i_pi[0])).first()
                    tot_alert = []
                    i_name = mySession.query(Indicadore.name_indicadores, Indicadore.id_indicadores).filter_by(
                        Id_pilares=int(i_pi[0])).all()

                    for i_n in i_name:
                        variables = mySession.query(VariablesInd).filter_by(id_indicadores=int(i_n[1])).all()
                        valCP = 0
                        acum = []
                        for v in variables:
                            sa = getVarValue(db, v.code_variable_ind, month, year, self.user.login)
                            # add variables data

                            valCP = valCP + calcValue(sa, v.id_variables_ind, 1, self.user.munic)

                            acum.append(calcValue(sa, v.id_variables_ind, 1, self.user.munic) * calcValue(sa,
                                                                                                          v.id_variables_ind,
                                                                                                          2,
                                                                                                          self.user.munic))
                        tot_alert.append([valCP, sum(acum)])
                    pilares.append(int(i_pi[0]))
                    # print tot_alert
                    t0 = 0
                    t1 = 0
                    for t in tot_alert:
                        t0 = t0 + t[0]
                        t1 = t1 + t[1]
                    alertP = getPilarAlert(p_name[1], "%.2f" % (t1 / t0))
                    data[p_name[0] + "_alert"] = ["%.2f" % (t1 / t0), alertP[1].title(), alertP[0]]

                    unames.append([db, self.user.login, alertP[0]])

                    result = mySession.query(Grupo.val_grupos).filter(
                        float("%.2f" % (t1 / t0)) <= Grupo.val_grupos).first()
                    valEqui.append(int(result.val_grupos))
                    result = mySession.query(Pilare.coef_pond).filter(Pilare.name_pilares == p_name[0]).first()
                    coefPon.append(int(result.coef_pond))

                meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre",
                         "Octubre",
                         "Noviembre", "Diciembre"]

                # *-*-*-*-*-
                # des = int(float(getVarValue("MSPAS", "dec_mi_nutri_edas_8", month, year, des_uname)))
                des = 10
                data["date"] = [meses[int(month) - 1], year, self.user.munic]
                data["plt_values"] = {"lluvia": "%s-%s" % (str(monthrange(int(year), int(month))[1]),
                                                           str(int(12))),
                                      "nin_des": "%s-%s" % (str(des), str(100 - des))}

    mySession.close()

    tot_ValAgg = []
    for a, b in zip(coefPon, valEqui):
        tot_ValAgg.append(a * b)

    san = "%.2f" % (sum(tot_ValAgg) / float(sum(coefPon)))
    data["san"] = [san, getSAN(san)[0], getSAN(san)[1]]

    data["points"] = []
    # for o in unames:
    #    for x in getVarValue(o[0], "sem_af_comunidad", month, year, o[1]).split((" ")):
    #        data["points"].append(getPob4Map(x, o[2]))

    print "*-*-*-*-"
    pprint(data)
    print "*-*-*-*-"
    return data


def getHelpFiles(request):
    files = glob(request.registry.settings['user.repository'] + "help_files/*.*")

    data = []
    files.sort(key=lambda item: (-len(item), item))
    for f in files:
        ext = os.path.splitext(f)[1]
        fa = ""
        if ext in [".jpg", ".jpg", ".png", ".svg"]:
            fa = "fa-file-picture-o"
        elif ext in [".mp4", ".mpg4"]:
            fa = "fa-file-movie-o"
        elif ext in [".mp3", ".wma"]:
            fa = "fa-file-sound-o"
        elif ext in [".doc", ".docx"]:
            fa = "fa-file-word-o"
        elif ext in [".xlsx", ".xls"]:
            fa = "fa-file-excel-o"
        elif ext in [".pdf"]:
            fa = "fa-file-pdf-o"
        elif ext in [".ppt", "pptx"]:
            fa = "fa-file-powerpoint-o"
        else:
            fa = "fa-file"

        data.append([f, fa, os.path.basename(f)])
    print data
    return data


def getSAN(value):
    if float(value) <= 11.9:
        return "#11c300", "Situacion Normal"
    else:
        if float(value) <= 47.5:
            return "#ffe132", "Alerta Temprana"
        else:
            if float(value) <= 83.6:
                return "#ff9936", "Crisis"
            else:
                if float(value) <= 100:
                    return "#ff1313", "Emergencia"


def valReport(self, month, year):
    mySession = DBSession()
    my_forms = mySession.query(FormsByUser.idforms).filter(FormsByUser.id_user == self.user.login)
    myDB = []
    if not my_forms is None:
        for row in my_forms:
            my_Pilars = mySession.query(Form).filter(Form.form_id == row.idforms).all()
            if not my_Pilars is None:
                for mp in my_Pilars:
                    myDB.append(mp.form_db)

    myDB = list(set(myDB))

    acum = []
    for i in myDB:
        muni = i.split("_")

        muni = " ".join(muni[1:]) + " " + self.user.login + "_"
        query = "SELECT COUNT(*) FROM %s.maintable WHERE MONTH(date_fecha_informe_6) = %s and YEAR (date_fecha_informe_6) = %s and surveyid like binary '%s' ;" % (
            i, str(month), str(year), "%" + muni + "%")
        result = mySession.execute(query).scalar()
        acum.append(int(result))
    mySession.close()
    if sum(acum) >= 1:
        return True
    else:
        return False


def fill_reg():
    res = {"munic": [], "insti": []}
    mySession = DBSession()
    result = mySession.query(Munic).all()
    for i in result:
        res["munic"].append([int(i.munic_id), str(i.munic_nombre).decode("latin1").encode("utf8")])
    result = mySession.query(Institucione).filter(Institucione.insti_id != 2).all()
    for i in result:
        res["insti"].append([int(i.insti_id), i.insti_nombre])
    mySession.close()
    return res


def getIntName(instId):
    mySession = DBSession()
    result = mySession.query(Institucione.insti_nombre).filter(Institucione.insti_id == instId).first()
    instName = result.insti_nombre
    mySession.close()
    return instName


def getMunicName(municId):
    mySession = DBSession()
    result = mySession.query(Munic.munic_nombre).filter(Munic.munic_id == municId).first()
    municName = result.munic_nombre
    mySession.close()
    return municName


def getMunicId(municName):
    mySession = DBSession()
    result = mySession.query(Munic.munic_id).filter(Munic.munic_nombre == municName).first()
    munic_id = result.munic_id
    mySession.close()
    return munic_id


def make_qr(repo, login, passw, uname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]

        config_data = {u'admin': {}, u'general': {u'username': uname, u'password': passw,
                                                  u'server_url': u'http://%s:6542/%s/%s' % (ip, login, uname),
                                                  u'metadata_username': uname}}
        qr_json = json.dumps(config_data)
        serialization = qr_json.encode('zlib_codec').encode('base64_codec')
        myCode = QR(data=serialization.replace("\n", ""))
        myCode.encode()

        img_path = os.path.join(repo, login, "user", uname, "config", "conf.png")

        os.system("mv " + myCode.filename + " " + img_path)
    except Exception as e:
        print e


def getSubmissionCount(fId):
    mySession = DBSession()

    result = mySession.query(Form.form_db).filter(Form.form_id == fId).first()

    result = mySession.execute("SELECT COUNT(*) FROM %s.maintable;" % result.form_db).scalar()

    return int(result)


def getForm_By_User(uname):
    mySession = DBSession()
    result = mySession.query(func.count(FormsByUser.idforms)).filter(FormsByUser.id_user == uname).scalar()
    return int(result)


def delUser(uname, login, request):
    mySession = DBSession()
    try:
        if getForm_By_User(uname) > 0:
            return ["Precaucion", "Este usuario no se puede elimiar porque esta relacionado a uno o mass formularios",
                    "warning"]

        transaction.begin()
        mySession.query(User).filter(User.user_name == uname).filter(User.user_parent == login).delete()
        transaction.commit()
        mySession.close()
        path = os.path.join(request.registry.settings["user.repository"],
                            *[login, "user", uname])
        shutil.rmtree(path, ignore_errors=True)
        mySession.close()
        return ["Correcto", "Usuario eliminado exitosamente", "success"]
    except:
        return ["Error", "No se pudo eliminar el usuario seleccinado", "error"]


def addNewUser(regDict, request, login):
    mySession = DBSession()

    res1 = mySession.query(LineasBase).filter(LineasBase.munic_id == regDict["munic"]).all()
    res2 = mySession.query(CoefPond).filter(CoefPond.munic_id == regDict["munic"]).all()

    if not res1 or not res2:
        return 4

    result = mySession.query(func.count(User.user_name)).filter(
        User.user_munic == int(regDict["munic"])).scalar()

    if not result is None:
        if result == 1:
            return 0
        else:
            if result == 0:
                addUser = User(user_fullname=regDict["fullname"],
                               user_name=regDict["user_name"],
                               user_joindate=str(t.now()),
                               user_password=encodeData(regDict["password"]),
                               user_email=regDict["email"],
                               user_munic=regDict["munic"],
                               user_active=1,
                               user_role=0,
                               user_parent=login)
                try:

                    transaction.begin()
                    mySession.add(addUser)
                    transaction.commit()
                    mySession.close()

                    # # create necessary files and directories
                    path = os.path.join(request.registry.settings["user.repository"],
                                        *[login, "user", regDict["user_name"], "config"])
                    os.makedirs(path)
                    #
                    # paths = [getIntName(regDict["inst"]) + "_" + getMunicName(regDict["munic"]).replace(" ", "") + "_" +
                    #          regDict[
                    #              "user_name"] + '.xml']

                    #
                    # xmlFile = os.path.join(path, *paths)
                    #
                    # pngFile = os.path.join(path, getIntName(regDict["inst"]).lower() + ".png")
                    #
                    # os.system("cp %s %s" % (
                    #     os.path.join(request.registry.settings["user.repository"], "forms", getIntName(regDict["inst"]),
                    #                  getIntName(regDict["inst"]) + ".xml"), xmlFile))
                    # os.system("cp %s %s" % (
                    #     os.path.join(request.registry.settings["user.repository"], "forms", getIntName(regDict["inst"]),
                    #                  getIntName(regDict["inst"]).lower() + ".png"), pngFile))
                    #
                    # paths = [getIntName(regDict["inst"]) + "_" + getMunicName(regDict["munic"]) + "_" + regDict[
                    #     "user_name"] + '.json']
                    # jsonFile = os.path.join(path, *paths)
                    #
                    # metadata = {}
                    # metadata["formID"] = getIntName(regDict["inst"]) + "_" + getMunicName(regDict["munic"])
                    # metadata["name"] = getIntName(regDict["inst"]) + "_" + getMunicName(regDict["munic"]) + "_" + \
                    #                    regDict[
                    #                        "user_name"]
                    # metadata["majorMinorVersion"] = "1.0"
                    # metadata["version"] = datetime.now().strftime("%Y%m%d")
                    # metadata["hash"] = 'md5:' + md5(open(xmlFile, 'rb').read()).hexdigest()
                    # metadata["descriptionText"] = getIntName(regDict["inst"]) + "_3" + getMunicName(
                    #     regDict["munic"]) + "_" + regDict["fullname"] + "_" + datetime.now().strftime("%Y%m%d")
                    #
                    # with open(jsonFile, "w") as outfile:
                    #     jsonString = json.dumps(metadata, indent=4, ensure_ascii=False).encode("utf8")
                    #     outfile.write(jsonString)
                    #
                    make_qr(request.registry.settings["user.repository"], login,
                            regDict["password"],
                            regDict["user_name"])

                    # create urban centers .csv file
                    result = mySession.query(CentrosUrbano.id_cu, CentrosUrbano.cu_name).filter_by(
                        munic_id=regDict["munic"]).all()
                    if result:
                        csv_curb = open(path.replace("config", "/curbanos.csv"), "w")
                        csv_curb.write("urban_id,urban_name\n")
                        for row in result:
                            csv_curb.write(str(row.id_cu) + "," + str(row.cu_name) + "\n")
                        csv_curb.close()

                    return 1

                except Exception, e:
                    print e
                    print Exception
                    transaction.abort()
                    mySession.close()
                    return 2
    return 3


def getComp(lb, act):
    if lb != "ND":
        try:
            lb = int(lb)
        except:
            lb = float(lb)
    try:
        act = int(act)
    except:
        act = float(act)

    if lb != "ND":
        if lb < act:
            return 1  # "Aumento"
        if lb > act:
            return 2  # "Disminuyo"
        if lb == act:
            return 3  # "Se mantiene"
    else:
        return 0


def getVarValue(db, code, month, year, uname):
    mySession = DBSession()
    ret = ""

    # try:
    result = mySession.execute(
        "SELECT AVG(%s) FROM %s.maintable WHERE MONTH(date_fecha_informe_6) = %s and YEAR (date_fecha_informe_6) = %s and surveyid like binary '%s' LIMIT 1;" % (
            code, db, month, year, "% " + uname + "_%"))
    for res in result:
        ret = str(res[0])
    # except:
    #    ret = "ND"
    mySession.close()
    return ret


def getComun(db, code, month, year, uname):
    mySession = DBSession()
    ret = ""

    # try:
    result = mySession.execute(
        "SELECT %s FROM %s.maintable WHERE MONTH(date_fecha_informe_6) = %s and YEAR (date_fecha_informe_6) = %s and surveyid like binary '%s' LIMIT 1;" % (
            code, db, month, year, "% " + uname + "_%"))
    for res in result:
        ret = str(res[0])
    # except:
    #    ret = "ND"
    mySession.close()
    return ret


def getCoefPond(idVar, munId):
    mySession = DBSession()

    result = mySession.query(CoefPond.coef_valor).filter(CoefPond.id_variables_ind == idVar).filter(
        CoefPond.munic_id == getMunicId(munId)).first()
    res = result.coef_valor
    mySession.close()
    return res


def calcValue(val, idVar,
              type,
              munId):  # if type = 2 calc Equivalent values elif type == 1 calc Weighting coefficient, if type =3 get pilar coeff
    mySession = DBSession()
    res = ""
    if type == 1:
        res = getCoefPond(idVar, munId)
    elif type == 2:
        sql = "CALL sesan_v2.getValueGroup(%s, %s);" % (idVar, val)
        result = mySession.execute(sql)
        for res in result:
            res = str(res[0])
    elif type == 3:
        result = mySession.query(Pilare.coef_pond).filter_by(name_pilarers=idVar).first()
        res = result.coef_pond

    mySession.close()
    return float(res)


def getAlertVar(valGrp, type):  # type, if i need the value of the group or the id of group
    # #ff1313 rojo#}
    # #ff9936 naranja#}
    # #ffe132 amarillo#}
    # #11c300 verde #}
    mySession = DBSession()
    if type == 1:
        result = mySession.query(Grupo.id_grupos, Grupo.name_grupos).filter_by(val_grupos=valGrp).first()
    if type == 2:
        result = mySession.query(Grupo.id_grupos, Grupo.name_grupos).filter_by(id_grupos=valGrp).first()
    if not result is None:
        if int(result[0]) == 1:
            return ["#11c300", result[1]]
        else:
            if int(result[0]) == 2:
                return ["#ffe132", result[1]]
            else:
                if int(result[0]) == 3:
                    return ["#ff9936", result[1]]
                else:
                    if int(result[0]) == 4:
                        return ["#ff1313", result[1]]


def getPilarAlert(idP, indP):
    mySession = DBSession()
    result = mySession.query(func.min(RangosPilare.id_grupo)).filter(RangosPilare.id_pilares == idP).filter(
        RangosPilare.nivel_afec >= float(indP)).first()
    mySession.close()
    return getAlertVar(int(result[0]), 2)


def getRepInfo(ruuid, db, type):
    mySession = DBSession()
    ret = []
    query = ""
    if type == "com":
        query = "SELECT @a:=@a+1 No, lk.sem_comunidad_totales_des FROM (select @a:=0) r, %s.maintable_msel_sem_af_comunidad ma,%s.lkpsem_comunidad_totales lk where ma.sem_af_comunidad=lk.sem_comunidad_totales_cod and ma.device_id_3 = '%s'" % (
            db, db, ruuid)
    if type == "acc":
        query = "SELECT repeat_prop_acciones_rowid, txt_prop_acciones_25 FROM %s.repeat_prop_acciones where device_id_3 = '%s';" % (
            db, ruuid)
    result = mySession.execute(query)
    if not result is None:
        for res in result:
            ret.append([str(int(res[0])), str(res[1]).title()])
    else:
        return None

    return ret


def getLB(id_var, munic):
    mySession = DBSession()
    result = mySession.query(LineasBase.lb_valor).filter(LineasBase.munic_id == getMunicId(munic)).filter(
        LineasBase.id_variables_ind == id_var).first()
    if result:
        lb_valor = result.lb_valor
    else:
        lb_valor = "ND"

    mySession.close()
    return lb_valor


def getDashReportData(self, month, year):
    # month = "05"
    # year = "2018"

    mySession = DBSession()
    data = {}

    my_forms = mySession.query(FormsByUser.idforms).filter(FormsByUser.id_user == self.user.login)
    res = []
    myDB = []
    if not my_forms is None:
        for row in my_forms:
            my_Pilars = mySession.query(Form).filter(Form.form_id == row.idforms).all()
            if not my_Pilars is None:
                for mp in my_Pilars:
                    myDB.append(mp.form_db)
                    mp = mp.pilar_id.split(",")
                    for m in mp:
                        res.append(m)

    res = list(set(res))
    myDB = list(set(myDB))

    resI = []
    for idP in res:
        my_Ind = mySession.query(Indicadore).filter(Indicadore.Id_pilares == int(idP)).all()
        if not my_Ind is None:
            for mI in my_Ind:
                resI.append(mI.id_indicadores)

    variables = mySession.query(VariablesInd).filter(VariablesInd.id_indicadores.in_(resI)).all()
    indicadores = []
    pilares = []

    for var in variables:
        if int(var.id_indicadores) not in indicadores:
            indicadores.append(int(var.id_indicadores))
    data["signatures"] = []
    data["comunidades2"] = []
    for db in myDB:

        result = mySession.execute(
            "SELECT COUNT(*) FROM %s.maintable WHERE MONTH(date_fecha_informe_6) = %s and YEAR (date_fecha_informe_6) = %s and surveyid like binary '%s' ;" % (
                db, month, year, "% " + self.user.login + "_%")).scalar()

        pilares_ind_db = mySession.query(Form.pilar_id).filter(Form.form_db == db).first()
        pilares_ind_db = pilares_ind_db[0].split(",")

        if int(result) != 0:
            for i in indicadores:
                i_pi = mySession.query(Indicadore.Id_pilares).filter_by(id_indicadores=i).first()

                if str(int(i_pi[0])) in pilares_ind_db:
                    p_name = mySession.query(Pilare.name_pilares, Pilare.id_pilares).filter_by(
                        id_pilares=int(i_pi[0])).first()
                    tot_alert = []
                    data[p_name[0]] = {}  # add pilar
                    i_name = mySession.query(Indicadore.name_indicadores, Indicadore.id_indicadores).filter_by(
                        Id_pilares=int(i_pi[0])).all()

                    for i_n in i_name:
                        # print i_n[0]
                        data[p_name[0]][i_n[0]] = {"var": [], "val": []}  # add indicadores
                        variables = mySession.query(VariablesInd).filter_by(id_indicadores=int(i_n[1])).all()
                        valCP = 1
                        acum = []
                        for v in variables:
                            # print v.code_variable_ind
                            sa = getVarValue(db, v.code_variable_ind, month, year, self.user.login)

                            # add variables data

                            if sa != "ND":
                                l_base = getLB(v.id_variables_ind, self.user.munic)

                                data[p_name[0]][i_n[0]]["var"].append(
                                    [v.name_variable_ind, v.unidad_variable_ind, l_base, sa,
                                     getComp(l_base, sa),
                                     getAlertVar(calcValue(sa, v.id_variables_ind, 2, self.user.munic), 1),
                                     v.code_variable_ind])
                                valCP = valCP + calcValue(sa, v.id_variables_ind, 1, self.user.munic)

                                acum.append(calcValue(sa, v.id_variables_ind, 1, self.user.munic) * calcValue(sa,
                                                                                                              v.id_variables_ind,
                                                                                                              2,
                                                                                                              self.user.munic))

                        tot_alert.append([valCP, sum(acum)])
                        # print "**-*-*-*-*-*\n\n\n\n\n\n\n"
                        # print db
                        # print valCP
                        # print v.id_variables_ind
                        # print "%.2f" % (sum(acum))
                        # print "**-*-*-*-*-*\n\n\n\n\n\n\n"
                        data[p_name[0]][i_n[0]]["val"].append("%.2f" % (sum(acum) / valCP))
                        # data[p_name[0]][i_n[0]]["val"].append("CCCC")
                    pilares.append(int(i_pi[0]))
                    # print tot_alert
                    t0 = 0
                    t1 = 0
                    for t in tot_alert:
                        t0 = t0 + t[0]
                        t1 = t1 + t[1]
                    alertP = getPilarAlert(p_name[1], "%.2f" % (t1 / t0))

                    data[p_name[0] + "_alert"] = ["%.2f" % (t1 / t0), alertP[1].title(), alertP[0]]
            # (db, uname, parent, month, year, request)
            data["signatures"].append(getSignature(db, self.user.login, self.user.parent, month, year, self.request))

            ruuid = getComun(db, "device_id_3", month, year, self.user.login)
            # data["comunidades"] = getRepInfo(ruuid, db, "com")
            com = getComun(db, "sem_comunidad_totales", month, year, self.user.login).split(" ")
            # data["comunidades2"] = []

            for id_cu in com:
                data["comunidades2"].append(getPob4Map(id_cu, alertP[0]))
            # data["acciones"] = getRepInfo(ruuid,db, "acc")
            data["coverage"] = calcDataCoverage(db, ruuid, getMunicId(self.user.munic))


            # else:
            #    data["error"] = True

    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
             "Noviembre", "Diciembre"]

    data["date"] = [meses[int(month) - 1], year]
    # import json
    # r = json.dumps(unicode(data),ensure_ascii=False,encoding='utf8')
    # with open("/home/acoto/pr_pptx/sort_db/data.json", 'wb') as f:
    #    json.dump(r,f, ensure_ascii=False, encoding='utf8')
    mySession.close()

    for i, s in enumerate(data["comunidades2"]):
        # if (s[0] not in data["comunidades2"]):
        data["comunidades2"][i] = s[0]
    # print list(set(data["comunidades2"]))




    return data


def getSignature(db, uname, parent, month, year, request):
    # if rol == "tec":
    mySession = DBSession()
    result = mySession.execute(
        "SELECT txt_rep_muni_comusan_4,img_sig_resp FROM %s.maintable WHERE MONTH(date_fecha_informe_6) = %s and YEAR (date_fecha_informe_6) = %s and surveyid like binary '%s' LIMIT 1;" % (
            db, month, year, "% " + uname + "_%")).first()

    img_path = os.path.join(request.registry.settings["user.repository"],
                            *[parent, "user", uname, "data", "xml", result[1]])  # "_".join(db.split("_")[2:]),

    f = open(img_path)
    data = f.read()
    f.close()
    img = base64.b64encode(data)
    return ["data:image/png;base64,%s" % img, result[0], "_".join(db.split("_")[2:])]
    # return [ result[0],"_".join(db.split("_")[2:]) ]


def getConfigQR(uname, parent, request):
    img_path = os.path.join(request.registry.settings["user.repository"],
                            *[parent, "user", uname, "config", "conf.png"])
    f = open(img_path)
    data = f.read()
    f.close()
    img = base64.b64encode(data)
    return "data:image/png;base64,%s" % img


def getBaselines(munic, flag):
    # print munic
    mySession = DBSession()
    if flag == "lb":
        query = "select v.id_variables_ind, v.name_variable_ind, i.name_indicadores, l.lb_valor from variables_ind v, lineas_base l, indicadores i where v.id_variables_ind = l.id_variables_ind and v.id_indicadores=i.id_indicadores and l.munic_id =%s;" % munic
    else:
        if flag == "cf":
            query = "select v.id_variables_ind, v.name_variable_ind, i.name_indicadores, l.coef_valor from variables_ind v, coef_pond l, indicadores i where v.id_variables_ind = l.id_variables_ind and v.id_indicadores=i.id_indicadores and l.munic_id =%s;" % munic

    # print query
    result = mySession.execute(query)
    data = {}
    if result:
        for row in result:
            data[int(row[0])] = {"id": str(int(row[0])), "var": row[1], "ind": row[2], "val": str(int(row[3]))}
    mySession.close()
    return data


def getBaselinesName():
    mySession = DBSession()
    query = "select v.id_variables_ind, v.name_variable_ind, i.name_indicadores from variables_ind v, indicadores i where v.id_indicadores=i.id_indicadores;"
    result = mySession.execute(query)
    data = {"vals": []}
    if result:
        for row in result:
            data["vals"].append({"id": int(int(row[0])), "var": row[1], "ind": row[2]})

    return data


def newBaseline(data, flag):
    mySession = DBSession()
    data = data.split("*")
    # print "insert"
    try:
        for row in data[:-1]:
            if row[0] == ",":
                row = row[1:]

            row = row.split(",")
            if flag == "lb":
                newLB = LineasBase(munic_id=row[1], id_variables_ind=row[0], lb_valor=row[2])
            elif flag == "cf":
                newLB = CoefPond(munic_id=row[1], id_variables_ind=row[0], coef_valor=row[2])

            transaction.begin()
            mySession.add(newLB)
            transaction.commit()
            # mySession.close()
        mySession.close()
        return ["Correcto", "Datos registrados exitosamente", "success"]
    except:
        return ["Error", "Ya existe un usuario para esa institucion en el municipio seleccionado", "error"]


def userInMunic(mun_id):
    mySession = DBSession()
    result = mySession.query(func.count(User.user_munic)).filter(User.user_munic == mun_id).scalar()
    return int(result)


def delete_lb(mun_id, flag):
    mySession = DBSession()
    try:

        if userInMunic(mun_id) >= 1:
            if flag == "lb":
                return ["Precaucion", "Esta linea base no se puede elimiar porque hay usuarios relacionados a ella",
                        "warning"]
            elif flag == "cf":
                return ["Precaucion",
                        "Estos coeficientes de ponderacion no se puede elimiar porque hay usuarios relacionados a ellos",
                        "warning"]

        transaction.begin()
        if flag == "lb":
            mySession.query(LineasBase).filter(LineasBase.munic_id == mun_id).delete()
        elif flag == "cf":
            mySession.query(CoefPond).filter(CoefPond.munic_id == mun_id).delete()
        transaction.commit()
        mySession.close()

        return ["Correcto", "Datos eliminados exitosamente", "success"]
    except:
        return ["Error", "No se pudo eliminar la linea base para este municipio", "error"]


def updateData(mun_id, data, flag):
    data = data.split("*")
    mySession = DBSession()
    try:
        for row in data[:-1]:
            if row[0] == ",":
                row = row[1:]
            row = row.split(",")
            transaction.begin()

            if flag == "lb":  # update baseline
                mySession.query(LineasBase).filter(LineasBase.munic_id == row[1]).filter(
                    LineasBase.id_variables_ind == row[0]).update({LineasBase.lb_valor: row[2]})
            elif flag == "cf":  # update weighing
                mySession.query(CoefPond).filter(CoefPond.munic_id == row[1]).filter(
                    CoefPond.id_variables_ind == row[0]).update({CoefPond.coef_valor: row[2]})

            transaction.commit()
        mySession.close()
        return ["Correcto", "Datos actualizados exitosamente", "success"]
    except:
        return ["Error", "Error al actualizar los datos", "error"]


def calcDataCoverage(db, device_id_3, mun_id):
    mySession = DBSession()
    query = "SELECT (100/count(*)) * (select count(sem_comunidad_totales) from %s.maintable_msel_sem_comunidad_totales where device_id_3 ='%s')  FROM sesan_v2.centros_urbanos where munic_id=%s;" % (
        db, device_id_3, mun_id)
    result = mySession.execute(query).scalar()
    if result:
        return int(result)
    else:
        return False


def genXLS(self, data, month):
    data.pop('signatures', None)

    path = os.path.join(self.request.registry.settings['user.repository'], "TMP", "datos_reporte.xlsx")

    workbook = xlsxwriter.Workbook(path)

    pilares = []
    workbook = xlsxwriter.Workbook(path)

    worksheet = workbook.add_worksheet("Metadata")

    san = dataReport(self, month, data["date"][1])
    data["san"]=san["san"]
    # worksheet.write(y, x, str)
    worksheet.write(0, 0, "Sala Situacional para el mes de %s, %s" % (data["date"][0], data["date"][1]))
    worksheet.write(1, 0, "Municipio: " + str(self.user.munic).title())
    # worksheet.write(2, 0, "Institucion que reporta: " + str(self.user.organization))
    worksheet.write(3, 0, "Cobertura en comunidades: " + str(data["coverage"]) + "%")

    color = ["#11c300", "#ffe132", "#ff9936", "#ff1313"]

    worksheet = workbook.add_worksheet("Rangos Criticos")
    worksheet2 = workbook.add_worksheet("Datos de monitoreo")
    worksheet3 = workbook.add_worksheet("Reporte de SSM")

    format = workbook.add_format({'bg_color': "#d0d0d0", "top": 1, "bottom": 1, "left": 1, "right": 1})

    worksheet.write(1, 0, "Pilar", format)
    worksheet.write(1, 1, "Indicador", format)
    worksheet.write(1, 2, "Variable", format)
    worksheet.write(1, 3, "Unidad de medida", format)

    format = workbook.add_format({'bg_color': color[0], "top": 1, "bottom": 1, "left": 1, "right": 1})
    worksheet.merge_range("E2:F2", "Sin Afectacion", format)
    format = workbook.add_format({'bg_color': color[1], "top": 1, "bottom": 1, "left": 1, "right": 1})
    worksheet.merge_range("G2:H2", "Afectacion Moderada", format)
    format = workbook.add_format({'bg_color': color[2], "top": 1, "bottom": 1, "left": 1, "right": 1})
    worksheet.merge_range("I2:J2", "Afectacion Alta", format)
    format = workbook.add_format({'bg_color': color[3], "top": 1, "bottom": 1, "left": 1, "right": 1})
    worksheet.merge_range("K2:L2", "Afectacion Muy Alta", format)

    format = workbook.add_format({'bg_color': "#d0d0d0", "top": 1, "bottom": 1, "left": 1, "right": 1})
    worksheet2.write(1, 0, "Pilar", format)
    worksheet2.write(1, 1, "Indicador", format)
    worksheet2.write(1, 2, "Variable", format)
    worksheet2.write(1, 3, "Unidad de medida", format)
    worksheet2.write(1, 4, "Linea Base", format)
    worksheet2.write(1, 5, "Situacion actual", format)
    worksheet2.write(1, 6, "Institucion responsable", format)
    worksheet2.write(1, 7, "Comparativo mensual", format)

    worksheet3.merge_range("A1:H1", "Reporte Municipal de Situacion General de SAN con base a la Sala Situacional ",
                           format)
    worksheet3.write(1, 0, "Indice de Situacion General de SAN", format)
    worksheet3.write(1, 1, "situacion actual", format)
    worksheet3.write(1, 2, "Indice de afectacion por pilar", format)
    worksheet3.write(1, 3, "Situacion actual ", format)
    worksheet3.write(1, 4, "Indice de afectacion por indicador", format)
    worksheet3.write(1, 5, "Situacion actual", format)
    worksheet3.write(1, 6, "Afectacion por variable", format)
    worksheet3.write(1, 7, "Situacion actual", format)

    ##99CC66

    row = 2
    cont = 3

    for p in data.keys():
        if "_alert" not in p and "date" not in p and "signatures" not in p and p not in ["comunidades", "acciones",
                                                                                         "coverage", "comunidades2",
                                                                                         "san"]:
            init = row + 1
            for d in data[p]:
                init2 = row + 1
                # print data[p][d]
                for v in data[p][d]["var"]:
                    cont = cont + 1
                    format = workbook.add_format({'bg_color': "#99CC66", "top": 1, "bottom": 1, "left": 1, "right": 1})
                    worksheet.write(row, 2, v[0].decode("utf-8").replace("_", " "), format)
                    worksheet.write(row, 3, v[1].decode("utf-8").replace("_", " "), format)
                    rang = getRanges(v[6], 1)
                    for col, r in enumerate(rang):
                        format = workbook.add_format({"top": 1, "bottom": 1, "left": 1, "right": 1})
                        worksheet.write(row, col + 4, r, format)

                    format = workbook.add_format({'bg_color': "#99CC66", "top": 1, "bottom": 1, "left": 1, "right": 1})
                    worksheet2.write(row, 2, v[0].decode("utf-8").replace("_", " "), format)
                    worksheet2.write(row, 3, v[1].decode("utf-8").replace("_", " "), format)
                    worksheet2.write(row, 4, v[2], format)
                    worksheet2.write(row, 5, float(v[3].decode("utf-8").replace("_", " ")), format)

                    worksheet3.write(row, 6, v[0].decode("utf-8").replace("_", " "), format)
                    worksheet3.write(row, 7, float(v[3].decode("utf-8").replace("_", " ")), format)

                    state = ""
                    if int(v[4]) == 1:
                        state = "Aumento"
                    elif int(v[4]) == 2:
                        state = "Disminuyo"
                    elif int(v[4]) == 3:
                        state = "Se mantiene"
                    elif int(v[4] == 4):
                        state = "ND"
                    format = workbook.add_format({"top": 1, "bottom": 1, "left": 1, "right": 1})
                    worksheet2.write(row, 7, state, format)

                    row = row + 1
                format = workbook.add_format({'bg_color': "#99CC66", "top": 1, "bottom": 1, "left": 1, "right": 1})
                if init2 != row:
                    worksheet.merge_range('B%s:B%s' % (init2, row), d.decode("utf-8").replace("_", " "), format)
                    worksheet2.merge_range('B%s:B%s' % (init2, row), d.decode("utf-8").replace("_", " "), format)
                    worksheet3.merge_range('E%s:E%s' % (init2, row), d.decode("utf-8").replace("_", " "), format)
                    worksheet3.merge_range('F%s:F%s' % (init2, row), data[p][d]["val"][0], format)

                else:
                    worksheet.write(row - 1, 1, d.decode("utf-8").replace("_", " "), format)
                    worksheet2.write(row - 1, 1, d.decode("utf-8").replace("_", " "), format)
                    worksheet3.write(row - 1, 4, d.decode("utf-8").replace("_", " "), format)
                    worksheet3.write(row - 1, 5, data[p][d]["val"][0], format)

            format = workbook.add_format({"top": 1, "bottom": 1, "left": 1, "right": 1})
            worksheet.merge_range('A%s:A%s' % (init, row), p.decode("utf-8"), format)
            worksheet2.merge_range('A%s:A%s' % (init, row), p.decode("utf-8"), format)
            worksheet3.merge_range('C%s:C%s' % (init, row), p.decode("utf-8"), format)
            worksheet3.merge_range('D%s:D%s' % (init, row), data[p + "_alert"][0], format)

            worksheet2.merge_range('G%s:G%s' % (init, row), "SESAN", format)

    format = workbook.add_format({"align": "center", "valign": "center"})
    worksheet3.merge_range('A%s:A%s' % (3, cont - 1), data["san"][2], format)
    worksheet3.merge_range('B%s:B%s' % (3, cont - 1), data["san"][0], format)

    workbook.close()

    response = FileResponse(path, request=self.request)
    headers = response.headers
    headers['Content-Type'] = 'application/download'
    headers['Accept-Ranges'] = 'bite'
    headers['Content-Disposition'] = 'attachment;filename=' + "datos_reporte.xlsx"
    return response


def getFileResponse(request):
    name = str(request.url).split("/")[-1:][0].replace("%20", " ")
    response = FileResponse(request.registry.settings['user.repository'] + "help_files/" + name, request=request)
    headers = response.headers
    headers['Content-Type'] = 'application/download'
    headers['Accept-Ranges'] = 'bite'
    headers['Content-Disposition'] = 'attachment;filename=' + name.replace(" ", "_")
    return response


def getUsersList(login):
    mySession = DBSession()
    result = mySession.query(User).filter(User.user_parent == login).all()
    data = []
    for row in result:
        data.append([row.user_fullname, row.user_name, row.user_email, getMunicName(row.user_munic).title()])
    mySession.close()

    return data


def getRanges(code, munic):
    print "*-*-*-"
    print code
    print munic
    print "*-*-*"
    mySession = DBSession()


    result= mySession.query()
    rang = [0, 10, 11, 15, 16, 22, 23, 100]

    return rang
