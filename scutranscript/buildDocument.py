#from PyLaTeX import *
from pylatex import Document, Section, Subsection, Table, Math, TikZ, Axis, \
            Plot
from pylatex.numpy import Matrix
from pylatex.utils import * 

from .helpers import debug_print

skip_sections = [
    'Saved',
    'Return',
    'Report Results'
]

def build_document(transcript_sections):
    """
    for skip in skip_sections:
        try:
            content.remove(skip)
        except ValueError:
            debug_print(skip + ' section to skip not found')
    """

    # Open temporary file
    doc = Document(documentclass='scrartcl')

    # Iterate through each transcript seuction
    for t_section in transcript_sections:
        # Create new section
        s = Section(escape_latex(t_section.title))
        # Add content to section
        for s_line in t_section.content:
            s.append(escape_latex(s_line))

        # Add subsections to section
        for t_subsection in t_section.subsections:
            ss = Subsection(escape_latex(t_subsection.title))
            for ss_line in t_subsection:
                ss.append(escape_latex(ss_line))

            s.append(ss)

        doc.append(s)
    doc.generate_pdf()
    return doc

def test():
    buildDocument(None)

#test()
