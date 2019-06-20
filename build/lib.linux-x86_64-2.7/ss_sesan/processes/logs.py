from ..models import DBSession, Log, Form
from datetime import datetime as dt
import transaction
from get_vals import getFullName,getUserMunic
#id = Column(Integer, primary_key=True)
#log_date = Column(DateTime)
#user = Column(String(45))
#action = Column(String(45))
#comment = Column(String(45))
#status = Column(String(45))


from dateutil import parser
from ago import human


def log(user,action,comment,status):


    try:
        mySession = DBSession()
        newLog=Log(log_date=dt.now(),user=user,action=action,comment=comment, status=status)
        transaction.begin()
        mySession.add(newLog)
        transaction.commit()
        mySession.close()
    except:
        pass


def getForms(parent):
    mySession = DBSession()
    result=mySession.query(Form.form_name).filter(Form.form_user==parent).all()
    data=[]
    for row in result:
        data.append(row.form_name.replace(" ", "_").title())
    mySession.close()
    return data



def getLoglist(self,uname):

    mySession = DBSession()

    result= mySession.query(Log).all()
    data=[[],[]]
    for row in result:
        try:
            data[0].append([human(row.log_date), getFullName(row.user), row.action, row.status])
        except:
            pass


    imported= open(self.request.registry.settings['user.repository']+"/imported.log", "r").readlines()

    ff=getForms(uname)

    for r in imported:
        print r
        j =r.split("_")
        del j[0]
        j="_".join(j)

        for f in ff:

            if f in j:
                j=j.replace(f+"_", "").split("_")
                us=j[0]
                mun=getUserMunic(us).replace(" ","_")
                del j[0]
                j = "_".join(j)
                j=j.replace(mun+"_","").split("_")
                data[1].append([f, getFullName(us)+" / "+mun.replace("_"," "), human(parser.parse(j[0] + " " + j[1].replace("\n", "")))])



    mySession.close()

    print data[1]


    return data