import sys
import re
import string

from .helpers import debug_print
from .transcript import *

skip_sections = [
    'Saved',
    'Return',
    'Report Results'
]

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
        line = line.strip()
        # Filter out empty lines
        if len(line) > 0 and not re.match(whitespace_regex, line) and line not in skip_sections:
            # Remove repeated spaces
            line = re.sub(' +', ' ', line)
            lexed.append(line)

    return lexed


"""
Populates and returns a Transcript object with raw pasted data from an eCampus unofficial web transcript.
"""
def parse_body(text):
    lexed = lex_by_lines(text)

#    for line in lexed:
#        debug_print(line)

    transcript = Transcript()
    # Divide into sections by section headers
    header_prefix = '- - - - -'
    metadata = []
    for line in lexed:
        if line[:len(header_prefix)] == header_prefix:
            # Start the new section
            sec = TranscriptSection(line)
            transcript.sections.append(sec)
            debug_print(line)
        else:
            # Or add to current section
            if len(transcript.sections) == 0:
                # First section contains metadata
                metadata.append(line)
            else:
                transcript.sections[-1].content.append(line)

    # Process metadata
    try:
        transcript.title = metadata[0]
        transcript.date = ' '.join(metadata[1].split(':')[-1].split('-'))
        transcript.school = metadata[2]
        transcript.student = metadata[3].split(':')[-1]
        transcript.address = metadata[4].split(':')[-1]
    except IndexError:
        raise Exception("Metadata missing")

    return transcript 


def test():
    inFile = open('samples/rick.txt', 'r')
    print(parseBody(inFile.read()))

#test()
