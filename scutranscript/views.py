from django.shortcuts import render
from django.http import HttpResponse

from transcript import TranscriptForm
from parsing import parseBody

import sys

# Create your views here.
def index(request):
   return render(request, 'index.html')

def transcript(request):
    if request.method == 'POST':
        form = TranscriptForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['paste_content']
            return HttpResponse(parseBody(content))

    else:
        return HttpResponse(content)
