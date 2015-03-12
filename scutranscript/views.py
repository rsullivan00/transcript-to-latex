import os 

from django.shortcuts import render
from django.http import HttpResponse

from .transcript import TranscriptForm
from .parsing import parse_body
from .buildDocument import *
from .helpers import debug_print
from .settings import DEBUG

import sys
import json
import jsonpickle

"""
Landing page. Template at templates/index.html.
"""
def index(request):
   return render(request, 'index.html')

"""
Creates page displaying a transcript based on the user's form input.
Currently only supports pdfs.
"""
def transcript(request):
    if request.method == 'POST':
        debug_print('Building transcript view')

        form = TranscriptForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['paste_content']
            try:
                transcript = parse_body(content)
            except Exception as e:
                return error_view(request, e) 
 
            if 'format_json' in request.POST:
                return json_view(request, transcript)

            # Default to pdf
            try:
                doc = build_document(transcript)
            except Exception as e:
                return error_view(request, e) 

            return pdf_view(request, doc)

    else:
        return error_view(request)

""" 
Directs the user to a page containing the pdf contained in the 'doc' file.
doc should be of type Document defined in the pylatex package.
"""
def pdf_view(request, doc):
    debug_print('Building pdf view')
    filePath = doc.filename + '.pdf'
    # Must read as binary, not unicode string
    with open(filePath, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')

        response['Content-Disposition'] = 'inline;filename=%s' % filePath.replace('/tmp/', '') 

        return response
    pdf.closed
    os.remove(filePath)

""" 
Default error page when document generation fails.
"""
def error_view(request, e):
    if DEBUG:
        debug_print("Error: %s" % e)
        return render(request)
    else:
        return render(request, 'error.html', status=400)

""" 
Returns structured JSON
"""
def json_view(request, transcript):
    def date_handler(obj):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj

    return HttpResponse(jsonpickle.encode(transcript, unpicklable=False), content_type="application/json")
