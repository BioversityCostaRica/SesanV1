from fanstatic import Library
from fanstatic import Resource
from fanstatic import Group

library = Library('ss_sesan', 'resources')

# requiered files for login

basicCSSArray = []
basicCSSArray.append(Resource(library, 'inspinia/css/bootstrap.css'))
basicCSSArray.append(Resource(library, 'inspinia/font-awesome/css/font-awesome.css'))
basicCSSArray.append(Resource(library, 'inspinia/css/animate.css'))
basicCSSArray.append(Resource(library, 'inspinia/css/style.css'))
basicCSSArray.append(Resource(library, 'inspinia/css/print.css'))
basicCSS = Group(basicCSSArray)
# Main JQuery library. Required by the rest
JQuery = Resource(library, 'inspinia/js/jquery-3.1.1.min.js', bottom=True)

# CommonJS is the set of common required JavaScript for the site
commonJSArray = []
commonJSArray.append(Resource(library, 'inspinia/js/bootstrap.min.js', depends=[JQuery], bottom=True))
commonJS = Group(commonJSArray)

# requiered files for dashboard
DashJSArray = []

DashJSArray.append(Resource(library, 'inspinia/js/inspinia.js', depends=[JQuery], bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/pace/pace.min.js', depends=[JQuery], bottom=True))
DashJSArray.append(
    Resource(library, 'inspinia/js/plugins/metisMenu/jquery.metisMenu.js', depends=[JQuery], bottom=True))
DashJSArray.append(
    Resource(library, 'inspinia/js/plugins/slimscroll/jquery.slimscroll.min.js', depends=[JQuery], bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/flot/jquery.flot.js', depends=[JQuery], bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/flot/jquery.flot.spline.js', depends=[JQuery], bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/chosen/chosen.jquery.js', depends=[JQuery], bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/footable/footable.all.min.js', depends=[JQuery], bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/peity/jquery.peity.min.js', depends=[JQuery], bottom=True))
#DashJSArray.append(Resource(library, 'inspinia/js/plugins/dropzone/dropzone.js', depends=[JQuery], bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/jasny/jasny-bootstrap.min.js', depends=[JQuery], bottom=True))



# DashJSArray.append(Resource(library, 'inspinia/js/plugins/datapicker/bootstrap-datepicker.es.min.js',depends=[JQuery],bottom=True))
DashJSArray.append(
    Resource(library, 'inspinia/js/plugins/datapicker/bootstrap-datepicker.js', depends=[JQuery], bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/chartJs/Chart.min.js', depends=[JQuery], bottom=True))

DashJSArray.append(Resource(library, 'dashboard/dist/jspdf.debug.js', depends=[JQuery], bottom=True))
DashJSArray.append(Resource(library, 'inspinia/js/plugins/steps/jquery.steps.min.js', depends=[JQuery], bottom=True))
DashJSArray.append(
    Resource(library, 'inspinia/js/plugins/validate/jquery.validate.min.js', depends=[JQuery], bottom=True))
DashJSArray.append(
    Resource(library, 'inspinia/js/plugins/bootstrap-tagsinput/bootstrap-tagsinput.js', depends=[JQuery], bottom=True))
# DashJSArray.append(Resource(library, 'inspinia/js/plugins/jquery-ui/jquery-ui.min.js', depends=[JQuery], bottom=True))
# DashJSArray.append(Resource(library, 'dashboard/range_slider/jquery-ui-range-slider.js', depends=[JQuery], bottom=True))


DashJSArray.append(Resource(library, 'dashboard/dashboard.js', depends=[JQuery], bottom=True))

DashJS = Group(DashJSArray)

DashCSSArray = []

DashCSSArray.append(Resource(library, 'inspinia/css/plugins/toastr/toastr.min.css', depends=[JQuery], bottom=True))
DashCSSArray.append(
    Resource(library, 'inspinia/css/plugins/chosen/bootstrap-chosen.css', depends=[JQuery], bottom=True))
DashCSSArray.append(Resource(library, 'inspinia/css/plugins/footable/footable.core.css', depends=[JQuery], bottom=True))
DashCSSArray.append(Resource(library, 'inspinia/css/plugins/datapicker/datepicker3.css', depends=[JQuery], bottom=True))
DashCSSArray.append(Resource(library, 'inspinia/css/plugins/steps/jquery.steps.css', depends=[JQuery], bottom=True))
DashCSSArray.append(
    Resource(library, 'inspinia/css/plugins/bootstrap-tagsinput/bootstrap-tagsinput.css', depends=[JQuery],
             bottom=True))
#DashCSSArray.append(Resource(library, 'inspinia/css/plugins/dropzone/basic.css', depends=[JQuery], bottom=True))
#DashCSSArray.append(Resource(library, 'inspinia/css/plugins/dropzone/dropzone.css', depends=[JQuery], bottom=True))
DashCSSArray.append(Resource(library, 'inspinia/css/plugins/jasny/jasny-bootstrap.min.css', depends=[JQuery], bottom=True))



# DashCSSArray.append(Resource(library, 'inspinia/js/plugins/jquery-ui/jquery-ui.min.css', depends=[JQuery], bottom=True))
# DashCSSArray.append(Resource(library, 'dashboard/range_slider/jquery-ui-range-slider.css', depends=[JQuery], bottom=True))


DashCSS = Group(DashCSSArray)

regJS_CSS = Group([Resource(library, 'inspinia/js/plugins/sweetalert/sweetalert.min.js', depends=[JQuery], bottom=True),
                   Resource(library, 'inspinia/css/plugins/sweetalert/sweetalert.css', depends=[JQuery], bottom=True),
                   Resource(library, 'dashboard/register.js', depends=[JQuery], bottom=True)])

reportJS = Group(
    [Resource(library, 'inspinia/js/plugins/typehead/bootstrap3-typeahead.min.js', depends=[JQuery], bottom=True),
     Resource(library, 'dashboard/pptxGenJS/jszip.min.js', depends=[JQuery], bottom=True),
     Resource(library, 'dashboard/pptxGenJS/pptxgen.js', depends=[JQuery], bottom=True),
     # Resource(library, 'inspinia/js/plugins/topojson/topojson.js', depends=[JQuery], bottom=True),

     # Resource(library, 'inspinia/js/plugins/datamaps/datamaps.all.min.js', depends=[JQuery], bottom=True),
     Resource(library, 'dashboard/report.js', depends=[JQuery], bottom=True)])

baselineR = Group([Resource(library, 'dashboard/baseline.js', depends=[JQuery], bottom=True)])

pilarArray = []
pilarArray.append(Resource(library, 'inspinia/js/plugins/jquery-ui/jquery-ui.min.js', depends=[JQuery], bottom=True))
pilarArray.append(Resource(library, 'inspinia/js/plugins/jquery-ui/jquery-ui.min.css', depends=[JQuery], bottom=True))

pilarArray.append(Resource(library, 'dashboard/uiSlider/nouislider.css', depends=[JQuery], bottom=True))
pilarArray.append(Resource(library, 'dashboard/uiSlider/nouislider.js', depends=[JQuery], bottom=True))

pilarArray.append(Resource(library, 'dashboard/pilar_helps.js', depends=[JQuery], bottom=True))

pilarCSS_JS = Group(pilarArray)

# <link href="css/plugins/switchery/switchery.css" rel="stylesheet">
# <script src="js/plugins/switchery/switchery.js"></script>
formsCSS_JS = Group([Resource(library, 'inspinia/js/plugins/dualListbox/jquery.bootstrap-duallistbox.js',
                              depends=[JQuery], bottom=True),
                     Resource(library, 'dashboard/forms.js',
                              depends=[JQuery], bottom=True),
                     Resource(library, 'inspinia/css/plugins/dualListbox/bootstrap-duallistbox.min.css',
                              depends=[JQuery], bottom=True),
                     Resource(library, 'bootstrap-toggle-master/js/bootstrap-toggle.js',
                              depends=[JQuery], bottom=True),
                     Resource(library, 'bootstrap-toggle-master/css/bootstrap-toggle.css',
                              depends=[JQuery], bottom=True)
                     ])

gtoolCSS_JS = Group([Resource(library, 'dashboard/gtool.js', depends=[JQuery], bottom=True), ])

seasonCSS_JS = Group([Resource(library, 'dashboard/season.js', depends=[JQuery], bottom=True), ])




rangCSS_JS = Group(
    [Resource(library, 'dashboard/ranges_helps.js', depends=[JQuery], bottom=True), pilarArray[0], pilarArray[1],
     pilarArray[2], pilarArray[3]])


# requiered files for profile
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
