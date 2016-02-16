from pylatex import Document
from pylatex import Section
from pylatex import Subsection
from pylatex import Command
from pylatex import Package
from pylatex import Table

from pylatex.utils import escape_latex


def build_document(transcript):
    """
    Processes a Transcript object to build a LaTeX document.
    """
    # Open temporary file
    doc = Document(documentclass='scrartcl', title=transcript.title,
                   subtitle=transcript.school,
                   author=transcript.student,
                   date=transcript.date.strftime('%d %B %Y'), temporary=True)

    doc.packages.append(Package('geometry', option='margin=1.0in'))
    doc.preamble.append(Command('renewcommand', argument=['\\familydefault', '\\sfdefault']))

    doc.append(Command('maketitle'))

    # Iterate through each transcript section
    for t_section in transcript.sections:
        # Create new section
        s = Section(escape_latex(t_section.title))
        # Add content to section
        for s_line in t_section.content:
            s_line = '\t'.join(s_line)
            s.append(escape_latex(s_line) + ' \\\n')

        # Add subsections to section
        for t_subsection in t_section.subsections:
            ss = Subsection(escape_latex(t_subsection.title))
            num_cols = max(len(l) for l in t_subsection.content)
            ss_table = Table(' l ' * num_cols)
            # Add content to subsection
            for ss_line in t_subsection.content:

                ss_line = '\t'.join(ss_line)
                if ss_line.startswith('Course Topic'):
                    ss_table.append('&')
                    ss_table.add_multicolumn(num_cols-1, 'l',
                                             escape_latex(ss_line))
                    ss_table.append(r'\\')
                elif not ss_line[:3].isupper() and not ss_line.startswith('Test'):
                    ss_table.add_multicolumn(num_cols, 'l', escape_latex(ss_line))
                    ss_table.append(r'\\')
                else:
                    if ss_line.startswith('TERM'):
                        ss_table.add_hline()
                    filled = escape_latex(ss_line).split('\t')
                    filled += (num_cols - len(filled)) * ['']
                    ss_table.add_row(filled)

            ss.append(ss_table)
            s.append(ss)

        doc.append(s)
    doc.generate_pdf(clean=True)

    return doc
