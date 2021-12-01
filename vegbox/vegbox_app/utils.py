from io import BytesIO #A stream implementation using an in-memory bytes buffer
                       # It inherits BufferIOBase
from django.http import HttpResponse
from django.template.loader import get_template
import os
from django.conf import settings
from django.contrib.staticfiles import finders
#pisa is a html2pdf converter using the ReportLab Toolkit,
#the HTML5lib and pyPdf.
from xhtml2pdf import pisa
#difine render_to_pdf() function

html4pdf = "<html><body><p>INVOICE</p></body></html>"
def render_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
     html4pdf = html
     #This part will create the pdf.
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None



def link_callback(uri, rel):
    """ Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):   result = [result]
        result = list(os.path.realpath(path) for path in result)
        path=result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):    path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):  path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:   return uri

            # make sure that file exists
    if not os.path.isfile(path):    raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
    return path

source_html = "<html><body><p>INVOICE</p></body></html>"
output_filename = "test.pdf"

# Utility function
def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")
    source_html = html4pdf
    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file, link_callback=link_callback
            )           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return False on success and True on errors
    return pisa_status.err

# # Main program
# if __name__ == "__main__":
#     pisa.showLogging()
#     convert_html_to_pdf(source_html, output_filename)