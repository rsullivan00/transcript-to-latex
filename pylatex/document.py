# -*- coding: utf-8 -*-
"""
    pylatex.document
    ~~~~~~~

    This module implements the class that deals with the full document.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

import subprocess
import tempfile 
from .package import Package
from .utils import dumps_list
from .base_classes import BaseLaTeXContainer


class Document(BaseLaTeXContainer):

    """A class that contains a full latex document."""

    def __init__(self, filename='default_filename', documentclass='article',
                 fontenc='T1', inputenc='utf8', author=None, title=None,
                 date=None, data=None, program='pdflatex', temporary=False):
        self.filename = filename

        self.documentclass = documentclass

        fontenc = Package('fontenc', option=fontenc)
        inputenc = Package('inputenc', option=inputenc)
        packages = [fontenc, inputenc, Package('lmodern')]
        self.preamble = []

        if title is not None:
            packages.append(Package(title, base='title'))
        if author is not None:
            packages.append(Package(author, base='author'))
        if date is not None:
            packages.append(Package(date, base='date'))

        self.program = program
        self.temporary = temporary

        super().__init__(data, packages=packages)

    def dumps(self):
        """Represents the document as a string in LaTeX syntax."""
        document = r'\begin{document}'

        document += dumps_list(self)

        document += r'\end{document}'

        super().dumps()

        head = r'\documentclass{' + self.documentclass + '}'

        head += self.dumps_packages()

        for command in self.preamble:
            head += command.dumps()

        return head + document

    def generate_tex(self):
        """Generates a .tex file."""
        newf = open(self.filename + '.tex', 'w')
        self.dump(newf)
        newf.close()

    def generate_pdf(self, clean=True):
        """Generates a pdf"""
        f = tempfile.NamedTemporaryFile(prefix='transcript_')
        self.filename = '.' + f.name
        f.close()

        self.generate_tex()
        #' --jobname="' + self.filename + 
        command = self.program + ' -output-directory=' + './tmp ' + \
            self.filename + '.tex'

        subprocess.check_call(command, shell=True)

        if clean:
            subprocess.call('rm "' + self.filename + '.aux" "' +
                            self.filename + '.log" "' +
                            self.filename + '.tex"', shell=True)
