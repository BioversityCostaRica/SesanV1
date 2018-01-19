from .models import DBSession,User as userModel, Institucione,Munic
from .encdecdata import decodeData

import urllib, hashlib,arrow


#User class Used to store information about the user
class User(object):
    def __init__(self, login, password, fullName, organization, email, munic, joindate, user_role):


        default = "identicon"
        size = 45
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})

        self.login = login
        self.password = password

        self.fullName = fullName
        self.organization = organization
        self.email = email
        self.munic = munic
        self.joindate = joindate
        self.user_role=user_role


        self.gravatarURL = gravatar_url

    def check_password(self, passwd):
        return checkLogin(self.login,passwd)

    def getGravatarUrl(self,size):
        default = "identicon"
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
        return gravatar_url

    def updateGravatarURL(self):
        default = "identicon"
        size = 45
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
        self.gravatarURL = gravatar_url

    def getJoinDate(self,joindate):
        ar = arrow.get(joindate)
        joindate = ar.format('dddd  d, MMMM, YYYY', locale="es")
        return joindate

# #We need to change this so the users are loaded from the database
# def add_user(login,fullName, organization, email,country, sector,about, **kw):
#     config.USERS[login] = User(login,"",fullName,organization,email,country,sector,about, **kw)
#     return config.USERS[login]
#
# #Root authorization we only have two set of groups. AuthUsers allowed to edit and admin
# class Root(object):
#     __acl__ = [
#         (Allow, 'g:authusers', 'edit'),
#         (Allow, 'g:admin', ALL_PERMISSIONS),
#     ]
#
#     def __init__(self, request):
#         self.request = request
#
# def groupfinder(userid, request):
#     user = config.USERS.get(userid)
#     if user:
#         return ['g:%s' % g for g in user.groups]

def getUserData(user):
    res = None
    mySession = DBSession()
    result = mySession.query(userModel).filter_by(user_name = user).filter_by(user_active = 1).first()

    if not result is None:
        res = User(result.user_name,"",result.user_fullname,getOrgName(result.user_organization),result.user_email, getMunicName(result.user_munic),result.user_joindate,result.user_role)
    mySession.close()
    return res


def getOrgName(org):
    res = None
    mySession = DBSession()
    result = mySession.query(Institucione).filter_by(insti_id = org).first()

    if not result is None:
        res = result.insti_nombre
    mySession.close()
    return res

def getMunicName(id):
    res = None
    mySession = DBSession()
    result = mySession.query(Munic).filter_by(munic_id =id).first()

    if not result is None:
        res = result.munic_nombre
    mySession.close()
    return res


def checkLogin(user,password):
    mySession = DBSession()
    result = mySession.query(userModel).filter_by(user_name = user).filter_by(user_active = 1).first()

    if result is None:
        mySession.close()
        return False
    else:
        cpass = decodeData(result.user_password)
        if cpass == password:
            mySession.close()
            return True
        else:
            mySession.close()
            return False


