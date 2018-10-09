from ..models import DBSession, Log
from datetime import datetime as dt
import transaction
from get_vals import getFullName
#id = Column(Integer, primary_key=True)
#log_date = Column(DateTime)
#user = Column(String(45))
#action = Column(String(45))
#comment = Column(String(45))
#status = Column(String(45))





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

def getLoglist(uname):
    mySession = DBSession()

    result= mySession.query(Log).all()
    data=[]
    for row in result:
        try:
            data.append([row.log_date, getFullName(row.user), row.action, row.status])
        except:
            pass

    return data