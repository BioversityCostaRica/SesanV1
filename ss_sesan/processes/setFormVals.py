# coding=utf-8
from ..models import DBSession, VariablesInd, Pilare, Indicadore, Grupo, RangosPilare, LineasBase, RangosGrupo, \
    CoefPond, User, Form, FormsByUser, CentrosUrbano
from get_vals import getRanges
from pprint import pprint
import ast, transaction
import sqlalchemy as sa
import xlsxwriter, os, sys, shutil, datetime, json
from pyxform import xls2xform
from hashlib import md5
from glob import glob
from subprocess import check_call, CalledProcessError, Popen, PIPE
from random import randint
import string

reload(sys)
sys.setdefaultencoding('utf8')


def genDefaultValues(id_var, mySession):
    result = mySession.query(LineasBase.munic_id).group_by(LineasBase.munic_id).all()
    if result:
        for row in result:
            LB = LineasBase(id_variables_ind=id_var, munic_id=row[0], lb_valor=1)
            mySession.add(LB)

    result = mySession.query(CoefPond.munic_id).group_by(CoefPond.munic_id).all()
    if result:

        for row in result:
            CP = CoefPond(id_variables_ind=id_var, munic_id=row[0], coef_valor=1)
            mySession.add(CP)


def verifyCode(code):
    mySession = DBSession()

    result = mySession.query(VariablesInd.code_variable_ind).all()
    data = []
    for row in result:
        data.append(row.code_variable_ind)

    while code in data:
        if code in data:
            code = code + str(randint(0, 100))
        else:
            break

    chars = set(string.printable)
    code = filter(lambda x: x in chars, code)
    return code.replace(".","")


def newPilar(jsondata, user):
    # try:
    mySession = DBSession()
    data = ast.literal_eval(jsondata)
    newPi = Pilare(name_pilares=data["pilarName"], coef_pond=int(data["coef_pond"]), user_name=user,
                   pilar_desc=data["desc"])
    transaction.begin()
    mySession.add(newPi)
    transaction.commit()

    id = mySession.query(sa.func.max(Pilare.id_pilares)).first()[0]

    rangData = data["rang"].split("|")
    newRang1 = RangosPilare(id_pilares=id, id_grupo=1, nivel_afec=float(rangData[0].split("-")[1]))
    newRang2 = RangosPilare(id_pilares=id, id_grupo=2, nivel_afec=float(rangData[1].split("-")[1]))
    newRang3 = RangosPilare(id_pilares=id, id_grupo=3, nivel_afec=float(rangData[2].split("-")[1]))
    newRang4 = RangosPilare(id_pilares=id, id_grupo=4, nivel_afec=float(rangData[3].split("-")[1]))

    transaction.begin()
    mySession.add(newRang1)
    mySession.add(newRang2)
    mySession.add(newRang3)
    mySession.add(newRang4)
    transaction.commit()

    for i in data["ind"]:
        newInd = Indicadore(Id_pilares=id, name_indicadores=i)
        transaction.begin()
        mySession.add(newInd)
        transaction.commit()

        for v in data["ind"][i]["vars"]:
            idInd = mySession.query(sa.func.max(Indicadore.id_indicadores)).first()[0]
            v = v.split(" ")
            var_code = []
            for c in v:
                var_code.append(c[:3].lower())

            newVar = VariablesInd(name_variable_ind=" ".join(v).decode("utf-8"), id_indicadores=idInd,
                                  code_variable_ind=verifyCode("_".join(var_code)[:40]), unidad_variable_ind="",
                                  v_pregunta="")
            transaction.begin()
            mySession.add(newVar)
            mySession.flush()
            id_v = newVar.id_variables_ind
            mySession.refresh(newVar)
            genDefaultValues(id_v,
                             mySession)  # se generan valores por default si el municipio ya tiene valores de lb o cf registrados

            transaction.commit()

    mySession.close()
    return ["Correcto", "Pilar creado correctamente", "success"]
    # except:
    #    return ["Error", "Sucedio un error al crear el nuevo pilar", "error"]
    # return ["Correcto", "Pilar creado correctamente", "success"]


def calcIndL(dict):
    list = []
    for row in dict:
        list.append(row["name"])
    return list


def verifyPilar(pId):
    mySession = DBSession()

    result = mySession.query(Indicadore.id_indicadores).filter(Indicadore.Id_pilares == pId).all()
    for r in result:
        var = mySession.query(VariablesInd).filter(VariablesInd.id_indicadores == r.id_indicadores).all()
        for v in var:
            if v.unidad_variable_ind == "" or v.v_pregunta == "":
                return False
    return True


def getPilarData(user):
    mySession = DBSession()
    data = {}
    vars_id = []
    result = mySession.query(Pilare).filter(Pilare.user_name == user).all()

    for res in result:
        data[res.name_pilares] = {"desc": res.pilar_desc, "coef": res.coef_pond, "p_id": res.id_pilares,
                                  "state": verifyPilar(res.id_pilares)}
        inds = mySession.query(Indicadore).filter(Indicadore.Id_pilares == res.id_pilares).all()
        data[res.name_pilares]["ind"] = []
        for ind in inds:
            vari = mySession.query(VariablesInd).filter(VariablesInd.id_indicadores == ind.id_indicadores).all()
            vars = []
            for v in vari:
                vars.append({"id_variables_ind": v.id_variables_ind,
                             "name_variable_ind": v.name_variable_ind,
                             "unidad_variable_ind": v.unidad_variable_ind,
                             "v_pregunta": v.v_pregunta,
                             "var_max": v.var_max,
                             "var_min": v.var_min,
                             "range":getRanges(v.code_variable_ind,"")})
                vars_id.append(str(v.id_variables_ind))
            data[res.name_pilares]["ind"].append({"name": ind.name_indicadores.replace("_", " "), "vars": vars})
        data[res.name_pilares]["indL"] = ",".join(calcIndL(data[res.name_pilares]["ind"]))
    #pprint(data)
    return data, vars_id


def delPilar(pilarId):
    try:

        mySession = DBSession()

        result = mySession.query(Form.pilar_id).all()
        for row in result:
            row = row.pilar_id.split(",")
            for r in row:
                if r == pilarId:
                    return ["Precaucion",
                            "Este pilar no se puede eliminar porque esta siendo utilizado por un formulario", "warning"]

        ind = mySession.query(Indicadore.id_indicadores).filter(Indicadore.Id_pilares == int(pilarId)).all()
        ids = []
        for i in ind:
            ids.append(i[0])
        transaction.begin()

        ind_v = mySession.query(VariablesInd.id_variables_ind).filter(VariablesInd.id_indicadores.in_(ids)).all()
        ids_v = []
        for i in ind_v:
            ids_v.append(i[0])
        mySession.query(LineasBase).filter(LineasBase.id_variables_ind.in_(ids_v)).delete(synchronize_session='fetch')
        mySession.query(CoefPond).filter(CoefPond.id_variables_ind.in_(ids_v)).delete(synchronize_session='fetch')

        mySession.query(RangosGrupo).filter(RangosGrupo.id_variables_ind.in_(ids_v)).delete(synchronize_session='fetch')

        mySession.query(VariablesInd).filter(VariablesInd.id_indicadores.in_(ids)).delete(synchronize_session='fetch')

        mySession.query(Indicadore).filter(Indicadore.Id_pilares == int(pilarId)).delete(synchronize_session='fetch')
        mySession.query(Pilare).filter(Pilare.id_pilares == int(pilarId)).delete(synchronize_session='fetch')
        mySession.query(RangosPilare).filter(RangosPilare.id_pilares == int(pilarId)).delete(
            synchronize_session='fetch')
        transaction.commit()
        mySession.close()

        mySession.close()
        return ["Correcto", "Pilar eliminado correctamente", "success"]
    except:
        return ["Error", "Sucedio un error al eliminar este pilar", "error"]
    return ["Correcto", "Pilar eliminado correctamente", "success"]


def updateVar(v1, v2, v3, v4, vId, rD):  # pregunta, medida , min, max, idvar, rangos

    try:
        mySession = DBSession()
        transaction.begin()
        mySession.query(VariablesInd).filter(VariablesInd.id_variables_ind == int(vId)).update(
            {VariablesInd.v_pregunta: v1, VariablesInd.unidad_variable_ind: v2, VariablesInd.var_min: v3,
             VariablesInd.var_max: v4})
        transaction.commit()

        result = mySession.query(RangosGrupo).filter(RangosGrupo.id_variables_ind == int(vId)).all()
        rangData = rD.split("|")

        if result:
            transaction.begin()
            mySession.query(RangosGrupo).filter(RangosGrupo.id_variables_ind == int(vId)).filter(
                RangosGrupo.id_grupos == 1).update(
                {RangosGrupo.r_min: rangData[0].split("-")[0], RangosGrupo.r_max: rangData[0].split("-")[1]})

            mySession.query(RangosGrupo).filter(RangosGrupo.id_variables_ind == int(vId)).filter(
                RangosGrupo.id_grupos == 2).update(
                {RangosGrupo.r_min: rangData[1].split("-")[0], RangosGrupo.r_max: rangData[1].split("-")[1]})

            mySession.query(RangosGrupo).filter(RangosGrupo.id_variables_ind == int(vId)).filter(
                RangosGrupo.id_grupos == 3).update(
                {RangosGrupo.r_min: rangData[2].split("-")[0], RangosGrupo.r_max: rangData[2].split("-")[1]})

            mySession.query(RangosGrupo).filter(RangosGrupo.id_variables_ind == int(vId)).filter(
                RangosGrupo.id_grupos == 4).update(
                {RangosGrupo.r_min: rangData[3].split("-")[0], RangosGrupo.r_max: rangData[3].split("-")[1]})
            transaction.commit()
        else:
            newRang1 = RangosGrupo(id_variables_ind=int(vId), id_grupos=1, r_min=rangData[0].split("-")[0],
                                   r_max=rangData[0].split("-")[1])
            newRang2 = RangosGrupo(id_variables_ind=int(vId), id_grupos=2, r_min=rangData[1].split("-")[0],
                                   r_max=rangData[1].split("-")[1])
            newRang3 = RangosGrupo(id_variables_ind=int(vId), id_grupos=3, r_min=rangData[2].split("-")[0],
                                   r_max=rangData[2].split("-")[1])
            newRang4 = RangosGrupo(id_variables_ind=int(vId), id_grupos=4, r_min=rangData[3].split("-")[0],
                                   r_max=rangData[3].split("-")[1])
            transaction.begin()
            mySession.add(newRang1)
            mySession.add(newRang2)
            mySession.add(newRang3)
            mySession.add(newRang4)
            transaction.commit()

        mySession.close()

        return ["Correcto", "Variable actualizada correctamente", "success"]


    except:
        return ["Error", "No se pudo actualizar la informacion para esta", "error"]


def getListPU(login):
    mySession = DBSession()
    result = mySession.query(Pilare.name_pilares, Pilare.id_pilares).filter(Pilare.user_name == login).all()
    pilares = []
    for row in result:
        if verifyPilar(row[1]):
            pilares.append([row[0], row[1]])

    result = mySession.query(User.user_fullname, User.user_name).filter(User.user_parent == login).all()
    users = []
    for row in result:
        users.append([row[0], row[1]])

    mySession.close()

    return [pilares, users]


def form_to_user(request, login, fname, users):
    users = users.split(",")
    for user in users:
        outdir = os.path.join(request.registry.settings["user.repository"], login, "user", user,
                              fname.title().replace(" ", "_"))

        if not os.path.exists(outdir):
            os.makedirs(outdir)

        jsonFile = os.path.join(outdir, login + "_" + fname.title().replace(" ", "_") + "_" + user + ".json")

        f1 = os.path.join(request.registry.settings["user.repository"], login, "forms", fname.title().replace(" ", "_"),
                          fname.title().replace(" ", "_") + ".xml")
        f2 = os.path.join(request.registry.settings["user.repository"], login, "user", user,
                          fname.title().replace(" ", "_"),
                          login + "_" + fname.title().replace(" ", "_") + "_" + user + ".xml")

        metadata = {}
        metadata["formID"] = login + "_" + fname.title().replace(" ", "_") + "_" + user
        metadata["name"] = login + "_" + fname.title().replace(" ", "_") + "_" + user
        metadata["majorMinorVersion"] = ""
        metadata["version"] = datetime.datetime.now().strftime("%Y%m%d")
        metadata["hash"] = 'md5:' + md5(login + "_" + fname.title().replace(" ", "_") + "_" + user).hexdigest()
        metadata["descriptionText"] = login + "_" + fname.title().replace(" ", "_") + "_" + user
        with open(jsonFile, "w") as outfile:
            jsonString = json.dumps(metadata, indent=4, ensure_ascii=False).encode("utf8")
            outfile.write(jsonString)

        cu1 = outdir.replace(fname.title().replace(" ", "_"), "curbanos.csv")
        cu2 = f2.replace(login + "_" + fname.title().replace(" ", "_") + "_" + user + ".xml", "curbanos.csv")

        os.system("cp %s %s" % (f1, f2))
        os.system("cp %s %s" % (cu1, cu2))

    return


def add_CU(db, request, login, users):
    mySession = DBSession()
    users=users.split(",")

    munics = []

    result = mySession.query(User.user_munic).filter(User.user_munic != 1000).filter(User.user_parent == login).filter(User.user_name.in_(users)).all()
    for row in result:
        munics.append(row.user_munic)

    result = mySession.query(CentrosUrbano.id_cu, CentrosUrbano.cu_name).filter(
        CentrosUrbano.munic_id.in_(munics)).all()
    file = open(request.registry.settings["user.repository"]+"/cen_u.sql", "w")
    for row in result:
        file.write(
            "INSERT INTO %s.lkpsem_comunidad_totales (sem_comunidad_totales_cod,sem_comunidad_totales_des)  VALUES ('%s','%s');" % (
                db, row.id_cu, str(row.cu_name).decode("latin1")))

    file.close()

    args = []
    args.append("mysql")
    args.append("--defaults-file=" + request.registry.settings['mysql.cnf'])
    args.append(db)

    with open(request.registry.settings["user.repository"]+"/cen_u.sql") as input_file:
        proc = Popen(args, stdin=input_file, stderr=PIPE, stdout=PIPE)
        output, error = proc.communicate()
        if output != "" or error != "":
            msg = "Error creating database \n"
            msg = msg + "File: cen_u.sql" + "\n"
            msg = msg + "Error: \n"
            msg = msg + error + "\n"
            msg = msg + "Output: \n"
            msg = msg + output + "\n"
            print msg
            error = True


def genForm_Files(login, pilarId, request, fname):
    mySession = DBSession()
    path = os.path.join(request.registry.settings["user.repository"], login, "forms", fname.title().replace(" ", "_"),
                        fname.title().replace(" ", "_") + ".xlsx")

    outputDir = os.path.join(request.registry.settings["user.repository"], login, "forms",
                             fname.title().replace(" ", "_"))

    # oldmask = os.umask(000)
    if not os.path.exists(outputDir):
        os.makedirs(outputDir,0777)

    book = xlsxwriter.Workbook(path)

    sheet1 = book.add_worksheet("survey")
    sheet1.write(0, 0, 'type')
    sheet1.write(0, 1, 'name')
    sheet1.write(0, 2, 'label')
    sheet1.write(0, 3, 'hint')
    sheet1.write(0, 4, 'constraint')
    sheet1.write(0, 5, 'constraint_message')
    sheet1.write(0, 6, 'required')
    sheet1.write(0, 7, 'required_message')
    sheet1.write(0, 8, 'appearance')
    sheet1.write(0, 9, 'default')
    sheet1.write(0, 10, 'relevant')
    sheet1.write(0, 11, 'repeat_count')
    sheet1.write(0, 12, 'read_only')
    sheet1.write(0, 13, 'choice_filter')
    sheet1.write(0, 14, 'calculation')

    sheet2 = book.add_worksheet("choices")
    sheet2.write(0, 0, 'list_name')
    sheet2.write(0, 1, 'name')
    sheet2.write(0, 2, 'label')

    sheet2.write(1, 0, 'lista_curb')
    sheet2.write(1, 1, 'urban_id')
    sheet2.write(1, 2, 'urban_name')

    sheet3 = book.add_worksheet("settings")
    sheet3.write(0, 0, 'form_id')
    sheet3.write(0, 1, 'form_title')
    sheet3.write(0, 2, 'instance_name')

    now = datetime.datetime.now()
    questions = [
        ["start", "start_time_survey_1", "", "", "", "", "", "", ""],
        ["today", "day_of_survey", "", "", "", "", "", "", ""],
        ["deviceid", "device_id_3", "", "", "", "", "", "", ""],
        ["note", "notex", u"%s, SESAN %s" % (fname, str(now.year)), "", "", "", "", "", ""],
        ["begin group", "grpx", "", "", "", "", "", "", "field-list"],
        ["text", "txt_rep_muni_comusan_4", u"Nombre de la persona que recopila la información", "", "", "", "yes", "",
         u"Debe ingresar el nombre de la persona que recopila la información"],
        ["date", "date_fecha_informe_6", "Fecha a la que corresponde el informe", "", "", "", "yes", "", "month-year"],
        ["select_multiple lista_curb", "sem_comunidad_totales",
         u"Seleccione la o las comunidades incluidas en este reporte",
         "", "", "", "", "", "search('curbanos') minimal"],
        ["end group", "grpx", "", "", "", "", "", "", ""],

    ]

    pilarId = pilarId.split(",")

    for p in pilarId:
        result = mySession.query(Pilare).filter(Pilare.id_pilares == p).first()
        questions.append(
            ["note", "note" + str(result.id_pilares), "Pilar:%s, %s" % (result.name_pilares, result.pilar_desc), "", "",
             "", "", "", ""])

        indicadores = mySession.query(Indicadore).filter(Indicadore.Id_pilares == p).all()
        for i in indicadores:
            questions.append(["begin group", "grp" + str(i.id_indicadores), "", "", "", "", "", "", "field-list"])
            questions.append(
                ["note", "note" + str(i.id_indicadores), "Indicador: %s" % i.name_indicadores, "", "", "", "", "", ""])

            variables = mySession.query(VariablesInd).filter(VariablesInd.id_indicadores == i.id_indicadores).all()
            for v in variables:
                questions.append(
                    ["decimal", v.code_variable_ind, v.v_pregunta, "Medida:" + v.unidad_variable_ind,
                     ".<=" + str(v.var_max), "El valor debe ser menor o igual que " + str(v.var_max), "yes",
                     "Complete: " + v.v_pregunta, ""])
                # agregar a variables ind_hint, regla, mensaje de error, y requiered
            questions.append(["end group", "grp" + str(i.id_indicadores), "", "", "", "", "", "", ""])

    questions.append(["begin group", "grp_signature", "", "", "", "", "", "", "field-list"])
    questions.append(["image", "img_sig_resp", "Firma del responsable de este formulario", "", "", "", "yes",
                      "Debe ingresar la firma del responsable del formulario", "signature"])
    questions.append(["end group", "grp_signature", "", "", "", "", "", "", ""])
    questions.append(["end", "end_time_survey_26", "", "", "", "", "", "", ""])

    for row in enumerate(questions):
        for col in enumerate(row[1]):
            sheet1.write(row[0] + 1, col[0], u"" + str(col[1]).decode('latin1').decode("utf-8"))
            # print col[1]

    book.close()

    # odktools para crear la base de datos

    args = []
    ODKtoMySQL = os.path.join(request.registry.settings["odktools.path"], *["ODKToMySQL", "odktomysql"])

    args.append(ODKtoMySQL)
    args.append("-x " + path)  # xlsx file
    args.append("-t maintable")  # maintable name
    args.append("-v device_id_3")  # Main survey variable

    args.append("-u " + os.path.join(outputDir, "uuid-triggers.sql"))
    args.append("-f " + os.path.join(outputDir, "manifest.xml"))
    args.append("-T " + os.path.join(outputDir, "iso639.sql"))
    args.append("-m " + os.path.join(outputDir, "metadata.sql"))
    args.append("-I " + os.path.join(outputDir, "insert.xml"))
    args.append("-i " + os.path.join(outputDir, "insert.sql"))
    args.append("-C " + os.path.join(outputDir, "create.xml"))
    args.append("-c " + os.path.join(outputDir, "create.sql"))

    error = False
    cnfFile = request.registry.settings["mysql.cnf"]

    try:  # odktomysql
        print"\n*-1-*\n"
        print path
        print args
        check_call(args)
        print"\n*-11-*\n"
    except CalledProcessError as e:
        msg = "Error exporting files to database \n"
        msg = msg + "Command: " + " ".join(args) + "\n"
        msg = msg + "Error: \n"
        msg = msg + e.message
        print msg
        print e


        error = True
        return False

    if not error:  # drop database if exist
        args = []
        args.append("mysql")
        args.append("--defaults-file=" + cnfFile)
        args.append('--execute=DROP DATABASE IF EXISTS ' + 'DATA_' + login + '_' + fname.title().replace(' ', '_'))
        try:
            print"\n*-2-*\n"
            check_call(args)
            print"\n*-21-*\n"
        except CalledProcessError as e:
            msg = "Error exporting files to database \n"
            msg = msg + "Commang: " + " ".join(args) + "\n"
            msg = msg + "Error: \n"
            msg = msg + e.message
            print msg
            return e

    if not error:  # create database
        args = []
        args.append("mysql")
        args.append("--defaults-file=" + cnfFile)
        args.append('--execute=CREATE DATABASE ' + 'DATA_' + login + '_' + fname.title().replace(' ', '_'))
        try:
            print"\n*-3-*\n"
            check_call(args)
            print"\n*-31-*\n"
        except CalledProcessError as e:
            msg = "Error exporting files to database \n"
            msg = msg + "Commang: " + " ".join(args) + "\n"
            msg = msg + "Error: \n"
            msg = msg + e.message
            print msg
            return e

    if not error:  # create.sql
        args = []
        args.append("mysql")
        args.append("--defaults-file=" + cnfFile)
        args.append('DATA_' + login + '_' + fname.title().replace(' ', '_'))

        with open(os.path.join(outputDir, 'create.sql')) as input_file:
            proc = Popen(args, stdin=input_file, stderr=PIPE, stdout=PIPE)
            output, error = proc.communicate()
            if output != "" or error != "":
                msg = "Error creating database \n"
                msg = msg + "File: " + os.path.join(outputDir, 'create.sql') + "\n"
                msg = msg + "Error: \n"
                msg = msg + error + "\n"
                msg = msg + "Output: \n"
                msg = msg + output + "\n"
                print msg
                error = True

    if not error:  # create triggers
        args = []
        args.append("mysql")
        args.append("--defaults-file=" + cnfFile)
        args.append('DATA_' + login + '_' + fname.title().replace(' ', '_'))

        with open(os.path.join(outputDir, 'uuid-triggers.sql')) as input_file:
            proc = Popen(args, stdin=input_file, stderr=PIPE, stdout=PIPE)
            output, error = proc.communicate()
            if output != "" or error != "":
                msg = "Error creating database \n"
                msg = msg + "File: " + os.path.join(outputDir, 'uuid-triggers.sql') + "\n"
                msg = msg + "Error: \n"
                msg = msg + error + "\n"
                msg = msg + "Output: \n"
                msg = msg + output + "\n"
                print msg
                error = True

    if not error:  # insert values
        args = []
        args.append("mysql")
        args.append("--defaults-file=" + cnfFile)
        args.append('DATA_' + login + '_' + fname.title().replace(' ', '_'))

        with open(os.path.join(outputDir, 'insert.sql')) as input_file:
            proc = Popen(args, stdin=input_file, stderr=PIPE, stdout=PIPE)
            output, error = proc.communicate()
            if output != "" or error != "":
                msg = "Error creating database \n"
                msg = msg + "File: " + os.path.join(outputDir, 'insert.sql') + "\n"
                msg = msg + "Error: \n"
                msg = msg + error + "\n"
                msg = msg + "Output: \n"
                msg = msg + output + "\n"
                print msg
                error = True

    # ALTER TABLE '%s'.`lkpsem_comunidad_totales`;CHANGE COLUMN `sem_comunidad_totales_des` `sem_comunidad_totales_des` VARCHAR(100) NULL DEFAULT NULL COMMENT 'Description' ;
    #sem_comunidad_totales
    if not error:  # create database
        args = []
        args.append("mysql")
        args.append("--defaults-file=" + cnfFile)
        args.append(
            "--execute=ALTER TABLE %s.lkpsem_comunidad_totales MODIFY COLUMN sem_comunidad_totales_des VARCHAR(100)" % (
                'DATA_' + login + '_' + fname.title().replace(' ', '_')))

        try:
            check_call(args)
        except CalledProcessError as e:
            msg = "Error exporting files to database \n"
            msg = msg + "Commang: ALTER TABLE\n"
            msg = msg + "Error: \n"
            msg = msg + e.message
            print msg
            return e

    if not error:  # create database
        args = []
        args.append("mysql")
        args.append("--defaults-file=" + cnfFile)
        args.append(
            "--execute=ALTER TABLE %s.maintable MODIFY COLUMN sem_comunidad_totales VARCHAR(150)" % (
                'DATA_' + login + '_' + fname.title().replace(' ', '_')))

        try:
            check_call(args)
        except CalledProcessError as e:
            msg = "Error exporting files to database \n"
            msg = msg + "Commang: ALTER TABLE\n"
            msg = msg + "Error: \n"
            msg = msg + e.message
            print msg
            return e

    if not error:

        xls2xform.xls2xform_convert(path, path.replace(".xlsx", ".xml"))
        os.system("cp "+request.registry.settings["user.repository"]+"/custom.js %s" % outputDir + "/custom.js")

    return True


# def form_to_user(parent, uname)

def newForm(request, vals, login):
    vals = vals.split("++")
    try:
        mySession = DBSession()

        newF = Form(form_user=login, form_name=vals[0], pilar_id=vals[1],
                    form_db="DATA_" + login + "_" + vals[0].title().replace(" ", "_"))
        transaction.begin()

        mySession.add(newF)

        if vals[2] != "" and vals[2] != "undefined":
            mySession.flush()
            id_F = newF.form_id
            mySession.refresh(newF)
            uList = vals[2].split(",")
            for u in uList:
                newF_U = FormsByUser(idforms=id_F, id_user=u)
                mySession.add(newF_U)



        if not genForm_Files(login, vals[1], request, vals[0]):
            delForm(request, id_F, login)
            raise
        else:
            form_to_user(request, login, vals[0], vals[2])
            add_CU('DATA_' + login + '_' + vals[0].title().replace(' ', '_'), request, login, vals[2])

        transaction.commit()
        mySession.close()
        return ["Correcto", "Formulario creado con exito", "success"]


    except:
        mySession.close()
        return ["Error", "Sucedio un error al generar el formulario", "error"]


def getPilarNames(ids):
    mySession = DBSession()
    ids = ids.split(",")
    data = []
    for i in ids:
        result = mySession.query(Pilare.name_pilares).filter(Pilare.id_pilares == i).first()
        data.append(result[0])
    mySession.close()
    return data


def getUname(id_user):
    mySession = DBSession()

    result = mySession.query(User.user_fullname).filter(User.user_name == id_user).first()
    return result[0]


def getUsersF(fid):
    mySession = DBSession()

    data = []
    result = mySession.query(FormsByUser.id_user).filter(FormsByUser.idforms == fid).all()

    if result:
        for row in result:
            data.append([row[0], getUname(row[0])])
    mySession.close()
    return data


def forms_id(login):
    mySession = DBSession()
    data = []
    result = mySession.query(Form.form_id).filter(Form.form_user == login).all()

    for res in result:
        data.append(str(res.form_id))
    return ",".join(data)


def getSubmissionCount(fId):
    mySession = DBSession()

    result = mySession.query(Form.form_db).filter(Form.form_id == fId).first()

    result = mySession.execute("SELECT COUNT(*) FROM %s.maintable;" % result.form_db).scalar()

    return int(result)


def getForms(login):
    # solo los pilares que esten completos

    mySession = DBSession()

    data = []

    result = mySession.query(Form).filter(Form.form_user == login).all()

    for res in result:
        row = []
        row.append([res.form_name, res.form_id])
        row.append(getPilarNames(res.pilar_id))
        row.append(getUsersF(res.form_id))
        row.append(getSubmissionCount(res.form_id))
        data.append(row[:])
    return data


def delForm(request, formid, login):
    # validar si la base de datos tiene datos
    # borrar archivos en carpetas de usuarios
    # eliminar tambien la base de datos
    formid = formid.split("--")

    try:

        if getSubmissionCount(formid[1]) > 0:
            return ["Precaucion", "Este formulario no se puede elimiar porque contiene datos", "warning"]

        mySession = DBSession()

        result = mySession.query(FormsByUser.id_user).filter(FormsByUser.idforms == formid[1]).all()
        for row in result:
            files = os.path.join(request.registry.settings["user.repository"], login, "user", row.id_user,
                                 formid[0].title().replace(' ', '_'))
            try:
                shutil.rmtree(files)
            except:
                pass

        transaction.begin()
        mySession.query(Form).filter(Form.form_id == formid[1]).delete(synchronize_session='fetch')

        mySession.query(FormsByUser).filter(FormsByUser.idforms == formid[1]).delete(synchronize_session='fetch')

        transaction.commit()
        mySession.close()

        files = os.path.join(request.registry.settings["user.repository"], login, "forms",
                             formid[0].title().replace(" ", "_"))
        shutil.rmtree(files)

        cnfFile = request.registry.settings['mysql.cnf']
        args = []
        args.append("mysql")
        args.append("--defaults-file=" + cnfFile)
        args.append('--execute=DROP DATABASE IF EXISTS ' + 'DATA_' + login + '_' + formid[0].title().replace(' ', '_'))
        try:
            check_call(args)
        except CalledProcessError as e:
            msg = "Error exporting files to database \n"
            msg = msg + "Commang: " + " ".join(args) + "\n"
            msg = msg + "Error: \n"
            msg = msg + e.message
            raise

        return ["Correcto", "Formulario eliminado correctamente", "success"]
    except:
        return ["Error", "Sucedio un error al eliminar este formulario", "error"]


def getFormName(fid):
    mySession = DBSession()
    result = mySession.query(Form.form_name).filter(Form.form_id==fid).first()
    mySession.close()
    return result[0]


def verifyUserData(db,uname):
    mySession= DBSession()
    result =mySession.execute("SELECT COUNT(*) FROM %s.maintable WHERE surveyid like binary '%s' ;" % (db, "% " + uname + "_%")).scalar()

    return result

def updateFU(vals, request, login):
    vals=vals.split("*")
    fid = vals[1]

    mySession =DBSession()

    result= mySession.query(FormsByUser.id_user).filter(FormsByUser.idforms==fid).all()
    result = [r[0] for r in result]
    cont=0
    try:
        if vals[0]!= "":
            ulist=vals[0].split(",")

            for u in ulist:
                if u not in result:
                    #add
                    form_to_user(request, login, getFormName(fid), u)
                    add_CU('DATA_' +login+"_"+getFormName(fid).title().replace(" ", "_"), request, login, u)
                    result.append(u)
                    transaction.begin()
                    newF_U = FormsByUser(idforms=fid, id_user=u)
                    mySession.add(newF_U)
                    transaction.commit()
            for r in result:
                if r not in ulist:
                    if verifyUserData('DATA_' +login+"_"+getFormName(fid).title().replace(" ", "_"), r)==0:
                        files = os.path.join(request.registry.settings["user.repository"], login, "user", r, getFormName(fid).title().replace(" ", "_"))
                        try:
                            shutil.rmtree(files)
                        except:
                            pass
                        transaction.begin()
                        mySession.query(FormsByUser).filter(FormsByUser.id_user == r).filter(FormsByUser.idforms == fid).delete(
                            synchronize_session='fetch')
                        transaction.commit()
                else:
                    cont=cont+1
        else:
            for r in result:
                if verifyUserData('DATA_' +login+"_"+ getFormName(fid).title().replace(" ", "_"), r) == 0:
                    files = os.path.join(request.registry.settings["user.repository"], login, "user",r,getFormName(fid).title().replace(" ", "_"))
                    try:
                        shutil.rmtree(files)
                    except:
                        pass
                    transaction.begin()
                    mySession.query(FormsByUser).filter(FormsByUser.id_user == r).filter(FormsByUser.idforms==fid).delete(synchronize_session='fetch')
                    transaction.commit()
                else:
                    cont=cont+1

            #new = list(set(ulist) - set(result))

        return ["Correcto", "Formulario modificado correctamente", "success"]
    except:
        return ["Error", "Sucedio un error al modificar los usuarios de este formulario", "error"]