import sys
import re
import string

from .helpers import debug_print
from .transcript import *

def lex_by_lines(s):
    # Remove repeated newlines
    s = re.sub('\n+', '\n', s)
    # Split into tokens of lines
    lines = s.split('\n')

    # Build regex to detect an all-whitespace string
    whitespace_regex = '^( '
    # Get all whitespace characters
    for char in string.whitespace:
        whitespace_regex += '|' + char
    whitespace_regex += ')+$'

    lexed = []
    # Filter out empty lines from array of strings
    for line in lines:
        # Filter out empty lines
        if len(line) > 0 and not re.match(whitespace_regex, line):
            cleaned = line.strip()
            # Remove repeated spaces
            cleaned = re.sub(' +', ' ', cleaned)
            lexed.append(cleaned)

    return lexed
 
def parse_body(text):
    lexed = lex_by_lines(text)
#    for line in lexed:
#        debug_print(line)

    sectioned = []
    # Divide into sections by section headers
    header_prefix = '- - - - -'
    for line in lexed:
        if line[:len(header_prefix)] == header_prefix:
            # Start the new section
            sec = TranscriptSection(line)
            sectioned.append(sec)
            debug_print(line)
        else:
            # Or add to current section
            if len(sectioned) == 0:
                header = TranscriptSection('header')
                sectioned.append(header)
            else:
                #import pdb; pdb.set_trace()
                sectioned[-1].content.append(line)

#    for section in sectioned:
#        for line in section.content:
#            debug_print(line)

    return sectioned


def test():
    inFile = open('samples/rick.txt', 'r')
    print(parseBody(inFile.read()))

#test()
