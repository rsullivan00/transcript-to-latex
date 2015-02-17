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

def lex(s):
    lines = lex_by_lines(s)
    tokens = []
    for line in lines:
        tokens.append(line.split('\t'))

    return tokens

def is_department_code(s):
    return re.match('[A-Z][A-Z][A-Z][A-Z]', s)

def condense_tokens(line, token, number_to_condense):
    for i, tok in enumerate(line):
        if not tok == token:
            continue
        for j in range(number_to_condense):
            line[i] += ' ' + line[i+j+1]

        for j in range(number_to_condense):
            del line[i+j+1]

    return line

"""
Populates and returns a Transcript object with raw pasted data from an eCampus unofficial web transcript.
"""
def parse_body(text):
    lexed = lex(text)

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
    section = 0
    for line in lexed:
        # New sections
        if line[0] == header_prefix:
            section += 1
            title = line[1]
            sec = TranscriptSection(title)
            transcript.sections.append(sec)
            debug_print('New section: ' + title)
        # Extract metadata
        elif section == 0:
            metadata.append(line[-1])
        # New subsection
        elif any(line[0].startswith(pre) for pre in subsection_prefixes):
            subsec = TranscriptSubSection(line[0])
            transcript.sections[-1].subsections.append(subsec)
        else:
            # Or add to current section/subsection
            if len(transcript.sections[-1].subsections) > 0:
                if line[0] == 'CUM':
                    condense_tokens(line, 'CUM', 1)

                transcript.sections[-1].subsections[-1].add_content('\t'.join(line))
            else:
                # Last added section
                transcript.sections[-1].add_content('\t'.join(line))


    # Process metadata
    if len(metadata) > 0:
        transcript.title = metadata[0].strip()
        datestring = metadata[1].strip()
        transcript.date = datetime.datetime.strptime(datestring, '%Y-%m-%d')
        transcript.school = metadata[2].strip()
        transcript.student = metadata[3].strip()
        transcript.address = metadata[4].strip()

    return transcript 


def test():
    inFile = open('samples/rick.txt', 'r')
    print(parseBody(inFile.read()))

#test()
