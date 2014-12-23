from enum import Enum
from django import forms
import sys
import datetime

class Format(Enum):
    pdf = 0
    doc = 1

class TranscriptForm(forms.Form):
    paste_content = forms.CharField(widget=forms.Textarea, max_length=15000)

class Transcript:
    """ Contains all information necessary to build a transcript. 
    Used as an intermediate representation that can be referenced for generating a transcript in a variety of formats.
    """
    def __init__(self, title='Web Unofficial Transcript', school='Santa Clara University', date=str(datetime.date), sections=['No content provided']):
        self.title = title
        self.school = school 
        self.date = date 
        self.sections = sections

class TranscriptSectionBase:
   def __init__(self, title, content=None, subsections=None):
        if content is None:
            content = []
        if subsections is None:
            subsections = []

        self.title = title
        self.content = content
        self.subsections = subsections

   def __str__(self):
       return "TranscriptSectionBase: " + self.title    
   
   def __repr__(self):
       return self.__str__()

class TranscriptSection(TranscriptSectionBase):
    """ Basic section of a transcript """

