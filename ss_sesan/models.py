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


class Form(Base):
    __tablename__ = 'forms'

    user_name = Column(String(40), primary_key=True)
    user_datacol = Column(String(45))


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


class Munic(Base):
    __tablename__ = 'munic'

    munic_id = Column(Integer, primary_key=True)
    munic_nombre = Column(String(45))


class Pilare(Base):
    __tablename__ = 'pilares'

    id_pilares = Column(Integer, primary_key=True)
    name_pilares = Column(String(45))
    coef_pond = Column(Integer)


class RangosGrupo(Base):
    __tablename__ = 'rangos_grupos'

    idrangos_grupos = Column(Integer, primary_key=True)
    id_variables_ind = Column(Integer)
    id_grupos = Column(Integer)
    r_min = Column(Numeric(10, 3))
    r_max = Column(Numeric(10, 3))


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
    user_organization = Column(Integer)
    user_email = Column(String(120))
    user_munic = Column(Integer)
    user_active = Column(Integer, server_default=text("'1'"))
    user_role = Column(Integer)


class VariablesInd(Base):
    __tablename__ = 'variables_ind'

    id_variables_ind = Column(Integer, primary_key=True)
    id_indicadores = Column(Integer)
    insti_id = Column(Integer)
    name_variable_ind = Column(String(200))
    unidad_variable_ind = Column(String(200))
    lbase_variable_ind = Column(String(45))
    code_variable_ind = Column(String(45))
    coef_pond = Column(Integer)
