from ..models import DBSession, Log

#id = Column(Integer, primary_key=True)
#log_date = Column(DateTime)
#user = Column(String(45))
#action = Column(String(45))
#comment = Column(String(45))
#status = Column(String(45))



def log():
    mySession = DBSession()

    #try:
    #    newLog=Log(log_date)
