from ..models import DBSession, Institucione, Munic, User, VariablesInd, Pilare, Indicadore
from sqlalchemy import func
from datetime import datetime as t
from ..encdecdata import encodeData
import transaction
from datetime import datetime
import os, json, base64
from pprint import pprint
from hashlib import md5

from qrtools import QR  # apt-get install libzbar-dev, pip install zbar, pip install qrtools
from climmob.config.encdecdata import decodeData


def fill_reg():
    res = {"munic": [], "insti": []}
    mySession = DBSession()
    result = mySession.query(Munic).all()
    for i in result:
        res["munic"].append([int(i.munic_id), str(i.munic_nombre).decode("latin1").encode("utf8")])
    result = mySession.query(Institucione).all()
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


def make_qr(repo,org,passw,uname):
    try:
        ip="172.17.10.158"
        config_data = {u'admin': {}, u'general': {u'username': uname, u'password': passw,
                                                  u'server_url': u'http://%s:6542/%s/%s' %(ip, org, uname),
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

                    paths = [getIntName(regDict["inst"]) + "_" + getMunicName(regDict["munic"]).replace(" ", "") + "_" + regDict[
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
                    return 1

                except Exception, e:
                    transaction.abort()
                    mySession.close()
                    return 2
    return 3


def getComp(lb, act):
    try:
        lb = int(lb)
    except:
        lb = float(lb)
    try:
        act = int(act)
    except:
        act = float(act)

    if lb < act:
        return 1  # "Aumento"
    if lb > act:
        return 2  # "Disminuyo"
    if lb == act:
        return 3  # "Se mantiene"
    return 0


def getVarValue(org, code, month,year, uname):
    mySession = DBSession()
    ret= ""
    result = mySession.execute(
        "SELECT %s FROM DATA_%s.maintable WHERE MONTH(date_fecha_informe_6) = %s and YEAR (date_fecha_informe_6) = %s and surveyid like '%s' LIMIT 1;" % (code, org, month,year, "%"+uname+"%"))
    for res in result:
        ret = str(res[0])
    mySession.close()
    return ret


def calcValue(val, idVar, type):  # if type = 1 calc Equivalent values elif type == 2 calc Weighting coefficient
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
    return float(res)


def getDashReportData(self, month, year):

    #month = "08"
    #year = "2017"

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
    result = mySession.execute("SELECT COUNT(*) FROM DATA_%s.maintable WHERE MONTH(date_fecha_informe_6) = %s and YEAR (date_fecha_informe_6) = %s and surveyid like '%s' ;" % (
    self.user.organization, month, year, "%"+self.user.login+"%")).scalar()

    if int(result) != 0:
        for i in indicadores:
            i_pi = mySession.query(Indicadore.Id_pilares).filter_by(id_indicadores=i).first()
            if int(i_pi[0]) not in pilares:
                p_name = mySession.query(Pilare.name_pilares).filter_by(id_pilares=int(i_pi[0])).first()
                tot_alert = []
                data[p_name[0]] = {}  # add pilar
                i_name = mySession.query(Indicadore.name_indicadores, Indicadore.id_indicadores).filter_by(
                    Id_pilares=int(i_pi[0])).all()
                for i_n in i_name:
                    # print i_n[0]
                    data[p_name[0]][i_n[0]] = {"var": [], "val": []}  # add indicadores
                    variables = mySession.query(VariablesInd).filter_by(id_indicadores=int(i_n[1])).all()
                    valCP = 0
                    acum = []
                    for v in variables:
                        sa = getVarValue(self.user.organization, v.code_variable_ind, month,year, self.user.login)
                        # add variables data
                        data[p_name[0]][i_n[0]]["var"].append(
                            [v.name_variable_ind, v.unidad_variable_ind, v.lbase_variable_ind, sa,
                             getComp(v.lbase_variable_ind, sa)])
                        valCP = valCP + calcValue(sa, v.id_variables_ind, 1)
                        acum.append(calcValue(sa, v.id_variables_ind, 1) * calcValue(sa, v.id_variables_ind, 2))

                    tot_alert.append([valCP, sum(acum)])

                    data[p_name[0]][i_n[0]]["val"].append("%.2f" % (sum(acum) / valCP))
                pilares.append(int(i_pi[0]))
                # print tot_alert
                t0 = 0
                t1 = 0
                for t in tot_alert:
                    t0 = t0 + t[0]
                    t1 = t1 + t[1]
                data[p_name[0] + "_alert"] = "%.2f" % (t1 / t0)
        data["signatures"] = [getSignature(self.user.login, self.user.organization, month, year, "rep", self.request),
                              getSignature(self.user.login, self.user.organization, month, year, "tec", self.request)]

    else:
        data["error"] = True

    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
             "Noviembre", "Diciembre"]

    data["date"] = [meses[int(month)-1], year]


    mySession.close()
    #print "*-*-*-*-*-*-*-*-"
    #pprint(data)
    #print "*-*-*-*-*-*-*-*-"
    return data


def getSignature(uname, org,month, year,rol,request):

    if rol == "tec":
        varSig = getVarValue(org, "img_sig_tec", month, year, uname)
        varName = getVarValue(org, "txt_tecnico_reporta_7", month, year, uname)
    else:
        varSig = getVarValue(org, "img_sig_rep", month, year, uname)
        varName = getVarValue(org, "txt_rep_muni_comusan_4", month, year, uname)


    img_path = os.path.join(request.registry.settings["user.repository"],*[org, uname, "data", "xml",varSig ])
    f = open(img_path)
    data = f.read()
    f.close()
    img = base64.b64encode(data)
    return ["data:image/png;base64,%s" % img, varName]



def getConfigQR(uname, org,request):
    img_path = os.path.join(request.registry.settings["user.repository"],*[org, uname, "config", "conf.png"])
    f = open(img_path)
    data = f.read()
    f.close()
    img = base64.b64encode(data)
    return "data:image/png;base64,%s" % img



