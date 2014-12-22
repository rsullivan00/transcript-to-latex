from django.shortcuts import render
from django.http import HttpResponse

from .transcript import TranscriptForm
from .parsing import parseBody
from .buildDocument import *

import sys

# Create your views here.
def index(request):
   return render(request, 'index.html')

def transcript(request):
    if request.method == 'POST':
        form = TranscriptForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['paste_content']
            parsed = parseBody(content)
            # Build document
            doc = buildDocument(parsed)
            return pdf_view(request, doc)

    else:
        return HttpResponse(content)

def pdf_view(request, doc):
    filePath = doc.filename + '.pdf'
    with open(filePath, 'r') as pdf:
#        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response = HttpResponse(pdf.read(), content_type='application/pdf')

        #response['Content-Disposition'] = 'inline;filename=' + filePath

        return response
        #return HttpResponse('blah')
    pdf.closed
