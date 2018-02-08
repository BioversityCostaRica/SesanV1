from ..models import DBSession, Institucione, Munic, User, VariablesInd, Pilare, Indicadore, Grupo, RangosPilare, \
    LineasBase, CentrosUrbano
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

from sqlalchemy import or_

def getPob4Map(id_cu, alert):
    mySession = DBSession()

    result = mySession.query(CentrosUrbano).filter(CentrosUrbano.id_cu==id_cu).first()
    data={"vals":[]}
    if result:
        data["vals"].append(([str(result.categoria).title(),str(result.cu_name).title(), float(result.Y), float(result.X), alert ]))


    mySession.close()

    return data


def dataReport(self, month, year):
    mySession = DBSession()

    prec_uname = ""
    des_uname = ""
    mides_uname = ""

    valEqui = []
    coefPon = []
    unames=[]

    inst_idS = mySession.query(Institucione).filter(Institucione.insti_id != 2).filter(Institucione.insti_id != 5).all()
    data = {}
    for inst_id in inst_idS:
        res = inst_id.insti_id
        if int(res) == 4:
            variables = mySession.query(VariablesInd).filter(or_(VariablesInd.insti_id == res, VariablesInd.insti_id == 5)).all()

        else:
            variables = mySession.query(VariablesInd).filter_by(insti_id=res).all()
        indicadores = []
        pilares = []

        result = mySession.query(Munic.munic_id).filter(Munic.munic_nombre == self.user.munic).first()
        municId = result.munic_id
        result = mySession.query(User.user_name).filter(User.user_organization == res).filter(
            User.user_munic == municId).first()
        tmp_uname = result.user_name
        if inst_id.insti_id == 4:
            prec_uname = tmp_uname
            result = mySession.query(User.user_name).filter(User.user_organization == 5).filter(
                User.user_munic == municId).first()
            mides_uname = result.user_name
        if inst_id.insti_id == 1:
            des_uname = tmp_uname



        for var in variables:
            if int(var.id_indicadores) not in indicadores:
                indicadores.append(int(var.id_indicadores))

        for i in indicadores:
            i_pi = mySession.query(Indicadore.Id_pilares).filter_by(id_indicadores=i).first()
            if int(i_pi[0]) not in pilares:
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
                        sa = getVarValue(inst_id.insti_nombre, v.code_variable_ind, month, year, tmp_uname)


                        # add variables data

                        if sa != "ND":
                            valCP = valCP + calcValue(sa, v.id_variables_ind, 1)

                            acum.append(calcValue(sa, v.id_variables_ind, 1) * calcValue(sa, v.id_variables_ind, 2))

                        else:
                            sa = getVarValue("MIDES", v.code_variable_ind, month, year, mides_uname)
                            valCP = valCP + calcValue(sa, v.id_variables_ind, 1)

                            acum.append(calcValue(sa, v.id_variables_ind, 1) * calcValue(sa, v.id_variables_ind, 2))


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

                unames.append([inst_id.insti_nombre, tmp_uname,alertP[0]])

                result = mySession.query(Grupo.val_grupos).filter(float("%.2f" % (t1 / t0)) <= Grupo.val_grupos).first()
                valEqui.append(int(result.val_grupos))
                result = mySession.query(Pilare.coef_pond).filter(Pilare.name_pilares == p_name[0]).first()
                coefPon.append(int(result.coef_pond))


        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
                 "Noviembre", "Diciembre"]

        des = int(float(getVarValue("MSPAS", "dec_mi_nutri_edas_8", month, year, des_uname)))

        data["date"] = [meses[int(month) - 1], year, self.user.munic]
        data["plt_values"] = {"lluvia": "%s-%s" % (str(monthrange(int(year), int(month))[1]),
                                                   str(int(getVarValue("MAGA", "int_dia_sin_lluvia", month, year,
                                                                       prec_uname)))),
                              "nin_des": "%s-%s" % (str(des), str(100 - des))}


    mySession.close()

    tot_ValAgg = []
    for a, b in zip(coefPon, valEqui):
        tot_ValAgg.append(a * b)

    san = "%.2f" % (sum(tot_ValAgg) / float(sum(coefPon)))
    data["san"] = [san, getSAN(san)[0], getSAN(san)[1]]

    data["points"] =[]
    for o in unames:
        for x in getVarValue(o[0], "sem_af_comunidad", month, year, o[1]).split((" ")):
            data["points"].append(getPob4Map(x, o[2]))




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
    insti = ["MIDES", "CONALFA", "MSPAS", "MAGA"]
    munic = self.user.munic
    acum = []
    for i in insti:
        query = "SELECT COUNT(*) FROM DATA_%s.maintable WHERE MONTH(date_fecha_informe_6) = %s and YEAR (date_fecha_informe_6) = %s and surveyid like binary '%s' ;" % (
            i, str(month), str(year), "%" + munic + "%")

        result = mySession.execute(query).scalar()
        acum.append(int(result))
    mySession.close()
    if sum(acum) == len(insti):
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


def make_qr(repo, org, passw, uname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]

        config_data = {u'admin': {}, u'general': {u'username': uname, u'password': passw,
                                                  u'server_url': u'http://%s:6542/%s/%s' % (ip, org, uname),
                                                  u'metadata_username': uname}}
        qr_json = json.dumps(config_data)
        serialization = qr_json.encode('zlib_codec').encode('base64_codec')
        myCode = QR(data=serialization.replace("\n", ""))
        myCode.encode()

        os.makedirs(os.path.join(repo, org, uname, "config"))
        img_path = os.path.join(repo, org, uname, "config", "conf.png")

        os.system("mv " + myCode.filename + " " + img_path)
    except Exception as e:

        print e


def addNewUser(regDict, request):
    mySession = DBSession()
    result = mySession.query(func.count(User.user_name)).filter(User.user_organization == int(regDict["inst"])).filter(
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
                               user_organization=regDict["inst"])
                try:

                    transaction.begin()
                    mySession.add(addUser)
                    transaction.commit()
                    mySession.close()
                    # create necessary files and directories
                    path = os.path.join(request.registry.settings["user.repository"],
                                        *[getIntName(regDict["inst"]), regDict["user_name"]])

                    paths = [getIntName(regDict["inst"]) + "_" + getMunicName(regDict["munic"]).replace(" ", "") + "_" +
                             regDict[
                                 "user_name"] + '.xml']
                    os.makedirs(path)

                    xmlFile = os.path.join(path, *paths)

                    pngFile = os.path.join(path, getIntName(regDict["inst"]).lower() + ".png")

                    os.system("cp %s %s" % (
                        os.path.join(request.registry.settings["user.repository"], "forms", getIntName(regDict["inst"]),
                                     getIntName(regDict["inst"]) + ".xml"), xmlFile))
                    os.system("cp %s %s" % (
                        os.path.join(request.registry.settings["user.repository"], "forms", getIntName(regDict["inst"]),
                                     getIntName(regDict["inst"]).lower() + ".png"), pngFile))

                    paths = [getIntName(regDict["inst"]) + "_" + getMunicName(regDict["munic"]) + "_" + regDict[
                        "user_name"] + '.json']
                    jsonFile = os.path.join(path, *paths)

                    metadata = {}
                    metadata["formID"] = getIntName(regDict["inst"]) + "_" + getMunicName(regDict["munic"])
                    metadata["name"] = getIntName(regDict["inst"]) + "_" + getMunicName(regDict["munic"]) + "_" + \
                                       regDict[
                                           "user_name"]
                    metadata["majorMinorVersion"] = "1.0"
                    metadata["version"] = datetime.now().strftime("%Y%m%d")
                    metadata["hash"] = 'md5:' + md5(open(xmlFile, 'rb').read()).hexdigest()
                    metadata["descriptionText"] = getIntName(regDict["inst"]) + "_3" + getMunicName(
                        regDict["munic"]) + "_" + regDict["fullname"] + "_" + datetime.now().strftime("%Y%m%d")

                    with open(jsonFile, "w") as outfile:
                        jsonString = json.dumps(metadata, indent=4, ensure_ascii=False).encode("utf8")
                        outfile.write(jsonString)

                    make_qr(request.registry.settings["user.repository"], getIntName(regDict["inst"]),
                            regDict["password"],
                            regDict["user_name"])

                    # create urban centers .csv file
                    result = mySession.query(CentrosUrbano.id_cu, CentrosUrbano.cu_name).filter_by(
                        munic_id=regDict["munic"]).all()
                    if result:
                        csv_curb = open(path + "/curbanos.csv", "w")
                        csv_curb.write("urban_id,urban_name\n")
                        for row in result:
                            csv_curb.write(str(row.id_cu) + "," + str(row.cu_name) + "\n")
                        csv_curb.close()

                    return 1

                except Exception, e:
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


def getVarValue(org, code, month, year, uname):
    mySession = DBSession()
    ret = ""

    try:
        result = mySession.execute(
            "SELECT %s FROM DATA_%s.maintable WHERE MONTH(date_fecha_informe_6) = %s and YEAR (date_fecha_informe_6) = %s and surveyid like binary '%s' LIMIT 1;" % (
                code, org, month, year, "%" + uname + "%"))
        for res in result:
            ret = str(res[0])
    except:
        ret = "ND"
    mySession.close()
    return ret


def calcValue(val, idVar,
              type):  # if type = 2 calc Equivalent values elif type == 1 calc Weighting coefficient, if type =3 get pilar coeff
    mySession = DBSession()
    res = ""
    if type == 1:
        result = mySession.query(VariablesInd.coef_pond).filter_by(id_variables_ind=idVar).first()
        res = result.coef_pond
    elif type == 2:
        sql = "CALL sesan_v1.getValueGroup(%s, %s);" % (idVar, val)
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


def getRepInfo(ruuid, org, type):
    mySession = DBSession()
    ret = []
    query = ""
    if type == "com":
        query = "SELECT @a:=@a+1 No, lk.sem_comunidad_totales_des FROM (select @a:=0) r, DATA_%s.maintable_msel_sem_af_comunidad ma,DATA_%s.lkpsem_comunidad_totales lk where ma.sem_af_comunidad=lk.sem_comunidad_totales_cod and ma.device_id_3 = '%s'" % (
            org,org, ruuid)
    if type == "acc":
        query = "SELECT repeat_prop_acciones_rowid, txt_prop_acciones_25 FROM DATA_%s.repeat_prop_acciones where device_id_3 = '%s';" % (
            org, ruuid)
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
    # month = "08"
    # year = "2017"

    mySession = DBSession()
    inst_id = mySession.query(Institucione).filter_by(insti_nombre=self.user.organization).first()
    data = {}
    if not inst_id is None:
        res = inst_id.insti_id

    variables = mySession.query(VariablesInd).filter_by(insti_id=res).all()
    indicadores = []
    pilares = []

    for var in variables:
        if int(var.id_indicadores) not in indicadores:
            indicadores.append(int(var.id_indicadores))
    result = mySession.execute(
        "SELECT COUNT(*) FROM DATA_%s.maintable WHERE MONTH(date_fecha_informe_6) = %s and YEAR (date_fecha_informe_6) = %s and surveyid like binary '%s' ;" % (
            self.user.organization, month, year, "%" + self.user.login + "%")).scalar()

    if int(result) != 0:
        for i in indicadores:
            i_pi = mySession.query(Indicadore.Id_pilares).filter_by(id_indicadores=i).first()
            if int(i_pi[0]) not in pilares:
                p_name = mySession.query(Pilare.name_pilares, Pilare.id_pilares).filter_by(
                    id_pilares=int(i_pi[0])).first()
                tot_alert = []
                data[p_name[0]] = {}  # add pilar
                if self.user.organization == "MIDES":
                    i_name = mySession.query(Indicadore.name_indicadores, Indicadore.id_indicadores).filter_by(
                        id_indicadores=int(i)).all()
                else:
                    i_name = mySession.query(Indicadore.name_indicadores, Indicadore.id_indicadores).filter_by(
                        Id_pilares=int(i_pi[0])).all()

                for i_n in i_name:
                    # print i_n[0]
                    data[p_name[0]][i_n[0]] = {"var": [], "val": []}  # add indicadores
                    variables = mySession.query(VariablesInd).filter_by(id_indicadores=int(i_n[1])).all()
                    valCP = 0
                    acum = []
                    for v in variables:
                        sa = getVarValue(self.user.organization, v.code_variable_ind, month, year, self.user.login)
                        # add variables data

                        if sa != "ND":
                            l_base = getLB(v.id_variables_ind, self.user.munic)

                            data[p_name[0]][i_n[0]]["var"].append(
                                [v.name_variable_ind, v.unidad_variable_ind, l_base, sa,
                                 getComp(l_base, sa),
                                 getAlertVar(calcValue(sa, v.id_variables_ind, 2), 1)])
                            valCP = valCP + calcValue(sa, v.id_variables_ind, 1)

                            acum.append(calcValue(sa, v.id_variables_ind, 1) * calcValue(sa, v.id_variables_ind, 2))

                    tot_alert.append([valCP, sum(acum)])
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
        data["signatures"] = [getSignature(self.user.login, self.user.organization, month, year, "rep", self.request),
                              getSignature(self.user.login, self.user.organization, month, year, "tec", self.request)]
        ruuid = getVarValue(self.user.organization, "device_id_3", month, year, self.user.login)
        data["comunidades"] = getRepInfo(ruuid, self.user.organization, "com")
        com=getVarValue(self.user.organization, "sem_af_comunidad", month, year, self.user.login).split(" ")
        data["comunidades2"]=[]
        for id_cu in com:
            data["comunidades2"].append(getPob4Map(id_cu, alertP[0]))
        data["acciones"] = getRepInfo(ruuid, self.user.organization, "acc")
        data["coverage"]=calcDataCoverage(self.user.organization, ruuid, getMunicId(self.user.munic))
    else:
        data["error"] = True

    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
             "Noviembre", "Diciembre"]

    data["date"] = [meses[int(month) - 1], year]
    # import json
    # r = json.dumps(unicode(data),ensure_ascii=False,encoding='utf8')
    # with open("/home/acoto/pr_pptx/sort_db/data.json", 'wb') as f:
    #    json.dump(r,f, ensure_ascii=False, encoding='utf8')
    mySession.close()
    #print "*-*-*-*-*"
    #pprint(data)
    #print "*-*-*-*-*"

    return data


def getSignature(uname, org, month, year, rol, request):
    if rol == "tec":
        varSig = getVarValue(org, "img_sig_tec", month, year, uname)
        varName = getVarValue(org, "txt_tecnico_reporta_7", month, year, uname)
    else:
        varSig = getVarValue(org, "img_sig_rep", month, year, uname)
        varName = getVarValue(org, "txt_rep_muni_comusan_4", month, year, uname)

    img_path = os.path.join(request.registry.settings["user.repository"], *[org, uname, "data", "xml", varSig])
    f = open(img_path)
    data = f.read()
    f.close()
    img = base64.b64encode(data)
    return ["data:image/png;base64,%s" % img, varName]


def getConfigQR(uname, org, request):
    img_path = os.path.join(request.registry.settings["user.repository"], *[org, uname, "config", "conf.png"])
    f = open(img_path)
    data = f.read()
    f.close()
    img = base64.b64encode(data)
    return "data:image/png;base64,%s" % img


def getBaselines(munic):
    # print munic
    mySession = DBSession()
    query = "select v.id_variables_ind, v.name_variable_ind, i.name_indicadores, l.lb_valor from variables_ind v, lineas_base l, indicadores i where v.id_variables_ind = l.id_variables_ind and v.id_indicadores=i.id_indicadores and l.munic_id =%s;" % munic
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


def newBaseline(data):
    mySession = DBSession()
    data = data.split("*")
    # print "insert"
    try:
        for row in data[:-1]:
            if row[0] == ",":
                row = row[1:]

            row = row.split(",")

            newLB = LineasBase(munic_id=row[1], id_variables_ind=row[0], lb_valor=row[2])
            transaction.begin()
            mySession.add(newLB)
            transaction.commit()
            # mySession.close()
        mySession.close()
        return ["Correcto", "Datos registrados exitosamente", "success"]
    except:
        return ["Error", "Ya existe un usuario para esa institucion en el municipio seleccionado", "error"]


def delete_lb(mun_id):
    mySession = DBSession()
    try:
        transaction.begin()
        mySession.query(LineasBase).filter(LineasBase.munic_id == mun_id).delete()
        transaction.commit()
        mySession.close()

        return ["Correcto", "Datos eliminados exitosamente", "success"]
    except:
        return ["Error", "No se pudo eliminar la linea base para este municipio", "error"]

def updateData(mun_id, data):
    data = data.split("*")
    mySession = DBSession()
    try:
        for row in data[:-1]:
            if row[0] == ",":
                row = row[1:]
            row = row.split(",")
            transaction.begin()
            mySession.query(LineasBase).filter(LineasBase.munic_id == row[1]).filter(
                LineasBase.id_variables_ind == row[0]).update({LineasBase.lb_valor: row[2]})
            transaction.commit()
        mySession.close()
        return ["Correcto", "Datos actualizados exitosamente", "success"]
    except:
        return ["Error", "Error al actualizar los datos", "error"]

def calcDataCoverage( org, device_id_3, mun_id):
    mySession = DBSession()
    query ="SELECT (100/count(*)) * (select count(sem_comunidad_totales) from DATA_%s.maintable_msel_sem_comunidad_totales where device_id_3 ='%s')  FROM sesan_v1.centros_urbanos where munic_id=%s;" %(org, device_id_3, mun_id)
    result = mySession.execute(query).scalar()
    if result:
        return int(result)
    else:
        return False

def genXLS(self,data):
    data.pop('signatures', None)
    path = os.path.join(self.request.registry.settings['user.repository'], "TMP","datos_reporte.xlsx")

    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()

    #worksheet.write(y, x, str)
    worksheet.write(0, 0, "Sala Situacional para el mes de %s, %s"%(data["date"][0],data["date"][1]))
    worksheet.write(1, 0, "Municipio: "+str(self.user.munic).title())
    worksheet.write(2, 0, "Institucion que reporta: " + str(self.user.organization))
    worksheet.write(3, 0, "Covertura en comunidades: " + str(data["coverage"])+ "%")

    pilares=[]
    row=7
    for p in data.keys():
        if "_alert" not in p and "date" not in p and "signatures" not in p and p not in ["comunidades", "acciones","coverage", "comunidades2"]:
            format = workbook.add_format({'bg_color':data[p+"_alert"][2] })
            worksheet.write(row, 0, "Pilar: " + str(p) )
            worksheet.write(row, 1, "Indice de afectacion: " + str(data[p+"_alert"][0]))
            worksheet.write(row, 2, "Nivel de alerta: " + str(data[p+"_alert"][1]).decode("latin-1"), format)
            row+=2
            for d in data[p]:
                worksheet.write(row, 0, "Indicador: "+str(d).decode("latin-1"))
                worksheet.write(row, 1, "Indice de la variable: "+str(data[p][d]["val"][0]))
                row += 1
                for c in data[p][d]["var"]:
                    worksheet.write(row, 0, "Variable: "+str(c[0]).decode("latin-1"))
                    worksheet.write(row, 1, "Unidad de Medida: "+str(c[1]).decode("latin-1"))
                    worksheet.write(row, 2, "Linea Base: "+str(c[2]).decode("latin-1"))
                    worksheet.write(row, 3, "Sitacion actual: "+str(c[3]))
                    worksheet.write(row, 4, "Comparativo mensual: "+str(c[4]))
                    format = workbook.add_format({'bg_color': c[5][0]})
                    worksheet.write(row, 5, "Nivel de afectacion: "+str(c[5][1]).decode("latin-1"),format )
                    row += 1
                row+=2


    o_vals=[["comunidades","Comunidades mas afectadas" ],["acciones", "Acciones propuestas a implementar"]]

    for o in o_vals:
        worksheet.write(row, 0, o[1])
        row += 1
        for k in data[o[0]]:
            worksheet.write(row, 0, k[0])
            worksheet.write(row, 1, k[1])
            row += 1
        row += 1

    workbook.close()