#Authorization framework
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .views import formList_view,manifest_view,mediaFile_view, XMLForm_view, push_view, submission_view,munic_kml
from pyramid.config import Configurator
from sqlalchemy import create_engine
from .models import (
    DBSession,
    Base
    )


from pyramid.session import SignedCookieSessionFactory
my_session_factory = SignedCookieSessionFactory('b@HdX5Y6nF')

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


    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('register', '/register')
    config.add_route('dashboard', '/dashboard')
    config.add_route('logout', '/logout')
    config.add_route('profile', '/profile')
    config.add_route('report', '/report/{date}')
    config.add_route('baseline', '/baseline')
    # odk routes
    config.add_route('odkformlist', '{organization}/{user}/formList')
    config.add_route('odksubmission', '/{organization}/{user}/submission')
    config.add_route('odkpush', '/{organization}/{user}/push')
    config.add_route('odkxmlform', '/{organization}/{user}/xmlform')
    config.add_route('odkmanifest', '/{organization}/{user}/manifest')
    config.add_route('odkmediafile', '/{organization}/{user}/{fileid}')

    config.add_view(formList_view, route_name="odkformlist", renderer=None)
    config.add_view(manifest_view, route_name="odkmanifest", renderer=None)
    config.add_view(mediaFile_view, route_name="odkmediafile", renderer=None)
    config.add_view(XMLForm_view, route_name="odkxmlform", renderer=None)

    config.add_view(push_view, route_name="odkpush", renderer=None)
    config.add_view(submission_view, route_name="odksubmission", renderer=None)

    config.add_route('kml', '/kml/{name}.kml')
    config.add_view(munic_kml, route_name="kml", renderer=None)

    config.scan()

    return config.make_wsgi_app()


"""
#if models.py is changed, then, add this code 
#run sqlacodegen mysql://root:inspinia4@localhost/sesan_v1 --outfile models.py



from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))



"""