from resources import commonJS, basicCSS
from pyramid.security import authenticated_userid
from auth import getUserData
from pyramid.httpexceptions import HTTPFound
from hashlib import md5
import uuid
from pyramid.response import Response
from webhelpers.html import literal
from pprint import pprint

class publicView(object):
    def __init__(self, request):
        self.request = request
        #self._ = self.request.translate

    def __call__(self):
        basicCSS.need()
        commonJS.need()
        return self.processView()

    def processView(self):
        return {}


class privateView(object):
    def __init__(self, request):
        self.request = request
        self.user = None
        #self._ = self.request.translate

    def __call__(self):
        basicCSS.need()
        commonJS.need()
        login = authenticated_userid(self.request)
        self.user = getUserData(login)
        if self.user == None:
            return HTTPFound(location=self.request.route_url('home'))
        return self.processView()

    def processView(self):
        return {'activeUser': self.user}

#ODKView is a Digest Authorization view. It automates all the Digest work
class odkView(object):
    def __init__(self, request):
        self.request = request
        self.nonce = md5(str(uuid.uuid4())).hexdigest()
        self.opaque = request.registry.settings['auth.opaque']
        self.realm = request.registry.settings['auth.realm']
        self.authHeader = {}
        self.user = ""


    def getAuthDict(self):
        authheader = self.request.headers["Authorization"].replace(", ", ",")
        authheader = authheader.replace('"', "")
        autharray = authheader.split(",")
        for e in autharray:
            t = e.split("=")
            self.authHeader[t[0]] = t[1]
        #pprint.pprint(self.authHeader)

    def authorize(self,correctPassword):
        #print "***********************77"
        #print self.request.method
        #pprint.pprint(self.authHeader)
        #print "***********************77"
        HA1 = ""
        HA2 = ""
        if self.authHeader["qop"] == 'auth':
            HA1 = md5(self.user + ":" + self.realm + ":" + correctPassword)
            HA2 = md5(self.request.method + ":" + self.authHeader["uri"])
        if self.authHeader["qop"] == 'auth-int':
            HA1 = md5(self.user + ":" + self.realm + ":" + correctPassword)
            MD5Body = md5(self.request.body).hexdigest()
            HA2 = md5(self.request.method + ":" + self.authHeader["uri"] + ":" + MD5Body)
        if HA1 == "":
            HA1 = md5(self.user + ":" + self.realm + ":" + correctPassword)
            HA2 = md5(self.request.method + ":" + self.authHeader["uri"])

        authLine = ":".join(
            [HA1.hexdigest(), self.authHeader["nonce"], self.authHeader["nc"], self.authHeader["cnonce"], self.authHeader["qop"], HA2.hexdigest()])

        resp = md5(authLine)
        if resp.hexdigest() == self.authHeader["response"]:
            return True
        else:
            #print "*********************88"
            #print "Calculated response: " + resp.hexdigest()
            #print "Header response: " + self.authHeader["response"]
            #print "*********************88"
            return False

    def askForCredentials(self):
        headers = [('WWW-Authenticate',
                    'Digest realm="' + self.realm + '",qop="auth,auth-int",nonce="' + self.nonce + '",opaque="' + self.opaque + '"')]
        reponse = Response(status=401, headerlist=headers)
        return reponse

    def createXMLResponse(self,XMLData):
        headers = [('Content-Type', 'text/xml; charset=utf-8'), ('X-OpenRosa-Accept-Content-Length', '10000000'),
                   ('Content-Language', self.request.locale_name), ('Vary', 'Accept-Language,Cookie,Accept-Encoding'),
                   ('X-OpenRosa-Version', '1.0'), ('Allow', 'GET, HEAD, OPTIONS')]
        response = Response(headerlist=headers, status=200)
        response.text = literal(XMLData)
        return response


    def __call__(self):
        if "Authorization" in self.request.headers:
            self.getAuthDict()
            self.user = self.authHeader["Digest username"]
            return self.processView()
        else:
            headers = [('WWW-Authenticate',
                        'Digest realm="' + self.realm + '",qop="auth,auth-int",nonce="' + self.nonce + '",opaque="' + self.opaque + '"')]
            reponse = Response(status=401, headerlist=headers)
            return reponse

    def processView(self):
        #At this point children of odkView have:
        # self.user which us the user requesting ODK data
        # authorize(self,correctPassword) which checks if the password in the authorization is correct
        # askForCredentials(self) which return a response to ask again for the credentials
        # createXMLResponse(self,XMLData) that can be used to return XML data to ODK with the required headers
        return {}