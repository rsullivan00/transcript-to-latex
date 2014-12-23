# -*- coding: utf-8 -*-
"""
    pylatex.package
    ~~~~~~~

    This module implements the class that deals with commands.

    :license: MIT, see License for more details.
"""

from .base_classes import BaseLaTeXClass


class Command(BaseLaTeXClass):

    """A class that represents a LaTeX command."""

    def __init__(self, name, option=None, argument=None):
        self.name = name
        self.option = option
        self.argument = argument 

        super().__init__(packages=None)

    def __key(self):
        return (self.name, self.option, self.argument)

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())

    def dumps(self):
        """Represents the command as a string in LaTeX syntax."""
        if self.option is None:
            option = ''
        else:
            if isinstance(self.option, str):
                options = self.option.split(' ') 
            else:
                options = self.option

            for opt in options:
                option += '[' + opt + ']'

        if self.argument is None:
            # Should these braces always be present?
            argument = '{}'
        else:
            if isinstance(self.argument, str):
                arguments = self.argument.split(' ') 
            else:
                arguments = self.argument

            for arg in arguments:
                argument += '{' + arg + '}'

        return '\\' + self.name + option + argument + '\n'
