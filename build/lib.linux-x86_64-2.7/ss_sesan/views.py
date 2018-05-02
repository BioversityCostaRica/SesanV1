from pyramid.view import view_config
from pyramid.security import remember, authenticated_userid,forget
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from classes import publicView,privateView,odkView
from auth import getUserData
from resources import DashJS,DashCSS, basicCSS
from processes.get_vals import fill_reg,addNewUser,getDashReportData,getConfigQR
from processes.utilform import isUserActive,getUserPassword, getFormList,isUserinOrg, getManifest,getMediaFile,getXMLForm,getOrganization,getOrganizationID, storeSubmission
from datetime import datetime


@view_config(route_name='profile', renderer='templates/profile.jinja2')
class profile_view(privateView):
    def processView(self):
        DashJS.need()
        DashCSS.need()


        return {'activeUser': self.user, "config" : getConfigQR(self.user.login, self.user.organization,self.request)}


@view_config(route_name='report', renderer='templates/report.jinja2')
class report_view(privateView):
    def processView(self):
        basicCSS.need()
        DashJS.need()
        DashCSS.need()
        return {'activeUser': self.user, "date":datetime.now().strftime("%d-%m-%Y")}



@view_config(route_name='logout', renderer=None)
def logout_view(request):
    headers = forget(request)
    loc = request.route_url('home')
    return HTTPFound(location=loc, headers=headers)


@view_config(route_name='dashboard', renderer='templates/dashboard.jinja2')
class dashboard_view(privateView):
    def processView(self):
        #self.needJS('dashboard')
        meses=["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
                "Noviembre", "Diciembre"]
        DashJS.need()
        DashCSS.need()
        if 'dateP' in self.request.POST:
            new_date = self.request.POST.get('dateP', '').split(" ")
            dashData=getDashReportData(self,str(meses.index(new_date[0])+1), new_date[1])
        else:
            date = datetime.now().strftime("%m %Y").split(" ")
            dashData=getDashReportData(self, date[0], date[1])

        return {'activeUser': self.user, "dashData": dashData}


@view_config(route_name='home', renderer='templates/login.jinja2')
class login_view(publicView):
    def processView(self):
        login = authenticated_userid(self.request)
        currentUser = getUserData(login)
        if currentUser is not None:
            return HTTPFound(location=self.request.route_url('dashboard'))
        next = self.request.params.get('next') or self.request.route_url('dashboard')
        login = ''
        curr_p=''
        did_fail = False
        if 'submit' in self.request.POST:
            login = self.request.POST.get('login', '')
            passwd = self.request.POST.get('passwd', '')
            user = getUserData(login)

            if not user == None and user.check_password(passwd):
                headers = remember(self.request, login)
                response = HTTPFound(location=next, headers=headers)
                response.set_cookie('_LOCALE_', value='es', max_age=31536000)

                return response
            did_fail = True

        return {'login': login, 'failed_attempt': did_fail, 'next': next, 'curr_p':curr_p}


@view_config(route_name='register', renderer='templates/register.jinja2')
class register_view(privateView):
    def processView(self):
        DashJS.need()
        DashCSS.need()
        if "reg" in self.request.POST:
            user_val=addNewUser(self.request.POST,self.request)
            if user_val == 0:
                print "ya existe un usuarios para esa institucion en ese municipio"
            if user_val == 1:
                print "usuario creado correctamente"
            if user_val == 2:
                print "ya existe ese nombre de usuario"
            if user_val == 3:
                print "el resultado es none"


        return {'activeUser': self.user, "fill_reg": fill_reg()}


class formList_view(odkView):
    def processView(self):
        try:
            org = getOrganization(self.user)
            if isUserActive(self.user):
                if self.authorize(getUserPassword(self.user,self.request)):
                    return self.createXMLResponse(getFormList(self.user,org,self.request))
                else:
                    return self.askForCredentials()
            else:
                return self.askForCredentials()
        except:
            return self.askForCredentials()

class manifest_view(odkView):
    def processView(self):
        org = getOrganization(self.user)
        orgId = getOrganizationID(self.user)
        if isUserinOrg(self.user, orgId):
            if self.authorize(getUserPassword(self.user,self.request)):
                return self.createXMLResponse(getManifest(self.user,org,self.request))
            else:
                return self.askForCredentials()
        else:
            return self.askForCredentials()

class mediaFile_view(odkView):
    def processView(self):
        org = getOrganization(self.user)
        if isUserActive(self.user):
            if self.authorize(getUserPassword(self.user, self.request)):
                return getMediaFile(org,self.user,self.request)
            else:
                return self.askForCredentials()
        else:
            return self.askForCredentials()


class XMLForm_view(odkView):
    def processView(self):
        orgId = getOrganizationID(self.user)
        org = getOrganization(self.user)
        if isUserinOrg(self.user,orgId):
            if self.authorize(getUserPassword(self.user, self.request)):
                return getXMLForm(self.user, org,self.request)
            else:
                return self.askForCredentials()
        else:
            return self.askForCredentials()


class push_view(odkView):
    def processView(self):
        if self.request.method == "POST":
            if isUserActive(self.user):
                if self.authorize(getUserPassword(self.user,self.request)):
                    if storeSubmission(self.user,self.request):
                        response = Response(status=201)
                        return response
                    else:
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
        #userid = self.request.matchdict['userid']
        if self.request.method == 'HEAD':
            if isUserActive(self.user):
                headers = [('location', self.request.route_url('odkpush', organization=getOrganization(self.user), user=self.user))]
                response = Response(headerlist=headers, status=204)
                return response
            else:
                return self.askForCredentials()
        else:
            response = Response(status=404)
            return response