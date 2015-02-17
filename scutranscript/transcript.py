from enum import Enum
from django import forms
import sys
import datetime

from pylatex.utils import escape_latex

class Format(Enum):
    pdf = 0
    doc = 1

class TranscriptForm(forms.Form):
    paste_content = forms.CharField(widget=forms.Textarea, max_length=15000)

class Transcript:
    """ Contains all information necessary to build a transcript. 
    Used as an intermediate representation that can be referenced for generating a transcript in a variety of formats.
    """
    def __init__(self, title='Web Unofficial Transcript', school='Santa Clara University', \
            date=datetime.date.today(), sections=[], student=None, address=None):
        self.title = title
        self.school = school 
        self.date = date 
        self.sections = sections
        self.student = student
        self.address = address

    def last_section(self):
        if len(self.sections) == 0:
            return self.sections 
        else:
            return self.sections[-1].last_section()

    def __repr__(self):
        return 'Transcript(title=%s, school=%s, date=%s, sections=%s, student=%s, address=%s' % \
                (self.title, self.school, self.date, self.sections, self.student, self.address)

class TranscriptSectionBase:
   def __init__(self, title, content=None, subsections=None):
        if content is None:
            content = []
        if subsections is None:
            subsections = []

        self.title = title
        self.content = content
        self.subsections = subsections

   def __repr__(self):
       return "TranscriptSectionBase(title=%s, content=%s, subsections=%s)" % \
               (self.title, self.content, self.subsections)

   def add_content(self, new_content):
       #if is_department_code(new_content[0]):
       self.content.append(new_content)

   def last_section(self):
       if len(self.subsections) == 0:
           return self 

       return self.subsections[-1].last_section()

class TranscriptSection(TranscriptSectionBase):
    """ Basic section of a transcript """

class TranscriptSubSection(TranscriptSectionBase):
    """ Basic subsection of a transcript """
class TranscriptTable:
    def __init__(self, columns):
        self.columns = columns
        self.content = [[]]

    def add_row(self, row_content_list):
        if len(row_content_list) != self.columns:
            raise AssertionError('Number of row elements must be the same as the number of columns')
        else: 
            self.content.append(row_content_list)

class TranscriptTableRow:
    def __init__(self, content=None):
        if content is None:
            content = []
        self.content = content



   
