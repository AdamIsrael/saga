from panflute import *

def increase_header_level(elem, doc):
    if type(elem) == Header:

        header = stringify(elem)

        # TODO: Format this nicer
        newheader = '{\\pard \\ql \\f0 \\sa180 \\li0 \\fi720 \\b ' + header + '\\par}\n'
        
        return(RawBlock(newheader, 'rtf'))

def main(doc=None):
    return run_filter(increase_header_level, doc=doc)

if __name__ == "__main__":
    main()