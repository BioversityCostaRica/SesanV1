from fanstatic import Library
from fanstatic import Resource
from fanstatic import Group


library = Library('ss_sesan', 'resources')

#requiered files for login

basicCSSArray = []
basicCSSArray.append(Resource(library, 'inspinia/css/bootstrap.css'))
basicCSSArray.append(Resource(library, 'inspinia/font-awesome/css/font-awesome.css'))
basicCSSArray.append(Resource(library, 'inspinia/css/animate.css'))
basicCSSArray.append(Resource(library, 'inspinia/css/style.css'))
basicCSS = Group(basicCSSArray)
#Main JQuery library. Required by the rest
JQuery = Resource(library, 'inspinia/js/jquery-3.1.1.min.js',bottom=True)

#CommonJS is the set of common required JavaScript for the site
commonJSArray = []
commonJSArray.append(Resource(library, 'inspinia/js/bootstrap.min.js',depends=[JQuery],bottom=True))
commonJS = Group(commonJSArray)

#requiered files for dashboard
DashJSArray = []

DashJSArray.append(Resource(library, 'inspinia/js/inspinia.js',depends=[JQuery],bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/pace/pace.min.js',depends=[JQuery],bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/metisMenu/jquery.metisMenu.js',depends=[JQuery],bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/slimscroll/jquery.slimscroll.min.js',depends=[JQuery],bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/flot/jquery.flot.js',depends=[JQuery],bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/flot/jquery.flot.spline.js',depends=[JQuery],bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/chosen/chosen.jquery.js',depends=[JQuery],bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/footable/footable.all.min.js',depends=[JQuery],bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/peity/jquery.peity.min.js',depends=[JQuery],bottom=True))
#DashJSArray.append(Resource(library, 'inspinia/js/plugins/datapicker/bootstrap-datepicker.es.min.js',depends=[JQuery],bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/datapicker/bootstrap-datepicker.js',depends=[JQuery],bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/chartJs/Chart.min.js',depends=[JQuery],bottom=True))

DashJSArray.append(Resource(library, 'dashboard/dashboard.js',depends=[JQuery],bottom=True))



DashJS = Group(DashJSArray)


DashCSSArray = []

DashCSSArray.append(Resource(library, 'inspinia/css/plugins/toastr/toastr.min.css',depends=[JQuery],bottom=True))
DashCSSArray.append(Resource(library, 'inspinia/css/plugins/chosen/bootstrap-chosen.css',depends=[JQuery],bottom=True))
DashCSSArray.append(Resource(library, 'inspinia/css/plugins/footable/footable.core.css',depends=[JQuery],bottom=True))
DashCSSArray.append(Resource(library, 'inspinia/css/plugins/datapicker/datepicker3.css',depends=[JQuery],bottom=True))
DashCSS = Group(DashCSSArray)

#requiered files for profile
# ProfJSArray = []
# ProfJSArray.append(Resource(library, 'inspinia/js/inspinia.js',depends=[JQuery],bottom=True))
# ProfJS = Group(ProfJSArray)
#
# ProfCSSArray = []
# ProfCSSArray.append(Resource(library, 'inspinia/css/plugins/toastr/toastr.min.css',depends=[JQuery],bottom=True))
# ProfCSS = Group(ProfCSSArray)

def pserve():
    """A script aware of static resource"""
    import pyramid.scripts.pserve
    import pyramid_fanstatic
    import os

    dirname = os.path.dirname(__file__)
    dirname = os.path.join(dirname, 'resources')
    pyramid.scripts.pserve.add_file_callback(
                pyramid_fanstatic.file_callback(dirname))
    pyramid.scripts.pserve.main()
