import os 

from django.shortcuts import render
from django.http import HttpResponse

from .transcript import TranscriptForm
from .parsing import parse_body
from .buildDocument import *
from .helpers import debug_print

import sys

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
            parsed = parse_body(content)
            # Build document
            doc = build_document(parsed)
            return pdf_view(request, doc)

    else:
        return HttpResponse('Failure')

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

        response['Content-Disposition'] = 'inline;filename=%s.pdf' %doc.filename 

        os.remove(filePath)
        return response
    pdf.closed
