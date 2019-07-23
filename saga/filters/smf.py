#!/usr/bin/env python3
from panflute import run_filter, Para, stringify, RawBlock

def smf(elem, doc):
    if type(elem) == Para:

        content = '{\pard \ql \\f0 \sa180 \li0 \\fi720 \sl480\slmult1 ' + stringify(elem) + ' \\par}\n'

        return(RawBlock(content, 'rtf'))


def main(doc=None):
    return run_filter(smf, doc=doc)


if __name__ == "__main__":
    main()