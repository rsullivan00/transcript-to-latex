#from PyLaTeX import *
from pylatex import Document, Section, Subsection, Table, Math, TikZ, Axis, \
            Plot
from pylatex.numpy import Matrix
from pylatex.utils import italic

def buildDocument(content):
    # Open temporary file
    doc = Document(documentclass='scrartcl')
    section = Section('Yaay the first section, it can even be ' + italic('italic'))

    section.append('Some regular text')

    math = Subsection('Math that is incorrect', data=[Math(data=['2*3', '=', 9])])

    section.append(math)
    table = Table('rc|cl')
    table.add_hline()
    table.add_row((1, 2, 3, 4))
    table.add_hline(1, 2)
    table.add_empty_row()
    table.add_row((4, 5, 6, 7))

    table = Subsection('Table of something', data=[table])

    section.append(table)

    doc.append(section)

    doc.generate_pdf()
    return doc

def test():
    buildDocument(None)

#test()
