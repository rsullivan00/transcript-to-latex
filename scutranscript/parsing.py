import sys
import re
import string
import datetime

from .helpers import debug_print
from .transcript import Transcript, TranscriptSection, TranscriptSubSection

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
            line = re.sub('  +', '\t', line)
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
    subsection_prefixes = [
        'Program :',
        'Test Credits Applied',
        'Fall',
        'Winter',
        'Spring',
        'Summer',
        'Undergraduate Career',
        'Graduate Career'
    ]
    metadata = []
    for line in lexed:
        if line[:len(header_prefix)] == header_prefix:
            # Start the new section
            title = line.split(header_prefix)[1].strip()
            sec = TranscriptSection(title)
            transcript.sections.append(sec)
            debug_print('New section: ' + title)
        elif any(line.startswith(pre) for pre in subsection_prefixes):
#            import pdb; pdb.set_trace()
            subsec = TranscriptSubSection(line)
            transcript.sections[-1].subsections.append(subsec)
        else:
            # Or add to current section/subsection
            if len(transcript.sections) == 0:
                # First section contains metadata
                metadata.append(line)
            elif len(transcript.sections[-1].subsections):
                # Last added subsection
#                if line[:4].isupper():
                    # Line has a class code, put it in a table
                transcript.sections[-1].subsections[-1].add_content(line)
            else:
                # Last added section
                transcript.sections[-1].add_content(line)

    # Process metadata
    try:
        transcript.title = metadata[0].strip()
        datestring = metadata[1].split(':')[-1].strip()
        transcript.date = datetime.datetime.strptime(datestring, '%Y-%m-%d')
        transcript.school = metadata[2].strip()
        transcript.student = metadata[3].split(':')[-1].strip()
        transcript.address = metadata[4].split(':')[-1].strip()
    except IndexError:
        raise Exception("Metadata missing")

    return transcript 


def test():
    inFile = open('samples/rick.txt', 'r')
    print(parseBody(inFile.read()))

#test()
