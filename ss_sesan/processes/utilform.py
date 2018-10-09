import os,glob,json
from lxml import etree
from ..encdecdata import decodeData
from ..models import DBSession, User, FormsByUser, Form
from pyramid.httpexceptions import HTTPNotFound
from hashlib import md5
from pyramid.response import FileResponse
import mimetypes, shutil
from get_vals import getIntName,sendGroup
from uuid import uuid4
from subprocess import check_call, CalledProcessError


def generateFormList(projectArray):
    root = etree.Element("xforms",xmlns="http://openrosa.org/xforms/xformsList")

    for project in projectArray:
        xformTag = etree.Element("xform")
        for key,value in project.iteritems():
            atag = etree.Element(key)
            atag.text = value
            xformTag.append(atag)
        root.append(xformTag)
    return etree.tostring(root, encoding='utf-8')

def generateManifest(mediaFileArray):
    root = etree.Element("manifest",xmlns="http://openrosa.org/xforms/xformsManifest")
    for file in mediaFileArray:
        #print file
        xformTag = etree.Element("mediaFile")
        for key,value in file.iteritems():
            atag = etree.Element(key)
            atag.text = value
            xformTag.append(atag)
        root.append(xformTag)
    return etree.tostring(root, encoding='utf-8')


def isUserActive(uname):
    mySession = DBSession()
    result = mySession.query(User).filter_by(user_name=uname).filter_by(user_active="1").first()
    if result:
        mySession.close()
        return True
    else:
        mySession.close()
        return False


def getUserPassword(uname,request):
    mySession = DBSession()
    result = mySession.query(User).filter(User.user_name == uname).first()
    dd=decodeData(result.user_password)
    mySession.close()
    return dd

def getParent(user):
    mySession =DBSession()

    result=mySession.query(User.user_parent).filter(User.user_name==user).first()
    mySession.close()
    return result.user_parent

def getFormList(user,request):
    prjList = []

    mySession = DBSession()
    result=mySession.query(FormsByUser.idforms).filter(FormsByUser.id_user==user).all()

    for row in result:
        forms=mySession.query(Form.form_db).filter(Form.form_id==row.idforms).first()
        fname="_".join(forms.form_db.split("_")[2:])
        path = os.path.join(request.registry.settings['user.repository'], *[getParent(user), "user", user,fname, '*.json'])
        files=glob.glob(path)[0]

        if files:
            with open(files) as data_file:
                data = json.load(data_file)
                data["downloadUrl"] = request.route_url('odkxmlform',parent=getParent(user),user=user,form=fname)
                data["manifestUrl"] = request.route_url('odkmanifest', parent=getParent(user),user=user,form=fname)

            prjList.append(data)
        else:
            raise HTTPNotFound()
    return generateFormList(prjList)


def getManifest(uname, request):

    mySession = DBSession()
    result = mySession.query(FormsByUser.idforms).filter(FormsByUser.id_user == uname).all()
    fileArray = []
    for row in result:
        forms = mySession.query(Form.form_db).filter(Form.form_id == row.idforms).first()
        fname = "_".join(forms.form_db.split("_")[2:])
        path = os.path.join(request.registry.settings['user.repository'],
                            *[getParent(uname), "user", uname, fname, '*.*'])

        files = glob.glob(path)
        if files:
            for file in files:
                fileName = os.path.basename(file)
                fileArray.append({'filename':fileName,'hash':'md5:' + md5(open(file, 'rb').read()).hexdigest(),'downloadUrl':request.route_url('odkmediafile', parent=getParent(uname), user=uname,form=fname, fileid=fileName)})
            #print fileArray
    if fileArray:
        return generateManifest(fileArray)
    else:
        return generateManifest([])


def getMediaFile(uname, request,fileid):

    #path = os.path.join(request.registry.settings['user.repository'],*[organization,uname, organization.lower()+".png"])
    fname = str(request.url).split("/")[-2:][0]
    path = os.path.join(request.registry.settings['user.repository'],
                        *[getParent(uname), "user",uname, fname,fileid])
    if os.path.isfile(path):
        content_type, content_enc = mimetypes.guess_type(path)
        fileName = os.path.basename(path)
        response = FileResponse(
            path,
            request=request,
            content_type=content_type
        )
        response.content_disposition = 'attachment; filename="' + fileName + '"'

        return response
    else:
        raise HTTPNotFound()


def getXMLForm(uname,request):

    fname=str(request.url).split("/")[-2:][0]

    path = os.path.join(request.registry.settings['user.repository'], *[getParent(uname),"user", uname,fname, '*.xml'])
    files = glob.glob(path)
    if files:
        f=files[0]
        content_type, content_enc = mimetypes.guess_type(f)
        fileName = os.path.basename(f)
        response = FileResponse(
            f,
            request=request,
            content_type=content_type
        )
        response.content_disposition = 'attachment; filename="' + fileName + '"'
        return response
    else:
        raise HTTPNotFound()


def convertXMLToJSON(uname,XMLFile,iniqueID,request):

    XMLFileName = os.path.basename(XMLFile)
    tree = etree.parse(XMLFile)
    root = tree.getroot()
    XFormID = root.get("id")
    if XFormID is not None:
        xFormIDParts = XFormID.split("_")
        #projectid = xFormIDParts[2]
        org =xFormIDParts[0].upper()
        path = None
        path = os.path.join(request.registry.settings['user.repository'],*[getParent(uname), "user",uname, "data", 'xml',iniqueID, '*.xml'])
        if path is not None:
            files = glob.glob(path)
            if files:
                XMLtoJSON = os.path.join(request.registry.settings['odktools.path'], *["XMLtoJSON", "xmltojson"])
                path = os.path.join(request.registry.settings['user.repository'], *[getParent(uname), "user", uname, "data", 'json', iniqueID])
                os.makedirs(path)
                JSONFile = os.path.join(request.registry.settings['user.repository'], *[getParent(uname), "user", uname, "data", 'json', iniqueID, XMLFileName.replace(".xml",".json")])
                FormXML = os.path.join(request.registry.settings['user.repository'], *[getParent(uname), "forms",XFormID,XFormID+".xml"])
                args = []
                args.append(XMLtoJSON)
                args.append("-i " + XMLFile)
                args.append("-o " + JSONFile)
                args.append("-x " + FormXML)
                try:
                    check_call(args)

                    # Now that we have the data in JSON format we check if any connected plugins
                    # may change the JSON data

                    with open(JSONFile) as data_file:
                        data = json.load(data_file)

                    with open(JSONFile, "w") as outfile:
                        jsonString = json.dumps(data, indent=4, ensure_ascii=False).encode("utf8")
                        outfile.write(jsonString)

                except CalledProcessError as e:
                    msg = "Error creating database files \n"
                    msg = msg + "Commang: " + " ".join(args) + "\n"
                    msg = msg + "Error: \n"
                    msg = msg + e.message
                    print msg
                    return False,""
            else:
                print "Unable to find XML Form File for ID" + XFormID
                return False,""
        else:
            print "Unable to find XML Form File path ID" + XFormID
            return False,""
    else:
        print "XFormID is empty"
        return False,""
    return True, XFormID

# ~/odktools/odktools/JSONToMySQL/./jsontomysql -u root -p inspinia4 -m CONALFA/manifest.xml -j sesan_data/CONALFA/56d9b4de-e8bd-495b-b8c8-2c7341434519.json -s DATA_CONALFA -J custom.js;
def makeJSONToMySQL(uname,iniqueID,request,xformid):

    JSONToMySQL = os.path.join(request.registry.settings['odktools.path'], *["JSONToMySQL", "jsontomysql"])

    JSONFile = os.path.join(request.registry.settings['user.repository'],*[getParent(uname), "user", uname, "data", 'json', iniqueID, "*.json"])
    JSONFile=glob.glob(JSONFile)
    mapDir = os.path.join(request.registry.settings['user.repository'],
                          *[getParent(uname), "user", uname, "data", "MAPS"])
    if JSONFile:

        args = []

        args.append(JSONToMySQL)
        args.append("-u " + request.registry.settings['mysql.user'])
        args.append("-p " + request.registry.settings['mysql.password'])
        args.append("-M " + mapDir)
        args.append("-m " + os.path.join(request.registry.settings['user.repository'], *[getParent(uname), "forms",xformid, "manifest.xml"]))
        args.append("-j " + JSONFile[0])
        args.append("-s " + "DATA_"+getParent(uname)+"_"+xformid)
        #modify custom.js

        try:
            file = open(os.path.join(request.registry.settings['user.repository'], *[getParent(uname), "forms",xformid, "custom.js"]), "r").read()
            file2 = open(os.path.join(request.registry.settings['user.repository'], *[getParent(uname), "forms",xformid, "custom2.js"]), "w")
            file2.write(file.replace("n_path", str(iniqueID)))

            file2.close()
        except:
            print ""

        if not os.path.exists(mapDir):
            os.makedirs(mapDir)

        args.append("-J " +os.path.join(request.registry.settings['user.repository'], *[getParent(uname), "forms",xformid, "custom2.js"]) )
        try:
            check_call(args)

            #print args
            #print "insert"
        except CalledProcessError as e:
            msg = "Error exporting files to database \n"
            msg = msg + "Commang: " + " ".join(args) + "\n"
            msg = msg + "Error: \n"
            msg = msg + e.message
            print msg
            return False
    else:
        print "Unable to find JSON files"
        return False

    return True

def storeSubmission(uname,request):
    try:
        fname = str(request.url).split("/")[-2:][0]

        iniqueID = uuid4()
        path = os.path.join(request.registry.settings['user.repository'],*[getParent(uname),"user",uname, "data", 'xml',str(iniqueID)])
        os.makedirs(path)
        XMLFile = ""
        for key in request.POST.keys():
            #print key
            filename = request.POST[key].filename

            input_file = request.POST[key].file
            file_path = os.path.join(path, filename)
            if file_path.upper().find('.XML') >=0:
                XMLFile = file_path
            temp_file_path = file_path + '~'

            input_file.seek(0)
            with open(temp_file_path, 'wb') as output_file:
                shutil.copyfileobj(input_file, output_file)
            # Now that we know the file has been fully saved to disk move it into place.
            os.rename(temp_file_path, file_path)
        if XMLFile != "":
            #print "convert XMLtoJson"
            flag, xformid=convertXMLToJSON(uname, XMLFile, str(iniqueID), request)

            if flag:
                makeJSONToMySQL(uname,str(iniqueID),request,xformid)
            else:
                return False
        #Send the message to process the xml
        return True
    except:
        return False
