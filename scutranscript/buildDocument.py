#from PyLaTeX import *
from pylatex import Document, Section, Subsection, Table, Command
from pylatex.numpy import Matrix
from pylatex.utils import * 

from .transcript import Transcript
from .helpers import debug_print
import re

"""
Processes a Transcript object to build a LaTeX document.
"""
def build_document(transcript):
    # Open temporary file
    doc = Document(documentclass='scrartcl', title=transcript.title, author=transcript.student, date=transcript.date.strftime('%d %B %Y'))

    doc.append(Command('maketitle'))

    # Iterate through each transcript section
    for t_section in transcript.sections:
        # Create new section
        s = Section(escape_latex(t_section.title))
        # Add content to section
        for s_line in t_section.content:
            s.append(escape_latex(s_line) + ' \\\n')

        # Add subsections to section
        for t_subsection in t_section.subsections:
            ss = Subsection(escape_latex(t_subsection.title))
            num_cols = 10 
            ss_table = Table(' l ' * num_cols)
            # Add content to subsection
            for ss_line in t_subsection.content:

#                if not re.match('^[A-Z][A-Z][A-Z]', ss_line):
                if ss_line.startswith('Course Topic'):
                    ss_table.add_multicolumn(1, 'l', ' ')
                    ss_table.append('&')
                    ss_table.add_multicolumn(num_cols-1, 'l', escape_latex(ss_line))
                    ss_table.append(r'\\')
                elif not ss_line[:3].isupper() and not ss_line.startswith('Test'):
                    #ss_table.add_multicolumn(1, 'l', ' ')
                    #ss_table.append('&')
                    ss_table.add_multicolumn(num_cols, 'l', escape_latex(ss_line))
                    ss_table.append(r'\\')
                else:
                    if ss_line.startswith('TERM'):
                        ss_table.add_hline()
                    filled = escape_latex(ss_line).split('\t')
                    filled += (num_cols - len(filled)) * [' ']
                    ss_table.add_row(filled)
                    #ss.append(escape_latex(ss_line) + ' \\\n')

            ss.append(ss_table)
            s.append(ss)

        doc.append(s)
    doc.generate_pdf()
    return doc

