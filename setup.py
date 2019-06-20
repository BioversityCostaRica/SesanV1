import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'plaster_pastedeploy',
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_fanstatic',
    'waitress',
    'fanstatic',
    'zbar',
    'qrtools',
    'sqlalchemy',
    'PyCrypto',
    'arrow',
    'zope.sqlalchemy',
    'webhelpers',
    'pillow',
    'lxml',
    'mysql-python',
    'xlsxwriter',
    'pyxform',
    'babel',
    'ruamel.ordereddict',
    'python-pptx',
    'gunicorn',
    'gevent',
    'ago',
    'rutter',
    'urlmap',
]



#sudo apt-get install zbar-tools
#sudo apt-get install libzbar-dev
#sudo apt-get install libmysqlclient-dev
#sudo apt install qrencode
#sudo apt-get install libqt5sql5-mysql

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov',
]

setup(
    name='ss_sesan',
    version='0.0',
    description='ss_sesan',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = ss_sesan:main',
        ],
        'fanstatic.libraries':
            ['ss_sesan = ss_sesan.resources:library']
    },
)
