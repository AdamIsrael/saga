#!/usr/bin/env python3
from panflute import run_filter, Para, stringify, RawBlock, BlockQuote

def smf(elem, doc):
    if type(elem) == Para:
        content = stringify(elem)

        # TODO: This shouldn't rewrite every paragraph (blockquotes, for example) so we need to dig into the elem attributes more.
        
        # Fix smart quotes, etc.
        content = content.replace("’", "\'")

        # Elipsis
        content = content.replace("…", "...")
       
        # Fix em-dash
        content = content.replace("–", "\emdash ")
        content = content.replace("—", "\emdash ")



        # {\pard \ql \f0 \sa180 \li720 \fi0
        content = '{\pard \ql \\f0 \sa180 \li0 \\fi720 \sl480 \slmult1 ' + content + ' \\par}\n'

        return(RawBlock(content, 'rtf'))

def main(doc=None):
    return run_filter(smf, doc=doc)


if __name__ == "__main__":
    main()