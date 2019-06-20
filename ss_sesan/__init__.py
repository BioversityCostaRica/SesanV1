#Authorization framework
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .views import formList_view,manifest_view,mediaFile_view, XMLForm_view, push_view, submission_view,munic_kml,download_xls,download_helpfiles
from pyramid.config import Configurator
from sqlalchemy import create_engine
from .models import (
    DBSession,
    Base
    )
from pyramid_jinja2 import add_jinja2_extension
import os
from pyramid.session import SignedCookieSessionFactory
my_session_factory = SignedCookieSessionFactory('b@HdX5Y6nF')


#Jinja2 Extensions
from .processes.jinja_extensions import jinjaEnv
from .processes.jinja_extensions import setLoader

from jinja2.ext import babel_extract


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    authn_policy = AuthTktAuthenticationPolicy(
        settings['auth.secret'],
    )
    #sqlacodegen mysql://root:inspinia4@localhost/sesan_v1 --outfile models.py

    authz_policy = ACLAuthorizationPolicy()


    engine = create_engine("mysql://" + settings['mysql.user'] + ":" + settings['mysql.password'] + "@" + settings['mysql.host'] + "/" + settings['mysql.schema'], pool_size=20, max_overflow=0, pool_recycle=3600)
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine



    config = Configurator(settings=settings,authentication_policy=authn_policy,
                          authorization_policy=authz_policy)

    config.include('pyramid_jinja2')
    config.include('pyramid_fanstatic')
    config.add_jinja2_renderer('.jinja2')
    templatesPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    setLoader(templatesPath)

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('register', '/register')
    config.add_route('dashboard', '/dashboard')
    config.add_route('logout', '/logout')
    config.add_route('profile', '/profile')
    config.add_route('report', '/report/{date}')
    config.add_route('baseline', '/baseline')
    config.add_route('pilares', '/pilares')
    config.add_route('forms', '/forms')
    config.add_route('seasonality', '/seasonality')
    config.add_route('weighing', '/weighing')
    config.add_route('about', '/about')
    config.add_route('gtool', '/gtool')
    config.add_route('mails', '/mails')
    config.add_route('ranges', '/ranges')
    config.add_route('uploadfiles', '/uploadfiles')
    config.add_route('downfiles', '/downfiles/{parent}/user/{user}/attach/{date}/{file}')
    config.add_route('logs', '/logs')

    # odk routes
    config.add_route('odkformlist', '{parent}/{user}/formList')
    config.add_route('odksubmission', '/{parent}/{user}/submission')
    config.add_route('odkpush', '/{parent}/{user}/push')
    config.add_route('odkxmlform', '/{parent}/{user}/{form}/xmlform')
    config.add_route('odkmanifest', '/{parent}/{user}/{form}/manifest')
    config.add_route('odkmediafile', '/{parent}/{user}/{form}/{fileid}')

    config.add_view(formList_view, route_name="odkformlist", renderer=None)
    config.add_view(manifest_view, route_name="odkmanifest", renderer=None)
    config.add_view(mediaFile_view, route_name="odkmediafile", renderer=None)
    config.add_view(XMLForm_view, route_name="odkxmlform", renderer=None)

    config.add_view(push_view, route_name="odkpush", renderer=None)
    config.add_view(submission_view, route_name="odksubmission", renderer=None)

    config.add_route('kml', '/kml/{name}.kml')
    config.add_view(munic_kml, route_name="kml", renderer=None)

    config.add_route('down', '/down/{name}.xlsx')
    config.add_view(download_xls, route_name="down", renderer=None)

    config.add_route('helpfiles', '/about/{filename}')
    config.add_view(download_helpfiles, route_name="helpfiles", renderer=None)

    #rules for seasonality
    config.add_route('rules', '/rules')




    config.scan()

    return config.make_wsgi_app()


"""
#if models.py is changed, then, add this code 
#run sqlacodegen mysql://root:inspinia4@localhost/sesan_v2 --outfile models.py



from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))



"""