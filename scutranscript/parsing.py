import sys
import re

def parseBody(text):
    # Make all newlines only one newline
    text = re.sub('\n+', '\n', text)
    text2d = text.split('\n')
    text = []
    for line in text2d:
        if  not len(line) or re.match('^(\n| )+$', line):
            print('Empty line')
        else:
            # Remove repeated spaces
            line = re.sub(' +', ' ', line)
            print(line)
            text.append(line)


    # Divide into sections by section headers
    return text

def test():
    inFile = open('samples/rick.txt', 'r')
    print(parseBody(inFile.read()))

#test()
