from pyramid.view import view_config
from pyramid.security import remember, authenticated_userid, forget
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from .classes import publicView, privateView, odkView
from .auth import getUserData
from .resources import DashJS, DashCSS, basicCSS, regJS_CSS, reportJS, baselineR, pilarCSS_JS, formsCSS_JS, gtoolCSS_JS, \
    rangCSS_JS,seasonCSS_JS
from processes.get_vals import updateData, delete_lb, newBaseline, fill_reg, addNewUser, getDashReportData, getConfigQR, \
    valReport, dataReport, getBaselines, getMunicName, getBaselinesName, genXLS, getUsersList, delUser, getForm_By_User, \
    getHelpFiles, getFileResponse, getGToolData, getData4Analize, getMails, addMail, getMunicId, delMail, getRangeList, \
    sendGroup, updateUser, UpdateOrInsertRange, getDeptName, getUserDeptoID, getMunics, getUserByMunic,getFilesList, getDepByMunic

from processes.get_pptx import genPPTX
from processes.utilform import isUserActive, getUserPassword, getFormList, getParent, getManifest, getMediaFile, \
    getXMLForm, storeSubmission
from datetime import datetime
from pyramid.response import FileResponse
import os, ast
from .processes.setFormVals import newPilar, getPilarData, delPilar, updateVar, getListPU, newForm, getForms, delForm, \
    forms_id, updateFU

from processes.logs import log,getLoglist

#from processes.rules import newRule,getRules,delRule

from processes.seasons import GetSeasonsRules



@view_config(route_name='profile', renderer='templates/profile.jinja2')
class profile_view(privateView):
    def processView(self):
        DashJS.need()
        DashCSS.need()
        if self.user.user_role == 2:
            return {'activeUser': self.user,
                    "dates": self.request.cookies["cur_date"].split("_"),
                    "depto": getDeptName(getUserDeptoID(self.user.login))}
        else:
            return {'activeUser': self.user, "config": getConfigQR(self.user.login, self.user.parent, self.request),
                    "forms": getForm_By_User(self.user.login), "dates": self.request.cookies["cur_date"].split("_")}


@view_config(route_name='about', renderer='templates/about.jinja2')
class about_view(privateView):
    def processView(self):
        DashJS.need()
        DashCSS.need()
        if self.user.user_role == 2:

            return {'activeUser': self.user, "file_list": getHelpFiles(self.request),
                    "dates": self.request.cookies["cur_date"].split("_"),
                    "depto": getDeptName(getUserDeptoID(self.user.login))}
        else:

            return {'activeUser': self.user, "file_list": getHelpFiles(self.request),
                    "dates": self.request.cookies["cur_date"].split("_")}


@view_config(route_name='baseline', renderer='templates/baseline.jinja2')
class baseline_view(privateView):
    def processView(self):
        DashJS.need()
        DashCSS.need()
        baselineR.need()
        regJS_CSS.need()
        fill_regN = fill_reg()
        msg = []

        if "submit" in self.request.POST:
            # if "update_data" in self.request.POST:

            fill_regN["sel"] = int(self.request.POST.get("munic", ""))
            fill_regN["s_depto"] = int(self.request.POST.get("depto", ""))
            fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("munic", ""))).title()
            fill_regN["lb_m"] = getBaselinesName()
            lb_data = getBaselines(int(self.request.POST.get("munic", "")), "lb")
            log(self.user.login, "get baselines from " + getMunicName(int(self.request.POST.get("munic", ""))).title(),
                "normal", "4")


        else:
            if "id_mun_sel" in self.request.POST and not "update_data" in self.request.POST and not "submit_lb" in self.request.POST:
                msg = delete_lb(self.request.POST.get("id_mun_sel", ""), "lb")
                fill_regN["sel"] = int(self.request.POST.get("id_mun_sel", ""))
                fill_regN["s_depto"] = int(self.request.POST.get("id_depto_sel", ""))
                fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("id_mun_sel", ""))).title()
                fill_regN["lb_m"] = getBaselinesName()
                lb_data = getBaselines(int(self.request.POST.get("id_mun_sel", "")), "lb")
                log(self.user.login,
                    "delete baselines from " + getMunicName(int(self.request.POST.get("id_mun_sel", ""))).title(),
                    "normal", "1")
            else:
                if "update_data" in self.request.POST:
                    msg = updateData(self.request.POST.get("id_mun_sel", ""),
                                     self.request.POST.get("mun_sel_data2", ""), "lb")
                    fill_regN["sel"] = int(self.request.POST.get("id_mun_sel", ""))
                    fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("id_mun_sel", ""))).title()
                    fill_regN["s_depto"] = int(self.request.POST.get("id_depto_sel", ""))
                    fill_regN["lb_m"] = getBaselinesName()
                    lb_data = getBaselines(int(self.request.POST.get("id_mun_sel", "")), "lb")
                    log(self.user.login,
                        "updates baselines from " + getMunicName(int(self.request.POST.get("id_mun_sel", ""))).title(),
                        "normal",
                        "2")
                else:
                    if "submit_lb" in self.request.POST:
                        save_data = self.request.POST.get("mun_sel_data", "")
                        fill_regN["sel"] = int(self.request.POST.get("id_mun_sel", ""))
                        fill_regN["s_depto"] = int(self.request.POST.get("id_depto_sel", ""))
                        fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("id_mun_sel", ""))).title()
                        fill_regN["lb_m"] = getBaselinesName()
                        msg = newBaseline(save_data, "lb")
                        lb_data = getBaselines(int(self.request.POST.get("id_mun_sel", "")), "lb")
                        log(self.user.login,
                            "new baselines from " + getMunicName(
                                int(self.request.POST.get("id_mun_sel", ""))).title(), "normal",
                            "1")
                    else:
                        fill_regN["sel"] = 0
                        fill_regN["sel_name"] = ""
                        fill_regN["lb_m"] = []
                        lb_data = getBaselines(0, "lb")

        return {'activeUser': self.user, "lb_data": lb_data, "fill_reg": fill_regN, "msg": msg}


@view_config(route_name='mails', renderer='templates/mails.jinja2')
class mails_view(privateView):
    def processView(self):
        DashJS.need()
        DashCSS.need()
        baselineR.need()
        regJS_CSS.need()
        fill_regN = fill_reg()
        msg = []
        mail_list = []

        if "delMail" in self.request.POST:
            fill_regN["sel_name"] = getMunicName(self.request.POST.get("sel_name", "").title())
            fill_regN["sel"] = self.request.POST.get("sel_name", "")

            fill_regN["s_depto"] = int(self.request.POST.get("depto", ""))
            msg = delMail(self.request.POST.get("delMail", ""))
            mail_list = getMails(self.request.POST.get("sel_name"))
            log(self.user.login,
                "mail deleted in munic" + self.request.POST.get("sel_name") + " for " + self.request.POST.get(
                    "delMail"),
                "normal", "3")

        if "reg" in self.request.POST:
            msg = addMail(self.request, self.request.POST.get("fullname"), self.request.POST.get("email"),
                          self.request.POST.get("munic_id"))
            fill_regN["sel_name"] = getMunicName(self.request.POST.get("munic_id"))
            fill_regN["s_depto"] = int(self.request.POST.get("depto", ""))
            fill_regN["sel"] = self.request.POST.get("munic_id")
            mail_list = getMails(self.request.POST.get("munic_id"))
            log(self.user.login,
                "new mail added in munic s" + self.request.POST.get("munic_id") + " for " + self.request.POST.get(
                    "fullname"),
                "normal", "1")
        if "munic" in self.request.POST:
            fill_regN["sel"] = int(self.request.POST.get("munic", ""))
            fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("munic", ""))).title()
            fill_regN["s_depto"] = int(self.request.POST.get("depto", ""))
            mail_list = getMails(self.request.POST.get("munic", ""))

        return {'activeUser': self.user, "msg": msg, "fill_reg": fill_regN, "mail_list": mail_list}


@view_config(route_name='ranges', renderer='templates/ranges.jinja2')
class ranges_view(privateView):
    def processView(self):
        DashJS.need()
        DashCSS.need()
        regJS_CSS.need()
        baselineR.need()
        rangCSS_JS.need()
        # pilarCSS_JS.need()
        fill_regN = fill_reg()
        range = []
        varsR_id = []
        msg = []
        #print self.request.POST
        if "saveRange" in self.request.POST:

            msg = UpdateOrInsertRange(self.request.POST);

            fill_regN["sel"] = int(self.request.POST.get("mun_id", ""))
            fill_regN["s_depto"] = int(self.request.POST.get("dep_id", ""))
            fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("mun_id", ""))).title()
            range = getRangeList(self.request.POST.get("mun_id", ""))
            for r in range:
                varsR_id.append(str(r[0]))

            varsR_id = ",".join(varsR_id)

            log(self.user.login, "range updated in " + getMunicName(
                int(self.request.POST.get("mun_id", ""))).title() + " for var " + str(self.request.POST.get("var_id")),
                "normal", "2")

        if "munic" in self.request.POST:
            fill_regN["sel"] = int(self.request.POST.get("munic", ""))
            fill_regN["s_depto"] = int(self.request.POST.get("depto", ""))
            fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("munic", ""))).title()
            range = getRangeList(self.request.POST.get("munic", ""))

            for r in range:
                varsR_id.append(str(r[0]))

            varsR_id = ",".join(varsR_id)

        return {'activeUser': self.user, "msg": msg, "fill_reg": fill_regN, "range": range, "varsR_id": varsR_id}


@view_config(route_name='weighing', renderer='templates/weighing.jinja2')
class weighing_view(privateView):
    def processView(self):
        DashJS.need()
        DashCSS.need()
        baselineR.need()
        regJS_CSS.need()
        fill_regN = fill_reg()
        msg = []
        rules=[]

        munId=""

        if "submit" in self.request.POST:
            # if "update_data" in self.request.POST:

            fill_regN["sel"] = int(self.request.POST.get("munic", ""))
            fill_regN["s_depto"] = int(self.request.POST.get("depto", ""))
            fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("munic", ""))).title()
            fill_regN["lb_m"] = getBaselinesName()
            lb_data = getBaselines(int(self.request.POST.get("munic", "")), "cf")
            #rules,munId=getRules(int(self.request.POST.get("munic", "")))
        else:
            if "id_mun_sel" in self.request.POST and not "update_data" in self.request.POST and not "submit_lb" in self.request.POST:
                msg = delete_lb(self.request.POST.get("id_mun_sel", ""), "cf")
                fill_regN["sel"] = int(self.request.POST.get("id_mun_sel", ""))
                fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("id_mun_sel", ""))).title()
                fill_regN["lb_m"] = getBaselinesName()
                fill_regN["s_depto"] = int(self.request.POST.get("id_depto_sel", ""))
                lb_data = getBaselines(int(self.request.POST.get("id_mun_sel", "")), "cf")
                #rules,munId = getRules(int(self.request.POST.get("id_mun_sel", "")))
                log(self.user.login, "weighing deleted in " + getMunicName(
                    int(self.request.POST.get("id_mun_sel", ""))).title(),
                    "normal", "3")
            else:
                if "update_data" in self.request.POST:
                    msg = updateData(self.request.POST.get("id_mun_sel", ""),
                                     self.request.POST.get("mun_sel_data2", ""), "cf")
                    fill_regN["sel"] = int(self.request.POST.get("id_mun_sel", ""))
                    fill_regN["s_depto"] = int(self.request.POST.get("id_depto_sel", ""))
                    fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("id_mun_sel", ""))).title()
                    fill_regN["lb_m"] = getBaselinesName()
                    lb_data = getBaselines(int(self.request.POST.get("id_mun_sel", "")), "cf")
                    #rules,munId = getRules(int(self.request.POST.get("id_mun_sel", "")))
                    log(self.user.login,
                        "weighing updated in " + getMunicName(int(self.request.POST.get("id_mun_sel", ""))).title(),
                        "normal", "2")
                else:
                    if "submit_lb" in self.request.POST:
                        save_data = self.request.POST.get("mun_sel_data", "")
                        fill_regN["s_depto"] = int(self.request.POST.get("id_depto_sel", ""))
                        fill_regN["sel"] = int(self.request.POST.get("id_mun_sel", ""))
                        fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("id_mun_sel", ""))).title()
                        fill_regN["lb_m"] = getBaselinesName()
                        msg = newBaseline(save_data, "cf")
                        lb_data = getBaselines(int(self.request.POST.get("id_mun_sel", "")), "cf")
                        #rules,munId = getRules(int(self.request.POST.get("id_mun_sel", "")))
                        # log(self.user.login, "new weighing in " + getMunicName(
                        #    int(self.request.POST.get("id_mun_sel", ""))).title() + " for var " + self.request.POST.get(
                        #    "id_mun_sel", ""),
                        #    "normal", "1")
                    else:
                        fill_regN["sel"] = 0
                        fill_regN["sel_name"] = ""
                        fill_regN["lb_m"] = []
                        lb_data = getBaselines(0, "cf")




        return {'activeUser': self.user, "lb_data": lb_data, "fill_reg": fill_regN, "msg": msg}


from pprint import pprint


@view_config(route_name='pilares', renderer='templates/pilares.jinja2')
class pilares_view(privateView):
    def processView(self):
        DashJS.need()
        DashCSS.need()
        regJS_CSS.need()
        pilarCSS_JS.need()

        msg = []
        if "jsondata" in self.request.POST:
            msg = newPilar(self.request.POST.get("jsondata", ""), self.user.login)
            data = ast.literal_eval(self.request.POST.get("jsondata", ""))
            log(self.user.login, "new pilar " + data["pilarName"] + " in " + self.user.login, "normal", "1")
        if "p_id" in self.request.POST:
            msg = delPilar(self.request.POST.get("p_id"))
            log(self.user.login, "pilar deleted " + self.request.POST.get("p_id") + " for " + self.user.login, "normal",
                "3")
        if "btn_save_var" in self.request.POST:
            msg = updateVar(self.request.POST.get("vd1"), self.request.POST.get("vd2"), self.request.POST.get("vd3"),
                            self.request.POST.get("vd4"), self.request.POST.get("vId"), self.request.POST.get("vdR"))
            log(self.user.login, "var " + self.request.POST.get("vId") + " updated ", "normal",
                "2")
        pilar_data, vars_id = getPilarData(self.user.login)
        # baselineR.need()
        # regJS_CSS.need()



        return {'activeUser': self.user, "pilar_data": pilar_data, "msg": msg, "vars_id": ",".join(vars_id)}


@view_config(route_name='forms', renderer='templates/forms.jinja2')
class forms_view(privateView):
    def processView(self):
        DashJS.need()
        DashCSS.need()
        regJS_CSS.need()
        formsCSS_JS.need()
        msg = []

        # print self.request.POST


        for f in self.request.POST:
            if "fu_" in f:
                msg = updateFU(self.request.POST.get(f), self.request, self.user.login)
                log(self.user.login, "form updated " + self.request.POST.get(f),
                    "normal",
                    "2")
        if "form_id" in self.request.POST:
            msg = delForm(self.request, self.request.POST.get("form_id"), self.user.login)
            log(self.user.login, "form " + str(self.request.POST.get("form_id")) + " deleted",
                "normal",
                "3")

        if "fn" in self.request.POST:
            msg = newForm(self.request, self.request.POST.get("fn"), self.user.login,
                          self.request.POST.get("if_select"))
            log(self.user.login, "new form " + self.request.POST.get("fn"),
                "normal",
                "1")

        formList = getForms(self.user.login)

        return {'activeUser': self.user, "msg": msg, "lists": getListPU(self.user.login), "formList": formList,
                "forms_id": forms_id(self.user.login)}


@view_config(route_name='report', renderer='templates/report.jinja2')
class report_view(privateView):
    def processView(self):
        basicCSS.need()
        DashJS.need()
        DashCSS.need()
        reportJS.need()
        regJS_CSS.need()
        # date = self.request.matchdict["date"]

        msg = []


        date = self.request.url.split("/")[-1].split("_")
        resp=""

        # date = date.split("_")
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
                 "Noviembre", "Diciembre"]

        log(self.user.login, "report generated for " + "_".join(date), "normal", "4")

        if "linkRep" in self.request.POST:
            if self.user.user_role == 2 or self.user.user_role == 3:
                user_d = getUserData(getUserByMunic(getMunicId(self.request.POST.get("rep_mun"))))

                if user_d == "ND":
                    msg = ["Info", "No hay ningun monitor asignado a este municipio", "info"]
                    data_rep = {}
                else:
                    user_d.user = user_d
                    user_d.request = self.request
                    return genPPTX(user_d, date)
            else:
                return genPPTX(self, date)

        if self.user.user_role == 2:
            #if "linkRep" in self.request.POST:
            #    return genPPTX(self, date)
            user_d = getUserData(getUserByMunic(self.request.POST.get("munic_sel")))
            if user_d == "ND":
                msg = ["Info", "No hay ningun monitor asignado a este municipio", "info"]
                data_rep = {}
            else:
                user_d.user = user_d
                user_d.request = self.request

                data_rep = dataReport(user_d, str(int(meses.index(date[0])) + 1), str(date[1]))

            return {'activeUser': self.user, "date": int(meses.index(date[0])) + 1,
                    "dataReport": data_rep, "dates": date, "depto": getDeptName(getUserDeptoID(self.user.login))
                , "munics": getMunics(getUserDeptoID(self.user.login)), "msg": msg,
                    "sel_m": self.request.POST.get("munic_sel")}

        if self.user.user_role == 3:
            #if "linkRep" in self.request.POST:
            #    return genPPTX(self, date)
            user_d = getUserData(getUserByMunic(self.request.POST.get("munic_sel")))
            if user_d == "ND":
                msg = ["Info", "No hay ningun monitor asignado a este municipio", "info"]
                data_rep = {}
            else:
                user_d.user = user_d
                user_d.request = self.request
                data_rep = dataReport(user_d, str(int(meses.index(date[0])) + 1), str(date[1]))

            return {'activeUser': self.user, "date": int(meses.index(date[0])) + 1,
                    "dataReport": data_rep, "dates": date,"fill_reg": fill_reg(), "msg": msg,
                    "sel_m": self.request.POST.get("munic_sel"), "sel_d":self.request.POST.get("dep_sel") }


        else:
            if "linkRep" in self.request.POST:
                return genPPTX(self, date)

            return {'activeUser': self.user, "date": int(meses.index(date[0])) + 1,
                    "dataReport": dataReport(self, str(int(meses.index(date[0])) + 1), str(date[1])), "dates": date,
                    "msg": msg}


@view_config(route_name='logout', renderer=None)
def logout_view(request):
    headers = forget(request)
    loc = request.route_url('home')
    return HTTPFound(location=loc, headers=headers)


import shutil,json

@view_config(route_name='uploadfiles', renderer=None)
class uploadfiles_view(privateView):
    def processView(self):


        if self.user.user_role:
            if self.request.POST.get("getFiles") !="1" :
                user_d = getUserData(getUserByMunic(self.request.POST.get("getFiles")))
                user_d.user = user_d
                user_d.request = self.request
                response = Response(status=201)
                response.body = json.dumps({"ff": getFilesList(user_d, self.request.POST.get("date")), "login":user_d.user.login})
                response.content_type = 'application/json'
                return response
            else:
                response = Response(status=201)
                response.body = json.dumps({"ff": getFilesList(self, self.request.POST.get("date"))})
                response.content_type = 'application/json'
                return response




        if "getFiles" in self.request.POST:
            response = Response(status=201)
            response.body = json.dumps({"ff":getFilesList(self,self.request.POST.get("date"))})
            response.content_type = 'application/json'
            return response
            #return response


        else:
            if "userfile" in self.request.POST:

                fname= self.request.params['userfile'].filename
                ff= self.request.POST['userfile'].file


                file_path = os.path.join(self.request.registry.settings['user.repository'], self.user.parent, "user",
                                    self.user.login, "attach", self.request.POST.get("date"))

                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                file_path=file_path+"/"+fname

                ff.seek(0)
                with open(file_path, 'wb') as output_file:
                    shutil.copyfileobj(ff, output_file)


                return Response(status=201)

@view_config(route_name='downfiles', renderer=None)
class downfiles(publicView):
    def processView(self):
        try:
            url=self.request.url.split("downfiles")
            path = self.request.registry.settings['user.repository'] + url[1].replace("%20", " ")



            if url[1][-8:] == "_delfile":
                os.remove(path.replace("_delfile", ""))
                #response = Response(status=201)
                #response.body = json.dumps({"ff": getFilesList(self, url[1].split("/")[-2])})
                #response.content_type = 'application/json'
                #return response
                loc = self.request.route_url('dashboard')
                return HTTPFound(location=loc)

            else:



                response = FileResponse(
                    path,
                    request=self.request,
                    content_type="application/download"
                )
                response.content_disposition = 'attachment; filename="' + self.request.url.split("/")[-1] + '"'

                return response
        except:
            return Response(status=404)


@view_config(route_name='logs', renderer='templates/logs.jinja2')
class logs_view(privateView):
    def processView(self):

        return {'activeUser': self.user, "plogs":getLoglist(self,self.user.login)}


@view_config(route_name='seasonality', renderer='templates/seasonality.jinja2')
class seasonality_view(privateView):
    def processView(self):
        DashJS.need()
        DashCSS.need()
        baselineR.need()
        regJS_CSS.need()
        seasonCSS_JS.need()
        print getBaselines(0, "lb")
        return {'activeUser': self.user,  "msg": [], "rules":GetSeasonsRules()}

@view_config(route_name='gtool', renderer='templates/gtool.jinja2')
class gtool_view(privateView):
    def processView(self):
        DashJS.need()
        DashCSS.need()
        regJS_CSS.need()
        msg = []
        data4plot = []
        gtoolCSS_JS.need()


        if "getData4Analize" in self.request.POST:
            if self.user.user_role == 2 or self.user.user_role == 3:
                if "if_munic" in self.request.POST:
                    user_d = getUserData(getUserByMunic(self.request.POST.get("if_munic")))

                    #user_d = getUserData(getUserByMunic(self.request.POST.get("munic_sel")))

                    if user_d == "ND":
                        msg = ["Info", "No hay ningun monitor asignado a este municipio", "info"]
                        data4plot = []
                    else:

                        user_d.user = user_d
                        user_d.request = self.request

                        vals = self.request.POST.get('getData4Analize', '').split("*$%")
                        val, data4plot = getData4Analize(user_d, vals)
                        if val == 1:
                            msg = data4plot
                            data4plot = []
                        log(self.user.login, "request data for gtool: " + self.request.POST.get('getData4Analize', ''),
                            "normal",
                            "4")
            else:
                vals = self.request.POST.get('getData4Analize', '').split("*$%")
                val, data4plot = getData4Analize(self, vals)
                if val == 1:
                    msg = data4plot
                    data4plot = []
                log(self.user.login, "request data for gtool: " + self.request.POST.get('getData4Analize', ''),
                    "normal",
                    "4")
        if self.user.user_role == 3:
            return {'activeUser': self.user, "filldata": getGToolData(self), "msg": msg, "data4plot": data4plot,"fill_reg": fill_reg(),
                    "dates": self.request.cookies["cur_date"].split("_"), "sel_d": getDepByMunic(self.request.POST.get("if_munic")),
                    "sel_m": self.request.POST.get("if_munic"),
                    "title": "Departamento: " }

        else:
            if self.user.user_role == 2:

                return {'activeUser': self.user, "filldata": getGToolData(self), "msg": msg, "data4plot": data4plot,
                        "dates": self.request.cookies["cur_date"].split("_"),
                        "depto": getDeptName(getUserDeptoID(self.user.login)),
                        "munics": getMunics(getUserDeptoID(self.user.login)), "sel_m":self.request.POST.get("if_munic"),  "title":"Departamento: "+getDeptName(getUserDeptoID(self.user.login))}
            else:
                return {'activeUser': self.user, "filldata": getGToolData(self), "msg": msg, "data4plot": data4plot,
                        "dates": self.request.cookies["cur_date"].split("_"), "title":"Municipio: "+self.user.munic}


@view_config(route_name='dashboard', renderer='templates/dashboard.jinja2')
class dashboard_view(privateView):
    def processView(self):
        # self.needJS('dashboard')
        regJS_CSS.need()

        DashJS.need()
        DashCSS.need()
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
                 "Noviembre", "Diciembre"]

        print self.request.POST
        msg = []

        if "munic_sel" in self.request.POST:
            if self.request.POST.get("munic_sel") == "":
                msg = ["Info", "Debe seleccioonar un municipio", "info"]
                date = self.request.POST.get('dateP', '').split(" ")
                dashData = getDashReportData(self, str(meses.index(date[0]) + 1), date[1])

            else:
                user_d = getUserData(getUserByMunic(self.request.POST.get("munic_sel")))

                if user_d == "ND":
                    msg = ["Info", "No hay ningun monitor asignado a este municipio", "info"]
                    date = self.request.POST.get('dateP', '').split(" ")
                    dashData = getDashReportData(self, str(meses.index(date[0]) + 1), date[1])
                else:
                    user_d.user = user_d
                    user_d.request = self.request

                    if 'dateP' in self.request.POST:
                        date = self.request.POST.get('dateP', '').split(" ")
                        dashData = getDashReportData(user_d, str(meses.index(date[0]) + 1), date[1])
                        log(self.user.login, "request data for dashboard for " + "_".join(date),
                            "normal",
                            "4")
                    else:

                        if "cur_date" in self.request.cookies:
                            date = self.request.cookies["cur_date"].split("_")
                            dashData = getDashReportData(user_d, str(meses.index(date[0]) + 1), date[1])
                        else:
                            date = datetime.now().strftime("%m %Y").split(" ")
                            dashData = getDashReportData(user_d, date[0], date[1])
                        log(self.user.login, "request data for dashboard for " + "_".join(date),
                            "normal",
                            "4")
        else:

            if 'dateP' in self.request.POST:
                date = self.request.POST.get('dateP', '').split(" ")
                dashData = getDashReportData(self, str(meses.index(date[0]) + 1), date[1])
                log(self.user.login, "request data for dashboard for " + "_".join(date),
                    "normal",
                    "4")

            else:
                if "cur_date" in self.request.cookies:
                    date = self.request.cookies["cur_date"].split("_")
                    dashData = getDashReportData(self, str(meses.index(date[0]) + 1), date[1])
                else:
                    date = datetime.now().strftime("%m %Y").split(" ")
                    dashData = getDashReportData(self, date[0], date[1])
                log(self.user.login, "request data for dashboard for " + "_".join(date),
                    "normal",
                    "4")

        if self.user.user_role ==3:
            return {'activeUser': self.user, "dashData": dashData, "report": True, "msg": msg,"sel_d": self.request.POST.get("dep_sel"),
                    "sel_m": self.request.POST.get("munic_sel"), "munid": self.request.POST.get("munic_sel"),  "fill_reg": fill_reg()}
        else:


            if self.user.user_role == 2:
                return {'activeUser': self.user, "dashData": dashData, "report": True,
                        "depto": getDeptName(getUserDeptoID(self.user.login)),
                        "munics": getMunics(getUserDeptoID(self.user.login)), "msg": msg,
                        "sel_m": self.request.POST.get("munic_sel"), "munid":self.request.POST.get("munic_sel")}
            else:
                return {'activeUser': self.user, "dashData": dashData, "report": True, "munid": getMunicId(self.user.munic),
                        "msg": msg}

            # return render_to_response({'activeUser': self.user, "dashData": dashData, "report": True}, request=request)


class download_xls(privateView):
    def processView(self):
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
                 "Noviembre", "Diciembre"]


        if "genXLS" in self.request.POST:
            if self.user.user_role == 2 or self.user.user_role == 3:
                date = self.request.POST.get('genXLS', '').split(" ")
                date[0] = str(meses.index(date[0]) + 1)
                user_d = getUserData(getUserByMunic(date[2]))
                user_d.user = user_d
                user_d.request = self.request
                response = genXLS(user_d, getDashReportData(user_d, date[0], date[1]), date[0])
                log(self.user.login, "download xls for %s-%s" % (str(date[0]), str(date[1])),
                    "normal",
                    "4")
            else:
                date = self.request.POST.get('genXLS', '').split(" ")
                date[0] = str(meses.index(date[0]) + 1)
                response = genXLS(self, getDashReportData(self, date[0], date[1]), date[0])
                log(self.user.login, "download xls for %s-%s" % (str(date[0]), str(date[1])),
                    "normal",
                    "4")

        return response


class download_helpfiles(privateView):
    def processView(self):
        return getFileResponse(self.request)


@view_config(route_name='home', renderer='templates/login.jinja2')
class login_view(publicView):
    def processView(self):
        login = authenticated_userid(self.request)
        currentUser = getUserData(login)
        if currentUser is not None:
            return HTTPFound(location=self.request.route_url('dashboard'))

        next = self.request.params.get('next') or self.request.route_url('dashboard')
        login = ''
        curr_p = ''
        did_fail = False
        if 'submit' in self.request.POST:
            login = self.request.POST.get('login', '')
            passwd = self.request.POST.get('passwd', '')
            user = getUserData(login)

            if not user == None and user.check_password(passwd):
                headers = remember(self.request, login)
                log(login, "login", "normal", "4")
                if user.user_role == 1:
                    response = HTTPFound(location=self.request.route_url('pilares'), headers=headers)
                else:
                    response = HTTPFound(location=next, headers=headers)
                response.set_cookie('_LOCALE_', value='es', max_age=1080000)

                return response
            did_fail = True

        return {'login': login, 'failed_attempt': did_fail, 'next': next, 'curr_p': curr_p}


@view_config(route_name='register', renderer='templates/register.jinja2')
class register_view(privateView):
    def processView(self):
        DashJS.need()
        DashCSS.need()
        regJS_CSS.need()
        formsCSS_JS.need()
        result = []


        if "up_user_val" in self.request.POST or "up_user_pass" in self.request.POST:
            result = updateUser(self.user.login, self.request, self.request.POST)
            if "up_user_pass" in self.request.POST:
                log(self.user.login, "update user pass " + self.request.POST.get("up_user_pass"), "normal", "2")
            else:
                log(self.user.login, "update user " + self.request.POST.get("up_user_val"), "normal", "2")

        if "uname_u" in self.request.POST:
            result = delUser(self.request.POST.get("uname_u", ""), self.user.login, self.request)
            log(self.user.login, "del user" + self.request.POST.get("uname_u", ""), "normal", "3")

        if "reg" in self.request.POST:
            user_val = addNewUser(self.request.POST, self.request, self.user.login)
            # user_val = 2
            if user_val == 0:
                result.append("Error")
                result.append("Ya existe un usuario asignado para ese lugar")
                result.append("error")
            if user_val == 1:
                result.append("Correcto")
                result.append("Usuario creado correctamente")
                result.append("success")
                log(self.user.login, "new user" + self.request.POST.get("user_name", ""), "normal", "1")
            if user_val == 2:
                result.append("Error")
                result.append("Ya existe ese nombre de usuario")
                result.append("warning")
            if user_val == 3:
                result.append("Error")
                result.append("Error al registrar este usuario")
                result.append("error")
            if user_val == 4:
                result.append("Error")
                result.append(
                    "Antes de agregar un usuario a este municipio debe ingresar las lineas base y coeficientes respectivos")
                result.append("error")

        return {'activeUser': self.user, "fill_reg": fill_reg(), "msg": result,
                "ulist": getUsersList(self.user.login, 0), "ulist2": getUsersList(self.user.login, 2), "ulist3": getUsersList(self.user.login, 3) }


class formList_view(odkView):
    def processView(self):

        try:
            if isUserActive(self.user):

                if self.authorize(getUserPassword(self.user, self.request)):

                    log(self.user, "formlist", "normal", "4")

                    return self.createXMLResponse(getFormList(self.user, self.request))

                else:

                    return self.askForCredentials()
            else:
                return self.askForCredentials()
        except:

            return self.askForCredentials()


class manifest_view(odkView):
    def processView(self):
        if self.authorize(getUserPassword(self.user, self.request)):

            return self.createXMLResponse(getManifest(self.user, self.request))
        else:
            return self.askForCredentials()


class mediaFile_view(odkView):
    def processView(self):
        fileid = self.request.matchdict['fileid']
        if isUserActive(self.user):
            if self.authorize(getUserPassword(self.user, self.request)):
                return getMediaFile(self.user, self.request, fileid)
            else:
                return self.askForCredentials()
        else:
            return self.askForCredentials()


class XMLForm_view(odkView):
    def processView(self):

        if self.authorize(getUserPassword(self.user, self.request)):
            return getXMLForm(self.user, self.request)
        else:
            return self.askForCredentials()


class push_view(odkView):
    def processView(self):

        if self.request.method == "POST":
            if isUserActive(self.user):
                if self.authorize(getUserPassword(self.user, self.request)):
                    print "here---------------"
                    if storeSubmission(self.user, self.request):
                        print "if---------------"
                        response = Response(status=201)
                        log(self.user, "store submission", "normal", "4")
                        sendGroup(self.request, self.user)
                        return response
                    else:
                        print "else---------------"

                        response = Response(status=502)
                        return response
                else:
                    return self.askForCredentials()
            else:
                response = Response(status=401)
                return response
        else:
            response = Response(status=404)
            return response


class submission_view(odkView):
    def processView(self):
        # userid = self.request.matchdict['userid']
        #print self.request.method
        if self.request.method == 'HEAD':
            if isUserActive(self.user):
                headers = [('Location',
                            self.request.route_url('odkpush', parent=getParent(self.user), user=self.user))]
                response = Response(headerlist=headers, status=204)
                return response
            else:
                return self.askForCredentials()
        else:
            response = Response(status=404)
            return response


class munic_kml(publicView):
    def processView(self):
        try:
            path = os.path.join(self.request.registry.settings['user.repository'], "kml_codes",
                                self.request.url.split("/")[-1])

            response = FileResponse(
                path,
                request=self.request,
                content_type="KML"
            )
            response.content_disposition = 'attachment; filename="' + self.request.url.split("/")[-1] + '"'

            return response
        except:
            return Response(status=404)


@view_config(route_name='rules', renderer=None)
class rules_view(publicView):
    def processView(self):


        if (self.request.POST.get("type")=="rm_rule"):
            data= delRule(self.request.POST)
            response = Response(status=200, body=json.dumps(data))
            response.headers.update({
                'Access-Control-Allow-Origin': '*',
            })

            return response

        data= newRule(self.request.POST)


        response = Response(status=200, body=json.dumps(data))
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
        })

        return response

