from pyramid.paster import get_app, setup_logging
#ini_path = '/home/allan/sesan_ss/ss_sesan/development.ini'
ini_path = '/home/itadmin/ssm_sys/ss_sesan/development.ini'
setup_logging(ini_path)
application = get_app(ini_path, 'main')