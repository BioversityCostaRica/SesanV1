from pyramid.view import view_config
from pyramid.security import remember, authenticated_userid, forget
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from .classes import publicView, privateView, odkView
from .auth import getUserData
from .resources import DashJS, DashCSS, basicCSS, regJS_CSS, reportJS, baselineR, pilarCSS_JS, formsCSS_JS
from processes.get_vals import updateData, delete_lb, newBaseline, fill_reg, addNewUser, getDashReportData, getConfigQR, \
    valReport, dataReport, getBaselines, getMunicName, getBaselinesName, genXLS, getUsersList, delUser
from processes.utilform import isUserActive, getUserPassword, getFormList, getParent, getManifest, getMediaFile, \
    getXMLForm, storeSubmission
from datetime import datetime
from pyramid.response import FileResponse
import os
from .processes.setFormVals import newPilar, getPilarData, delPilar, updateVar, getListPU, newForm, getForms,delForm,forms_id


#task
# validar que se pueda borrar un pilar en uso o un form en uso
# elimnar usuario tambien del form
# cantidad de envios del form
# revisar que no se pueda borrar lineas base y coef en munic con datos solo update
#

@view_config(route_name='profile', renderer='templates/profile.jinja2')
class profile_view(privateView):
    def processView(self):
        DashJS.need()
        DashCSS.need()

        return {'activeUser': self.user, "config": getConfigQR(self.user.login,self.user.parent, self.request)}

@view_config(route_name='about', renderer='templates/about.jinja2')
class about_view(privateView):
    def processView(self):
        DashJS.need()
        DashCSS.need()

        return {'activeUser': self.user}




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
            fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("munic", ""))).title()
            fill_regN["lb_m"] = getBaselinesName()
            lb_data = getBaselines(int(self.request.POST.get("munic", "")), "lb")
        else:
            if "id_mun_sel" in self.request.POST and not "update_data" in self.request.POST and not "submit_lb" in self.request.POST:
                msg = delete_lb(self.request.POST.get("id_mun_sel", ""), "lb")
                fill_regN["sel"] = int(self.request.POST.get("id_mun_sel", ""))
                fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("id_mun_sel", ""))).title()
                fill_regN["lb_m"] = getBaselinesName()
                lb_data = getBaselines(int(self.request.POST.get("id_mun_sel", "")), "lb")
            else:
                if "update_data" in self.request.POST:
                    msg = updateData(self.request.POST.get("id_mun_sel", ""),
                                     self.request.POST.get("mun_sel_data2", ""), "lb")
                    fill_regN["sel"] = int(self.request.POST.get("id_mun_sel", ""))
                    fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("id_mun_sel", ""))).title()
                    fill_regN["lb_m"] = getBaselinesName()
                    lb_data = getBaselines(int(self.request.POST.get("id_mun_sel", "")), "lb")
                else:
                    if "submit_lb" in self.request.POST:
                        save_data = self.request.POST.get("mun_sel_data", "")
                        fill_regN["sel"] = int(self.request.POST.get("id_mun_sel", ""))
                        fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("id_mun_sel", ""))).title()
                        fill_regN["lb_m"] = getBaselinesName()
                        msg = newBaseline(save_data, "lb")
                        lb_data = getBaselines(int(self.request.POST.get("id_mun_sel", "")), "lb")
                    else:
                        fill_regN["sel"] = 0
                        fill_regN["sel_name"] = ""
                        fill_regN["lb_m"] = []
                        lb_data = getBaselines(0, "lb")

        return {'activeUser': self.user, "lb_data": lb_data, "fill_reg": fill_regN, "msg": msg}

@view_config(route_name='weighing', renderer='templates/weighing.jinja2')
class weighing_view(privateView):
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
            fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("munic", ""))).title()
            fill_regN["lb_m"] = getBaselinesName()
            lb_data = getBaselines(int(self.request.POST.get("munic", "")), "cf")
        else:
            if "id_mun_sel" in self.request.POST and not "update_data" in self.request.POST and not "submit_lb" in self.request.POST:
                msg = delete_lb(self.request.POST.get("id_mun_sel", ""), "cf")
                fill_regN["sel"] = int(self.request.POST.get("id_mun_sel", ""))
                fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("id_mun_sel", ""))).title()
                fill_regN["lb_m"] = getBaselinesName()
                lb_data = getBaselines(int(self.request.POST.get("id_mun_sel", "")), "cf")
            else:
                if "update_data" in self.request.POST:
                    msg = updateData(self.request.POST.get("id_mun_sel", ""),
                                     self.request.POST.get("mun_sel_data2", ""), "cf")
                    fill_regN["sel"] = int(self.request.POST.get("id_mun_sel", ""))
                    fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("id_mun_sel", ""))).title()
                    fill_regN["lb_m"] = getBaselinesName()
                    lb_data = getBaselines(int(self.request.POST.get("id_mun_sel", "")), "cf")
                else:
                    if "submit_lb" in self.request.POST:
                        save_data = self.request.POST.get("mun_sel_data", "")
                        fill_regN["sel"] = int(self.request.POST.get("id_mun_sel", ""))
                        fill_regN["sel_name"] = getMunicName(int(self.request.POST.get("id_mun_sel", ""))).title()
                        fill_regN["lb_m"] = getBaselinesName()
                        msg = newBaseline(save_data, "cf")
                        lb_data = getBaselines(int(self.request.POST.get("id_mun_sel", "")), "cf")
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
        print self.request.POST
        if "jsondata" in self.request.POST:
            msg = newPilar(self.request.POST.get("jsondata", ""), self.user.login)
        if "p_id" in self.request.POST:
            msg = delPilar(self.request.POST.get("p_id"))
        if "btn_save_var" in self.request.POST:
            msg = updateVar(self.request.POST.get("vd1"), self.request.POST.get("vd2"), self.request.POST.get("vd3"),
                            self.request.POST.get("vd4"), self.request.POST.get("vId"),self.request.POST.get("vdR"))
        pilar_data,vars_id = getPilarData(self.user.login)
        # baselineR.need()
        # regJS_CSS.need()
        return {'activeUser': self.user, "pilar_data": pilar_data, "msg": msg, "vars_id":",".join(vars_id)}


@view_config(route_name='forms', renderer='templates/forms.jinja2')
class forms_view(privateView):
    def processView(self):
        DashJS.need()
        DashCSS.need()
        regJS_CSS.need()
        formsCSS_JS.need()
        msg=[]

        print self.request
        if "form_id" in self.request.POST:
            msg=delForm(self.request,self.request.POST.get("form_id"), self.user.login)

        if "fn" in self.request.POST:
            msg=newForm(self.request,self.request.POST.get("fn"), self.user.login)
        formList=getForms(self.user.login)


        return {'activeUser': self.user, "msg":msg, "lists":getListPU(self.user.login), "formList":formList, "forms_id":forms_id(self.user.login)}




@view_config(route_name='report', renderer='templates/report.jinja2')
class report_view(privateView):
    def processView(self):
        basicCSS.need()
        DashJS.need()
        DashCSS.need()
        reportJS.need()
        date = self.request.matchdict["date"]

        date = date.split("_")
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
                 "Noviembre", "Diciembre"]
        return {'activeUser': self.user, "date": int(meses.index(date[0])) + 1,
                "dataReport": dataReport(self, str(int(meses.index(date[0])) + 1), str(date[1]))}


@view_config(route_name='logout', renderer=None)
def logout_view(request):
    headers = forget(request)
    loc = request.route_url('home')
    return HTTPFound(location=loc, headers=headers)


@view_config(route_name='dashboard', renderer='templates/dashboard.jinja2')
class dashboard_view(privateView):
    def processView(self):
        # self.needJS('dashboard')

        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
                 "Noviembre", "Diciembre"]
        DashJS.need()
        DashCSS.need()
        date = ""

        if 'dateP' in self.request.POST:
            date = self.request.POST.get('dateP', '').split(" ")
            dashData = getDashReportData(self, str(meses.index(date[0]) + 1), date[1])
            rep = valReport(self, str(meses.index(date[0]) + 1), date[1])
        else:
            date = datetime.now().strftime("%m %Y").split(" ")
            dashData = getDashReportData(self, date[0], date[1])
            rep = valReport(self, date[0], date[1])
            print rep
        return {'activeUser': self.user, "dashData": dashData, "report": rep}


class download_xls(privateView):
    def processView(self):
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
                 "Noviembre", "Diciembre"]
        if "genXLS" in self.request.POST:
            date = self.request.POST.get('genXLS', '').split(" ")
            date[0] = str(meses.index(date[0]) + 1)
            response = genXLS(self, getDashReportData(self, date[0], date[1]))

        return response


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
                if user.user_role == 1:
                    response = HTTPFound(location=self.request.route_url('pilares'), headers=headers)
                else:
                    response = HTTPFound(location=next, headers=headers)
                response.set_cookie('_LOCALE_', value='es', max_age=31536000)

                return response
            did_fail = True

        return {'login': login, 'failed_attempt': did_fail, 'next': next, 'curr_p': curr_p}


@view_config(route_name='register', renderer='templates/register.jinja2')
class register_view(privateView):
    def processView(self):
        DashJS.need()
        DashCSS.need()
        regJS_CSS.need()
        result = []

        #

        if "delUser" in self.request.POST:
            result = delUser(self.request.POST.get("uname_u", ""), self.user.login, self.request)

        if "reg" in self.request.POST:
            user_val = addNewUser(self.request.POST, self.request, self.user.login)
            # user_val = 2
            if user_val == 0:
                result.append("Error")
                result.append("Ya existe un usuario para esa institucion en el municipio seleccionado")
                result.append("error")
            if user_val == 1:
                result.append("Correcto")
                result.append("Usuario creado correctamente")
                result.append("success")
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
                result.append("Antes de agregar un usuario a este municipio debe ingresar las lineas base y coeficientes respectivos")
                result.append("error")

        return {'activeUser': self.user, "fill_reg": fill_reg(), "msj": result, "ulist": getUsersList(self.user.login)}


class formList_view(odkView):
    def processView(self):
        try:
            if isUserActive(self.user):
                if self.authorize(getUserPassword(self.user, self.request)):
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

                    if storeSubmission(self.user, self.request):
                        response = Response(status=201)
                        return response
                    else:

                        response = Response(status=502)
                        return response
                else:
                    print "push"
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
        if self.request.method == 'HEAD':
            if isUserActive(self.user):
                headers = [('location',
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
        # print self.request.url.split("/")[-1]
        try:
            path = os.path.join(self.request.registry.settings['user.repository'], "KML",
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
