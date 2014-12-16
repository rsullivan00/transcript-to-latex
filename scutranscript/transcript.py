from enum import Enum
from django import forms
import sys

class Format(Enum):
    pdf = 0
    doc = 1

class TranscriptForm(forms.Form):
    paste_content = forms.CharField(widget=forms.Textarea, max_length=15000)

