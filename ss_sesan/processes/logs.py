from ..models import DBSession, Log
from datetime import datetime as dt
import transaction

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
