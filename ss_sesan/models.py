# coding: utf-8
from sqlalchemy import Column, DECIMAL, DateTime, Float, String, text
from sqlalchemy.dialects.mysql import INTEGER
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

    id_cu = Column(INTEGER(11), primary_key=True)
    munic_id = Column(INTEGER(11))
    categoria = Column(String(45))
    cu_name = Column(String(45))
    pob_tot = Column(INTEGER(11))
    hombres = Column(INTEGER(11))
    mujeres = Column(INTEGER(11))
    X = Column(String(45))
    Y = Column(String(45))


class CoefPond(Base):
    __tablename__ = 'coef_pond'

    idcoef_pond = Column(INTEGER(11), primary_key=True)
    id_variables_ind = Column(INTEGER(11))
    munic_id = Column(INTEGER(11))
    coef_valor = Column(Float(asdecimal=True))


class Departamento(Base):
    __tablename__ = 'departamentos'

    cod_depto = Column(INTEGER(11), primary_key=True)
    name_depto = Column(String(45))


class Form(Base):
    __tablename__ = 'forms'

    form_id = Column(INTEGER(11), primary_key=True)
    form_user = Column(String(45))
    form_name = Column(String(100))
    pilar_id = Column(String(45))
    form_db = Column(String(100))


class FormsByUser(Base):
    __tablename__ = 'forms_by_user'

    idforms = Column(INTEGER(11))
    id_user = Column(String(45))
    id = Column(INTEGER(11), primary_key=True)


class Grupo(Base):
    __tablename__ = 'grupos'

    id_grupos = Column(INTEGER(11), primary_key=True)
    name_grupos = Column(String(45))
    val_grupos = Column(INTEGER(11))


class Indicadore(Base):
    __tablename__ = 'indicadores'

    id_indicadores = Column(INTEGER(11), primary_key=True)
    Id_pilares = Column(INTEGER(11))
    name_indicadores = Column(String(150))


class Institucione(Base):
    __tablename__ = 'instituciones'

    insti_id = Column(INTEGER(11), primary_key=True)
    insti_nombre = Column(String(45))


class LineasBase(Base):
    __tablename__ = 'lineas_base'

    uid = Column(INTEGER(11), primary_key=True)
    id_variables_ind = Column(INTEGER(11))
    munic_id = Column(INTEGER(11))
    lb_valor = Column(Float(asdecimal=True))


class Log(Base):
    __tablename__ = 'log'

    id = Column(INTEGER(11), primary_key=True)
    log_date = Column(DateTime)
    user = Column(String(45))
    action = Column(String(450))
    comment = Column(String(45))
    status = Column(String(45))


class MailList(Base):
    __tablename__ = 'mail_list'

    idmail_list = Column(INTEGER(11), primary_key=True)
    munic_id = Column(INTEGER(11))
    mail = Column(String(45))
    mail_name = Column(String(45))


class Munic(Base):
    __tablename__ = 'munic'

    munic_id = Column(INTEGER(11), primary_key=True)
    munic_nombre = Column(String(45))
    cod_depto = Column(INTEGER(11))


class Pilare(Base):
    __tablename__ = 'pilares'

    id_pilares = Column(INTEGER(11), primary_key=True)
    name_pilares = Column(String(45))
    coef_pond = Column(INTEGER(11))
    user_name = Column(String(45))
    pilar_desc = Column(String(500))


class RangosGrupo(Base):
    __tablename__ = 'rangos_grupos'

    idrangos_grupos = Column(INTEGER(11), primary_key=True)
    id_variables_ind = Column(INTEGER(11))
    id_grupos = Column(INTEGER(11))
    r_min = Column(DECIMAL(10, 3))
    r_max = Column(DECIMAL(10, 3))
    munic_code = Column(INTEGER(11))


class RangosPilare(Base):
    __tablename__ = 'rangos_pilares'

    uuid = Column(INTEGER(11), primary_key=True)
    id_pilares = Column(INTEGER(11))
    id_grupo = Column(INTEGER(11))
    nivel_afec = Column(DECIMAL(10, 3))


class Role(Base):
    __tablename__ = 'roles'

    role_id = Column(INTEGER(11), primary_key=True)
    role_name = Column(String(45))


class Sesonality(Base):
    __tablename__ = 'sesonality'

    idsesonality = Column(INTEGER(11), primary_key=True)
    id_munic = Column(INTEGER(11))
    id_var_with_rule = Column(INTEGER(11))
    id_var_new_cf = Column(INTEGER(11))
    rule_month = Column(INTEGER(11))
    rule_cf = Column(Float(asdecimal=True))


class User(Base):
    __tablename__ = 'user'

    user_name = Column(String(40), primary_key=True)
    user_fullname = Column(String(120))
    user_joindate = Column(DateTime)
    user_password = Column(String(80))
    user_parent = Column(String(50))
    user_email = Column(String(120))
    user_munic = Column(INTEGER(11))
    user_active = Column(INTEGER(11), server_default=text("'1'"))
    user_role = Column(INTEGER(11))
    user_dept = Column(String(120))


class VariablesInd(Base):
    __tablename__ = 'variables_ind'

    id_variables_ind = Column(INTEGER(11), primary_key=True)
    id_indicadores = Column(INTEGER(11))
    name_variable_ind = Column(String(200))
    unidad_variable_ind = Column(String(200))
    lbase_variable_ind = Column(String(45))
    code_variable_ind = Column(String(45))
    coef_pond = Column(INTEGER(11))
    v_pregunta = Column(String(210))
    var_max = Column(INTEGER(11))
    var_min = Column(String(45))
