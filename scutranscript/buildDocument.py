#from PyLaTeX import *
from pylatex import Document, Section, Subsection, Table, Command
from pylatex.numpy import Matrix
from pylatex.utils import * 

from .transcript import Transcript
from .helpers import debug_print

"""
Processes a Transcript object to build a LaTeX document.
"""
def build_document(transcript):
    # Open temporary file
    doc = Document(documentclass='scrartcl', title=transcript.title, author=transcript.student, date=transcript.date.strftime('%d %B %Y'))

    doc.append(Command('maketitle'))

    # Iterate through each transcript seuction
    for t_section in transcript.sections:
        # Create new section
        s = Section(escape_latex(t_section.title))
        # Add content to section
        for s_line in t_section.content:
            s.append(escape_latex(s_line))

        # Add subsections to section
        for t_subsection in t_section.subsections:
            ss = Subsection(escape_latex(t_subsection.title))
            for ss_line in t_subsection.content:
                ss.append(escape_latex(ss_line) + ' \\\n')

            s.append(ss)

        doc.append(s)
    doc.generate_pdf()
    return doc

def test():
    buildDocument(None)

#test()
