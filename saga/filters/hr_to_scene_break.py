#!/usr/bin/env python3
from panflute import *

def increase_header_level(elem, doc):
    if type(elem) == HorizontalRule:
        # TODO: Format this nicer
        # TODO: Don't do this if the next block is a Header. Doesn't quite work yet
        if type(elem.next) != Header:
            return(RawBlock('{\pard \\qc \\f0 \\sa180 \\li0 \\fi0 # \\par}\n', 'rtf'))

def main(doc=None):
    return run_filter(increase_header_level, doc=doc)

if __name__ == "__main__":
    main()