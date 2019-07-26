"""
Language-related code
"""

import collections
import math
from operator import itemgetter
import re
import sys

class Words():
    """Word-related functions."""
    
    def __init__(self, text):
        self.text = text
        pass

    def stripComments(self, text):
        # Strip lines that start with a hash
        text = re.sub("(#.*?\n)", "", text, flags=re.DOTALL)

        # Strip text between <!-- and ->
        text = re.sub("(<!--.*?-->)", "", text, flags=re.DOTALL)

        return text

    def getWordsByFrequency(self, limit=25):
        words = {}

        text = "\n".join(self.text)

        text = self.stripComments(text)
        for line in text.lower().split('\n'):
            for word in line.split(' '):
                if len(word) <= 2 or word in ['and', 'the']:
                    break

                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1

        words = sorted(words.items(), key=itemgetter(1), reverse=True)

        return words[:limit]

    def getWordCount(self):
        lines = []

        text = "\n".join(self.text)

        text = self.stripComments(text)

        for line in text.split('\n'):
            # Strip whitespace and blank lines
            line = line.rstrip()
            if len(line) > 0:
                lines.append(line)

        # Get the # of lines
        lc = len(lines)

        # What's the average line length?
        lens = []
        for line in lines:
            lens.append(len(line))
        
        # Get the average characters per line
        avg = 0
        if sum(lens) > 0:
            avg = float(sum(lens)) / len(lens)

        # Get the number of words per line
        wpl = avg / 6

        # Multiply by the number of lines
        wc = wpl * len(lines)

        # return wc
        return self.roundup(wc)

    def roundup(self, x):
        return int(math.ceil(x / 100.0)) * 100