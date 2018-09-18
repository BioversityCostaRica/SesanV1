# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, Numeric, String, text
from sqlalchemy.ext.declarative import declarative_base



from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))



Base = declarative_base()
metadata = Base.metadata


class CentrosUrbano(Base):
    __tablename__ = 'centros_urbanos'

    id_cu = Column(Integer, primary_key=True)
    munic_id = Column(Integer)
    categoria = Column(String(45))
    cu_name = Column(String(45))
    pob_tot = Column(Integer)
    hombres = Column(Integer)
    mujeres = Column(Integer)
    X = Column(String(45))
    Y = Column(String(45))


class CoefPond(Base):
    __tablename__ = 'coef_pond'

    idcoef_pond = Column(Integer, primary_key=True)
    id_variables_ind = Column(Integer)
    munic_id = Column(Integer)
    coef_valor = Column(Numeric(10, 0))


class Departamento(Base):
    __tablename__ = 'departamentos'

    cod_depto = Column(Integer, primary_key=True)
    name_depto = Column(String(45))


class Form(Base):
    __tablename__ = 'forms'

    form_id = Column(Integer, primary_key=True)
    form_user = Column(String(45))
    form_name = Column(String(100))
    pilar_id = Column(String(45))
    form_db = Column(String(100))


class FormsByUser(Base):
    __tablename__ = 'forms_by_user'

    idforms = Column(Integer)
    id_user = Column(String(45))
    id = Column(Integer, primary_key=True)


class Grupo(Base):
    __tablename__ = 'grupos'

    id_grupos = Column(Integer, primary_key=True)
    name_grupos = Column(String(45))
    val_grupos = Column(Integer)


class Indicadore(Base):
    __tablename__ = 'indicadores'

    id_indicadores = Column(Integer, primary_key=True)
    Id_pilares = Column(Integer)
    name_indicadores = Column(String(150))


class Institucione(Base):
    __tablename__ = 'instituciones'

    insti_id = Column(Integer, primary_key=True)
    insti_nombre = Column(String(45))


class LineasBase(Base):
    __tablename__ = 'lineas_base'

    uid = Column(Integer, primary_key=True)
    id_variables_ind = Column(Integer)
    munic_id = Column(Integer)
    lb_valor = Column(Integer)


class Log(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True)
    log_date = Column(DateTime)
    user = Column(String(45))
    action = Column(String(450))
    comment = Column(String(45))
    status = Column(String(45))


class MailList(Base):
    __tablename__ = 'mail_list'

    idmail_list = Column(Integer, primary_key=True)
    munic_id = Column(Integer)
    mail = Column(String(45))
    mail_name = Column(String(45))


class Munic(Base):
    __tablename__ = 'munic'

    munic_id = Column(Integer, primary_key=True)
    munic_nombre = Column(String(45))
    cod_depto = Column(Integer)


class Pilare(Base):
    __tablename__ = 'pilares'

    id_pilares = Column(Integer, primary_key=True)
    name_pilares = Column(String(45))
    coef_pond = Column(Integer)
    user_name = Column(String(45))
    pilar_desc = Column(String(250))


class RangosGrupo(Base):
    __tablename__ = 'rangos_grupos'

    idrangos_grupos = Column(Integer, primary_key=True)
    id_variables_ind = Column(Integer)
    id_grupos = Column(Integer)
    r_min = Column(Numeric(10, 3))
    r_max = Column(Numeric(10, 3))
    munic_code = Column(Integer)


class RangosPilare(Base):
    __tablename__ = 'rangos_pilares'

    uuid = Column(Integer, primary_key=True)
    id_pilares = Column(Integer)
    id_grupo = Column(Integer)
    nivel_afec = Column(Numeric(10, 3))


class Role(Base):
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(45))


class User(Base):
    __tablename__ = 'user'

    user_name = Column(String(40), primary_key=True)
    user_fullname = Column(String(120))
    user_joindate = Column(DateTime)
    user_password = Column(String(80))
    user_parent = Column(String(50))
    user_email = Column(String(120))
    user_munic = Column(Integer)
    user_active = Column(Integer, server_default=text("'1'"))
    user_role = Column(Integer)
    user_dept = Column(String(120))


class VariablesInd(Base):
    __tablename__ = 'variables_ind'

    id_variables_ind = Column(Integer, primary_key=True)
    id_indicadores = Column(Integer)
    name_variable_ind = Column(String(200))
    unidad_variable_ind = Column(String(200))
    lbase_variable_ind = Column(String(45))
    code_variable_ind = Column(String(45))
    coef_pond = Column(Integer)
    v_pregunta = Column(String(210))
    var_max = Column(Integer)
    var_min = Column(String(45))
